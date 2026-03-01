def sum_natural(n):
    t = 0
    for i in range(1, n + 1):
        t += i
    print(f"Sum of first {n} natural numbers = {t}")

n = int(input("Enter number of natural numbers: "))
sum_natural(n)