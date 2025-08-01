sum = 0;

while(True):
    userInput = input("Enter the price or press q to quit ")
    if (userInput != 'q'):
        sum = sum + int(userInput)
        print(f"Order total : {sum}")
    else:
        print(f"Order total is : {sum}")
        print("Thanks for using our service")
        break