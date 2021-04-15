import tkinter as tk
from tkinter import ttk
import os

class ProfileCreateScreen(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        # List of all profiles (folders) in output
        self.profileList = controller.profileList
        # makes widgets
        self.createWidgets(controller)
        # create a button for every profile
        self.drawProfiles()
        # place widgets onto frame
        self.placeWidgets()
        # resize rows and columns on grid
        self.configureRowsColumns()


    def drawProfiles(self):
        # places a button for every profile
        if(len(self.profileList) > 0):
            for index in range(0, len(self.profileList)):
                self.button = ttk.Button(self.frame, text = self.profileList[index], command = lambda x = self.profileList[index]: self.openProfile(x))
                self.button.grid(column = 0, row = index + 1, sticky = "nsew", padx = 100, pady = 2)

    def configCanvas(self, event):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def itemConfigCanvas(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvasFrame, width = canvas_width)

    def createWidgets(self, controller):
        self.backButton = ttk.Button(self, text = "Back", command = lambda: controller.showFrame("StartScreen"))
        self.createCanvasElements()

    def configureRowsColumns(self):
        # resize configs
        self.parent.columnconfigure(0, weight = 1)
        self.parent.rowconfigure(0, weight = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 3)
        self.columnconfigure(2, weight = 3)
        self.columnconfigure(3, weight = 1)
        self.columnconfigure(4, weight = 1)
        self.columnconfigure(5, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 3)
        self.rowconfigure(2, weight = 3)
        self.rowconfigure(3, weight = 1)

        self.frame.columnconfigure(0, weight = 1)

    def createCanvasElements(self):
        self.canvas = tk.Canvas(self)
        # set up frame and widget(s) on frame
        self.frame = tk.Frame(self.canvas)
        self.profileLabel = ttk.Label(self.frame, text = "Select Profile", justify = "center", anchor = "center")
        # make scroll bar for canvas
        self.scrollBar = ttk.Scrollbar(self, orient = "vertical", command = self.canvas.yview)
        # change scroll properties when self.frame changes size
        self.frame.bind("<Configure>", self.configCanvas)
        self.canvas.bind("<Configure>", self.itemConfigCanvas)
        # setting up canvas
        self.canvasFrame = self.canvas.create_window((0, 0), window = self.frame, anchor = "nw")
        self.canvas.configure(yscrollcommand = self.scrollBar.set, highlightthickness = 0)

    def placeWidgets(self):
        self.backButton.grid(column = 0, row = 3, sticky = "nsew", padx = 10, pady = 10)
        self.canvas.grid(column = 1, row = 0, columnspan = 2, rowspan = 4, sticky = "nsew", padx = 10, pady = 10)
        self.profileLabel.grid(column = 0, row = 0, sticky = "nsew", padx = 100, pady = 10)
        self.scrollBar.grid(column = 3, row = 0, rowspan = 4, sticky = "nsew", padx = 5, pady = 5)

    def openProfile(self, profileName):
        print(profileName)

        