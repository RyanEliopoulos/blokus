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

    ## listen for
    def setKeyListener(self, listener):
        self.root.bind('<Right>', listener)
        self.root.bind('<Up>', listener)

    ## Initial screen state.
    def initScreen(self, squares):
        """
        :param squares: list of coordinates and options used in canvas.create_rectangle.
                        Perhaps x,y,a,b, (fill string)
        :return: None
        """
        print("heyo we here?")
        for opts in squares:
            new_item = self.canvas.create_rectangle(opts[0], opts[1], opts[2], opts[3], fill=opts[4])
            print(new_item)

    ## Update the square positions on screen
    def updateScreen(self, squares):
        if squares is None:
            return
        for square in squares:
            ## This keeps growing longer...I guess this is why dicts are better??
            x = square[0]
            y = square[1]
            x2 = square[2]
            y2 = square[3]
            fill = square[4]
            item_number = square[5]

            print(f'this is a square {square}')
            self.canvas.itemconfigure(item_number, fill=fill)
            self.canvas.coords(item_number, x, y, x2, y2)
            if fill == 'pink':      ## Need obstructed squares to show at the highest level
                self.canvas.tag_raise(item_number)


    ## Begin main program loop
    def beginLoop(self):
        self.root.mainloop()
