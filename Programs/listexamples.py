#  fruits = ['apple', 'banana']
#  cost = []
#  for i in range(len(fruits)):
#      j = int(input('enter'))
#      cost.append(j)

number = [23, 4, 563, 6, 18, 4, 55, 7]
l = len(number)
i = 0
while l > 0:
    j = number.pop(i)
    if j % 2 == 0:
        number.remove(j)
    i += 1
    l -= 1
print(number)

# students = ['Aksh', 'Aashish', 'Ishita', 'Mohak', 'Udit', 'Yuvraj']
# students.insert(2, 'Divyansh')
# students.insert(6, 'Yash')
# students.remove('Ishita')
# print(students)
