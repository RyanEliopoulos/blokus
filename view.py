"""
    Should have 1) initScreen: Method to construct all screen elements not spawned at creation time.
                            So, the grid and the shapes.
                2) updateScreen: Method to update the squares displayed on screen
"""




from tkinter import *
from tkinter import ttk


class View(object):

    def __init__(self):
        ## Build tk components
        self.root       = self._initRoot()
        self.mainframe  = self._initFrame()
        self.canvas     = self._initCanvas()


    def _initRoot(self):
        new_root = Tk()
        new_root.title("Blockus")
        new_root.columnconfigure(0, weight=1)
        new_root.rowconfigure(0, weight=1)
        return new_root

    def _initFrame(self):
        new_frame = ttk.Frame(self.root)
        new_frame.grid(column=0, row=0, sticky=(N, S, W, E))
        return new_frame

    def _initCanvas(self):
        new_canvas = Canvas(self.mainframe, height=1000, width=1000)
        new_canvas.grid(column=0, row=0, sticky=(N, S, E, W))
        return new_canvas


    ## bind listner to <Motion> of root or canvas
    def setMovementListener(self, listener):
        self.root.bind('<Motion>', listener)


    def beginLoop(self):
        self.root.mainloop()
