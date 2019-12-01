from tkinter import Tk, Canvas

def mouse_movement (event):
    return canvas.coords(event)

main_window = Tk()
canvas = Canvas(main_window, width = 300, height=300)

canvas.bind('<Motion>',mouse_movement)
rectangle = canvas.create_rectangle(0, 0, 50, 70, fill="black")
canvas.move(rectangle,10,230)
canvas.pack()

main_window.mainloop()