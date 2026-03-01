def check(name):
    if len(name) >=3 :
        vip.append(name)
    else:
        non_vip.append(name)

vip = []
non_vip = []
n=int(input("Enter number of people : "))
for i in range(n):
    name = input("Enter name : ")
    check(name)

full = vip + non_vip

print("Vip : ",vip)
print("Non vip : ",non_vip)
print("Full list : ",full)