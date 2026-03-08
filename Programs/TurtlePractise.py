# %%
import turtle
import random

# Programs Created / Updated by Rishith using 'Turtle' Module
# 1. Create different shapes 'Square', 'Star', 'Circle' etc
# 2. Create a Flower
# 3. Create a Robot
# 4.
# 5.
# 6.
# 7.


# CHAPTER 6: TURTLE (114)
# 1. Creating Outline
turtle.setup(900, 900)  # Canvas Layout Size Length and Breadth
turtle.Screen().colormode(255)  # Specifies RGB Mode
turtle.Screen().bgcolor(0, 0, 0)  # Red, Green, Blue
turtle.shape('turtle')  # Arrow will come if you Delete this line
# turtle.color(58, 132, 40)  # Color of the Shape
turtle.pencolor(58, 132, 40)  # Outline Pen Color of the Shape
turtle.turtlesize(10, 10, 2)  # Size of the Shape Length, Breadth, Outline Thickness
turtle.turtlesize(outline=10)  # Change Outline Thickness
# turtle.resizemode('auto')  # ReSize to default shape
turtle.forward(200)  # turtle.back(200)
turtle.left(90)  # turtle.right(30) - Parameter is Angle
turtle.forward(200)
turtle.left(90)
turtle.exitonclick()  # Exit on Click
# turtle.done() # You have to manually close the Window

# %%
# 2. Creating Shapes by using Pen
pen = turtle.Turtle()
pen.color('red')
pen.pensize(5)
pen.begin_fill()  # We Signal the computer to fill the shape with color that we are about to draw
for i in range(4):
    pen.forward(200)
    pen.left(90)
pen.fillcolor('black')  # We Signal the computer to fill the color
pen.end_fill()  # We Signal the computer to end the fill
pen.hideturtle()  # It hides the Pen
turtle.exitonclick()

# %%
# 3. Spiral Shape
turtle.setup(1000, 1000)
pen = turtle.Turtle()
pen.color('red')
pen.pensize(3)
for i in range(1, 10):
    pen.circle(i*30, 180, 60)  # radius, extent, steps (or deviation in degrees)
turtle.exitonclick()

# %%
# 4. Spiral Shape with stamp function and random module
pen = turtle.Turtle()
pen.shape('turtle')
pen.penup()
turtle.colormode(255)
paces = 20
for i in range(50):
    random_red = random.randint(0, 255)
    random_green = random.randint(0, 255)
    random_blue = random.randint(0, 255)
    pen.color(random_red, random_green, random_blue)
    pen.stamp()
    paces += 3
    pen.forward(paces)
    pen.right(25)
turtle.exitonclick()

# %%
# ACTIVITY 1: LET'S DRAW A STAR!
turtle.colormode(255)
pen = turtle.Turtle()
pen.color(255, 147, 53)
pen.pensize(5)
pen.pensize(5)
pen.ht()
for i in range(5):
    pen.forward(100)
    pen.right(144)
turtle.exitonclick()

# %%
# ACTIVITY 2: FORTUNE-TELLER
pointer = turtle.Turtle()
pointer.turtlesize(3, 3, 2)
pen = turtle.Turtle()
spin_amount = random.randint(1, 360)
pen.penup()

# right side
pen.goto(200, 0)
pen.pendown()
pen.write("Yes!", font=('Open Sans', 30))
pen.penup()

# left side
pen.goto(-400, 0)
pen.pendown()
pen.write("Absolutely not!", font=('Open Sans', 30))
pen.penup()

# top side
pen.goto(-100, 300)
pen.pendown()
pen.write("Uhh, maybe?", font=('Open Sans', 30))
pen.penup()

# bottom side
pen.goto(0, -200)
pen.pendown()
pen.write("Yes, but after 50 years!", font=('Open Sans', 30))
pen.ht()

pointer.left(spin_amount)
turtle.exitonclick()

# %%
# ACTIVITY 3: RAINBOW TURTLES!
pen = turtle.Turtle()
pen.turtlesize(2, 2, 2)
pen.shape('turtle')
pen.penup()
for i in range(7):
    pen.forward(50)
    if i == 0:
        pen.color('red')
    elif i == 1:
        pen.color('orange')
    elif i == 2:
        pen.color('yellow')
    elif i == 3:
        pen.color('green')
    elif i == 4:
        pen.color('blue')
    elif i == 5:
        pen.color('indigo')
    elif i == 6:
        pen.color('violet')
    pen.stamp()
turtle.exitonclick()

# %%
# ACTIVITY 4: CIRCLECEPTION
pen = turtle.Turtle()
for i in [75, 50, 25]:
    if i == 75:
        pen.begin_fill()
        pen.circle(i)
        pen.fillcolor('violet')
        pen.end_fill()
    if i == 50:
        pen.begin_fill()
        pen.circle(i)
        pen.fillcolor('blue')
        pen.end_fill()
    if i == 25:
        pen.begin_fill()
        pen.circle(i)
        pen.fillcolor('red')
        pen.end_fill()
turtle.exitonclick()

# %%
# ACTIVITY 5: TOOGA’S HOUSE
tooga = turtle.Turtle()
tooga.turtlesize(2, 2, 2)
tooga.shape('turtle')
tooga.color('green')
tooga.penup()

pen = turtle.Turtle()
pen.pensize(10)
pen.color('yellow')
pen.right(90)
pen.forward(325)
pen.left(90)
pen.forward(275)
pen.left(90)
pen.forward(100)
pen.left(90)
pen.forward(50)
pen.right(90)
pen.forward(225)
pen.color('red')
pen.left(45)
pen.forward(162.5)
pen.left(90)
pen.forward(162.5)
pen.ht()
tooga.right(45)
tooga.forward(150)
turtle.exitonclick()

# %%
# ACTIVITY 6: WRITING IN PYTHON
pen = turtle.Turtle()
pen.color('black')
turtle.write('Rishith', font=("Freestyle Script", 50, "normal"))
pen.forward(200)
turtle.exitonclick()

