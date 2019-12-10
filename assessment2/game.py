from tkinter import Tk, Canvas, Menu, messagebox, PhotoImage, Button, Label, Entry
import math
import time
import random
import re

player_settings = {
    'player_name': None,
    'level': 1,
    'score': 0,
    'lives': 5,
    'key': '<Button-1>',
    'screen_height': 900,
    'screen_width': 1200
}
width = player_settings['screen_width']
height = player_settings['screen_height']


def update_dictonary():
    pass

def btn_switch(mode):
    global main_window, canvas, height, width, list_of_btns
    for l in list_of_btns:
        l.destroy()
    if mode == 0:
        game_run(main_window, canvas, height, width)
    if mode == 1:
        load_game()
    if mode == 2:
        leaderboard()
    if mode == 3:
        resolution_change()
    if mode == 4:
        change_binding()
    if mode == 5:
        main_window.destroy()
    if mode == 6:
        entry_menu()
    if mode == 7:
        enter_name()
def enter_name():
    global main_window, width, list_of_btns
    label_enter_name = Label(main_window, text="Enter a Name", font = ('Times new roman', 25))
    label_enter_name.place(relx=0.1, rely=0.5)
    entry_name = Entry(main_window, width=int(width*0.06))
    entry_name.place(relx=0.1, rely=0.6)
    confirm_btn = Button(text='start', command=lambda: btn_switch(0))
    confirm_btn.place(relx=0.1, rely=0.7)
    list_of_btns.append(label_enter_name)
    list_of_btns.append(entry_name)
    list_of_btns.append(confirm_btn)





def resolution_change():
    global width, height,main_window, list_of_btns
    btn_width = int(width*0.6)
    btn_height = int(height*0.1)
    full_screen_btn = Button(main_window, width=btn_width, height=btn_height, image=play_btn_img, command=lambda :full_res())
    full_screen_btn.place(x=width*0.03, y=height*0.1)
    mid_res_btn = Button(main_window,width=btn_width,height=btn_height,image=load_btn_img,command=lambda : mid_res())
    mid_res_btn.place(x=width*0.03, y=height*0.25)
    small_res_btn = Button(main_window,width=btn_width,height=btn_height,image=leaderboard_btn_img,command=lambda : small_res())
    small_res_btn.place(x=width*0.03, y=height*0.4)
    back_btn = Button(main_window,width=btn_width,height=btn_height,image=resolution_btn_img,command=lambda : btn_switch(6))
    back_btn.place(x=width*0.03, y=height*0.55)
    list_of_btns.append(full_screen_btn)
    list_of_btns.append(mid_res_btn)
    list_of_btns.append(small_res_btn)
    list_of_btns.append(back_btn)


def change_binding():
    global main_window, list_of_btns
    label_info_bind = Label(main_window, text ="Press any key to change it to the shooting key", font=("Times new roman", 25))
    label_info_bind.place(relx = 0.1, rely=0.5)
    list_of_btns.append(label_info_bind)
    main_window.bind('<Key>', bind_new_key)


def bind_new_key(event):
    global shoot_key, main_window, list_of_btns
    shoot_key = '<'+event.keysym + '>'
    info_key = "key choosen was " + shoot_key
    main_window.unbind('<Key>')
    messagebox.showinfo("Key changes!", info_key)
    btn_switch(6)


def pause_game():
    messagebox.showinfo("Pause", "Game paused")


def load_game():
    pass


def leaderboard():
    pass


def restart(mode):
    global main_window, canvas, height, width, enemy_box,\
            ball, list_of_boxes, grid, ball_movement, player_box, level, score
    if mode == 0:
        level = 1
        score = 0
    ball = []
    list_of_boxes = []
    grid = []
    ball_movement = []
    enemy_box = 0
    player_box = 0
    place_player
    canvas.delete("all")
    game_run(main_window, canvas, height, width)


def exit_game(main_window):
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        main_window.destroy()


def full_res():
    global width
    width = int(main_window.winfo_screenwidth()*0.97)
    global height
    height = int(main_window.winfo_screenheight()*0.92)
    main_window.geometry(str(width)+"x"+str(height))
    canvas.configure(width=width, height=height)

def mid_res():
    global width
    width = 1200
    global height
    height = 1000
    main_window.geometry(str(width)+"x"+str(height))
    canvas.configure(width=width, height=height)


def small_res():
    global width
    width = 600
    global height
    height = 800
    main_window.geometry(str(width)+"x"+str(height))
    canvas.configure(width=width, height=height)



def player_won():
    global level, score
    level +=1
    score += 100
    messagebox.showinfo("Game WON", "CONGRATS")
    restart(1)


def player_lost():
    global level, score, lives
    level -=1
    score -= 150
    if score < 0 :
        score = 0
    if level < 1:
        level = 1
    if lives == 0:
        level = 1
    messagebox.showinfo("LOST YA BASIC", "YOU LOOOOOOOOSEEE")
    restart(1)


def ball_move():
    global ball, ball_movement, width, height, player, list_of_boxes, enemy
    if len(ball) == 3:
        canvas.unbind('<Button-1>')
    while True:
        for i in range(0, len(ball)):
            i_coords = canvas.coords(ball[i])      
            if i_coords[2] >= width:
                ball_movement[i][0] = - ball_movement[i][0]
            if i_coords[0] <= 0:
                ball_movement[i][0] = - ball_movement[i][0]
            if i_coords[3] >= height:
                ball_movement[i][1] = - ball_movement[i][1]
            if i_coords[1] <= 0.1*height:
                ball_movement[i][1] = - ball_movement[i][1]
            if ball_hits_object(ball[i], player):
                player_lost()
            if ball_hits_object(ball[i], enemy):
                player_won()
            if len(list_of_boxes) != 0:
                for j in range(len(list_of_boxes)):
                    box_coords = canvas.coords(list_of_boxes[j])
                    if (i_coords[0] > box_coords[0] and i_coords[0] < box_coords[2]) or (i_coords[2] > box_coords[0] and i_coords[2] < box_coords[2]):
                        #coming from left side
                        if (i_coords[1] <= box_coords[3]) and (i_coords[3] >= box_coords[3]):
                            ball_movement[i][1] = - ball_movement[i][1]
                        elif (i_coords[3] >= box_coords[1]) and (i_coords[1] <= box_coords[1]):
                            ball_movement[i][1] = - ball_movement[i][1]

                    if (i_coords[1] > box_coords[1] and i_coords[1] < box_coords[3]) or (i_coords[3] > box_coords[1] and i_coords[3] < box_coords[3]):
                        if (i_coords[0] <= box_coords[2]) and (i_coords[2] >= box_coords[2]):
                            ball_movement[i][0] = - ball_movement[i][0]
                        elif (i_coords[2] >= box_coords[0]) and (i_coords[0] <= box_coords[0]):
                            ball_movement[i][0] = - ball_movement[i][0]
            canvas.move(ball[i], ball_movement[i][0], ball_movement[i][1])
        canvas.update()
        time.sleep(0.001)

def ball_hits_object(i, j):
    i_coords = canvas.coords(i)
    box_coords = []
    if j == player:
        box_coords = player_hit_box()
    if j == enemy:
        box_coords = enemy_hit_box()
    #check for right and left 
    if (i_coords[1] >= box_coords[1] and i_coords[1] <= box_coords[3]) or (i_coords[3] >= box_coords[1] and i_coords[3] <= box_coords[3]):
        #coming from left side
        if (i_coords[0] <= box_coords[2]) and (i_coords[2] >= box_coords[2]):
            return True
        elif (i_coords[2] >= box_coords[0]) and (i_coords[0] <= box_coords[0]):
            return True
    if (i_coords[0] >= box_coords[0] and i_coords[0] <= box_coords[2]) or (i_coords[2] >= box_coords[0] and i_coords[2] <= box_coords[2]):
        # coming from left side
        if (i_coords[1] <= box_coords[3]) and (i_coords[3] >= box_coords[3]):
            return True
        elif (i_coords[3] >= box_coords[1]) and (i_coords[1] <= box_coords[1]):
            return True
    return False


def mouse_movement(event):
    global player_direction, aim, player, current_player_img
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    rec_pos = player_hit_box()
    line_pos = canvas.coords(aim_line)
    if (x < rec_pos[2]):
        line_pos[0] = rec_pos[0]
        line_pos[2] = rec_pos[0] - 50
        canvas.itemconfig(player, image=aim_f[0])
        current_player_img = aim_f[0]
    if (x > rec_pos[2]):
        line_pos[0] = rec_pos[2]
        line_pos[2] = rec_pos[2] + 50
        canvas.itemconfig(player, image=aim[0])
        current_player_img = aim[0]
    i_component = x - line_pos[0]
    j_component = y - line_pos[1]
    vector_length = math.sqrt(i_component**2 + j_component**2)
    unit_vector_i = i_component / vector_length
    unit_vector_j = j_component / vector_length
    canvas.coords(aim_line, line_pos[0], line_pos[1], (unit_vector_i*50) + line_pos[0], (unit_vector_j*50)+line_pos[1])
    canvas.update()


def shoot(event):
    global ball, aim_line, ball_movement, aim, player, current_player_img, shoot_anim, idle
    pos_of_theline = canvas.coords(aim_line)
    i_component = pos_of_theline[2] - pos_of_theline[0]
    j_component = pos_of_theline[3] - pos_of_theline[1]
    vector_length = math.sqrt(i_component**2 + j_component**2)
    unit_vector_i = i_component / vector_length
    unit_vector_j = j_component / vector_length
    if current_player_img == aim[0]:
        for i in range(1,len(aim)-1):
            time.sleep(0.1)
            canvas.itemconfig(player, image=aim[i])
            current_player_img = aim[i]
            canvas.update()
        for i in range(0,len(shoot_anim)):
            time.sleep(0.1)
            canvas.itemconfig(player, image=shoot_anim[i])
            current_player_img = shoot_anim[i]
            canvas.update()
    if current_player_img == aim_f[0]:
        for i in range(1,len(aim_f)-1):
            time.sleep(0.1)
            canvas.itemconfig(player, image=aim_f[i],anchor = 'ne')
            current_player_img = aim_f[i]
            canvas.update()
        for i in range(0,len(shoot_anim_f)):
            time.sleep(0.1)
            canvas.itemconfig(player, image=shoot_anim_f[i], anchor = 'ne')
            current_player_img = shoot_anim_f[i]
            canvas.update()
    canvas.itemconfig(player, image=idle, anchor='nw')
    current_player_img = idle

    ball.append(canvas.create_oval(pos_of_theline[2],pos_of_theline[3],pos_of_theline[2]+10,pos_of_theline[3]+10,fill="yellow"))
    ball_movement.append([unit_vector_i*2,unit_vector_j*2])
    ball_move()



def create_grid(height, width, total):
    main_height = height*0.9
    total_grid = []
    one_box = []
    x = 0
    y = height*0.1
    width_of_box = width / total
    height_of_box = main_height/total
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


def player_hit_box():
    global player, current_player_img
    x2 = canvas.coords(player)[0] + current_player_img.width()
    y2 = canvas.coords(player)[1] + current_player_img.height()
    return [canvas.coords(player)[0], canvas.coords(player)[1], x2, y2]


def enemy_hit_box():
    global enemy, enemy_img
    x2 = canvas.coords(enemy)[0] + enemy_img.width()
    y2 = canvas.coords(enemy)[1] + enemy_img.height()
    return [canvas.coords(enemy)[0],canvas.coords(enemy)[1], x2, y2]


def place_player(grid):
    global player_box, player, aim_line, idle,current_player_img
    player_box = random.randint(0, len(grid)-1)
    rec_size_x = current_player_img.width()
    rec_size_y = current_player_img.height()
    # generate point to place the box
    # x coords
    point_x = random.uniform(grid[player_box][0],grid[player_box][2])
    point_x2 = point_x + rec_size_x
    while point_x2 >= grid[player_box][2]:
        point_x = random.uniform(grid[player_box][0],grid[player_box][2])
        point_x2 = point_x + rec_size_x
    # generate y coords
    point_y = random.uniform(grid[player_box][1], grid[player_box][3])
    point_y2 = point_y + rec_size_y
    while point_y2 >= grid[player_box][3]:
        point_y = random.uniform(grid[player_box][1], grid[player_box][3])
        point_y2 = point_y + rec_size_y
    player = canvas.create_image(point_x, point_y, anchor="nw", image=idle)
    aim_line = canvas.create_line(0, width*0.1, height*0.1, 0)
    rect_coords = player_hit_box()
    mid_rect = (rect_coords[1]+rect_coords[3]) * 0.5
    canvas.coords(aim_line, rect_coords[2], mid_rect, rect_coords[2] + 50, mid_rect+50)


def place_enemy(grid, level):
    global enemy_box, enemy, player_box, enemy_img
    rec_size_x = enemy_img.width()
    rec_size_y = enemy_img.height()
    enemy_box = player_box
    while enemy_box == player_box:
        enemy_box = random.randint(0, len(grid)-1)
    print(grid[enemy_box])
    if level >= 3:
        while check_placement(grid, enemy_box, player_box):
            enemy_box = random.randint(0, len(grid)-1)
    point_x = random.uniform(grid[enemy_box][0],grid[enemy_box][2])
    point_x2 = point_x + rec_size_x
    while point_x2 >= grid[enemy_box][2]:
        point_x = random.uniform(grid[enemy_box][0], grid[enemy_box][2])
        point_x2 = point_x + rec_size_x
    # generate y coords 
    point_y = random.uniform(grid[enemy_box][1],grid[enemy_box][3])
    point_y2 = point_y + rec_size_y
    while point_y2 >= grid[enemy_box][3]:
        point_y = random.uniform(grid[enemy_box][1],grid[enemy_box][3])
        point_y2 = point_y + rec_size_y    
    enemy = canvas.create_image(point_x,point_y, anchor="nw", image = enemy_img)  


def check_placement(grid, enemy_box, player_box):
    print("enemy",str(enemy_box) , "player" , str(player_box))
    if grid[enemy_box][0] == grid[player_box][2] and grid[enemy_box][1] == grid[player_box][3]:
        return True
    if grid[enemy_box][0] == grid[player_box][0] and grid[enemy_box][1] == grid[player_box][3]:
        return True
    if grid[enemy_box][0] == grid[player_box][2] and grid[enemy_box][1] == grid[player_box][1]:
        return True
    # corner 2
    if grid[enemy_box][2] == grid[player_box][0] and grid[enemy_box][1] == grid[player_box][3]:
        return True
    if grid[enemy_box][2] == grid[player_box][2] and grid[enemy_box][1] == grid[player_box][3]:
        return True
    if grid[enemy_box][2] == grid[player_box][0] and grid[enemy_box][1] == grid[player_box][1]:
        return True
    # corner 3
    if grid[enemy_box][0] == grid[player_box][2] and grid[enemy_box][3] == grid[player_box][1]:
        return True
    if grid[enemy_box][0] == grid[player_box][2] and grid[enemy_box][3] == grid[player_box][3]:
        return True
    if grid[enemy_box][0] == grid[player_box][0] and grid[enemy_box][3] == grid[player_box][1]:
        return True
    # corner 4
    if grid[enemy_box][2] == grid[player_box][0] and grid[enemy_box][3] == grid[player_box][1]:
        return True
    if grid[enemy_box][2] == grid[player_box][0] and grid[enemy_box][3] == grid[player_box][3]:
        return True
    if grid[enemy_box][2] == grid[player_box][2] and grid[enemy_box][3] == grid[player_box][1]:
        return True
    # equal
    if  enemy_box == player_box:
        return True
    return False


def generated_areas(list_of_grid):
    global enemy_box, player_box
    generated_boxes = []
    for i in range(len(list_of_grid)):
        size_x = 0 
        size_y = 0
        if i != player_box and i != enemy_box:
            x = list_of_grid[i][0]
            y = list_of_grid[i][1]
            x1 = list_of_grid[i][2]
            y1 = list_of_grid[i][3]
            rand_x = random.uniform(x,x1)
            rand_y = random.uniform(y,y1)
            while size_x < ((x1-x) *0.3 ) or size_y < ((y1-y)*0.2):
                rand_x = random.uniform(x,x1)
                rand_y = random.uniform(y,y1)
                size_x = random.uniform(0, x1 -rand_x)
                size_y = random.uniform(0,y1-rand_y)
            generated_boxes.append(canvas.create_rectangle(rand_x, rand_y, rand_x+size_x ,rand_y+size_y, fill="red"))
    return generated_boxes


def game_run(window, canvas,height,width):
    global list_of_boxes, shoot_key
    total = 0
    level_x_pos = width*0.1
    level_y_pos = (0.1*height)/3
    score_x_pos = width*0.7
    score_y_pos = level_y_pos
    level_txt = "level: " + str(level)
    score_txt = "score: " + str(score)
    bg_for_txt = canvas.create_rectangle(0,0,width,height*0.1,fill="red")
    level_label = canvas.create_text(level_x_pos,level_y_pos,font="Times 20 italic bold",text = level_txt ,anchor = "nw")
    score_label = canvas.create_text(score_x_pos,score_y_pos,font="Times 20 italic bold",text = score_txt ,anchor = "nw")
    if level == 1:
        total = 2
    if level == 2:
        total = 3
    if level == 3:
        total = 4
    if level >= 4:
        total = 5
    grid = create_grid(height,width,total)
    for i in grid:
        canvas.create_rectangle(i)
    place_player(grid)
    place_enemy(grid,level)
    list_of_boxes = generated_areas(grid)
    main_window.bind('<Motion>',mouse_movement)
    main_window.bind(shoot_key,shoot)
    canvas.pack()
    window.mainloop()


def entry_menu():
    global main_window,height,width,canvas,height,width, list_of_btns
    btn_width = int(width*0.6)
    btn_height= int(height*0.1)
    play_btn = Button(main_window,width=btn_width,height=btn_height,image=play_btn_img,command=lambda : btn_switch(7))
    play_btn.place(x=width*0.03, y=height*0.1)
    load_game_btn = Button(main_window,width=btn_width,height=btn_height,image=load_btn_img,command=lambda : btn_switch(1))
    load_game_btn.place(x=width*0.03, y=height*0.25)
    leaderboard_btn = Button(main_window,width=btn_width,height=btn_height,image=leaderboard_btn_img,command=lambda : btn_switch(2))
    leaderboard_btn.place(x=width*0.03, y=height*0.4)
    resoloution_btn = Button(main_window,width=btn_width,height=btn_height,image=resolution_btn_img,command=lambda : btn_switch(3))
    resoloution_btn.place(x=width*0.03, y=height*0.55)
    change_keys_btn = Button(main_window,width=btn_width,height=btn_height,image= change_keys_btn_img,command=lambda : btn_switch(4))
    change_keys_btn.place(x=width*0.03, y=height*0.70)
    quit_key_btn = Button(main_window,width=btn_width,height=btn_height,image= quit_key_btn_img,command=lambda : btn_switch(5))
    quit_key_btn.place(x=width*0.03, y=height*0.85)
    list_of_btns.append(play_btn)
    list_of_btns.append(load_game_btn)
    list_of_btns.append(leaderboard_btn)
    list_of_btns.append(resoloution_btn)
    list_of_btns.append(change_keys_btn)
    list_of_btns.append(quit_key_btn)


### var decleration ###
main_window = Tk()
main_window.geometry(str(width)+"x"+str(height))
main_window.resizable(0, 0)
main_window.wm_attributes("-topmost", 1)
grid = []
ball = []
list_of_boxes = []
ball_movement = []
player = None
aim_line = None
enemy = None
player_box = 0
enemy_box = 0 
canvas = Canvas(main_window, width = width, height=height)
level = player_settings['level']
enemy_img = PhotoImage(file=".//enemy//enemy.png")
aim = []
aim_f = []
shoot_anim = []
shoot_anim_f = []
shoot_key = player_settings['key']
score = player_settings['score']
lives = player_settings['lives']

aim.append(PhotoImage(file=".//Aim//Aim_01.png"))
aim.append(PhotoImage(file=".//Aim//Aim_02.png"))
aim.append(PhotoImage(file=".//Aim//Aim_03.png"))
aim.append(PhotoImage(file=".//Aim//Aim_04.png"))
aim.append(PhotoImage(file=".//Aim//Aim_05.png"))
aim.append(PhotoImage(file=".//Aim//Aim_06.png"))
shoot_anim.append(PhotoImage(file=".//Shoot//Shoot_01.png"))
shoot_anim.append(PhotoImage(file=".//Shoot//Shoot_02.png"))
shoot_anim.append(PhotoImage(file=".//Shoot//Shoot_03.png"))
shoot_anim.append(PhotoImage(file=".//Shoot//Shoot_04.png"))
shoot_anim.append(PhotoImage(file=".//Shoot//Shoot_05.png"))
aim_f.append(PhotoImage(file=".//Aim//Aim_01F.png"))
aim_f.append(PhotoImage(file=".//Aim//Aim_02F.png"))
aim_f.append(PhotoImage(file=".//Aim//Aim_03F.png"))
aim_f.append(PhotoImage(file=".//Aim//Aim_04F.png"))
aim_f.append(PhotoImage(file=".//Aim//Aim_05F.png"))
aim_f.append(PhotoImage(file=".//Aim//Aim_06F.png"))
shoot_anim_f.append(PhotoImage(file=".//Shoot//Shoot_01F.png"))
shoot_anim_f.append(PhotoImage(file=".//Shoot//Shoot_02F.png"))
shoot_anim_f.append(PhotoImage(file=".//Shoot//Shoot_03F.png"))
shoot_anim_f.append(PhotoImage(file=".//Shoot//Shoot_04F.png"))
shoot_anim_f.append(PhotoImage(file=".//Shoot//Shoot_05F.png"))
idle = PhotoImage(file=".//Idle//idle.gif")

play_btn_img = PhotoImage(file="./btns//play_btn.png")
load_btn_img = PhotoImage(file="./btns//load_btn.png")
leaderboard_btn_img = PhotoImage(file="./btns//leaderboard_btn.png")
resolution_btn_img = PhotoImage(file="./btns//resolution_btn.png")
change_keys_btn_img = PhotoImage(file="./btns//change_keys_btn.png")
quit_key_btn_img = PhotoImage(file="./btns//quit_btn.png")
list_of_btns = []
current_player_img = idle
main_menu = Menu(main_window)
main_window.configure(menu = main_menu)
sub_menu = Menu(main_menu)
main_menu.add_command(label = 'pause', command = pause_game)
main_menu.add_command(label = 'restart', command = lambda:restart(0))
main_menu.add_cascade(label = 'settings', menu = sub_menu)
main_menu.add_command(label = 'Quit', command = lambda: exit_game(main_window))
res_sub_menu = Menu(sub_menu)
sub_menu.add_cascade(label = 'resolution', menu = res_sub_menu)
res_sub_menu.add_command(label ="full screen", command = full_res)
res_sub_menu.add_command(label ="1200 x 1000", command = mid_res)
res_sub_menu.add_command(label ="400 x 300", command = small_res)
sub_menu.add_command(label = 'change keys', command = change_binding)
entry_menu()
main_window.mainloop()
