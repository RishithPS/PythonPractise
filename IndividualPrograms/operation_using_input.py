x = int(input('enter the number for x'))
y = int(input('enter the number for y'))
operation = input('enter the operation')
if operation == 'a':
    print('Addition=', x+y)
elif operation == 's':
    print('Subraction=', x-y)
elif operation == 'm':
    print('Muplication=', x*y)
elif operation == 'D':
    print('Division=', x/y)
elif operation == 'M':
    print('Modulus=', x % y)
else:
    print('wrong')
