print("Welcome to password security checks.\nEnter a password that follows all of the following conditions:\n1)Must contain an uppercase.\n2)Must contain atleast one number.\n3)Must be 8 characters long.")
password = input("Enter password : ")
up = 0
digit = 0
if (len(password)>=8):
    for char in password:
        if(char.isupper()):
            up = up + 1
        elif(char.isdigit()):
            digit = digit + 1
else:
    print("Password lenght is less than 8!")

if digit > 0 and up > 0:
    print("Password is secure.")
else:
    print("Password is not secure.")