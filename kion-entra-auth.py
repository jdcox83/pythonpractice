import requests
from msal import ConfidentialClientApplication

# Replace these values with your Azure AD app registration details
CLIENT_ID = "dcae11f9-48ac-48ff-b9ec-094fb530a5a1"
CLIENT_SECRET = "your-client-secret"
TENANT_ID = "44467e6f-462c-4ea2-823f-7800de5434e3"

# Microsoft Graph API endpoint
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

# Initialize the MSAL confidential client application
app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}"
)

# Acquire a token for Microsoft Graph
token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

if "access_token" in token_response:
    access_token = token_response["access_token"]
    print("Access token acquired successfully!")

    # Retrieve all groups from Microsoft Graph
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{GRAPH_API_ENDPOINT}/groups", headers=headers)

    if response.status_code == 200:
        groups = response.json().get("value", [])
        if groups:
            for group in groups:
                print(f"Group Name: {group['displayName']}, Object ID: {group['id']}")
        else:
            print("No groups found.")
    else:
        print(f"Failed to retrieve groups. Status Code: {response.status_code}")
        print(response.json())
else:
    print("Failed to acquire access token.")
    print(token_response.get("error"))
    print(token_response.get("error_description"))