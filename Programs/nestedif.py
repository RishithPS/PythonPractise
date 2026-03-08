# Take the input grade / score
# Above 90 1st Rank
# Between 80 and 89 2nd Rank
# Between 70 and 79 3rd Rank
# Between 60 and 69 4th Rank
# Between 50 and 59 5th Rank
# Less than or equal to 49 Student Failed
grade = int(input('Enter the Score'))
if grade >= 90:
    print('1st')
elif grade >= 80 and grade <= 89:
    print('2nd')
elif grade >= 70 and grade <= 79:
    print('3rd')
elif grade >= 60 and grade <= 69:
    print('4th')
elif grade >= 50 and grade <= 59:
    print('5th')
else:
    print('FAIL')
