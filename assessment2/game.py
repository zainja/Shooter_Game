from tkinter import Tk, Canvas
x = 0
y = 0

def mouse_movement (event):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    canvas.coords(2,110,230,x,y)
    canvas.update()

main_window = Tk()
canvas = Canvas(main_window,width=300,height=300)
rectangle = canvas.create_rectangle(0, 0, 50, 70, fill="black")
canvas.move(rectangle,60,230)
aim_line = canvas.create_line(0,50,50,0)
canvas.coords(aim_line,110,230,160,200)
canvas.bind('<Motion>',mouse_movement)
canvas.pack()

main_window.mainloop()