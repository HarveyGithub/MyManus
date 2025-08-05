import random

target_number = random.randint(1, 100)

while True:
    try:
        guess = int(input('Guess a number between 1 and 100: '))
        break
    except ValueError:
        print('Invalid input. Please enter an integer.')