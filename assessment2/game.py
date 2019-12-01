from tkinter import Tk, Canvas, Menu, messagebox
import math
import time
import random
game_running = True
width = 400
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
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        main_window.destroy()

rectangle_list = []
def generated_areas(x, y, x1, y1):
    size_x =0 
    size_y = 0
    while size_x < 20 or size_y < 20:
        rand_x = random.randint(x,x1)
        rand_y = random.randint(y,y1)
        size_x = random.randint(0, x1 -rand_x)
        size_y = random.randint(0,y1-rand_y)
    return canvas.create_rectangle(rand_x, rand_y, rand_x+size_x ,rand_y+size_y, fill="red")

def ball_moves():
    global ball
    for i in ball:
        i.ball_move()
    # time.sleep(0.01)
    # ball_moves()

x = 0
y = 0
def mouse_movement (event):
    global aim_line
    global rectangle
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    rec_pos= canvas.coords(rectangle)
    line_pos = canvas.coords(aim_line)
    max_movement = rec_pos[2]
    # to not allow the shooter to shoot from the back
    if (x>max_movement):
        i_component = x - line_pos[0]
        j_component = y - line_pos[1]
        vector_length = math.sqrt(i_component**2 + j_component**2)
        unit_vector_i = i_component / vector_length
        unit_vector_j = j_component / vector_length
        canvas.coords(aim_line,line_pos[0],line_pos[1],(unit_vector_i*50)+line_pos[0],(unit_vector_j*50)+line_pos[1])
        canvas.update()

def shoot (event):
    global ball
    global aim_line
    pos_of_theline = canvas.coords(aim_line)
    i_component = pos_of_theline[2] - pos_of_theline[0]
    j_component = pos_of_theline[3] - pos_of_theline[1]
    vector_length = math.sqrt(i_component**2 + j_component**2)
    unit_vector_i = i_component / vector_length
    unit_vector_j = j_component / vector_length
    ball.append(Ball(canvas,1,1))
    ball_moves()
    # while ball.hit <= 10:
    #     main_window.update_idletasks()  # background
    #     main_window.update()  # foreground
    #     time.sleep(0.01)
    print("pew")
    

class Ball:
    def __init__(self,canvas,x,y):
        global aim_line
        self.canvas = canvas
        self.start_coords = canvas.coords(aim_line)
        self.size = 10
        self.id = canvas.create_oval(0,0,10,10)
        # self.canvas.coords(self.id,self.start_coords[0],self.start_coords[1],self.start_coords[0]+10,self.start_coords[1]+10)
        self.x = x
        self.y = y
        self.hit = 0
    def ball_move(self):
        self.canvas.move(self.id, self.x, self.y)
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
        # else:
        #     self.canvas.coords(self.id,-1,-1,-1,-1)
    def ball_hits_something(element):
        pass


main_window = Tk()
# menu bar
ball = []
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
rectangle = canvas.create_rectangle(0,height*0.7, width*0.1, height*0.4, fill="black")
aim_line = canvas.create_line(0,50,50,0)
rect_coords = canvas.coords(rectangle)
mid_rect = (rect_coords[1]+rect_coords[3])*0.5
canvas.coords(aim_line,rect_coords[2],mid_rect,rect_coords[2]+50,mid_rect+50)
canvas.bind('<Motion>',mouse_movement)
canvas.bind('<Button-1>',shoot)
canvas.pack()
while True:
    canvas.update()
main_window.mainloop()
