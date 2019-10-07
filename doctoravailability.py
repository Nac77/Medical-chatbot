# import modules

from tkinter import *
import sqlite3
import tkinter.messagebox
# connect to the databse.
conn = sqlite3.connect('doctor.db')
# cursor to move around the databse
c = conn.cursor()
class Application:
    def __init__(self, master):
        self.master = master
        
         # creating the frames in the master
        self.left = Frame(master, width=800, height=720, bg='lightgreen')
        self.left.pack(side=LEFT)

        self.right = Frame(master, width=400, height=720, bg='steelblue')
        self.right.pack(side=RIGHT)

        # labels for the window
       
        
        self.name = Label(self.left, text="Enter doctor id: 1. A 2. B 3. C ", font=('arial 18 bold'), fg='black', bg='lightgreen')
        self.name.place(x=0, y=0)
        
        self.name_ent = Entry(self.left, width=30)
        self.name_ent.place(x=250, y=100)
        
        self.submit = Button(self.left, text="Doctor Availability", width=20, height=2, bg='steelblue', command=self.add_appointment)
        self.submit.place(x=300, y=340)
        
    def add_appointment(self):
        # getting the user inputs
        self.val1 = self.name_ent.get()
        	
        if self.val1 == '':
        			
        	tkinter.messagebox.showinfo("Warning", "Please Fill Up")
        else:
        	c.execute("Select time from avail where doctorid=?",(self.val1))
        	conn.commit()
        	rows = c.fetchall()
        	for row in rows:
        		tkinter.messagebox.showinfo(row)	 
        		
		    
        
root = Tk()
b = Application(root)

# resolution of the window
root.geometry("1200x720+0+0")

# preventing the resize feature
root.resizable(False, False)

# end the loop
root.mainloop()        

       
