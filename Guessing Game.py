import random

lowest_value = int(input("Enter the lower value: "))
highest_value = int(input("Enter the higher value: "))

answer = random.randint(lowest_value, highest_value)

guesses = 0

is_running = True

print("Python Number Guessing Game")
print(f"Select a number between {lowest_value} and {highest_value}")

while is_running:
    guess = input("Enter your guess: ")
    
    if guess.isdigit():
        guess = int(guess)
        guesses += 1
        
        if guess < lowest_value or guess > highest_value:
            print("The guess is out of range.")
            print(f"Please select a number between {lowest_value} and {highest_value}.")
        
        elif guess < answer:
            print("The guess is too low.")
            
        elif guess > answer:
            print("The guess is too high.")
            
        else:
            print("Excellent!! The guess is correct!!!")
            print(f"The correct guess is {answer}.")
            print(f"The number of guesses is {guesses}.")
            is_running = False  # End the loop when the correct answer is guessed
    else:
        print("Invalid Guess.")
        print(f"Please select a number between {lowest_value} and {highest_value}.")
