from tkinter import *
import time
import os

#setting up window
root = Tk()
root.minsize(1500,900)
root.config(bg='Black')
root.title('Todo List')
root.config(bg = '#0D1117')

font = ('Calibri', 20, 'bold')

#Creating Title Label 
title = Label(text = "To Do List",font=('Calibri',40, 'bold'),height=1,bg = '#0D1117',fg='purple')
title.place(x=645, y=20)

needtocomplete = Label(text= 'Not Completed',font=('Calibri',30, 'bold'),height=1,bg = '#0D1117',fg='purple')
completed = Label(text= 'Completed',font=('Calibri',30, 'bold'),height=1,bg = '#0D1117',fg='purple')
needtocomplete.place(x=1080, y=95)
completed.place(x=170,y=95)
# List Left
l_listbox = Listbox(root)
l_listbox.place(x=115,y=200)
l_listbox.config(width=52, height=32, bg='#0D1117',fg='white')

# List Right
r_listbox = Listbox(root)
r_listbox.place(x=1050,y=200)
r_listbox.config(width=52, height=32, bg='#0D1117',fg='white')

###############################################################
######Inserting Not Completed tasks and Completed task from files
############################################################
with open('todotasks.txt','r') as insert_todo:
    for lines in insert_todo:
        r_listbox.insert(END, lines)

with open('completedtasks.txt','r') as insert_comp:
    for line in insert_comp:
        l_listbox.insert(END, line)




###############################################################################################
#FUNCTIONS
################################################################################################
#Start function 
activity = ''
def start_function():
    global activity
    current_activity.config(text=f"Current Activity: {r_listbox.get(ANCHOR)}" )
    activity = r_listbox.get(ANCHOR)
    

#delete function 
original_file = 'todotasks.txt'
temp_file = 'temp.txt'
def delete():
    r_listbox.delete(ANCHOR)
    with open(original_file, 'r') as input:
        with open(temp_file, 'w')as output:
            for line in input:
                for word in input_entry.get():
                    line = line.replace(word,"")
                output.write(line)
    os.replace('temp.txt', 'todotasks.txt')
#replace file with original name

    
#mark completed function
def mark_completed():
    #removing empty lines from the completedtasks.txt file and the todotasks.txt file
    
    l_listbox.insert(END, activity)
    current_activity.config(text='Current Activity: Choose A Task')

    with open('completedtasks.txt','a') as completed_file:
            completed_file.write(f'\n {activity}')

    # with open(original_file, 'r') as input:
    #     with open(temp_file, 'w')as output:
    #         for line in input:
    #             for word in input_entry.get():
    #                 line = line.replace(word,"")
    #             output.write(line)

    with open(original_file, 'r') as input_file, open(temp_file, 'w') as output_file:
        for line in input_file:
            if activity not in line:
                output_file.write(line)
    os.replace('temp.txt', 'todotasks.txt')
    global paused_time, timer_running
    paused_time = 0
    timer_running = False
    timer_label.config(text="Timer: 00:00:00")
# remove empty lines func
def remove_empty_lines(file_path):
    temp_file = 'tempT.txt'

    with open(file_path, 'r') as inputR, open(temp_file, 'w') as outputW:
        for line in inputR:
            if not line.isspace():
                outputW.write(line)
    os.replace(temp_file, file_path)

# remove empty lines from listbox func
def remove_empty_lines_from_listbox(listbox):
    items = listbox.get(0, END)
    for item in items:
        if not item.strip():
            listbox.delete(listbox.get(0, END).index(item))

#adding items to listbox
def add_items():
    with open('todotasks.txt','a') as todo_file:
        todo_file.write(f'\n{ input_entry.get()}')
    r_listbox.insert(END, input_entry.get())


###########################################################################################################################
#ENTRY to get input to add items to activitys
input_entry = Entry(root,bg='black',fg='white')
input_entry.place(x=1375,y=200)



###############################################################################################
#BUTTONS
################################################################################################
#add items button
add_task = Button(text='Add Item To List',command=add_items,width=12,height=2,bg='red',fg='white',activebackground='darkred',borderwidth=0.5)
add_task.place(x=1400,y=235)


#delete button 
delete_button = Button(root, text="Delete", command=delete,width=10,height=2,bg='red',fg='white',activebackground='darkred',borderwidth=0.5)
delete_button.place(x=1177,y=725)


# Start Button 
start_button = Button(text='Start',command=start_function, width=10,height=2,bg='lightgreen',fg='black',activebackground='green',borderwidth=0.5)
start_button.place(x=1177, y=150)


#mark completed button
mark_completed_button = Button(root, text="Mark as Completed", font=font, command=mark_completed,bg='yellow')
mark_completed_button.place(x=640, y=600)


#current activity label ##########################################################
current_activity = Label(text = "Current Activity: Choose A Task",font=('Calibri',30, 'bold'),height=2,bg = '#0D1117',fg='purple',wraplength=400,)
current_activity.place(x=625, y=425)


#######################################################################################################
# Timer Labe/Variables##########################################################
timer_label = Label(text="Timer: 00:00:00", font=('Calibri', 40), bg='#0D1117', fg='purple')
timer_label.place(x=600, y=250)
timer_running = False
start_time = None
paused_time = 0

# Counting the time
def update_timer():
    global start_time, paused_time, timer_running
    if timer_running:
        current_time = int(time.time())
        elapsed_time = current_time - start_time + paused_time
        hours, remainder = divmod(elapsed_time, 3600)
        mins, secs = divmod(remainder, 60)
        timer_label.config(text=f"Timer: {hours:02d}:{mins:02d}:{secs:02d}")
        timer_label.after(1000, update_timer)

def start_timer():
    global timer_running, start_time
    if not timer_running:
        timer_running = True
        start_time = int(time.time()) - paused_time
        update_timer()

def pause_timer():
    global timer_running, paused_time
    if timer_running:
        timer_running = False
        paused_time = int(time.time()) - start_time

# Timer buttons ##########################################################
start_button = Button(root, text="Start Timer", font=font, command=start_timer,bg='yellow')
start_button.place(x=600, y=310)                        

pause_button = Button(root, text="Pause Timer", font=font, command=pause_timer,bg='yellow')
pause_button.place(x=780, y=310)
#######################################################################################################

remove_empty_lines('todotasks.txt')
remove_empty_lines('completedtasks.txt')
remove_empty_lines_from_listbox(l_listbox)
remove_empty_lines_from_listbox(r_listbox)



root.mainloop()

