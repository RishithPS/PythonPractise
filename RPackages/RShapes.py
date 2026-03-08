# Draw a Square
def square(pen):
    for i in range(4):
        pen.right(90)
        pen.forward(100)

# Draw an Equilateral Triangle
def triangle(pen):
        pen.left(60)
        pen.forward(90)
        pen.right(120)
        pen.forward(90)
        pen.left(240)
        pen.forward(90)

# Draw a Pentagon
def pentagon(pen):
    sides = 5
    for i in range(sides):
        pen.forward(75)  
        pen.right(360 / sides)
        
def volume_and_surface_area_finder(l,b,h):        
    l=int(input('enter the number of lenght:'))
    b=int(input('enter the number of breadth:'))
    h=int(input('enter the number of height:'))
    un=input('what are its units:')
    volume=l*b*h
    surface_area=h*l*2+h*b*2+l*b*2
    print(f'volume is {volume}{un} to the power of 3')
    print(f'surface area is {surface_area}{un} to the power of 2')
    
