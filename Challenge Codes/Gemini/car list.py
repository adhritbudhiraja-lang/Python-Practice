car = []
same = []
n = int(input("Enter number of car brands [USE SAME SPELLING]: "))
for i in range(n):
    brand = input(f"Enter name of brand number {i+1} : ")
    car.append(brand)

print("Entered list : ",car)

for i in range(n):
    count = 0
    for j in range(n):
        if(car[i]==car[j]):
            count = count + 1
    same.append(count)        
    
printed = []
for i in range(n):
    if(car[i] not in printed):
        print(f"Brand {car[i]} has {same[i]} cars.")
        printed.append(car[i])