import csv
import requests
import getpass
import logging
import argparse
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Create budgets in Kion from a CSV file, separated by Project ID.")
parser.add_argument("--dry-run", type=bool, default=False, help="If true, outputs the curl command instead of making the API calls.")
args = parser.parse_args()

# Kion API Endpoint
url = "https://portal.kion.io/api/v3/budget"

# Prompt for API Key
api_key = getpass.getpass(prompt="Enter your Kion API Key: ")

# Headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Read the CSV and prepare budget entries
csv_filename = "budget_2025.csv"

try:
    # Dictionary to group budgets by project_id
    budgets_by_project = {}

    # Read the CSV
    logging.debug(f"Reading CSV file: {csv_filename}")
    with open(csv_filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            project_id = int(row["Project ID"])
            month = row["Month"]
            funding_source_id = int(row["Funding Source ID"])
            amount = row["Amount"]

            # Initialize budget data for the project_id if not already present
            if project_id not in budgets_by_project:
                budgets_by_project[project_id] = {
                    "data": [],
                    "funding_source_ids": set(),
                    "earliest_month": None,
                    "latest_month": None,
                    "total_amount": 0
                }

            # Add entry to the budget data
            budgets_by_project[project_id]["data"].append({
                "amount": amount,
                "datecode": month,
                "funding_source_id": funding_source_id,
                "priority": 1  # Default priority
            })
            budgets_by_project[project_id]["funding_source_ids"].add(funding_source_id)
            budgets_by_project[project_id]["total_amount"] += int(amount)

            # Update earliest and latest months
            if (budgets_by_project[project_id]["earliest_month"] is None or
                month < budgets_by_project[project_id]["earliest_month"]):
                budgets_by_project[project_id]["earliest_month"] = month

            if (budgets_by_project[project_id]["latest_month"] is None or
                month > budgets_by_project[project_id]["latest_month"]):
                budgets_by_project[project_id]["latest_month"] = month

    # Prepare and send budgets for each project
    for project_id, budget_info in budgets_by_project.items():
        # Calculate end_datecode (one month beyond the latest_month)
        latest_date = datetime.strptime(budget_info["latest_month"], "%Y-%m")
        end_datecode = (latest_date + relativedelta(months=1)).strftime("%Y-%m")

        # Budget payload
        payload = {
            "amount": budget_info["total_amount"],
            "data": budget_info["data"],
            "start_datecode": budget_info["earliest_month"],
            "end_datecode": end_datecode,
            "project_id": project_id,
            "funding_source_ids": list(budget_info["funding_source_ids"])
        }

        # Debug log the payload
        logging.debug(f"Payload for project_id {project_id}: {json.dumps(payload, indent=2)}")

        # If --dry-run is set, output the curl command
        if args.dry_run:
            curl_command = f"""curl -X POST "{url}" \\
-H "Authorization: Bearer {api_key}" \\
-H "Content-Type: application/json" \\
-d '{json.dumps(payload)}'"""
            print(f"\nDry Run Mode: Curl command for project_id {project_id}:\n{curl_command}")
        else:
            # Send the API request
            logging.info(f"Sending API request to Kion for project_id {project_id}...")
            response = requests.post(url, json=payload, headers=headers)
            
            # Log response details
            logging.debug(f"Response status code for project_id {project_id}: {response.status_code}")
            logging.debug(f"Response content for project_id {project_id}: {response.content.decode('utf-8')}")

            # Raise an error for bad status codes (4xx and 5xx)
            response.raise_for_status()
            print(f"Budget created successfully for project_id {project_id}:", response.json())

except requests.exceptions.HTTPError as http_err:
    logging.error(f"HTTP error occurred: {http_err}")
except FileNotFoundError:
    logging.error(f"CSV file '{csv_filename}' not found. Please ensure the file exists.")
except Exception as e:
    logging.error("An unexpected error occurred.", exc_info=e)
