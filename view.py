from tkinter import *
from tkinter import ttk

def move(event):
    print("hey yo")



class View(object):

    def __init__(self):
        ## Build tk components
        self.root       = self._initRoot()
        self.mainframe  = self._initFrame()
        self.canvas     = self._initCanvas()


    def _initRoot(self):
        newRoot = Tk()
        newRoot.title("Blockus")
        newRoot.columnconfigure(0, weight=1)
        newRoot.rowconfigure(0, weight=1)
        return newRoot

    def _initFrame(self):
        newFrame = ttk.Frame(self.root)
        newFrame.grid(column=0, row=0, sticky=(N, S, W, E))
        return newFrame

    def _initCanvas(self):
        newCanvas = Canvas(self.mainframe, height=1000, width=1000)
        newCanvas.grid(column=0, row=0, sticky=(N, S, E, W))
        return newCanvas


    ## bind listner to <Motion> of root or canvas
    def setMovementListener(self, listener):
        self.root.bind('<Motion>', listener)


    def beginLoop(self):
        self.root.mainloop()
