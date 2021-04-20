import tkinter as tk
from tkinter import ttk
import os

from startScreen import StartScreen
from profileSelectScreen import ProfileSelectScreen
from profileCreateScreen import ProfileCreateScreen
from uploadDataScreen import UploadDataScreen
from goHomeScreen import GoHomeScreen

class HandwritingApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.grid(column = 0, row = 0, sticky = "nsew")
        container.grid_columnconfigure(0, weight = 1)
        container.grid_rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)

        self.profileList = []
        self.searchProfiles()

        self.frames = {}
        for F in (StartScreen, ProfileSelectScreen, ProfileCreateScreen, UploadDataScreen, GoHomeScreen):
            screenName = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[screenName] = frame
            frame.grid(column = 0, row = 0, sticky = "nsew")
        self.showFrame("StartScreen")

    def showFrame(self, screenName):
        frame = self.frames[screenName]
        frame.tkraise()

    def searchProfiles(self):
        root='output'
        self.profileList = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]
        print (self.profileList)
        #self.after(1000, self.searchProfiles)

def main():
    root = HandwritingApp()
    root.geometry("1280x720")
    root.mainloop()

if __name__ == '__main__':
    main()