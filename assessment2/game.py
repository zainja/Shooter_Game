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
def restart(ball,main_menu,canvas,height,width,player,aim_line,enemy_box,ball_movement):
    ball = []
    ball_movement = []
    canvas.delete("all")
    game_run(main_menu,canvas,height,width,player,aim_line,enemy_box)


def full_res():
    global width
    width = main_menu.winfo_screenwidth()
    global height
    height = main_menu.winfo_screenheight()
    canvas.configure(width = width ,height = height)
    restart()

def mid_res():
    global width
    width = 1200
    global height
    height = 1000
    canvas.configure(width = width ,height = height)
    restart()

def small_res():
    global width
    width = 400
    global height
    height = 300
    canvas.configure(width = width ,height = height)
    restart()

def exit_game(main_window):
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        main_window.destroy()

def ball_move():
    global ball,ball_movement,width ,height, player, list_of_boxes,enemy
    if len(ball) == 3:
        canvas.unbind('<Button-1>')
    while True :
        for i in range (0, len(ball)):
            i_coords = canvas.coords(ball[i])
            
            if i_coords[2] >= width:
                ball_movement[i][0] = - ball_movement[i][0]
            if i_coords[0] <= 0:
                ball_movement[i][0] = - ball_movement[i][0]
            if i_coords[3] >= height:
                ball_movement[i][1] = - ball_movement[i][1]
            if i_coords[1] <= 0:
                ball_movement[i][1] = - ball_movement[i][1]
            if ball_hits_object(ball[i],player):
                ball_movement[i]= [0,0]
                pause_game()
                restart()
            if ball_hits_object(ball[i],enemy):
                pause_game()
                restart()
            
            for j in range (0,len(list_of_boxes)):
                if ball_hits_object(ball[i],list_of_boxes[j]) == 1:
                    ball_movement[i][0] = - ball_movement[i][0]
                if ball_hits_object(ball[i], list_of_boxes[j]) == 2:
                    ball_movement[i][1] = - ball_movement[i][1]
            
            canvas.move(ball[i], ball_movement[i][0],ball_movement[i][1])
        canvas.update()
        time.sleep(0.001)
    
def ball_hits_object(i,j):
    i_coords = canvas.coords(i)
    box_coords = canvas.coords(j)

    if (i_coords[0] <= box_coords[2]) and (i_coords[2] >= box_coords[2]) and \
        (i_coords[1] >= box_coords[1] and i_coords[1] <= box_coords [3]):
        return 1
    # from left to right
    if (i_coords[0] <= box_coords[0]) and (i_coords[2] >= box_coords[0] and \
        i_coords[1] >= box_coords[1] and i_coords[1] <= box_coords [3] ):
        return 1
    # top to bottom
    if (i_coords[0] >= box_coords[0]) and (i_coords[0] <= box_coords[2] and \
        i_coords[1] <= box_coords[1] and i_coords[3] >= box_coords [1] ):
        return 2
    # bottom to top
    if (i_coords[0] >= box_coords[0]) and (i_coords[0] <= box_coords[2] and \
        i_coords[1] <= box_coords[3] and i_coords[3] >= box_coords [3] ):
        return 2
   
    return 0
    


def mouse_movement (event):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    rec_pos= canvas.coords(player)
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
    global ball_movement
    pos_of_theline = canvas.coords(aim_line)
    i_component = pos_of_theline[2] - pos_of_theline[0]
    j_component = pos_of_theline[3] - pos_of_theline[1]
    vector_length = math.sqrt(i_component**2 + j_component**2)
    unit_vector_i = i_component / vector_length
    unit_vector_j = j_component / vector_length
    ball.append(canvas.create_oval(pos_of_theline[0]+2,pos_of_theline[1]+2,pos_of_theline[0]+12,pos_of_theline[1]+12,fill = 'red'))
    ball_movement.append([unit_vector_i*2,unit_vector_j*2])
    ball_move()

def create_grid(height,width,total):
    
    total_grid = []
    one_box = []
    x = 0
    y = 0
    width_of_box = width/ total
    height_of_box = height/total
    number_of_boxes = total**2
    for box in range (0,number_of_boxes):
        one_box.append(x)
        one_box.append(y)
        x += width_of_box
        one_box.append(x)
        one_box.append(y+height_of_box)
        total_grid.append(one_box)
        one_box = []
        if x == width:
            y += height_of_box
            x = 0
    return total_grid


def place_player(grid):
    global player_box,player,aim_line
    player_box = random.randint(0,len(grid)-1)
    # generate point to place the box
    # x coords
    point_x = random.uniform(grid[player_box][0],grid[player_box][2])
    point_x2 =  point_x + rec_size_x 
    while point_x2 >= grid[player_box][2]:
        point_x = random.uniform(grid[player_box][0],grid[player_box][2])
        point_x2 =  point_x + rec_size_x 
    # generate y coords 
    point_y = random.uniform(grid[player_box][1],grid[player_box][3])
    point_y2 = point_y + rec_size_y
    while point_y2 >= grid[player_box][3]:
        point_y = random.uniform(grid[player_box][1],grid[player_box][3])
        point_y2 = point_y + rec_size_y

    player = canvas.create_rectangle(point_x,point_y,point_x2,point_y2)
    aim_line = canvas.create_line(0,width*0.1,height*0.1,0)
    rect_coords = canvas.coords(player)
    mid_rect = (rect_coords[1]+rect_coords[3])*0.5
    canvas.coords(aim_line,rect_coords[2],mid_rect,rect_coords[2]+50,mid_rect+50)

def place_enemy(grid):
    global enemy_box,enemy
    enemy_box = random.randint(0,len(grid)-1)

    while  abs(enemy_box - player_box) == 1:
        enemy_box = random.randint(0,len(grid)-1)

    while enemy_box == player_box:
        enemy_box = random.randint(0,len(grid)-1)
    
    point_x = random.uniform(grid[enemy_box][0],grid[enemy_box][2])
    point_x2 =  point_x + rec_size_x 
    while point_x2 >= grid[enemy_box][2]:
        point_x = random.uniform(grid[enemy_box][0],grid[enemy_box][2])
        point_x2 =  point_x + rec_size_x 
    # generate y coords 
    point_y = random.uniform(grid[enemy_box][1],grid[enemy_box][3])
    point_y2 = point_y + rec_size_y
    while point_y2 >= grid[enemy_box][3]:
        point_y = random.uniform(grid[enemy_box][1],grid[enemy_box][3])
        point_y2 = point_y + rec_size_y    
    enemy = canvas.create_rectangle(point_x,point_y,point_x2,point_y2, fill = "green")  

def generated_areas(list_of_grid):
    global enemy_box,player_box
    generated_boxes = [] 
    for i in range(len(list_of_grid)):
        size_x =0 
        size_y = 0
        if i != player_box and i != enemy_box:
            x = list_of_grid[i][0]
            y = list_of_grid[i][1]
            x1 = list_of_grid[i][2]
            y1 = list_of_grid[i][3]
            while size_x < 40 or size_y < 40:
                rand_x = random.uniform(x,x1)
                rand_y = random.uniform(y,y1)
                size_x = random.uniform(0, x1 -rand_x)
                size_y = random.uniform(0,y1-rand_y)
            generated_boxes.append(canvas.create_rectangle(rand_x, rand_y, rand_x+size_x ,rand_y+size_y, fill="red"))
    return generated_boxes  


def game_run(window,canvas,height,width,player,aim_line,enemy):
    global list_of_boxes
    grid = create_grid(height,width)
    for i in grid:
        canvas.create_rectangle(i)
    place_player(grid)
    place_enemy(grid)
    canvas.bind('<Motion>',mouse_movement)
    canvas.bind('<Button-1>',shoot)
    list_of_boxes = generated_areas(grid)
    canvas.pack()
    window.mainloop()  

### var decleration ###
main_window = Tk()
grid = []
ball = []
list_of_boxes = None
ball_movement = []
player = None
aim_line = None
enemy = None
player_box = 0
enemy_box = 0 
canvas = Canvas(main_window, width = width, height=height)
rec_size_x = width*0.09
rec_size_y = height*0.2

main_menu = Menu(main_window)
main_window.configure(menu = main_menu)
sub_menu = Menu(main_menu)
main_menu.add_command(label = 'pause', command = pause_game)
main_menu.add_command(label = 'restart', command = lambda : restart(ball,main_menu,canvas,height,width,player,aim_line,enemy_box,ball_movement))
main_menu.add_cascade(label = 'settings', menu = sub_menu)
main_menu.add_command(label = 'Quit', command = lambda: exit_game(main_window))
res_sub_menu = Menu(sub_menu)
sub_menu.add_cascade(label = 'resolution', menu = res_sub_menu)
res_sub_menu.add_command(label ="full screen", command = full_res)
res_sub_menu.add_command(label ="1200 x 1000", command = mid_res)
res_sub_menu.add_command(label ="400 x 300", command = small_res)
sub_menu.add_command(label = 'change keys', command = change_binding)

game_run(main_menu,canvas,height,width,player,aim_line,enemy_box)
