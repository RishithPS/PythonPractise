z = int(input('enter the number for z'))
y = int(input('enter the number for y'))
x = int(input('enter the number for x'))
if z > y and z > x:
    print('z is largest number')
elif y > z and y > x:
    print('y is largest number')
else:
    print('x is largest number')
