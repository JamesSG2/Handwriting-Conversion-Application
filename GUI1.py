#Just a very basic GUI. Still very messy but I figured I would upload
#just in case.


import tkinter as tk
from tkinter import filedialog
#from PIL import ImageTk, Image

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)

root = tk.Tk()
button = tk.Button(root, text='Open', command=UploadAction)
button.pack()

#image1 = Image.open(r"C:\Users\jghau\Downloads/Img.png")
#test = ImageTk.PhotoImage(image1)

#label1 = tkinter.Label(image=test)
#label1.image = test
root.mainloop()
