print('hello world')
answer = 9
guess = input ('Guess a number between 1 and 10: ')
guess = int(guess)

if guess == answer:
    print('You got it!')
else: 
    print('Guess again!')
    


class Counter:
    def __init__(self):
        self.number = 0
    def count(self, plus):
        self.number += plus

if