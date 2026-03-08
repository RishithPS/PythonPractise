# CHALLENGE 3: MORE RAINBOW TURTLES!
import turtle
pen = turtle.Turtle()
pen.shape('turtle')
pen.penup()


def drawcircle(r, color):
    pen.pendown()
    pen.circle(r, -180)
    pen.fillcolor(color)
    pen.penup()
    return


for i in range(8):

    if i == 0:
        pen.goto(-400, 0)
        pen.left(270)
        pen.color('red')
        pen.begin_fill()
        drawcircle(400, 'red')
        pen.end_fill()
        pen.stamp()

    elif i == 1:
        pen.goto(-350, 0)
        pen.left(180)
        pen.color('orange')
        pen.begin_fill()
        drawcircle(350, 'orange')
        pen.end_fill()
        pen.stamp()

    elif i == 2:
        pen.goto(-300, 0)
        pen.left(180)
        pen.color('green')
        pen.begin_fill()
        drawcircle(300, 'green')
        pen.end_fill()
        pen.stamp()

    elif i == 3:
        pen.goto(-250, 0)
        pen.left(180)
        pen.color('yellow')
        pen.begin_fill()
        drawcircle(250, 'yellow')
        pen.end_fill()
        pen.stamp()

    elif i == 4:
        pen.goto(-200, 0)
        pen.left(180)
        pen.color('blue')
        pen.begin_fill()
        drawcircle(200, 'blue')
        pen.end_fill()
        pen.stamp()

    elif i == 5:
        pen.goto(-150, 0)
        pen.left(180)
        pen.color('indigo')
        pen.begin_fill()
        drawcircle(150, 'indigo')
        pen.end_fill()
        pen.stamp()

    elif i == 6:
        pen.goto(-100, 0)
        pen.left(180)
        pen.color('violet')
        pen.begin_fill()
        drawcircle(100, 'violet')
        pen.end_fill()
        pen.stamp()

    elif i == 7:
        pen.goto(-50, 0)
        pen.left(180)
        pen.color('white')
        pen.begin_fill()
        drawcircle(50, 'white')
        pen.end_fill()
        pen.stamp()

turtle.exitonclick()
