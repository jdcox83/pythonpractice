# This is a simple Python script that demonstrates basic programming concepts. 
# These are just simple examples to illustrate the concepts and are not intended to be comprehensive or exhaustive.

###

# Print a greeting message. This is a simple print sta  tement.
print('hello world')

# Define the correct answer for a guessing game
answer = 9

# Prompt the user to guess a number
guess = input('Guess a number between 1 and 10: ')
# Convert the user's input to an integer
guess = int(guess)

# Check if the user's guess matches the answer
if guess == answer:
    print('You got it!')
else: 
    print('Guess again!')

# Define a Counter class to keep track of a number
class Counter:
    def __init__(self):
        # Initialize the counter to 0
        self.number = 0

    def count(self, plus):
        # Increment the counter by the given value
        self.number += plus

# Import necessary modules for making HTTP requests
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

try:
    # Make an HTTP GET request to the specified URL
    response = urlopen('https://www.cloudacademy.com')
    # Check if the response status is 200 (OK)
    if response.status == 200:
        # Read the content of the response
        response = response.read()
        print(response)
    else:
        # Print a message if the status code is not 200
        print(f"Unexpected status code: {response.status}")
except HTTPError as e:
    # Handle HTTP-specific errors
    print(f"HTTP error occurred: {e.code} - {e.reason}")
except URLError as e:
    # Handle URL-related errors
    print(f"URL error occurred: {e.reason}")
except Exception as e:
    # Handle any other unexpected errors
    print(f"An unexpected error occurred: {e}")

# Import the Deck class from the cards module
from cards import Deck



#Practicing Comprehensions
# the title converts the first letter of each word to uppercase.

people_to_know = ['lovelace', 'curie', 'tesla', 'newton']
revised_people = []
for person in people_to_know:
    revised_people.append(person.title())
print(revised_people)

revised_people2 = [people.title() for people in people_to_know]
print(revised_people2)  
