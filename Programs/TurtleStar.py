import turtle
import random
turtle.colormode(255)
turtle.Screen().setup(1000, 1000)
turtle.Screen().bgcolor(35, 58, 119)
divider_pen = turtle.Turtle()
divider_pen.color(255, 212, 31)
divider_pen.pensize(10)
divider_pen.back(500)
divider_pen.forward(1000)
divider_pen.ht()

pen = turtle.Turtle()
pen.penup()
pen.ht()
pen.goto(-200, 300)
pen.color(255, 215, 0)
pen.pensize(5)

tooga = turtle.Turtle()
tooga.shape('turtle')
tooga.color(9, 185, 13)
tooga.pencolor(0, 128, 0)
tooga.turtlesize(3, 3, 3)
tooga.penup()
tooga. goto(0, -100)


def draw_star():
    pen.pendown()
    for i in range(5):
        pen.forward(100)
        pen.right(144)
    pen.penup()
    pen.goto(pen.xcor() + 200, pen.ycor() + 20)
    return


tooga.left(90)
for i in range(1, 6):
    turtle.delay(30)
    tooga.forward(150)
    cloudy_night = random.choice([True, False])
    print(f'Is Cloudy? {cloudy_night}')
    if cloudy_night == False:
        draw_star()
    tooga.right(180)
    tooga.forward(150)
turtle.exitonclick()
