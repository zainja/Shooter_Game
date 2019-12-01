from tkinter import Tk, Canvas, Menu
width = 300
height = 300
def mouse_movement (event):
    return canvas.coords(event)
def res ():
    pass
def change_binding():
    pass
def pause_game():
    pass
def full_res():
    canvas.configure(width = main_menu.winfo_screenwidth() ,height = main_menu.winfo_screenheight())
    global width = main_menu.winfo_screenwidth()
    global height = main_menu.winfo_screenheight()
def mid_res():
    canvas.configure(width = 1200 ,height = 1000)
    global width = 1200
    global height = 1000
    # canvas.pack()
def small_res():
    canvas.configure(width = 400 ,height = 300)
    global width = 400
    global height = 300


main_window = Tk()
main_menu = Menu(main_window)
main_window.configure(menu = main_menu)

sub_menu = Menu(main_menu)
main_menu.add_command(label = 'pause', command = pause_game)
main_menu.add_cascade(label = 'settings', menu = sub_menu)
res_sub_menu = Menu(sub_menu)
sub_menu.add_cascade(label = 'resolution', menu = res_sub_menu)
res_sub_menu.add_command(label ="full screen", command = full_res)
res_sub_menu.add_command(label ="1200 x 1000", command = mid_res)
res_sub_menu.add_command(label ="400 x 300", command = small_res)

sub_menu.add_command(label = 'change keys', command = change_binding)
canvas = Canvas(main_window, width = width, height=height)
canvas.bind('<Motion>',mouse_movement)
rectangle = canvas.create_rectangle(0, 0, 50, 70, fill="black")
canvas.move(rectangle,10,230)
canvas.pack()

main_window.mainloop()