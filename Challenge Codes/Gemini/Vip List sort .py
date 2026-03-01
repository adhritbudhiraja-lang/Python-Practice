vip = []
non_vip = []
n = int(input("Enter number of people : "))
for i in range(n):
    name = input("Enter name : ")
    if len(name)>=3:
        vip.append(name)
    else :
        non_vip.append(name)

full = vip + non_vip

print("Vip list : ",vip)
print("Non vip list : ",non_vip)
print("Full list : ",full)