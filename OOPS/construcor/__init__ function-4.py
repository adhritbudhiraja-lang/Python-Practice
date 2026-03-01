class Student:
    college_name = "Chandigarh University"
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        print("Adding student to database")
s1 = Student("Adhrit",97)
print(s1.name,s1.marks)
s2 = Student("Adhrit_2",87)
print(s2.name,s2.marks)
print(s1.college_name)
print(s2.college_name)
print(Student.college_name)