
"""

    1)x-axis mirror and right rotation now work.  Need to add their counterparts

    2)  Need to handle player count and initial spawn locations.  Then beef up valid move logic to restrict
        moves to spawn corner or those adjacent to pieces already played.

    3)  Need to start implementing the idea of players and turns.

    4) Update view to take a dictionary of square data rather than the list of list.

"""


class Board(object):

    def __init__(self):
        ## Board layout
        self.side_length    = 50
        self.columns        = 10
        self.rows           = 10
        self.padding        = 5         ## space between window edge and grid edge

        ## player-related settings
        self.player_count   = None      ## updated by controller
        self.player_slots   = ['red', 'blue', 'green', 'yellow']

        ## graphics
        self.grid_squares   = []        ## Square objects representing the grid
        self.shapes         = []        ## shape objects
        self.active_shape   = None      ## shape/game piece currently selected and moving

        ## Logic variables
        self.mouse_x        = -1
        self.mouse_y        = -1
        self.square_count   = 0
        self.snap_square    = None      ## grid square occupied by the cursor

    ## Starting pieces
    def initShapes(self):
        """
                Builds out the Shapes (playing pieces) on the board

        :return: None
        """
        new_shape = self.Shape(700, 600, ['X', 'D', 'R'], 'red', self.side_length, self.square_count)
        self.square_count += len(new_shape.squares)
        other_shape = self.Shape(700, 300, ['X', 'U', 'U', 'U'], 'red', self.side_length, self.square_count)
        self.square_count += len(other_shape.squares)

        self.shapes.append(new_shape)
        self.shapes.append(other_shape)

        new_shape = self.Shape(500, 600, ['X', 'D', 'R'], 'blue', self.side_length, self.square_count)
        self.square_count += len(new_shape.squares)
        other_shape = self.Shape(500, 300, ['X', 'U', 'U', 'U'], 'blue', self.side_length, self.square_count)
        self.square_count += len(other_shape.squares)

        self.shapes.append(new_shape)
        self.shapes.append(other_shape)

    ## Build out initial screen state
    def initScreen(self):

        """
            Builds out the squares comprising the screen graphics.  Grid squares are computed,
            then the Shape square coordinate list is appended and returned to the view.

            Square item_numbers are tracked based on the order they are init-ed.  This isn't consumed by the view,
            but we preserve order so it lines up as we expect

        :return: List of lists: x, y, x2, y2, (fill color string). Feeds into the view
        """
        dimensions = []

        ## First take care of grid
        for i in range(self.columns):
            for j in range(self.rows):
                ### Top left corning position (x, y, <>, <>) and bottom right corning (<>, <>, x, y)#
                sl = self.side_length
                padding = self.padding

                x = i * sl + padding
                y = j * sl + padding  ## y
                x2 = (i + 1) * sl + padding  ## x2
                y2 = (j + 1) * sl + padding  ## y2

                new_square = Board.Square(x, y, x2, y2, self.square_count+1, '')
                self.grid_squares.append(new_square)
                self.square_count += 1

                dimensions.append((x, y, x2, y2, ""))

        ## init shapes
        self.initShapes()
        ## then add them to the mix
        for shape in self.shapes:
            dimensions += shape.getCoords()

        ## and send them to the view for drawing
        return dimensions

    ## Processing mouse movement.  Probably the most complex method.
    ## Responsible for snap-to-grid / smooth movement detection
    ## Responsible for 'drawing' the board state
    def updateCoords(self, new_x, new_y):

        ## initial movement on the board.  Prior position is undefined
        if self.mouse_x is None:   ## no previous movement to compare to..undefined delta
            self.mouse_x = new_x
            self.mouse_y = new_y
            return

        ## updating mouse position and GTFOing
        if self.active_shape is None:
            self.mouse_x = new_x
            self.mouse_y = new_y
            return

        ####### There is an active shape. Deterine snap or smooth movement
        on_grid = False
        x_diff  = 0
        y_diff  = 0

        ### checking if on the grid.
        for square in self.grid_squares:
            if new_x < square.x2 and new_x > square.x and new_y < square.y2 and new_y > square.y:
                ## In this square. Let's update coords
                if square is not self.snap_square:
                    self.snap_square = square
                    x_diff = square.x - self.active_shape.active_square.x
                    y_diff = square.y - self.active_shape.active_square.y
                on_grid = True
                break

        ########  Shape is snapped to grid.
        if on_grid:
            self.active_shape.updateCoords(x_diff, y_diff)

            ### evaluate overlapping/off grid squares.

            ## checking if any active_shape square is off the grid
            searchspace = [[sq.x, sq.y] for sq in self.grid_squares]
            for shape_square in self.active_shape.squares:
                coord = [shape_square.x, shape_square.y]

                ## use fill indicator to display error to player
                if coord not in searchspace:

                    ## update with appropriate error colors
                    if shape_square.fill == 'red':
                        shape_square.fill = 'pink'
                    elif shape_square.fill == 'blue':
                        shape_square.fill = 'light blue'
                else:
                    shape_square.fill = self.active_shape.color

            # Checking shape_squares against grid_squares occupied status
            searchspace = [[sq.x, sq.y] for sq in self.grid_squares if sq.occupied]
            for square in self.active_shape.squares:
                coord = [square.x, square.y]

                ## use fill indicator to display error to player
                if coord in searchspace:
                    if self.active_shape.color == 'red':
                        square.fill = 'pink'
                    elif self.active_shape.color == 'blue':
                        square.fill = 'light blue'

        ## Smooth movement - shape is not snapped to grid
        else:
            if self.snap_square:            ## Transitioning from grid to smooth
                self.snap_square = None     ## clearing potential last grid square
                for square in self.active_shape.squares:
                    square.fill = self.active_shape.color       ## update squares in off-grid camo

            x_diff = new_x - self.mouse_x
            y_diff = new_y - self.mouse_y

            print(f"x diff: {x_diff}, y diff: {y_diff}")
            self.active_shape.updateCoords(x_diff, y_diff)

        ## updating game board mouse position
        self.mouse_x = new_x
        self.mouse_y = new_y
        coords = []
        ## building coords
        for shape in self.shapes:
            shape_coords = shape.getCoords()
            ## Need to make sure view draws the active shape above everything else
            for s_coord in shape_coords:
                bring_fore = True if shape is self.active_shape else False
                s_coord.append(bring_fore)
                coords.append(s_coord)

        return coords

    ## Processing mouse click
    def clickEvent(self, event):

        ## Potentially picking a piece
        if self.active_shape is None:
            ## check if click is within a shape.
            for shape in self.shapes:
                if shape.clicked(event.x, event.y) and not shape.placed:
                    #print(f"new active shape: {shape}")
                    self.active_shape = shape
                    return

        ## Or dropping a piece
        else:
            if self.snap_square:  ## indicates we are currently on grid
                ## Checking if move is valid
                if self.moveCheck():    # successful move
                    self.active_shape.placed = True
                    self.active_shape.active_square = None
                    self.active_shape = None
                    ####
                #### CHANGE PLAYER TURN
            else:  # clicked off grid -- respawn or drop piece where it is?
                self.active_shape.active_square = None
                self.active_shape               = None


    ### Called when a click event happens with an active shape
    ### Checks if the click is placing a valid move
    def moveCheck(self):
        """

        :return: True if valid move is made, otherwise False
        """

        ## First check if anything is off grid
        for shape_square in self.active_shape.squares:
            coord = [shape_square.x, shape_square.y]
            searchspace = [[sq.x, sq.y] for sq in self.grid_squares]
            if coord not in searchspace:
                print("invalid move - there are pieces hanging off the grid`")
                return False

        ## Now check for obstructions on the game board. (in the ugliest way possible)
        considered_squares = []             ## grid_squares that might be occupied by this move
        for square in self.grid_squares:
            for shape_square in self.active_shape.squares:
                if shape_square.x == square.x and shape_square.y == square.y:
                    if square.occupied:
                        print("invalid move - There are pieces in the way.")
                        return False
                    considered_squares.append(square)


        """
        
            ######
            ######  Need to ensure piece is corner-to-corner with another piece of the same color
            ######  AND no surface-to-surface contact is occuring between same-colored pieces. 
            ###### 
        
        """



        print("valid move.")
        ## Updated grid_squares
        for square in considered_squares:
            square.occupied = True

        return True

    ## rotation or mirroring of the active shape
    def rotationEvent(self, event):
        if not self.active_shape:
            return

        print("about to event active shape rotate method")
        self.active_shape.rotate(event.keysym)
        print("exited active shape rotate method")
        ## requres coordinates, but is only being used to redraw
        return self.updateCoords(self.mouse_x, self.mouse_y)




    class Square(object):

        def __init__(self, x, y, x2, y2, item_number, fill=''):
            self.x              = x
            self.y              = y
            self.x2             = x2
            self.y2             = y2
            self.item_number    = item_number   ## len(Board.grid_squares) + 1
            self.fill           = fill          ## create_rectangle(fill=)
            self.occupied       = False         ## used only by the grid squares
            self.off_grid       = False         ## used only by the pieces
            self.to_fore        = False         ## flag for view to raise to uppermost position


    class Shape(object):

        def __init__(self, anchor_x, anchor_y, build_order, shape_color, side_length, square_count):
            """

            :param anchor_x: x origin of initial square
            :param anchor_y: y origin of the initial square
            :param build_order: list of letters indicating direction to move
            :param side_length: square side length
            """
            self.anchor_x       = anchor_x
            self.anchor_y       = anchor_y
            self.build_order    = build_order   ## for respawning at default loc
            self.color          = shape_color
            self.side_length    = side_length
            self.active_square  = None          ## clicked by cursor
            self.squares        = []            ## coordinates of the current positions
            self.placed         = False         ## Has this piece been placed on the board yet?

            ##### init squares
            self.spawn(anchor_x, anchor_y, build_order, side_length, square_count, shape_color)

        ## puts shape at initial position. Can be used for respawns
        def spawn(self, anchor_x, anchor_y, build_order, side_length, square_count, color):

            for direction in build_order:
                if direction == 'U':
                    anchor_y = anchor_y - side_length
                elif direction == 'D':
                    anchor_y = anchor_y + side_length
                elif direction == 'L':
                    anchor_x = anchor_x - side_length
                elif direction == 'R':
                    anchor_x = anchor_x + side_length

                new_square = Board.Square(anchor_x,
                                    anchor_y,
                                    anchor_x + side_length,
                                    anchor_y + side_length,
                                    square_count + 1,
                                    color)
                print(f"new square..square count is: {square_count}")
                self.squares.append(new_square)
                square_count += 1

        ## Passes fields to create/modify canvas.rectangle stuff
        def getCoords(self):
            coords = []
            for square in self.squares:
                coords.append([square.x, square.y, square.x2, square.y2, square.fill, square.item_number])
            return coords

        ## checks if current shape has just been selected
        ## aka did the click just land inside here?
        def clicked(self, click_x, click_y):

            for square in self.squares:
                ## Check x axis
                if click_x > square.x and click_x < square.x2:
                    if click_y > square.y and click_y < square.y2:
                        self.active_square = square
                        return True
            return False

        ## Reponse to mouse movemtn. Update position data if currently selected
        ## only passed the difference between the previous and current mouse position
        def updateCoords(self, x_diff, y_diff):
            for square in self.squares:
                square.x += x_diff
                square.x2 += x_diff
                square.y += y_diff
                square.y2 += y_diff

        ## Rotates shape 90* in the specified direction
        ## rotation is about the active_square
        def rotate(self, direction):
            """

            :param direction:  String - 'left' or 'right' 90 degrees
            :return:
            """

            """
            1) make the active square the point of rotation.  
            2) Calculate the vertical and horizontal square distance from each square to the point of rotation. 
            3) translate 'right': down = right, right = up, up = left, left = down
                          'left': down = left, right = down, up = right, left = up
            
            """

            print("shape is rotating...")
            if direction == 'Up':
                ## mirror x axis

                for square in self.squares:
                    if square.x < self.active_square.x:
                        square.x = self.active_square.x + (self.active_square.x - square.x)
                        square.x2 = square.x + self.side_length
                    else:
                        square.x = self.active_square.x - (square.x - self.active_square.x)
                        square.x2 = square.x + self.side_length

            ### Right 90* about the active_square
            elif direction == 'Right':
                for square in self.squares:

                    ## translate vertical differences to horizontal differences
                    horizontal_moves = abs((self.active_square.y - square.y) / self.side_length)
                    if square.y > self.active_square.y:
                        new_x = self.active_square.x - (horizontal_moves * self.side_length)
                    else:
                        new_x = self.active_square.x + (horizontal_moves * self.side_length)

                    ## translate horizontal differences to vertical differences
                    vertical_moves = abs((self.active_square.x - square.x) / self.side_length)
                    if square.x > self.active_square.x:
                        new_y = self.active_square.y + (vertical_moves * self.side_length)
                    else:
                        new_y = self.active_square.y - (vertical_moves * self.side_length)

                    ## updating square to new reality
                    square.x = new_x
                    square.x2 = new_x + self.side_length

                    square.y = new_y
                    square.y2 = new_y + self.side_length
