# Screen with two buttons
# 
# 

from tkinter import *
from tkinter.ttk import *
import numpy

resolutionWidth = 1280
resolutionHeight = 720

# function that gets called when the toTextButton is clicked
def onToTextButtonClick():
    print('toTextButton Clicked')

# function that getes called when toWritingButton is clicked
def onToWritingButtonClick():
    print('toWritingButton Clicked')    


# setting up root
root = Tk()
root.title('Handwriting')
root.geometry('{}x{}'.format(resolutionWidth, resolutionHeight))
root.minsize(600, 300)

# setting styles
style = Style()
style.configure('Button.TButton', font = ('Calibri', 20))

# adding buttons
toTextButton = Button(root, text = 'Create Profile', style = 'Button.TButton', command = onToTextButtonClick)
toTextButton.place(relx = 0.05, rely = 0.1, relwidth = 0.4, relheight = 0.8)

toWritingButton = Button(root, text = 'Create Handwriting', style = 'Button.TButton', command = onToWritingButtonClick)
toWritingButton.place(relx = 0.55, rely = 0.1, relwidth = 0.4, relheight = 0.8)



root.mainloop()