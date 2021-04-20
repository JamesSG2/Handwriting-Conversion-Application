

#tkinter is pre-installed with python to make very basic GUI's
from tkinter import *
from tkinter import filedialog
root = Tk()
#Function gets the file path and prints it in the command
#prompt as well as on the screen.
def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    #print('Selected:', filename)
    myLabel1 = Label(root, text=filename)
    myLabel1.grid(row=1,column=1)
    itterate(filename)


#very simple button that calls the upload action Function
button = Button(root, text='Upload a sample', command=UploadAction, width=40)
button.grid(row=0, column=1)
#===================================================================================
#function takes the user back to the create a profile screen
def myClick():
    print("take the user back")
        #Havent yet learned the screen system entirely, this is the back button

#creates button that calls function myClick
BackButton = Button(root, text="back", command = myClick)
BackButton.grid(row=2, column=0)
#====================================================================================

def myClick2():
    print("take the user to the next screen")

ContinueButton = Button(root, text="continue", command = myClick2)
ContinueButton.grid(row=2, column=2)



#===================================================================================
filenameList = []
def itterate(filename):
    filenameList.append(filename)
    for x in filenameList:
        print(x)



root.mainloop()
