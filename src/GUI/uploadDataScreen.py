import tkinter as tk
from tkinter import ttk
import os

class UploadDataScreen(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        # List of all profiles (folders) in output
        self.profileList = controller.profileList
        # makes widgets
        self.createWidgets(controller)
        # place widgets onto frame
        self.placeWidgets()
        # resize rows and columns on grid
        self.configureRowsColumns()

    def createWidgets(self, controller):
        self.backButton = ttk.Button(self, text = "Back", command = lambda: controller.showFrame("ProfileCreateScreen"))

    def configureRowsColumns(self):
        # resize configs
        self.parent.columnconfigure(0, weight = 1)
        self.parent.rowconfigure(0, weight = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 5)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 2)
        self.rowconfigure(3, weight = 1)


    def placeWidgets(self):
        self.backButton.grid(column = 0, row = 3, sticky = "nsew", padx = 10, pady = 10)

    def openProfile(self, profileName):
        print(profileName)

        