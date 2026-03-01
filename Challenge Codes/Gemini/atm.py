pin = 1234
z = 3
acc_bal = 500
check = int(input("Enter pin: "))
while z != 0:
    if pin != check:
        print("Invalid pin!\nRetry!")
        z -= 1
        print(f"Retry left {z}/3")
        if z == 0:
            break
        check = int(input("Enter pin: "))
    else:
        print("Account balance:", acc_bal)
        withdraw = int(input("Enter amount to withdraw: "))
        if withdraw > acc_bal:
            print("Insufficient funds!")
        else:
            if withdraw % 10 == 0:
                acc_bal -= withdraw
                print("Balance:", acc_bal)
            else:
                print("Amount should be a multiple of 10 only!")
        break