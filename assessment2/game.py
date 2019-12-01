from tkinter import Tk, Canvas, Menu

def mouse_movement (event):
    return canvas.coords(event)
def res ():
    pass
def change_binding():
    pass
def pause_game():
    pass
main_window = Tk()
main_menu = Menu(main_window)
main_window.configure(menu = main_menu)

sub_menu = Menu(main_menu)
main_menu.add_command(label = 'pause', command = pause_game)
main_menu.add_cascade(label = 'settings', menu = sub_menu)
sub_menu.add_command(label = 'resolution', command = res)
sub_menu.add_command(label = 'change keys', command = change_binding)
canvas = Canvas(main_window, width = 300, height=300)

canvas.bind('<Motion>',mouse_movement)
rectangle = canvas.create_rectangle(0, 0, 50, 70, fill="black")
canvas.move(rectangle,10,230)
canvas.pack()

main_window.mainloop()