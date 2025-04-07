print('Hello, World!')
sum = 1 + 2
print(sum)


product = sum * 2
print(product)

distance_to_alpha_centauri = 4.367 # looks like a float
type(distance_to_alpha_centauri) ## <class 'float'>

left_side = 10
right_side = 5
left_side / right_side

from datetime import date
date.today
print(date.today())
#Print today's date as a string
print("Today's date is: " + str(date.today()))



parsecs = 11
lightyears = parsecs * 3.26
print(str(parsecs) + " parsecs is " + str(lightyears) + " lightyears")

import sys

print(sys.argv)
print(sys.argv[0]) # program name
print(sys.argv[1]) # first arg

#User Input:
print("Welcom to the greeter program")
name = input("Enter your name: ")
print("Greetings " + name)

#working with numbers

print("calculator program")
first_number = input("first number: ")
second_number = input("second number: ")
print(first_number + second_number)
#this won't work as desired as the numbers are entered as strings
#we need to use the int() function to make them be treated as numbers
print(int(first_number) + int(second_number))

# Another User Input Code example
parsecs_input = input("Input number of parsecs:")
parsecs = int(parsecs_input)
lightyears = 3.26156 * parsecs
print(parsecs_input + " parsecs is " + str(lightyears) + " lightyears")


