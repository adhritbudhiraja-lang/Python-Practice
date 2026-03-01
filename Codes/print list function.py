def disp(v):
    print(*v)

s = []
n = int(input("Enter number of elements : "))
for i in range(n):
    elm = input(f"Element {i} : ")
    s.append(elm)
disp(s)