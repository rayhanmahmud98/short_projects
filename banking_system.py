#banking system

def show_balance(balance):
    print("---------------------------------")
    print((f"Your balance is {balance:.2f} TK"))
    print("---------------------------------")

def deposit():
    amount = float(input("Enter a amount to be deposited : "))
    
    if amount < 0:
        print("---------------------------------")
        print("------Thats invalid amount-------")
        print("---------------------------------")
        return 0
    else:
        return amount

def withdraw(balance):
    amount = float(input("Enter a amount to withdraw : "))
    
    if amount > balance:
        print("---------------------------------")
        print("------Insufficient Balance-------")
        print("---------------------------------")
        return 0
    elif amount < 0:
        print("---------------------------------")
        print("-----Amount must be positive-----")
        print("---------------------------------")
        return 0
    else:
        return amount


def main():

    balance = 0
    is_running = True

    while is_running:
        print("---------------------------------")
        print("--------Banking Programme--------")
        print("--------1.Show Balance-----------")
        print("--------2.Deposit----------------")
        print("--------3.Withdraw---------------")
        print("--------4.Exit-------------------")
        
        choice = input("Enter your choice (1-4) : ")
        
        if choice == '1':
            show_balance(balance)
        elif choice == '2':
            balance += deposit()
        elif choice == '3':
            balance -= withdraw(balance)
        elif choice == '4':
            is_running = False
        else:
            print("---------------------------------")
            print("-----The choice is not valid-----")
            print("---------------------------------")
    print("---------------------------------")
    print("------ Have a nice day !! -------")
    print("---------------------------------")
    
if __name__  == "__main__":
    main()