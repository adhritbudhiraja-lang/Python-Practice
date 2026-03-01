op = (input("Enter an operator : "))
num1 = float(input("Enter first number : "))
num2 = float(input("Enter second number : "))

match op:
    case '+':
        sum = num1 + num2
        print(f"{num1} + {num2} = {sum}")
    case '-':
        sub = num1 - num2
        print(f"{num1} - {num2} = {sub}")
    case '*':
        mult = num1 * num2
        print(f"{num1} * {num2} = {mult}")
    case '/': 
        if num2 == 0 :
            print("Invalid! division by zero not possible!")
        else :
            div = num1 / num2
            print(f"{num1} / {num2} = {div}")
    case '%':
        if num2 == 0 :
            print("Invalid! division by zero not possible!")
        else :
            rem = num1 % num2
            print(f"{num1} % {num2} = {rem}")
