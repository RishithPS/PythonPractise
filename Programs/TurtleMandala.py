# CHALLENGE 2: MANDALA
import turtle
pen = turtle.Turtle()
pen.pensize(5)


def drawcircle(pencolor, fillcolor):
    pen.pendown()
    pen.color(pencolor)
    pen.begin_fill()
    pen.circle(i*30)
    pen.fillcolor(fillcolor)
    pen.end_fill()
    return


for i in reversed(range(1, 6)):
    if i == 1:
        pen.penup()
        pen.goto(0, 20)
        drawcircle('red', 'black')
    elif i == 2:
        pen.penup()
        pen.goto(0, -10)
        drawcircle('green', 'yellow')
    elif i == 3:
        pen.penup()
        pen.goto(0, -40)
        drawcircle('blue', 'purple')
    elif i == 4:
        pen.penup()
        pen.goto(0, -70)
        drawcircle('yellow', 'red')
    elif i == 5:
        pen.penup()
        pen.goto(0, -100)
        drawcircle('purple', 'green')

turtle.exitonclick()
