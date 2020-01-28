from tkinter import *
from tkinter import ttk

ACTIVE_SQUARE = -1      ## This tracks the blue fill magic I did
COLUMNS     = 10
BOX_WIDTH   = 50
ROWS        = 10
BOX_HEIGHT  = 50

ACTIVE_SHAPE = None    ## Currently selected shape
ACTIVE_X = -1           ## Calculate relative mouse movement. Then translate that to the squares
ACTIVE_Y = -1




"""
    Called on <M1>.  Pick up shape and glue shape to cursor
    
"""

def clickCheck(event):
    global ACTIVE_SHAPE
    global ACTIVE_X
    global ACTIVE_Y

    """
        On M1 do we drop a currently-selected shape? 
        Certainly if we just clicked on a different chape.
    """

    ACTIVE_X = event.x
    ACTIVE_Y = event.y
    print("checking mouse click")
    for shape in shapes:
        ## Iterate through shapes to detect if they were clicked on
        if shape.selectionCheck(event.x, event.y):
            ##
            ## ACTIVE_SHAP
            ## shape.update()
            ##
            ACTIVE_SHAPE = shape
            print("OMG WE CLICKED ON A SHAPE!!")
            break


def shapeMovement(event):
    global ACTIVE_SHAPE
    global ACTIVE_X
    global ACTIVE_Y
    if ACTIVE_SHAPE != None:
        print("Mouse_X:{}, Mouse_y: {}, ACTIVE_X: {}, ACTIVE_Y: {}".format(event.x, event.y, ACTIVE_X, ACTIVE_Y))
        ACTIVE_SHAPE.update(event.x, event.y)
        ACTIVE_X = event.x
        ACTIVE_Y = event.y



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

    def update(self, mouse_x, mouse_y):

        ## Load location variables
        next_x = next_y = None          ## position to update to
        x_diff = ACTIVE_X - mouse_x                          ## current shape position minus current mouse coords
        y_diff = ACTIVE_Y - mouse_y

        print('x_diff: {}, y_diff: {}'.format(x_diff, y_diff))
        for squares in self.squares:
            current_x, current_y, trash1, trash2 = self.canvas.coords(squares)
            ### Determining direction and updating accordingly
            # x first
            if x_diff > 0:  # mouse is moving left
                next_x = current_x - x_diff
            else:
                next_x = current_x - x_diff
            # y last
            if y_diff > 0:
                next_y = current_y - y_diff
            else:
                next_y = current_y - y_diff
            self.canvas.coords(squares, next_x, next_y, next_x+BOX_WIDTH, next_y+BOX_HEIGHT)






    def selectionCheck(self, clicked_x, clicked_y):
        for square in self.squares:
            x, y, x2, y2 = self.canvas.coords(square)
            if clicked_x >= x and clicked_x <= x2 and clicked_y >= y and clicked_y <= y2:
                return True
            return False



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
    shapeMovement(event)
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

#root.bind('<Motion>', updateSquares)
#root.bind('<Motion>', shapeMovement)

# primary frame
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, S, E, W))

## Canvas
canvas = Canvas(mainframe, height=1000, width=1000)
canvas.grid(column=0, row=0, sticky=(N, S, E, W))

canvas.bind('<Motion>', shapeMovement)

for i in range(COLUMNS):#
    for j in range(ROWS):#
        ### Top left corning position (x, y, <>, <>) and bottom right corning (<>, <>, x, y)#
        value = canvas.create_rectangle(i*BOX_WIDTH+5, j*BOX_HEIGHT+5, (i+1)*BOX_WIDTH+5, (j+1)*BOX_HEIGHT+5) #### X (starting position, Y (starting position of top left corner, Width, height#
        print(f"The value of  'value' is: {value}")#


root.bind('<Button-1>', clickCheck)
#### Testing the Shape object
shapes = []

shape = Shape(700, 600, ['-', 'D', 'R'], canvas)
shapes.append(shape)

#----
root.mainloop()
