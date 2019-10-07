# import modules

from tkinter import *
import sqlite3
import tkinter.messagebox
# connect to the databse.
conn = sqlite3.connect('database.db')
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
       
        
        self.name = Label(self.left, text="Enter your id ", font=('arial 18 bold'), fg='black', bg='lightgreen')
        self.name.place(x=0, y=0)
        
        self.name_ent = Entry(self.left, width=30)
        self.name_ent.place(x=250, y=100)
        
        self.submit = Button(self.left, text="Generate fees", width=20, height=2, bg='steelblue', command=self.add_fee)
        self.submit.place(x=300, y=340)
        self.box = Text(self.right, width=50, height=40)
    def add_fee(self):
        # getting the user inputs
        self.val1 = self.name_ent.get()
        str2="Fees are"
        str1="00"	
        if self.val1 == '':
        			
        	tkinter.messagebox.showinfo("Warning", "Please Fill Up")
        else:
        	c.execute("Select location from 'appointments' where ID="+(self.val1))
        	#tkinter.messagebox.showinfo("Fees are Rs.100")
        	conn.commit()
        	rows = c.fetchall()
        	for row in rows:
        		
        		tkinter.messagebox.showinfo((str2,)+row+(str1,))
        		

root = Tk()
b = Application(root)

# resolution of the window
root.geometry("1200x720+0+0")

# preventing the resize feature
root.resizable(False, False)

# end the loop
root.mainloop()        
        
#id1=input("Enter doctor id: 1. A 2. B 3. C" )
#c.execute("Select time from avail where doctorid=?",(id1,))
#rows = c.fetchall()
#for row in rows:
#        print(row)
       
