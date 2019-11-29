from tkinter import Tk, Canvas
x = 0
y = 0

def mouse_movement (event):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    canvas.coords(1,x,y,x-50,y-70)
    canvas.update()

main_window = Tk()
canvas = Canvas(main_window,width=300,height=300)
rectangle = canvas.create_rectangle(0, 0, 50, 70, fill="black")
canvas.bind('<Motion>',mouse_movement)
canvas.pack()

main_window.mainloop()