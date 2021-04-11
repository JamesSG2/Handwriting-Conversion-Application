#tkinter is pre-installed with python to make very basic GUI's
from tkinter import *
from tkinter import filedialog
root = Tk()
#Function gets the file path and prints it in the command
#prompt as well as on the screen.
def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    myLabel1 = Label(root, text=filename)
    myLabel1.grid(row=1,column=0)

#function specifies actions that take place on the click of myButton
    def myClick():
        #prints the user input from the entry box.
        mylabel2 = Label(root, text="retrieving data for: " + e.get())
        mylabel2.grid(row=4,column=0)

#creates button that calls function myClick
    myButton = Button(root, text="type your name", command = myClick)
    myButton.grid(row=2, column=0)
#entry box for user's name when adding images to program
    e = Entry(root, width=50)
    e.grid(row=3, column =0)

#very simple button that calls the upload action Function
button = Button(root, text='Upload a sample', command=UploadAction, width=40)
button.grid(row=0, column=0)

#-----------------------------------------------------------------------------------------

#hand used when the user wants to type a sentece and see the ai output
def hand():
    #function prints the string that the user wants converted.
    def sentence():
        mylabel3 = Label(root, text="your sentece is: " + entry2.get())
        mylabel3.grid(row=4,column=1)
    #Button and corrisponding entry box that obtains characters to be converted.
    myButton3 = Button(root, text="now type your desired characters", command=sentence)
    myButton3.grid(row=2, column=1)
    entry2 = Entry(root, width=50)
    entry2.grid(row=3, column=1)

#the name of the person who wants to type and see their generated handwriting
button2 = Button(root, text="recive handwriting, type your name below", command=hand)
button2.grid(row=0, column=1)
entry = Entry(root, width=50)
entry.grid(row=1, column=1)



root.mainloop()
