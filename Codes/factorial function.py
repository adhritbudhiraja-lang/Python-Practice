def fact(x):
    f = 1
    for i in range(1,x+1):
        f = f * i
        
    print(f"Factorial of {x} is {f}.")

n = int(input("Enter number : "))
fact(n)