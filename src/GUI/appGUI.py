import tkinter as tk
from tkinter import ttk

from StartScreen import StartScreen
from TempProfile import TempProfile
from TempGenerate import TempGenerate

class HandwritingApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.grid(column = 0, row = 0, sticky = "nsew")
        container.grid_columnconfigure(0, weight = 1)
        container.grid_rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)

        self.frames = {}
        for F in (StartScreen, TempProfile, TempGenerate):
            screenName = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[screenName] = frame
            frame.grid(column = 0, row = 0, sticky = "nsew")
        self.showFrame("StartScreen")

    def showFrame(self, screenName):
        frame = self.frames[screenName]
        frame.tkraise()


def main():
    root = HandwritingApp()
    root.geometry("1280x720")
    root.mainloop()

if __name__ == '__main__':
    main()