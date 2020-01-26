from tkinter import *
from tkinter import ttk

ACTIVE_SQUARE = -1


"""

    For calculating which block the mouse is currently under... Divide width of canvas by number of columns
    and height of canvas by number of rows (take into account padding, if applicable) to get dimensions for a single
    block.

    Column # = mouse.x // (floor division) width of single block
    row # = moouse.y // neight of a single block  
    
    if board.(column, row) = board.active_square:    If already updated
        pass
    else:
        board.active_square.revert_default          ## Return to default visuals
        board.active_square = board.(column, row)
        board.active_square.active_coloring         ## change to 'active' visuals
        
        
    I don't see a way to be updated on mouse movements regularly.  So, each square will need to be a widget..
    How to link them to show shadow movement of tetris pieces?
    
    Root -> Frame -> Many Canvases, where one canvas is one square
    
"""

COLUMNS     = 10
BOX_WIDTH   = 50
ROWS        = 10
BOX_HEIGHT  = 50


def updateSquares(event):
    global ACTIVE_SQUARE
    #print("motion of the ocean: %, %" % event.x, event.y)
    print("motion of the ocean: {}, {}".format(event.x, event.y))

    ## Check ifm mouse is in the board
    if event.x < 5 or event.x >= (COLUMNS * BOX_WIDTH):
        print("mouse outside game board")
        return

    if event.y < 5 or event.y >= (ROWS * BOX_HEIGHT):
        print("mouse outside game board")
        return

    ## Determine which square the mosue is occupying
    column = event.x // BOX_WIDTH
    row = event.y // BOX_HEIGHT
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
#mainframe.bind('<Motion>', updateSquares)

## Canvas
canvas = Canvas(mainframe, height=1000, width=1000)#
canvas.grid(column=0, row=0, sticky=(N, S, E, W))#



for i in range(COLUMNS):#
    for j in range(ROWS):#
        ### Top left corning position (x, y, <>, <>) and bottom right corning (<>, <>, x, y)#
        value = canvas.create_rectangle(i*BOX_WIDTH+5 , j*BOX_HEIGHT+5, (i+1)*BOX_WIDTH+5, (j+1)*BOX_HEIGHT+5) #### X (starting position, Y (starting position of top left corner, Width, height#
        print(f"The value of  'value' is: {value}")#



#


#----
root.mainloop()
