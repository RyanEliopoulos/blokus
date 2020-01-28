from tkinter import *
from tkinter import ttk

ACTIVE_SQUARE = -1
COLUMNS     = 10
BOX_WIDTH   = 50
ROWS        = 10
BOX_HEIGHT  = 50


class Shape(object):

    """
        build_order: 'up', 'down', 'left', 'right' -> indicating where the next square is relative to the current one.
    """

    def __init__(self, anchor_x, anchor_y, build_order, canvas):
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.squares = []               ##  list of pairs: [item id, [anchor coordinate pair]]?
        self.build_order = build_order  ##  construction blueprints
        self.canvas= canvas
        self._build()

    def _build(self):
        first_square = True
        current_x = self.anchor_x
        current_y = self.anchor_y

        for step in self.build_order:
            if first_square:
                new_square = self.canvas.create_rectangle(current_x, current_y, current_x+BOX_WIDTH, current_y+BOX_HEIGHT)
                canvas.itemconfigure(new_square, fill='blue')
                self.squares.append(new_square)
                first_square = False
            else:
                current_x, current_y = self._next_anchor(step, current_x, current_y)
                new_square = self.canvas.create_rectangle(current_x, current_y, current_x+BOX_WIDTH, current_y+BOX_HEIGHT)
                canvas.itemconfigure(new_square, fill='blue')
                self.squares.append(new_square)





    def _next_anchor(self, next_direction, current_x, current_y):
        if next_direction == 'D':
            return current_x, current_y+BOX_HEIGHT
        if next_direction == 'U':
            return current_x, current_y-BOX_HEIGHT
        if next_direction == 'L':
            return current_x-BOX_WIDTH, current_y
        if next_direction == 'R':
            return current_x+BOX_WIDTH, current_y






"""

    Piece objects: contain list of (x, y) coordinates indicating the top left position of the 
    squares that compries the piece.
    
"""


def updateSquares(event):
    global ACTIVE_SQUARE
    #print("motion of the ocean: %, %" % event.x, event.y)
    print("motion of the ocean: {}, {}".format(event.x, event.y))


    ## Check ifm mouse is in the board
    if event.x < 5 or event.x >= (COLUMNS * BOX_WIDTH):
        print("mouse outside game board")
        if ACTIVE_SQUARE > -1:
            canvas.itemconfigure(ACTIVE_SQUARE, fill='')
            ACTIVE_SQUARE = -1
        return

    if event.y < 5 or event.y >= (ROWS * BOX_HEIGHT):
        print("mouse outside game board")
        if ACTIVE_SQUARE > -1:
            canvas.itemconfigure(ACTIVE_SQUARE, fill='')
            ACTIVE_SQUARE = -1
        return

    ## Determine which square the mosue is occupying
    column = (event.x-5) // BOX_WIDTH
    row = (event.y-5) // BOX_HEIGHT
    print(type(column))
    print(f"We think we have column {column} and row {row}")


    ## item id: column * 10 + row
    squareID = 10 * column + row + 1
    print(f'square id is {squareID}')
    if squareID == ACTIVE_SQUARE:
        return

    canvas.itemconfigure(ACTIVE_SQUARE, fill='')
    canvas.itemconfigure(squareID, fill='blue')
    ACTIVE_SQUARE = squareID

## root
root = Tk()
root.title("BlockOS")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.bind('<Motion>', updateSquares)

# primary frame
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, S, E, W))

## Canvas
canvas = Canvas(mainframe, height=1000, width=1000)
canvas.grid(column=0, row=0, sticky=(N, S, E, W))



for i in range(COLUMNS):#
    for j in range(ROWS):#
        ### Top left corning position (x, y, <>, <>) and bottom right corning (<>, <>, x, y)#
        value = canvas.create_rectangle(i*BOX_WIDTH+5, j*BOX_HEIGHT+5, (i+1)*BOX_WIDTH+5, (j+1)*BOX_HEIGHT+5) #### X (starting position, Y (starting position of top left corner, Width, height#
        print(f"The value of  'value' is: {value}")#



#### Testing the Shape object

shape = Shape(700, 600, ['-', 'D', 'R'], canvas)


#----
root.mainloop()
