import turtle
import time

bg_color=input("Enter background/Page color (e.g, white, black, blue etc.): ").strip().lower()
pen_color= input("Enter pen color (e.g, red, green, blue): ").strip().lower()

print("/n--- Freehand Drawing Controls ---")
print("To Start/Stop Drawing: Click on the Screen")
print("To erase a portion: Press E")
print("To Clear the entire page: Press C")
print("To increase Pen/Eraser size: Press +")
print("To decrease Pen/Eraser size: Press -")
print("To change the Pen colour while Drawing: Press P")
print("To Quit: Press Q")
print("---------------------------------\n")

ready = input("Are you ready to start? (yes/any other input for no): ").strip().lower()

if ready not in ["y","yes"]:
    print("Exiting the Program. Restart when ready.")
    exit()


screen=turtle.Screen()
screen.title("Freehand Writing/Darwing")
screen.bgcolor(bg_color)
screen.setup(width=1.0, height=1.0)
screen.tracer(0)
t=turtle.Turtle()
t.speed(0)

t.color(pen_color)
t.pensize(5)
t.turtlesize(2)
t.penup()

is_drawing = False
is_erasing = False
turtle_size = 2


def toggle_drawing(x,y):
    global is_drawing, is_erasing
    is_erasing = False
    t.pencolor(pen_color)
    t.shape("classic")
    t.shapesize(1,1)
    if is_drawing:
        t.penup()
    else:
        t.pendown()
    is_drawing = not is_drawing

def enable_erasing():
    global is_erasing
    is_erasing = True
    t.pencolor(bg_color)
    t.pendown()
    t.shape("square")
    t.shapesize(turtle_size/10)
    eraser_stamp=t.stamp()
    t.clearstamp(eraser_stamp)
    screen.update()

def clear_screen():

    t.clear()
    t.penup()
    t.goto(0,0)
    t.pencolor(pen_color)

    global is_drawing, is_erasing
    is_drawing = False
    is_erasing = False

def increase_size():
    global turtle_size
    if turtle_size < 10:
        turtle_size+=1
        t.turtlesize(turtle_size)
        t.pensize(turtle_size * 2)

def decrease_size():
    global turtle_size
    if turtle_size>1:
        turtle_size-=1
        t.turtlesize(turtle_size)
        t.pensize(turtle_size * 2)

def quit_program():
    screen.bye()



def change_pen_color():
    global pen_color
    time.sleep(0.5)
    while True:
        rgb_input = screen.textinput("Change Pen Color", "Enter RGB Values (e.g, 255,0,0 for Red): ")
        if rgb_input:
            try:
              r,g,b = map(int,rgb_input.split(","))
              if 0<=r<=255 and 0<=g<=255 and 0<=b<=255:
                  pen_color=(r/255,g/255,b/255)
                  t.pencolor(pen_color)
                  screen.listen()
                  break
              else:
                  screen.textinput("Invalid RGB values! Must be between 0-255.Try again: ")
            except ValueError:
                print("Invalid input format, use: R,G,B (e.g., 255,0,0).Try again: ")
                change_pen_color()

def follow_cursor(event):
    width = screen.window_width()
    height = screen.window_height()
    x=event.x - width // 2
    y=height // 2 - event.y

    t.setheading(t.towards(x,y))#faces towards x,y
    t.goto(x,y)

    if not is_drawing and not is_erasing:
        t.penup()
    screen.update()

screen.cv.bind("<Motion>", follow_cursor)

screen.onclick(toggle_drawing)

screen.listen()
screen.onkey(enable_erasing, "e")
screen.onkey(clear_screen, "c")
screen.onkey(change_pen_color, "p")
screen.onkey(increase_size,"+")
screen.onkey(decrease_size,"-")
screen.onkey(quit_program,"q")


screen.mainloop()