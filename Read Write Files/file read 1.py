f = open(r"C:\Users\Adhrit\Desktop\Coding\Python\Read Write Files\demo.txt")
data = f.read()
print("The full file contains : \n",data)
f.seek(0) # Send the read back to begining sunce f.read sends it to the end
print("\nLine 1 : ",f.readline())
print("\nLine 2 : ",f.readline())