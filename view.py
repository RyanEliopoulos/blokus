"""
    Should have 1) initScreen: Method to construct all screen elements not spawned at creation time.
                            So, the grid and the shapes.
                2) updateScreen: Method to update the squares displayed on screen


                So obviously the model knows each squareID. It knows tkinters generation algorithms.
"""
from tkinter import *
from tkinter import ttk


class View(object):

    def __init__(self, height, width):
        ## Build tk components
        self.root       = self._initRoot()
        self.mainframe  = self._initFrame()
        self.canvas     = self._initCanvas(height, width)

    ## Used at creation
    def _initRoot(self):
        new_root = Tk()
        new_root.title("Blockus")
        new_root.columnconfigure(0, weight=1)
        new_root.rowconfigure(0, weight=1)
        return new_root
    ## Used at creation
    def _initFrame(self):
        new_frame = ttk.Frame(self.root)
        new_frame.grid(column=0, row=0, sticky=(N, S, W, E))
        return new_frame
    ## Used at creation
    def _initCanvas(self, height, width):
        new_canvas = Canvas(self.mainframe, height=height, width=width)
        new_canvas.grid(column=0, row=0, sticky=(N, S, E, W))
        return new_canvas

    ## Binding controller method to mouse movement
    def setMovementListener(self, listener):
        self.root.bind('<Motion>', listener)

    ## Controller method to call on click
    def setClickListener(self, listener):
        self.root.bind('<Button-1>', listener)

    ## Initial screen state.
    def initScreen(self, squares):
        """
        :param squares: list of coordinates and options used in canvas.create_rectangle.
                        Perhaps x,y,a,b, (fill string)
        :return: None
        """
        print("heyo we here?")
        for opts in squares:
            self.canvas.create_rectangle(opts[0], opts[1], opts[2], opts[3], fill=opts[4])

    ## Update the square positions on screen
    def updateScreen(self, squares):
        pass

    ## Begin main program loop
    def beginLoop(self):
        self.root.mainloop()
