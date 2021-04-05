#Just a very basic GUI. Still very messy but I figured I would upload
#just in case.

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
    myLabel1.pack()

#very simple button that calls the upload action Function
button = Button(root, text='Upload an image', command=UploadAction)
button.pack()

root.mainloop()
