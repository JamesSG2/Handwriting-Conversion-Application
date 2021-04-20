import tkinter as tk
from tkinter import ttk
import os

class HandwritingGenerateScreen(tk.Frame):
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

    def configTextCanvas(self, event):
        self.textCanvas.configure(scrollregion = self.textCanvas.bbox("all"))

    def configWritingCanvas(self, event):
        self.writingCanvas.configure(scrollregion = self.writingCanvas.bbox("all"))

    def itemConfigTextCanvas(self, event):
        canvas_width = event.width
        self.textCanvas.itemconfig(self.textCanvasFrame, width = canvas_width)

    def itemConfigWritingCanvas(self, event):
        canvas_width = event.width
        self.writingCanvas.itemconfig(self.writingCanvasFrame, width = canvas_width)

    def createWidgets(self, controller):
        self.backButton = ttk.Button(self, text = "Back", command = lambda: controller.showFrame("StartScreen"))
        self.continueButton = ttk.Button(self, text = "Continue", command = lambda: controller.showFrame("UploadDataScreen"))
        self.createCanvasElements()
        self.entry = ttk.Entry(self.textFrame)

    def configureRowsColumns(self):
        # resize configs
        self.parent.columnconfigure(0, weight = 1)
        self.parent.rowconfigure(0, weight = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 6)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.columnconfigure(4, weight = 6)
        self.columnconfigure(5, weight = 1)
        self.columnconfigure(6, weight = 1)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 8)
        self.rowconfigure(2, weight = 1)


    def createCanvasElements(self):
        self.textCanvas = tk.Canvas(self)
        self.writingCanvas = tk.Canvas(self)
        # set up frame and widget(s) on frame
        self.textFrame = tk.Frame(self.textCanvas, background = "gray")
        self.writingFrame = tk.Frame(self.writingCanvas, background = "gray")
        self.textLabel = ttk.Label(self.textFrame, text = "Enter Text", justify = "center", anchor = "center")
        self.writingLabel = ttk.Label(self.writingFrame, text = "Result", justify = "center", anchor = "center")
        # make scroll bar for canvas
        self.textScrollBar = ttk.Scrollbar(self, orient = "vertical", command = self.textCanvas.yview)
        self.writingScrollBar = ttk.Scrollbar(self, orient = "vertical", command = self.writingCanvas.yview)
        # change scroll properties when self.frame changes size
        self.textFrame.bind("<Configure>", self.configTextCanvas)
        self.writingFrame.bind("<Configure>", self.configWritingCanvas)
        self.textCanvas.bind("<Configure>", self.itemConfigTextCanvas)
        self.writingCanvas.bind("<Configure>", self.itemConfigWritingCanvas)
        # setting up canvas
        self.textCanvasFrame = self.textCanvas.create_window((0, 0), window = self.textFrame, anchor = "nw")
        self.writingCanvasFrame = self.writingCanvas.create_window((0, 0), window = self.writingFrame, anchor = "nw")
        self.textCanvas.configure(yscrollcommand = self.textScrollBar.set, highlightthickness = 0)
        self.writingCanvas.configure(yscrollcommand = self.writingScrollBar.set, highlightthickness = 0)

    def placeWidgets(self):
        self.backButton.grid(column = 0, row = 3, sticky = "nsew", padx = 10, pady = 10)
        self.continueButton.grid(column = 6, row = 3, sticky = "nsew", padx = 10, pady = 10)
        self.textCanvas.grid(column = 1, row = 1, sticky = "nsew", padx = 10, pady = 10)
        self.writingCanvas.grid(column = 4, row = 1, sticky = "nsew", padx = 10, pady = 10)
        self.textLabel.grid(column = 0, row = 0, sticky = "nsew", padx = 100, pady = 10)
        self.writingLabel.grid(column = 0, row = 0, sticky = "nsew", padx = 100, pady = 10)
        self.textScrollBar.grid(column = 2, row = 0, rowspan = 4, sticky = "nsew", padx = 5, pady = 5)
        self.writingScrollBar.grid(column = 5, row = 0, rowspan = 4, sticky = "nsew", padx = 5, pady = 5)
        self.entry.grid(column = 0, row = 1, sticky = "nsew", padx = 10, pady = 10)
