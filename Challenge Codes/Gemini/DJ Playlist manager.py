music = []
while True:
    print("1)Add song\n2)Add priority song\n3)Remove song\n4)Clear playlist\n5)Setup playlist\n6)Display playlist\n7)End\n8)Currently Playing")
    choice = int(input("Enter choice : "))
    if choice == 1:
        name = input("Enter name : ")
        music.append(name)
    elif choice == 2:
        name = input("Enter name : ")
        music.insert(0,name)
        print(music)
    elif choice == 3:
        name = input("Enter name : ")
        music.remove(name)
        print(music)
    elif choice == 4:
        print("Playlist cleared!")
        music.clear()
        print(music)
    elif choice == 5:
        n = int(input("Enter number of songs : "))
        for i in range(n):
            name = input("Enter song name : ")
            music.append(name)
        print(music)
    elif choice == 6:
        print(music)
    elif choice == 7:
        break
    elif choice == 8:
        print("Currently playing")
        print(music[0])
    else:
        print("Error")