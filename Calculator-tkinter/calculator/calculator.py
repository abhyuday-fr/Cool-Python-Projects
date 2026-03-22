from tkinter import *
import tkinter.messagebox
#imported message box for a special case(used in equal function for division)

window=Tk()
window.geometry("400x300")
window.title("Calculator")

e=Entry(window,width=56,borderwidth=5)
e.place(x=0,y=0)

def click(num):
    result=e.get()
    e.delete(0,END)
    e.insert(0,str(result)+str(num))

b=Button(window,text="1",width=12,activebackground="cyan",activeforeground="black",command=lambda:click(1))
b.place(x=10,y=60)
b=Button(window,text="2",width=12,activebackground="cyan",activeforeground="black",command=lambda:click(2))
b.place(x=80,y=60)
b=Button(window,text="3",width=12,activebackground="cyan",activeforeground="black",command=lambda:click(3))
b.place(x=170,y=60)
b=Button(window,text="4",width=12,activebackground="cyan",activeforeground="black",command=lambda:click(4))
b.place(x=10,y=120)
b=Button(window,text="5",width=12,activebackground="cyan",activeforeground="black",command=lambda:click(5))
b.place(x=80,y=120)
b=Button(window,text="6",width=12,activebackground="cyan",activeforeground="black",command=lambda:click(6))
b.place(x=170,y=120)
b=Button(window,text="7",width=12,activebackground="cyan",activeforeground="black",command=lambda:click(7))
b.place(x=10,y=180)
b=Button(window,text="8",width=12,activebackground="cyan",activeforeground="black",command=lambda:click(8))
b.place(x=80,y=180)
b=Button(window,text="9",width=12,activebackground="cyan",activeforeground="black",command=lambda:click(9))
b.place(x=170,y=180)
b=Button(window,text="0",width=12,activebackground="cyan",activeforeground="black",command=lambda:click(0))
b.place(x=10,y=240)

def add():
    n1=e.get()
    global i
    global math
    math="addition"
    i=float(n1)
    e.delete(0,END)
b=Button(window,text="+",width=12,activebackground="black",activeforeground="white",command=add)
b.place(x=270,y=60)
#x=80,y=240
def sub():
    n1=e.get()
    global i
    global math
    math = "subtraction"
    i=float(n1)
    e.delete(0,END)
b=Button(window,text="-",width=12,activebackground="black",activeforeground="white",command=sub)
b.place(x=270,y=120)

def mult():
    n1=e.get()
    global i
    global math
    math = "multiplication"
    i=float(n1)
    e.delete(0,END)
b=Button(window,text="*",width=12,activebackground="black",activeforeground="white",command=mult)
b.place(x=270,y=180)

def div():
    n1=e.get()
    global i
    global math
    math = "division"
    i=float(n1)
    e.delete(0,END)
b=Button(window,text="/",width=12,activebackground="black",activeforeground="white",command=div)
b.place(x=270,y=240)

def equal():
    n2=e.get()
    e.delete(0,END)
    if(math=="addition"):
        e.insert(0,i+float(n2))
    elif(math=="subtraction"):
        e.insert(0,i-float(n2))
    elif(math=="multiplication"):
        e.insert(0,i*float(n2))
    elif(math=="division"):
        #error handling for DivisionByZero
        try:
         e.insert(0,i/float(n2))
        except ZeroDivisionError:
         tkinter.messagebox.showerror("Error","division by zero")
b=Button(window,text="=",width=12,activebackground="black",activeforeground="white",command=equal)
b.place(x=170,y=240)

def clear():
    e.delete(0,END)
b=Button(window,text="clear",width=12,activebackground="red",activeforeground="white",fg="red",command=clear)
b.place(x=80,y=240)

window.mainloop()