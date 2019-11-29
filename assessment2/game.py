from tkinter import Tk, Canvas
import math
import time
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
    ball = canvas.create_oval(0,0,10,10, fill="red")
    canvas.coords(ball,110,230,120,240)
    pos_of_theline = canvas.coords(2)
    i_component = pos_of_theline[2] - pos_of_theline[0]
    j_component = pos_of_theline[3] - pos_of_theline[1]
    vector_length = math.sqrt(i_component**2 + j_component**2)
    unit_vector_i = i_component / vector_length
    unit_vector_j = j_component / vector_length
    canvas.move(3,unit_vector_i*4,unit_vector_j*4)
    print("pew")
    
       
main_window = Tk()
canvas = Canvas(main_window,width=300,height=300)
rectangle = canvas.create_rectangle(0, 0, 50, 70, fill="black")
canvas.move(rectangle,60,230)
aim_line = canvas.create_line(0,50,50,0)
canvas.coords(aim_line,110,230,160,200)
canvas.bind('<Motion>',mouse_movement)
canvas.bind('<Button-1>',shoot)
canvas.pack()
main_window.mainloop()