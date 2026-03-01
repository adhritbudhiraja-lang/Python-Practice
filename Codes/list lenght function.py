def length(s):
    count = 0
    for char in s:
        count += 1
    return count

n = input("Enter a string: ")
print("Lenght of string : ",length(n))