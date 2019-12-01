from tkinter import Tk, Canvas, Menu, messagebox
import math
import time
game_running = True
width = 300
height = 300
def change_binding():
    pass
def pause_game():
    messagebox.showinfo("Pause", "Game paused")
def full_res():
    canvas.configure(width = main_menu.winfo_screenwidth() ,height = main_menu.winfo_screenheight())
    global width
    width = main_menu.winfo_screenwidth()
    global height
    height = main_menu.winfo_screenheight()
def mid_res():
    canvas.configure(width = 1200 ,height = 1000)
    global width
    width = 1200
    global height
    height = 1000
    # canvas.pack()
def small_res():
    canvas.configure(width = 400 ,height = 300)
    global width
    width = 400
    global height
    height = 300
def exit_game():
    main_window.destroy()

x = 0
y = 0
def mouse_movement (event):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    rec_pos= canvas.coords(1)
    line_pos = canvas.coords(2)
    max_movement = rec_pos[2]
    # to not allow the shooter to shoot from the back
    if (x>max_movement):
        i_component = x - line_pos[0]
        j_component = y - line_pos[1]
        vector_length = math.sqrt(i_component**2 + j_component**2)
        unit_vector_i = i_component / vector_length
        unit_vector_j = j_component / vector_length
        canvas.coords(2,line_pos[0],line_pos[1],(unit_vector_i*50)+line_pos[0],(unit_vector_j*50)+line_pos[1])
        canvas.update()
def shoot (event):
    pos_of_theline = canvas.coords(2)
    i_component = pos_of_theline[2] - pos_of_theline[0]
    j_component = pos_of_theline[3] - pos_of_theline[1]
    vector_length = math.sqrt(i_component**2 + j_component**2)
    unit_vector_i = i_component / vector_length
    unit_vector_j = j_component / vector_length
    ball = Ball(canvas,unit_vector_i,unit_vector_j)
    while True:
        ball.ball_move()
        main_window.update_idletasks()  # background
        main_window.update()  # foreground
        time.sleep(0.01)
    print("pew")
    
class Ball:
    def __init__(self,canvas,x,y):
        self.canvas = canvas
        self.id = canvas.create_oval(0,0,10,10)
        self.canvas.coords(self.id,110,230,120,240)
        self.x = x
        self.y = y
        self.hit = 0
    def ball_move(self):
        self.canvas.move(self.id, self.x*10, self.y*10)
        coords = self.canvas.coords(self.id)
        if self.hit < 10:
            if coords[2] >= width:
                self.x = -self.x
                self.hit +=1
            if coords[0] <= 0:
                self.x = -self.x
                self.hit +=1
            if coords[3] >= height:
                self.y = -self.y
                self.hit +=1
            if coords[1] <= 0:
                self.y = -self.y
                self.hit +=1
        else:
            self.canvas.coords(self.id,-1,-1,-1,-1)
    def ball_hits_something():
        pass


main_window = Tk()
# menu bar
main_menu = Menu(main_window)
main_window.configure(menu = main_menu)
sub_menu = Menu(main_menu)
main_menu.add_command(label = 'pause', command = pause_game)
main_menu.add_cascade(label = 'settings', menu = sub_menu)
main_menu.add_command(label = 'Quit', command = exit_game)
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
aim_line = canvas.create_line(0,50,50,0)
canvas.coords(aim_line,110,230,160,200)
canvas.bind('<Motion>',mouse_movement)
canvas.bind('<Button-1>',shoot)

canvas.pack()

main_window.mainloop()
