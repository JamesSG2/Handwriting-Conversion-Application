# Screen with two buttons
# 
# 

from tkinter import *
from tkinter.ttk import *
import numpy

resolutionWidth = 1280
resolutionHeight = 720

# setting up root

root = Tk()
root.title('Handwriting')
root.geometry('{}x{}'.format(resolutionWidth, resolutionHeight))
root.resizable(width = False, height = False)

# setting styles

style = Style()
style.configure('Button.TButton', font = ('Arial', int(numpy.minimum(int(resolutionWidth * 0.4), int(resolutionHeight * 0.8)) * 0.05)))

# adding buttons

toTextButton = Button(root, text = 'Convert Handwriting to Text', style = 'Button.TButton')
toTextButton.place(x = int(resolutionWidth * 0.05), y = int(resolutionHeight * 0.1), width = int(resolutionWidth * 0.4), height = int(resolutionHeight * 0.8))

toWritingButton = Button(root, text = 'Convert Text to Handwriting', style = 'Button.TButton')
toWritingButton.place(x = int(resolutionWidth * 0.55), y = int(resolutionHeight * 0.1), width = int(resolutionWidth * 0.4), height = int(resolutionHeight * 0.8))


root.mainloop()