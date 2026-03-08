import turtle
pen = turtle.Turtle()
pen.shape('turtle')
pen.penup()
for i in range(7):
    pen.forward(20)
    if i == 0:
        pen.color('red')
        pen.stamp()
    elif i == 1:
        pen.color('orange')
        pen.stamp()
    elif i == 2:
        pen.color('green')
        pen.stamp()
    elif i == 3:
        pen.color('yellow')
        pen.stamp()
    elif i == 4:
        pen.color('blue')
        pen.stamp()
    elif i == 5:
        pen.color('indigo')
        pen.stamp()
    elif i == 6:
        pen.color('violet')
        pen.stamp()

turtle.exitonclick()
