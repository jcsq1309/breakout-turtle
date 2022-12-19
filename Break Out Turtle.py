import turtle
import random
from playsound import playsound

# Draw screen
screen = turtle.Screen()
screen.title("Break Out")
screen.bgcolor("black")
screen.setup(width=700, height=900)
screen.tracer(0)

# Draw paddle
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("dodger blue")
paddle.shapesize(stretch_wid=1, stretch_len=4)
paddle.penup()
paddle.goto(-10, -300)

# Length of the paddle's collision
len_col = 60


# Draw Color Paddles
# The space between each brick is 45
x_list = [-318, -273, -228, -183, -138, -93, -48, -3, 42, 87, 132, 177, 222, 267, 312]
y_list = [100, 125, 150, 175, 200, 225, 250, 275]
colors = ["yellow", "green", "orange", "red"]
brick_list = []

# Creating the bricks
for i in y_list:
    for j in x_list:
        brick = turtle.Turtle()
        brick.speed(0)
        brick.shape('square')
        brick.shapesize(stretch_len=2, stretch_wid=1)
        brick.color(random.choice(colors))
        brick.up()
        brick.goto(j, i)
        brick_list.append(brick)


# Draw ball
ball = turtle.Turtle()
accel = 0
# Made in this way so the speed can be increased
ball.speed(accel)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(-10, -250)
ball.dx = 1
ball.dy = 1

# score
score = 0

# Lives
Lives = 3

# head-up display
hud = turtle.Turtle()
hud.speed(0)
hud.shape("square")
hud.color("white")
hud.penup()
hud.hideturtle()
hud.goto(0, 350)
hud.write("0", align="left", font=("Press Start 2P", 24, "normal"))


# Paddle´s controls
def paddle_right():
    x = paddle.xcor()
    if x < 300:
        x += 30
    else:
        x = 300
    paddle.setx(x)


def paddle_left():
    x = paddle.xcor()
    if x > -310:
        x += -30
    else:
        x = -310
    paddle.setx(x)


# Moves from left to right
screen.listen()
screen.onkeypress(paddle_left, "a")
screen.onkeypress(paddle_right, "d")

while True:
    screen.update()

    # Ball movement
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Collision with the upper wall
    if ball.ycor() > 380:
        playsound('bouncing_ball.wav')
        ball.sety(380)
        ball.dy *= -1
        paddle.shapesize(stretch_len=2)
        len_col = 30

    # Collision with the floor
    if ball.ycor() < -400:
        playsound('score_got.wav')
        ball.goto(-100, 50)
        paddle.shapesize(stretch_len=4)
        len_col = 60
        Lives -= 1

    # Game Over
    if Lives == 0:
        break

    # Collision with left wall
    if ball.xcor() < -340:
        playsound('bouncing_ball.wav')
        ball.setx(-340)
        ball.dx *= -1

    # Collision with right wall
    if ball.xcor() > 330:
        playsound('bouncing_ball.wav')
        ball.setx(330)
        ball.dx *= -1

    # Collision with the Paddle
    if (-280 > ball.ycor() > -290) and (paddle.xcor() + len_col > ball.xcor() > paddle.xcor() - len_col):
        ball.sety(-280)
        ball.dy *= -1
        playsound('bouncing_ball.wav')

    # Resets speed
    if accel > 10:
        accel = 5
        ball.speed(accel)

    # Collision with the bricks
    for i in brick_list:
        if ball.xcor() + 10 >= i.xcor() - 30 and ball.xcor() - 10 <= i.xcor() + 30:
            if i.ycor() - 10 <= ball.ycor() <= i.ycor() + 10:
                ball.dy *= -1
                i.goto(1000, 1000)
                score += 1
                hud.clear()
                hud.write("{}".format(score), align="center", font=("Press Start 2P", 24, "normal"))
                playsound('bouncing_ball.wav')

            # Red and Orange bricks increase speed when hit
            if i.color() == "red" or "orange":
                accel += 1
                ball.speed(accel)

    # Speed increases with higher score
    if score >= 30:
        accel += 2
        ball.speed(accel)
    if score >= 60:
        accel += 3
        ball.speed(accel)
