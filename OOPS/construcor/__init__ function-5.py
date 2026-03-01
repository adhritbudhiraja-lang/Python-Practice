class Student:
    college_name = "Chandigarh University"
    def __init__(self, name = "Adhrit_3", marks=0):
        self.name = name #Obj attribute
        self.marks = marks
        print("Adding student to database")
    def welcome(self):
        print("Welcome student : ", self.name)
    def get_marks(self):
        return self.marks
s1 = Student("Adhrit",97)
print(s1.name,s1.marks)
s2 = Student("Adhrit_2",87)
print(s2.name,s2.marks)
s3 = Student(marks=99)
print(s3.name,s3.marks,s3.college_name) #Will print Adhrit_3
s4 = Student("Adhrit_4")
s4.welcome()
print(s4.get_marks()) # Will print 0
print(s1.college_name)
print(s2.college_name)
print(Student.college_name)

# Will print Adhrit since obj attributes have more precidence than the class attribute