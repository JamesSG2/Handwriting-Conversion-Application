import tkinter as tk
from tkinter import ttk

class TempGenerate(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        # adding widgets to frame
        self.profileButton = ttk.Button(self, text = "Create and Manage Profiles", width = 30, command = lambda: controller.showFrame("TempProfile"))
        self.generateButton = ttk.Button(self, text = "Back", width = 30, command = lambda: controller.showFrame("StartScreen"))

        # placing frame and widgets on frame
        self.grid(column = 0, row = 0, sticky = "nsew")
        self.profileButton.grid(column = 0, row = 0, rowspan = 2, sticky = "nsew", padx = 10, pady = 20)
        self.generateButton.grid(column = 1, row = 0, rowspan = 2, sticky = "nsew", padx = 10, pady = 20)

        # resize configs
        self.parent.columnconfigure(0, weight = 1)
        self.parent.rowconfigure(0, weight = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)