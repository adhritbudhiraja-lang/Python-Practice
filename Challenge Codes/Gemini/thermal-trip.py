temps = []
trip = False
sum = 0
flag = 0
n = int(input("Enter number of temperature entries : "))
for i in range(n):
    elm = int(input(f"Entry [{i+1}] : "))
    temps.append(elm)

print("Entered temperature list : ",temps)
for i in range(n):
    sum = temps[i] + sum

for i in range(n):
    if temps[i] >= 100:
        flag = flag + 1

if flag != 0:
    trip = True

print("Average temperature : ",sum/n)
if trip == True:
    print(f"Temperature exceeded 100*C {flag} times.")
else:
    print("Temperature stayed within trip limits.")