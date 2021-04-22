import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import backend

class UploadDataScreen(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        # List of all profiles (folders) in output
        self.profileList = controller.profileList
        self.files = ""
        # makes widgets
        self.createWidgets(controller)
        # place widgets onto frame
        self.placeWidgets()
        # resize rows and columns on grid
        self.configureRowsColumns()

    def createWidgets(self, controller):
        self.backButton = ttk.Button(self, text = "Back", command = lambda: controller.showFrame("ProfileCreateScreen"))
        self.continueButton = ttk.Button(self, text = "Continue", command = self.analyzeData)
        self.selectDataButton = ttk.Button(self, text = "Upload", command = self.selectFiles)
        self.label = ttk.Label(self, background = "gray")

    def selectFiles(self):
        try:
            self.files = filedialog.askopenfilenames(parent = self, title = "Choose Data")
            if len(self.files) > 1:
                self.label.configure(text = (self.files[0][:20]) + "...+ "+ str(len(self.files)-1) + " more" )
                return
            self.label.configure(text = (self.files[0][:20])+"...")
            self.continueButton.grid(column = 3, row = 3, sticky = "nsew", padx = 10, pady = 10)
        except:
            self.label.configure(text = "Could Not Select Files")
            self.continueButton.grid_remove()

    def analyzeData(self):
        print("debug1")
        for x in range(0, len(self.files)):
            print("debug2")
            f_name, f_ext = os.path.splitext(os.path.basename(self.files[x]))
            backend.analyze_sample(self.controller.selectedProfile, f_name)
        self.controller.showFrame("GoHomeScreen")
        self.continueButton.grid_remove()
        self.files = ""

    def configureRowsColumns(self):
        # resize configs
        self.parent.columnconfigure(0, weight = 1)
        self.parent.rowconfigure(0, weight = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 4)
        self.columnconfigure(3, weight = 1)
        self.rowconfigure(0, weight = 10)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 9)
        self.rowconfigure(3, weight = 1)


    def placeWidgets(self):
        self.backButton.grid(column = 0, row = 3, sticky = "nsew", padx = 10, pady = 10)
        self.selectDataButton.grid(column = 1, row = 1, sticky = "nsew", padx = 1, pady = 10)
        self.label.grid(column = 2, row = 1, sticky = "nsew", padx = 1, pady = 10)
