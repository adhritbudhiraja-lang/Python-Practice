class Student:
    def __init__(self, name):
        self.name = name
        print("Adding student to database")
s1 = Student("Adhrit")
print(s1.name)
s2 = Student("Adhrit_2")
print(s2.name)