top = []
high = []
low = []
n = int(input("Enter number of entries : "))
for i in range(n):
    entry = int(input(f"Enter entry {i} : "))
    top.append(entry)

print("Entered list : ",top)

def speed_classification():
    for i in range(n):
        if(top[i]>=300):  #300 is the benchmark speed
            high.append(top[i])
        elif(top[i]<300):
            low.append(top[i])

    print("Low speeds : ",low)
    print("High speed : ",high)

def hl_speed():
    highest = lowest = top[0]
    for i in range(1, n):
        if top[i] >= highest:
            highest = top[i]
        if top[i] < lowest:  
            lowest = top[i]

    print("Highest speed : ", highest)
    print("Lowest speed : ", lowest)

def avg():
    s=0
    telm=0
    for i in high:
        s = s + i
        telm = telm+1
    avg=s/telm
    if(avg==0):
        print("No cars passed the benchmark, avg = 0")
    else:
        print("Cars that passed the benchmark will only be taken into consideration.")
        print("Average speed : ",avg)
    
speed_classification()
hl_speed()
avg()