kill = []
death = []
ratio = []
n = int(input("Enter number of rounds in the match : "))
if(n==0):
    print("Invalid")
else:
    for i in range(n):
        k = int(input(f"Kills in round {i+1}  : "))
        kill.append(k)
        d = int(input(f"Deaths in round {i+1} : "))
        death.append(d)

    print("Entered kills data  : ",kill)
    print("Entered deaths data : ",death)

    for i in range(n):
        if(death[i]==0):
            r=kill[i]
            ratio.append(r)
        else:   
            r = kill[i]/death[i]
            ratio.append(r)

    print("Kill to death ratio as per matches : ",ratio)
    s = 0
    for i in range(n):
        s = s + kill[i]/death[i]
    print("Average K/D ratio : ",s/n)

    for i in range(n):
        if ratio[i] >= ratio[0]:
            z = i

    print("Best match : ",z)