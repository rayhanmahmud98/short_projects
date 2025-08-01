import random

while True:
    def get_user_choice():
        user_input = input("Enter your choice from (rock, paper, scissors): ").lower()
        if user_input in ["rock", "paper", "scissors"]:
            return user_input
        else:
            print("Please enter a valid choice.")
            return get_user_choice()  # Call the function again if the input is invalid

    def get_computer_choice():
        return random.choice(["rock", "paper", "scissors"])

    def determine_winner(user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a tie!"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
            (user_choice == "paper" and computer_choice == "rock") or \
            (user_choice == "scissors" and computer_choice == "paper"):
            return "You Win!"
        else:
            return "Computer Wins!"

    def play_game():
        user_choice = get_user_choice()  # This calls the function and gets the user's choice
        computer_choice = get_computer_choice()
        
        print(f"\nYou chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")
        
        result = determine_winner(user_choice, computer_choice)
        print(result)

    if __name__ == "__main__":
        play_game()
