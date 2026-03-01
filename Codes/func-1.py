def get_details():
    global name,age
    name = input("Enter name : ")
    age = int(input("Enter age : "))
    return name, age

def show_details():
    print(name)
    print(age) 

get_details()
show_details()