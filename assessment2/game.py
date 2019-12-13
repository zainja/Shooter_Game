import math
import random
import re
import time
from tkinter import Tk, Canvas, messagebox, PhotoImage, Button, Label, Entry


# Created by Zain Alden Jaffal uni id 10344889
# Shooting is a shooter game were you have to hit the target in a randomly
#  generated map
# the game starts with a 2x2 grid with two obstacles then the game increases
# in complexity as the user progresses
# highest complexity is a 5 x 5 grid
# the player can change the shooting key
# cheat codes
# limits for unlimited bullets
# nowall ball doesn't bounce from balls
# ghost to move the character
# p is a pause button
# x exit pause
# b boss mode
# esc fullscreen


# updates data entries
def update_dictionary(mode, var_to_update):
    if mode == 0:
        player_settings['player_name'] = var_to_update
    elif mode == 1:
        player_settings['level'] = var_to_update
    elif mode == 2:
        player_settings['score'] = var_to_update
    elif mode == 3:
        player_settings['lives'] = var_to_update
    elif mode == 4:
        player_settings['shoot_key'] = var_to_update
    elif mode == 5:
        player_settings['screen_height'] = var_to_update
    elif mode == 6:
        player_settings['screen_width'] = var_to_update
    player_settings_file = open('player_settings', 'w')
    player_info = ''
    for x in player_settings.keys():
        player_info += str(player_settings[x]) + '\n'
    player_settings_file.write(player_info)
    player_settings_file.close()


# move between the screens
# destroy the previous screens' items
def btn_switch(mode):
    global main_window, canvas, height, width, list_of_tk_items, canvas, \
        pause, screen_number, default_canvas_color, shoot_key, pause_btn, \
        boss_key, unpause_btn, quitting, list_of_bound_btns
    pause = False
    main_window.unbind(shoot_key)
    main_window.unbind('<Motion>')
    main_window.unbind(pause_btn)
    main_window.unbind(unpause_btn)
    main_window.unbind(boss_key)
    main_window.unbind('nowall')
    main_window.unbind('limits')
    main_window.unbind('<Key>')
    screen_number = mode
    empty_game_lists()
    main_window.configure(background='#d9d9d9')
    canvas.configure(bg='#d9d9d9')
    for items in list_of_tk_items:
        items.destroy()
    if mode == 0:
        game_play()
    if mode == 1:
        load_game()
    if mode == 2:
        canvas.configure(bg='#42db8e')
        main_window.configure(background='#42db8e')
        leaderboard_read()
    if mode == 3:
        resolution_change()
    if mode == 4:
        canvas.configure(bg='#ff8429')
        main_window.configure(background='#ff8429')
        change_binding()
    if mode == 5:
        # pause = True
        quitting = True
        empty_game_lists()
        main_window.destroy()
    if mode == 6:
        entry_menu()
    if mode == 7:
        canvas.configure(bg='#00fefe')
        main_window.configure(bg='#00fefe')
        enter_name()
    if mode == 8:
        canvas.delete('all')
        pause = True
        entry_menu()


def enter_name():
    global main_window, width, list_of_tk_items, halt, enter_name_bg
    main_window.configure(bg='#00fefe')
    label_enter_name = Label(main_window, image=enter_name_bg, relief='flat',
                             highlightcolor='#00fefe')
    label_enter_name.place(relx=0.5, rely=0.5, anchor='center')
    entry_name = Entry(main_window, width=int(width * 0.02),
                       font='Times 30 bold', justify='center')
    entry_name.place(relx=0.5, rely=0.5, anchor='center')
    confirm_btn = Button(image=start_btn_img,
                         command=lambda: update_name(entry_name.get()))
    confirm_btn.place(relx=0.5, rely=0.7, anchor='center')
    back_btn = Button(main_window, image=back_btn_small_img,
                      command=lambda: btn_switch(6))
    back_btn.place(relx=0.5, rely=0.9, anchor='center')
    list_of_tk_items.append(back_btn)
    list_of_tk_items.append(label_enter_name)
    list_of_tk_items.append(entry_name)
    list_of_tk_items.append(confirm_btn)


def update_name(name):
    global list_of_tk_items, level, score, lives
    if name == '':
        messagebox.showerror('Entry Error', 'Enter a name ')
    if not re.search('^[a-zA-Z0-9{1,8}$]', name):
        messagebox.showerror('Entry Error', 'dont enter spaces')
    else:
        empty_game_lists()
        if len(name) > 10:
            name = name[0:9]
        update_dictionary(0, name)
        for items in list_of_tk_items:
            items.destroy()
        empty_game_lists()
        level = 1
        update_dictionary(1, level)
        score = 0
        update_dictionary(2, score)
        lives = 5
        update_dictionary(3, lives)
        main_window.configure(background='#d9d9d9')
        canvas.configure(bg='#d9d9d9')
        game_play()


def res_one():
    global width
    width = 1200
    global height
    height = 900
    main_window.geometry(str(width) + 'x' + str(height))
    canvas.configure(width=width, height=height)
    update_dictionary(5, height)
    update_dictionary(6, width)


def res_two():
    global width
    width = 1000
    global height
    height = 1000
    main_window.geometry(str(width) + 'x' + str(height))
    canvas.configure(width=width, height=height)
    update_dictionary(5, height)
    update_dictionary(6, width)


# handles changing resolution
def resolution_change():
    global width, height, main_window, list_of_tk_items
    btn_width = 720
    btn_height = 90
    mid_res_btn = Button(main_window, width=btn_width, height=btn_height,
                         image=mid_res_btn_img, command=lambda: res_one())
    mid_res_btn.place(relx=0.5, rely=0.25, anchor='center')
    small_res_btn = Button(main_window, width=btn_width, height=btn_height,
                           image=small_res_btn_img,
                           command=lambda: res_two())
    small_res_btn.place(relx=0.5, rely=0.4, anchor='center')
    back_btn = Button(main_window, width=btn_width, height=btn_height,
                      image=back_btn_img,
                      command=lambda: btn_switch(6))
    back_btn.place(relx=0.5, rely=0.55, anchor='center')
    list_of_tk_items.append(mid_res_btn)
    list_of_tk_items.append(small_res_btn)
    list_of_tk_items.append(back_btn)


# change the shooter key
def change_binding():
    global main_window, list_of_tk_items, bindbackground_img
    main_window.configure(background='#ff8429')
    label_info_bind = Label(main_window,
                            image=bindbackground_img)
    label_info_bind.place(relx=0.5, rely=0.5, anchor='center')
    back_btn = Button(main_window, image=back_btn_small_img,
                      command=lambda: btn_switch(6))
    back_btn.place(relx=0.5, rely=0.9, anchor='center')
    list_of_tk_items.append(back_btn)
    list_of_tk_items.append(label_info_bind)
    main_window.bind('<Key>', bind_new_key)


def bind_new_key(event):
    global shoot_key, main_window, list_of_tk_items, list_of_bound_btns
    if event.keysym in list_of_bound_btns:
        messagebox.showerror('Error binding', 'key taken')
        change_binding()
    else:
        shoot_key = '<' + event.keysym + '>'
        update_dictionary(4, shoot_key)
        info_key = 'key chosen was ' + event.keysym
        main_window.unbind('<Key>')
        messagebox.showinfo('Key changes!', info_key)
        btn_switch(6)


def pause_game(event):
    global pause, shoot_key, main_window, boss_key, canvas, \
        height, width, pause_label
    pause = True
    pause_label = canvas.create_text(int(width / 2), int(height / 2),
                                     text='Paused',
                                     font='Times 50 bold')
    # to stop the user from moving stuff while the pause is on
    main_window.unbind('<Motion>')
    main_window.unbind(shoot_key)
    main_window.unbind(pause_btn)
    main_window.bind(unpause_btn, unpause)
    main_window.unbind('nowall')
    main_window.unbind('limits')


# rebind everything and introduce a delay
def unpause(event):
    global pause, shoot_key, main_window, boss_key, pause_btn, \
        width, height, pause_label
    pause = False
    canvas.delete(pause_label)
    main_window.bind('<Motion>', mouse_movement)
    main_window.bind(shoot_key, shoot)
    main_window.bind(boss_key, boss_key_start)
    main_window.bind(pause_btn, pause_game)
    main_window.bind('nowall', no_walls)
    main_window.unbind(unpause_btn)
    main_window.bind('limits', no_limit_bullets)
    wait_label = canvas.create_text(width / 2, height / 2, text='3',
                                    font='fixedsys 30')
    canvas.update()
    time.sleep(1)
    canvas.itemconfig(wait_label, text='2')
    canvas.update()
    time.sleep(1)
    canvas.itemconfig(wait_label, text='1')
    canvas.update()
    time.sleep(1)
    canvas.delete(wait_label)


# loads blackboard image as a boss key image
def boss_key_start(event):
    global height, width, pause, main_window, work_scrn, pause_btn, canvas, \
        fullscreen_btn, list_of_tk_items
    pause = True
    main_window.wm_attributes('-fullscreen', True)
    work_scrn_width = main_window.winfo_screenwidth()
    work_scrn_height = main_window.winfo_screenheight()
    for items in list_of_tk_items:
        items.destroy()
    canvas.configure(width=work_scrn_width,
                     height=work_scrn_height)
    canvas.pack()
    work_scrn = canvas.create_image(0, 0, image=work, anchor='nw')
    canvas.pack()
    main_window.unbind('<Motion>')
    main_window.unbind(shoot_key)
    main_window.unbind(unpause_btn)
    main_window.unbind('nowall')
    main_window.unbind('limits')
    main_window.unbind(pause_btn)
    main_window.unbind(fullscreen_btn)
    main_window.bind('b', boss_key_destroy)


# stops boss key mode and returns back to bind everything
def boss_key_destroy(event):
    global work_scrn, height, width, main_window, canvas, fullscreen_btn, \
        list_of_tk_items
    if not screen_full:
        main_window.wm_attributes('-fullscreen', False)
    restart_btn = Button(canvas, text='restart', width=4, height=2,
                         command=lambda: restart())
    restart_btn.place(relx=0.95, rely=0.05, anchor='center')
    main_btn = Button(canvas, text='main menu', width=6, height=2,
                      command=lambda: btn_switch(6))
    main_btn.place(relx=0.87, rely=0.05, anchor='center')
    list_of_tk_items.append(restart_btn)
    list_of_tk_items.append(main_btn)
    main_window.geometry(str(width) + 'x' + str(height))
    canvas.configure(width=width, height=height)
    canvas.delete(work_scrn)
    main_window.bind('b', boss_key_start)
    main_window.bind(fullscreen_btn, fullscreen_toggle)
    main_window.bind(unpause_btn, unpause)


# game cheats
def cheat_no_walls(event):
    global no_walls
    no_walls = True


def unlimited_bullets(event):
    global no_limit_bullets
    no_limit_bullets = True


def move_up(event):
    global player, aim_line
    canvas.move(player, 0, -5)
    canvas.move(aim_line, 0, -5)


def move_down(event):
    global player, aim_line
    canvas.move(player, 0, 5)
    canvas.move(aim_line, 0, 5)


def move_left(event):
    global player, aim_line
    canvas.move(player, -5, 0)
    canvas.move(aim_line, -5, 0)


def move_right(event):
    global player, aim_line
    canvas.move(player, 5, 0)
    canvas.move(aim_line, 5, 0)


def player_move_cheat(event):
    global main_window, list_of_boxes, no_walls
    no_walls = True
    main_window.bind('<Up>', move_up)
    main_window.bind('<Down>', move_down)
    main_window.bind('<Left>', move_left)
    main_window.bind('<Right>', move_right)


# function triggered from the load button from main screen
def load_start():
    global player_settings
    # suspects that if there is no name that means a new player
    if player_settings['player_name'] == 'stock':
        btn_switch(7)
    else:
        btn_switch(0)


# load contents from a file into a dictionary
def load_game():
    global player_settings, level, canvas
    global score, lives, shoot_key, height, width
    try:
        game_settings_read = open('player_settings')
        game_settings_read_items = game_settings_read.read().split('\n')
        for index in range(len(game_settings_read_items)):
            update_dictionary(index, game_settings_read_items[index])
        game_settings_read.close()
        level = int(player_settings['level'])
        score = int(player_settings['score'])
        lives = int(player_settings['lives'])
        shoot_key = player_settings['shoot_key']
        height = int(player_settings['screen_height'])
        width = int(player_settings['screen_width'])
        if lives == 0:
            level = 1
            score = 0
            lives = 5
            update_dictionary(1, level)
            update_dictionary(2, score)
            update_dictionary(3, lives)
        main_window.geometry(str(width) + 'x' + str(height))
        canvas.configure(width=width, height=height)
    except IOError:
        update_dictionary(0, 'stock')
        level = 1
        update_dictionary(1, level)
        score = 0
        update_dictionary(2, score)
        lives = 5
        update_dictionary(3, lives)
        update_dictionary(4, shoot_key)
        update_dictionary(5, height)
        update_dictionary(6, width)


# read the contents of the leaderboard file
# display a leaderboard in a descending order
def leaderboard_read():
    global canvas, main_window, width, height, list_of_tk_items, game_ended
    main_window.configure(background='#42db8e')
    canvas.configure(bg='#42db8e')
    lead_label = Label(main_window, image=leaderboard_btn_img)
    lead_label.place(relx=0.5, rely=0.05, anchor='center')
    back_btn = Button(main_window, image=back_btn_small_img,
                      command=lambda: btn_switch(6))
    back_btn.place(relx=0.5, rely=0.95, anchor='center')
    list_of_tk_items.append(back_btn)
    list_of_tk_items.append(lead_label)
    canvas.pack()
    # handles any errors
    try:
        y = height * 0.18
        read_leaderboard = open('leaderboard')
        read_leaderboard_list = read_leaderboard.read().split('\n')
        read_list = []
        for i in range(0, len(read_leaderboard_list) - 1):
            x = read_leaderboard_list[i].split()
            name = ''
            for i in range(0, len(x) - 1):
                name += x[i]
            read_list.append([name, int(x[len(x) - 1])])
        read_list = sorted(read_list, key=lambda x: x[1], reverse=True)
        max_board = len(read_list)
        if max_board > 8:
            max_board = 8
        for entries in range(0, max_board):
            place = str(entries + 1) + 'th'
            if entries == 0:
                place = '1st'
            if entries == 1:
                place = '2nd'
            if entries == 2:
                place = '3rd'

            canvas.create_text(width * 0.1, y,
                               text=place + ". " + read_list[entries][
                                   0].upper(),
                               font='Times 20 italic bold', anchor='nw')
            canvas.create_line(width * 0.275, y + 20, width * 0.78,
                               y + 20, dash=(4, 4), width=3)
            canvas.create_text(width * 0.8, y,
                               text=int(read_list[entries][1]),
                               font='Times 20 italic bold', anchor='nw')
            y += height * 0.1
        canvas.pack()
        read_leaderboard.close()
        if game_ended:
            play_again = Button(main_window, image=play_agian_btn,
                                command=lambda: btn_switch(7))
            play_again.place(relx=0.3, rely=0.95, anchor='center')
            list_of_tk_items.append(play_again)
            game_ended = False
    except IOError:
        messagebox.showerror('File not found', 'there is no previous games')
        btn_switch(6)


# after the game finishes write info to the leaderboard file
def leaderboard_write():
    leaderboard = open('leaderboard', 'a')
    string_single_entry = ''
    player_name = player_settings['player_name']
    score = str(player_settings['score'])
    if player_name != 'stock':
        if len(player_name) > 10:
            player_name = player_name[0:10]
        string_single_entry = player_name + ' ' + score + '\n'
        leaderboard.write(string_single_entry)
        leaderboard.close()


# resets everything in the game back to initial state
def empty_game_lists():
    global ball, list_of_boxes, grid, ball_movement, player_box, \
        enemy_box, quitting
    if not quitting:
        ball = []
        list_of_boxes = []
        grid = []
        ball_movement = []
        enemy_box = 0
        player_box = 0
        canvas.delete('all')


# restart button functionality
def restart():
    global main_window, canvas, height, width, lives, \
        level, score
    main_window.unbind(shoot_key)
    main_window.unbind('<Motion>')
    main_window.unbind(pause_btn)
    main_window.unbind(unpause_btn)
    main_window.unbind(boss_key)
    main_window.unbind('nowall')
    main_window.unbind('limits')
    main_window.unbind('<Key>')
    level = 1
    update_dictionary(1, level)
    score = 0
    update_dictionary(2, score)
    lives = 5
    update_dictionary(3, lives)
    empty_game_lists()
    game_play()


# toggle between current resolution and full screen
# calls btn_switch to regenerate the
def fullscreen_toggle(event):
    global screen_full, main_window, canvas, height, width, screen_number, \
        player_settings
    if not screen_full:
        screen_full = True
        main_window.wm_attributes('-fullscreen', True)
        width = main_window.winfo_screenwidth()
        height = main_window.winfo_screenheight()
        canvas.configure(width=width,
                         height=height)
        canvas.pack()
        if screen_number == -1:
            game_intro()
        else:
            btn_switch(screen_number)
    else:
        screen_full = False
        main_window.wm_attributes('-fullscreen', False)
        width = int(player_settings['screen_width'])
        height = int(player_settings['screen_height'])
        canvas.configure(width=width, height=height)
        canvas.pack()
        if screen_number == -1:
            game_intro()
        else:
            btn_switch(screen_number)


def player_won():
    global level, score
    level += 1
    score += 100
    update_dictionary(1, level)
    update_dictionary(2, score)
    messagebox.showinfo('Game WON', 'CONGRATS')


def player_lost():
    global level, score, lives, main_window, shoot_key
    level -= 1
    lives -= 1
    if level < 1:
        level = 1
    update_dictionary(1, level)
    update_dictionary(3, lives)
    messagebox.showinfo('Game Lost', 'Try again')


# mouse movement method
# detects the vector from the pointer to the aim line
# creates a unit vector
# uses that to move the aim line
def mouse_movement(event):
    global aim, player, current_player_img, pause, canvas, shoot_key
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    rec_pos = player_hit_box()
    line_pos = canvas.coords(aim_line)
    # flip the image to the other side
    if x < rec_pos[2]:
        line_pos[0] = rec_pos[0]
        line_pos[2] = rec_pos[0] - 50
        canvas.itemconfig(player, image=aim_f[0])
        current_player_img = aim_f[0]
    if x > rec_pos[2]:
        line_pos[0] = rec_pos[2]
        line_pos[2] = rec_pos[2] + 50
        canvas.itemconfig(player, image=aim[0])
        current_player_img = aim[0]
    i_component = x - line_pos[0]
    j_component = y - line_pos[1]
    vector_length = math.sqrt(i_component ** 2 + j_component ** 2)
    unit_vector_i = i_component / vector_length
    unit_vector_j = j_component / vector_length
    # places correct coords for line
    canvas.coords(aim_line, line_pos[0], line_pos[1],
                  (unit_vector_i * 50) + line_pos[0],
                  (unit_vector_j * 50) + line_pos[1])
    canvas.update()


# initiate ball move numbers depending on the aim line
def shoot(event):
    global ball, aim_line, ball_movement, aim, player, current_player_img, \
        shoot_anim, idle, shoot_key
    pos_of_the_line = canvas.coords(aim_line)
    i_component = pos_of_the_line[2] - pos_of_the_line[0]
    j_component = pos_of_the_line[3] - pos_of_the_line[1]
    vector_length = math.sqrt(i_component ** 2 + j_component ** 2)
    unit_vector_i = i_component / vector_length
    unit_vector_j = j_component / vector_length
    if current_player_img == aim[0]:
        for i in range(1, len(aim) - 1):
            time.sleep(0.1)
            canvas.itemconfig(player, image=aim[i])
            current_player_img = aim[i]
            canvas.update()
        for i in range(0, len(shoot_anim)):
            time.sleep(0.1)
            canvas.itemconfig(player, image=shoot_anim[i])
            current_player_img = shoot_anim[i]
            canvas.update()
    else:
        if not quitting:
            for i in range(1, len(aim_f) - 1):
                time.sleep(0.1)
                canvas.itemconfig(player, image=aim_f[i], anchor='ne')
                current_player_img = aim_f[i]
                canvas.update()
            for i in range(0, len(shoot_anim_f)):
                time.sleep(0.1)
                canvas.itemconfig(player, image=shoot_anim_f[i], anchor='ne')
                current_player_img = shoot_anim_f[i]
                canvas.update()
    if not quitting:
        canvas.itemconfig(player, image=idle, anchor='nw')
        current_player_img = idle
        # add the generated ball to the list of balls
        ball.append(
            canvas.create_oval(pos_of_the_line[2] - 2, pos_of_the_line[3] - 2,
                               pos_of_the_line[2] + 10,
                               pos_of_the_line[3] + 10,
                               fill='black'))
        # add the vectors for ball movement to the list
        ball_movement.append([unit_vector_i * 2, unit_vector_j * 2])
    else:
        ball = []


# move ball and check for collisions with other objects
def ball_move():
    global ball, ball_movement, width, height, player, list_of_boxes, \
        enemy, no_walls, no_limit_bullets
    for i in range(0, len(ball)):
        i_coords = canvas.coords(ball[i])
        if i_coords[2] >= width:
            ball_movement[i][0] = - ball_movement[i][0]
        if i_coords[0] <= 0:
            ball_movement[i][0] = - ball_movement[i][0]
        if i_coords[3] >= height:
            ball_movement[i][1] = - ball_movement[i][1]
        if i_coords[1] <= 0.1 * height:
            ball_movement[i][1] = - ball_movement[i][1]
        if ball_hits_object(ball[i], player):
            return 1
        if ball_hits_object(ball[i], enemy):
            return 2
        # check for the cheat code
        if not no_walls:
            if len(list_of_boxes) != 0:
                # loop through the boxes to check collisions
                for j in range(len(list_of_boxes)):
                    box_coords = canvas.coords(list_of_boxes[j])
                    if (box_coords[0] < i_coords[0] < box_coords[2]) or (
                            box_coords[0] < i_coords[2] < box_coords[2]):
                        # coming from left side
                        if (i_coords[1] <= box_coords[3]) and (
                                i_coords[3] >= box_coords[3]):
                            ball_movement[i][1] = - ball_movement[i][1]
                        elif (i_coords[3] >= box_coords[1]) and (
                                i_coords[1] <= box_coords[1]):
                            ball_movement[i][1] = - ball_movement[i][1]
                    if (box_coords[1] < i_coords[1] < box_coords[3]) or (
                            box_coords[1] < i_coords[3] < box_coords[3]):
                        if (i_coords[0] <= box_coords[2]) and (
                                i_coords[2] >= box_coords[2]):
                            ball_movement[i][0] = - ball_movement[i][0]
                        elif (i_coords[2] >= box_coords[0]) and (
                                i_coords[0] <= box_coords[0]):
                            ball_movement[i][0] = - ball_movement[i][0]
        canvas.move(ball[i], ball_movement[i][0], ball_movement[i][1])


# checking if ball hit the player or the enemy
def ball_hits_object(i, j):
    i_coords = canvas.coords(i)
    box_coords = []
    if i == player:
        i_coords = player_hit_box()
    if j == player:
        box_coords = player_hit_box()
    if j == enemy:
        box_coords = enemy_hit_box()
    if (j != enemy) and (j != player):
        box_coords = canvas.coords(j)
    # check for right and left
    if (box_coords[1] <= i_coords[1] <= box_coords[3]) or (
            box_coords[1] <= i_coords[3] <= box_coords[3]):
        # coming from left side
        if (i_coords[0] <= box_coords[2]) and (i_coords[2] >= box_coords[2]):
            return True
        elif (i_coords[2] >= box_coords[0]) and (i_coords[0] <= box_coords[0]):
            return True
    if (box_coords[0] <= i_coords[0] <= box_coords[2]) or (
            box_coords[0] <= i_coords[2] <= box_coords[2]):
        # coming from left side
        if (i_coords[1] <= box_coords[3]) and (i_coords[3] >= box_coords[3]):
            return True
        elif (i_coords[3] >= box_coords[1]) and (i_coords[1] <= box_coords[1]):
            return True
    return False


# function to generate the grid so no item is placed on top of another item
def create_grid(height, width, total):
    main_height = height * 0.9
    total_grid = []
    one_box = []
    x = 0
    y = height * 0.1
    width_of_box = width / total
    height_of_box = main_height / total
    number_of_boxes = total ** 2
    for box in range(0, number_of_boxes):
        one_box.append(x)
        one_box.append(y)
        x += width_of_box
        one_box.append(x)
        one_box.append(y + height_of_box)
        total_grid.append(one_box)
        one_box = []
        if x == width:
            y += height_of_box
            x = 0
    return total_grid


# player is an image with only one point in the nw corner
# this is generated to check for a correct placement for pllayer and for the
# collisions between ball and player
def player_hit_box():
    global player, current_player_img
    if not pause:
        x2 = canvas.coords(player)[0] + current_player_img.width()
        y2 = canvas.coords(player)[1] + current_player_img.height()
        return [canvas.coords(player)[0], canvas.coords(player)[1], x2, y2]
    else:
        return 0


# enemy is an image with only one point in the nw corner
# this is generated to check for a correct placement for enemy and for the
# collisions between ball and enemy
def enemy_hit_box():
    global enemy, enemy_img
    x2 = canvas.coords(enemy)[0] + enemy_img.width()
    y2 = canvas.coords(enemy)[1] + enemy_img.height()
    return [canvas.coords(enemy)[0], canvas.coords(enemy)[1], x2, y2]


# place the player in the middle of a box in grid
def place_player(grid):
    global player_box, player, aim_line, idle, current_player_img
    player_box = random.randint(0, len(grid) - 1)
    size_x = (grid[player_box][2] - grid[player_box][0]) / 2
    size_y = (grid[player_box][3] - grid[player_box][1]) / 2
    player = canvas.create_image(grid[player_box][0] + size_x,
                                 grid[player_box][1] + size_y,
                                 anchor='nw', image=idle)
    aim_line = canvas.create_line(0, width * 0.1, height * 0.1, 0)
    canvas.move(player, -current_player_img.width() / 2,
                -current_player_img.height() / 2)
    rect_coords = player_hit_box()
    mid_rect = (rect_coords[1] + rect_coords[3]) * 0.5
    canvas.coords(aim_line, rect_coords[2], mid_rect, rect_coords[2] + 50,
                  mid_rect + 50)


# place enemy in a grid
def place_enemy(grid, level):
    global enemy_box, enemy, player_box, enemy_img
    rec_size_x = enemy_img.width()
    rec_size_y = enemy_img.height()
    enemy_box = player_box
    while enemy_box == player_box:
        enemy_box = random.randint(0, len(grid) - 1)
    if level >= 3:
        while check_placement(grid, enemy_box, player_box):
            enemy_box = random.randint(0, len(grid) - 1)
    point_x = random.uniform(grid[enemy_box][0], grid[enemy_box][2])
    point_x2 = point_x + rec_size_x
    while point_x2 >= grid[enemy_box][2]:
        point_x = random.uniform(grid[enemy_box][0], grid[enemy_box][2])
        point_x2 = point_x + rec_size_x
    # generate y coords
    point_y = random.uniform(grid[enemy_box][1], grid[enemy_box][3])
    point_y2 = point_y + rec_size_y
    while point_y2 >= grid[enemy_box][3]:
        point_y = random.uniform(grid[enemy_box][1], grid[enemy_box][3])
        point_y2 = point_y + rec_size_y
    enemy = canvas.create_image(point_x, point_y, anchor='nw', image=enemy_img)


# added complication for higher levels so the player and the enemy are not
# placed in neighboring boxes
def check_placement(grid, enemy_box, player_box):
    if grid[enemy_box][0] == grid[player_box][2] and \
            grid[enemy_box][1] == grid[player_box][3]:
        return True
    if grid[enemy_box][0] == grid[player_box][0] and \
            grid[enemy_box][1] == grid[player_box][3]:
        return True
    if grid[enemy_box][0] == grid[player_box][2] and \
            grid[enemy_box][1] == grid[player_box][1]:
        return True
    # corner 2
    if grid[enemy_box][2] == grid[player_box][0] and \
            grid[enemy_box][1] == grid[player_box][3]:
        return True
    if grid[enemy_box][2] == grid[player_box][2] and \
            grid[enemy_box][1] == grid[player_box][3]:
        return True
    if grid[enemy_box][2] == grid[player_box][0] and \
            grid[enemy_box][1] == grid[player_box][1]:
        return True
    # corner 3
    if grid[enemy_box][0] == grid[player_box][2] and \
            grid[enemy_box][3] == grid[player_box][1]:
        return True
    if grid[enemy_box][0] == grid[player_box][2] and \
            grid[enemy_box][3] == grid[player_box][3]:
        return True
    if grid[enemy_box][0] == grid[player_box][0] and \
            grid[enemy_box][3] == grid[player_box][1]:
        return True
    # corner 4
    if grid[enemy_box][2] == grid[player_box][0] and \
            grid[enemy_box][3] == grid[player_box][1]:
        return True
    if grid[enemy_box][2] == grid[player_box][0] and \
            grid[enemy_box][3] == grid[player_box][3]:
        return True
    if grid[enemy_box][2] == grid[player_box][2] and \
            grid[enemy_box][3] == grid[player_box][1]:
        return True
    # equal
    if enemy_box == player_box:
        return True
    return False


# generate different boxes in all of the remaining grid locations
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
            rand_x = random.uniform(x, x1)
            rand_y = random.uniform(y, y1)
            while size_x < ((x1 - x) * 0.3) or size_y < ((y1 - y) * 0.2):
                rand_x = random.uniform(x, x1)
                rand_y = random.uniform(y, y1)
                size_x = random.uniform(0, x1 - rand_x)
                size_y = random.uniform(0, y1 - rand_y)
            generated_boxes.append(
                canvas.create_rectangle(rand_x, rand_y, rand_x + size_x,
                                        rand_y + size_y, fill='#6cc8d4'))
    return generated_boxes


# generate the grid and the player and enemy placements
# update counters and increase the complexity
def game_set_up():
    global screen_number, canvas, level, score, width, height, list_of_boxes, \
        lives, list_of_tk_items, quitting
    if not quitting:
        total = 0
        level_x_pos = int(width * 0.02)
        labels_y_pos = int((0.1 * height) / 3)
        lives_x_pos = int(width * 0.13)
        score_x_pos = int(width * 0.40)
        level_txt = 'level: ' + str(level)
        lives_text = 'lives: ' + str(lives)
        score_txt = 'score: ' + str(score)
        canvas.create_rectangle(0, 0, width, height * 0.1, fill='red')
        canvas.create_text(level_x_pos, labels_y_pos,
                           font='Times 20',
                           text=level_txt, anchor='nw')
        canvas.create_text(lives_x_pos, labels_y_pos,
                           font='Times 20',
                           text=lives_text, anchor='nw')
        canvas.create_text(score_x_pos, labels_y_pos,
                           font='Times 20',
                           text=score_txt, anchor='nw')
        restart_btn = Button(canvas, text='restart', width=4, height=2,
                             command=lambda: restart())
        restart_btn.place(relx=0.95, rely=0.05, anchor='center')
        main_btn = Button(canvas, text='main menu', width=6, height=2,
                          command=lambda: btn_switch(8))
        main_btn.place(relx=0.87, rely=0.05, anchor='center')
        list_of_tk_items.append(restart_btn)
        list_of_tk_items.append(main_btn)
        if level == 1:
            total = 2
        if level == 2:
            total = 3
        if level == 3:
            total = 4
        if level >= 4:
            total = 5
        grid = create_grid(height, width, total)
        place_player(grid)
        place_enemy(grid, level)
        list_of_boxes = generated_areas(grid)


# moves the objects and binds the keys for menu, pause, boss key and cheats
def game_play():
    global main_window, pause, lives, ball, screen_number, quitting, game_ended
    screen_number = 0
    if not quitting:
        while lives != 0:
            empty_game_lists()
            game_set_up()
            bullet = 3
            if not quitting:
                bullet_label = canvas.create_text(int(width * 0.23),
                                                  int((0.1 * height) / 3),
                                                  font='Times 20',
                                                  anchor='nw')
                wall_cheat = canvas.create_text(int(width * 0.6),
                                                int((0.1 * height) / 3),
                                                font='Times 20',
                                                anchor='nw')
                main_window.bind('ghost', player_move_cheat)
                main_window.bind('<Motion>', mouse_movement)
                main_window.bind(shoot_key, shoot)
                main_window.bind(pause_btn, pause_game)
                main_window.bind(boss_key, boss_key_start)
                main_window.bind('nowall', cheat_no_walls)
                main_window.bind('limits', unlimited_bullets)
                canvas.pack()
            else:
                break
            while True:
                bullet = 3 - len(ball)
                if quitting:
                    break
                if not pause:
                    canvas.itemconfig(bullet_label,
                                      text='bullets: ' + str(bullet))

                if not no_limit_bullets:
                    if len(ball) == 3:
                        main_window.unbind(shoot_key)
                else:
                    canvas.itemconfig(bullet_label, text='bullets: ∞')
                if no_walls:
                    canvas.itemconfig(wall_cheat, text='no wall active')
                if not pause:
                    ball_move()
                    if ball_move() == 1:
                        player_lost()
                        break
                    if ball_move() == 2:
                        player_won()
                        break
                    if lives == 0:
                        break
                    time.sleep(0.006)
                canvas.update()
        if not quitting:
            messagebox.showinfo('Game lost', 'You have no lives left')
            leaderboard_write()
            game_ended = True
            btn_switch(2)
    main_window.mainloop()


# main menu to move between the different items
def entry_menu():
    global main_window, height, width, canvas, height, width, \
        list_of_tk_items, no_limit_bullets, no_walls, screen_number
    no_limit_bullets = False
    no_walls = False
    btn_width = 720
    btn_height = 90
    play_btn = Button(main_window, width=btn_width, height=btn_height,
                      image=play_btn_img, command=lambda: btn_switch(7))
    play_btn.place(relx=0.5, rely=0.1, anchor='center')
    load_game_btn = Button(main_window, width=btn_width, height=btn_height,
                           image=load_btn_img, command=lambda: load_start())
    load_game_btn.place(relx=0.5, rely=0.25, anchor='center')
    leaderboard_btn = Button(main_window, width=btn_width, height=btn_height,
                             image=leaderboard_btn_img,
                             command=lambda: btn_switch(2))
    leaderboard_btn.place(relx=0.5, rely=0.4, anchor='center')
    resoloution_btn = Button(main_window, width=btn_width, height=btn_height,
                             image=resolution_btn_img,
                             command=lambda: btn_switch(3))
    resoloution_btn.place(relx=0.5, rely=0.55, anchor='center')
    change_keys_btn = Button(main_window, width=btn_width, height=btn_height,
                             image=change_keys_btn_img,
                             command=lambda: btn_switch(4))
    change_keys_btn.place(relx=0.5, rely=0.70, anchor='center')
    quit_key_btn = Button(main_window, width=btn_width, height=btn_height,
                          image=quit_key_btn_img,
                          command=lambda: btn_switch(5))
    quit_key_btn.place(relx=0.5, rely=0.85, anchor='center')
    list_of_tk_items.append(play_btn)
    list_of_tk_items.append(load_game_btn)
    list_of_tk_items.append(leaderboard_btn)
    list_of_tk_items.append(resoloution_btn)
    list_of_tk_items.append(change_keys_btn)
    list_of_tk_items.append(quit_key_btn)


# intro screen
def game_intro():
    global main_window, canvas, player_settings, intro_title, player_image, \
        enemy_image, start_btn_img, screen_number
    screen_number = -1
    if player_settings['player_name'] != 'stock':
        welcome_label = Label(main_window, text='Welcome back ' +
                                                player_settings['player_name'],
                              font='Times 20 bold')
        welcome_label.place(relx=0.5, rely=0.05, anchor='center')
        save_txt = 'Your last game was saved score: ' + \
                   str(player_settings['score']) + '  level: ' + \
                   str(player_settings['level']) + '  lives: ' + \
                   str(player_settings['lives'])
        save_label = Label(main_window, text=save_txt, font='Times 20 bold')
        save_label.place(relx=0.5, rely=0.9, anchor='center')
        list_of_tk_items.append(welcome_label)
        list_of_tk_items.append(save_label)
    intro_title_label = Label(main_window, image=intro_title)
    intro_title_label.place(relx=0.5, rely=0.63, anchor='center')
    player_label = Label(main_window, image=player_image)
    player_label.place(relx=0.3, rely=0.3, anchor='center')
    enemy_label = Label(main_window, image=enemy_image)
    enemy_label.place(relx=0.9, rely=0.3, anchor='center')
    start_btn = Button(image=start_btn_img,
                       command=lambda: btn_switch(6))
    start_btn.place(relx=0.5, rely=0.8, anchor='center')
    list_of_tk_items.append(intro_title_label)
    list_of_tk_items.append(player_label)
    list_of_tk_items.append(enemy_label)
    list_of_tk_items.append(start_btn)


# var deceleration
player_settings = {
    'player_name': 'stock',
    'level': 1,
    'score': 0,
    'lives': 5,
    'shoot_key': '<Button-1>',
    'screen_height': 900,
    'screen_width': 1200
}
width = player_settings['screen_width']
height = player_settings['screen_height']

main_window = Tk()
main_window.geometry(str(width) + 'x' + str(height))
screen_full = False
screen_number = 6
main_window.wm_attributes('-fullscreen', False)
shoot_key = player_settings['shoot_key']
list_of_bound_btns = ['<Escape>', 'p', 'x', 'b', 'Up', 'Down',
                      'Left', 'Right']
fullscreen_btn = '<Escape>'
pause_btn = 'p'
unpause_btn = 'x'
boss_key = 'b'
main_window.bind(fullscreen_btn, fullscreen_toggle)
main_window.configure(background='#d9d9d9')
grid = []
ball = []
list_of_boxes = []
ball_movement = []
player = None
aim_line = None
enemy = None
player_box = 0
enemy_box = 0
canvas = Canvas(main_window, width=width, height=height)
level = player_settings['level']
enemy_img = PhotoImage(file='./enemy/enemy.png')
aim = []
aim_f = []
shoot_anim = []
shoot_anim_f = []
work_scrn = None
no_walls = False
no_limit_bullets = False
restart_btn = None
score = player_settings['score']
lives = player_settings['lives']
pause = False
quitting = False
game_ended = False
pause_label = None
work = PhotoImage(file='work.png')
aim.append(PhotoImage(file='./Aim/Aim_01.png'))
aim.append(PhotoImage(file='./Aim/Aim_02.png'))
aim.append(PhotoImage(file='./Aim/Aim_03.png'))
aim.append(PhotoImage(file='./Aim/Aim_04.png'))
aim.append(PhotoImage(file='./Aim/Aim_05.png'))
aim.append(PhotoImage(file='./Aim/Aim_06.png'))
shoot_anim.append(PhotoImage(file='./Shoot/Shoot_01.png'))
shoot_anim.append(PhotoImage(file='./Shoot/Shoot_02.png'))
shoot_anim.append(PhotoImage(file='./Shoot/Shoot_03.png'))
shoot_anim.append(PhotoImage(file='./Shoot/Shoot_04.png'))
shoot_anim.append(PhotoImage(file='./Shoot/Shoot_05.png'))
aim_f.append(PhotoImage(file='./Aim/Aim_01F.png'))
aim_f.append(PhotoImage(file='./Aim/Aim_02F.png'))
aim_f.append(PhotoImage(file='./Aim/Aim_03F.png'))
aim_f.append(PhotoImage(file='./Aim/Aim_04F.png'))
aim_f.append(PhotoImage(file='./Aim/Aim_05F.png'))
aim_f.append(PhotoImage(file='./Aim/Aim_06F.png'))
shoot_anim_f.append(PhotoImage(file='./Shoot/Shoot_01F.png'))
shoot_anim_f.append(PhotoImage(file='./Shoot/Shoot_02F.png'))
shoot_anim_f.append(PhotoImage(file='./Shoot/Shoot_03F.png'))
shoot_anim_f.append(PhotoImage(file='./Shoot/Shoot_04F.png'))
shoot_anim_f.append(PhotoImage(file='./Shoot/Shoot_05F.png'))
idle = PhotoImage(file='./Idle/Idle_01.png')
play_btn_img = PhotoImage(file='./btns/play_btn.png')
load_btn_img = PhotoImage(file='./btns/load_btn.png')
leaderboard_btn_img = PhotoImage(file='./btns/leaderboard_btn.png')
resolution_btn_img = PhotoImage(file='./btns/resolution_btn.png')
change_keys_btn_img = PhotoImage(file='./btns/change_keys_btn.png')
quit_key_btn_img = PhotoImage(file='./btns/quit_btn.png')
mid_res_btn_img = PhotoImage(file='./btns/mid_res_btn.png')
small_res_btn_img = PhotoImage(file='./btns/small_res_btn_img.png')
back_btn_img = PhotoImage(file='./btns/back_btn_img.png')
back_btn_small_img = PhotoImage(file='./btns/back_btn_small_img.png')
play_agian_btn = PhotoImage(file='./btns/playagain_btn_small_img.png')
enter_name_bg = PhotoImage(file='./btns/enter_name.png')
start_btn_img = PhotoImage(file='./btns/start_btn_img.png')
bindbackground_img = PhotoImage(file='./btns/bindbackground.png')
leaderboard_background_img = PhotoImage(file='./btns/leaderboard_back.png')
intro_title = PhotoImage(file='./intro/title_game.png')
enemy_image = PhotoImage(file='./intro/intro_enemy.png')
player_image = PhotoImage(file='./intro/intro_player.png')

list_of_tk_items = []
current_player_img = idle
load_game()
game_intro()
main_window.mainloop()

