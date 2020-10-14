
"""

    1)x-axis mirror and right rotation now work.  Need to add their counterparts

    3) Update view to take a dictionary of square data rather than the list of list.




    @@BUGS:
        Sometimes a piece can be dropped onto the board (but not played) when it is otherwise an invalid move.
        Piece isn't considered played and the player's turn isn't over.  Seems like it might be when the mouse is
        over the exact coordinates of the line separating the grid squares.

"""


class Board(object):

    def __init__(self):
        # Board layout
        self.side_length       = 50
        self.columns           = 10
        self.rows              = 10
        self.padding           = 5         ## space between window edge and grid edge
        self.corner_coordinates = []

        # player-related settings
        self.player_count   = 2      ## updated by controller
        self.player_slots   = ['red', 'blue']
        self.current_player = 'red'

        # graphics
        self.grid_squares   = []        ## Square objects representing the grid
        self.shapes         = []        ## shape objects
        self.active_shape   = None      ## shape/game piece currently selected and moving

        # Logic variables
        self.mouse_x        = -1
        self.mouse_y        = -1
        self.square_count   = 0
        self.snap_square    = None      ## grid square occupied by the cursor


    # Starting pieces
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

    # Build out initial screen state
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

    # Processing mouse click
    def clickEvent(self, event):

        # Potentially picking a piece
        if self.active_shape is None:
            # check if click is within a shape.
            for shape in self.shapes:
                if shape.clicked(event.x, event.y) and not shape.placed:
                    # Checking if the clicked shape matches active player
                    if shape.color == self.current_player:
                        self.active_shape = shape
                        return

        # Or dropping a piece
        else:
            if self.snap_square:  ## indicates we are currently on grid
                ## Checking if move is valid
                if self.moveCheck():    # successful move
                    self.active_shape.placed = True
                    self.active_shape.active_square = None
                    self.active_shape = None
                    self.update_current_player()
            else:  # clicked off grid -- respawn or drop piece where it is?
                self.active_shape.active_square = None
                self.active_shape = None

    def update_current_player(self):
        if self.current_player == 'red':
            self.current_player = 'blue'
        else:
            self.current_player = 'red'


    ### Called when a click event happens with an active shape
    ### Checks if the click is placing a valid move
    def moveCheck(self):
        """

        :return: True if valid move is made, otherwise False
        """

        # First check if anything is off grid
        for shape_square in self.active_shape.squares:
            coord = [shape_square.x, shape_square.y]
            searchspace = [[sq.x, sq.y] for sq in self.grid_squares]
            if coord not in searchspace:
                print("invalid move - there are pieces hanging off the grid`")
                return False

        # Now check for obstructions on the game board. (in the ugliest way possible)
        considered_squares = []             # grid_squares that might be occupied by this move
        for square in self.grid_squares:
            for shape_square in self.active_shape.squares:
                if shape_square.x == square.x and shape_square.y == square.y:
                    if square.occupied:
                        print("invalid move - There are pieces in the way.")
                        return False
                    considered_squares.append(square)

        # Checking for surface contact with friendly shapes
        for shape in self.shapes:                       # Boards list of player shapes
            if shape.placed and shape.color == self.current_player:
                if shape.check_face_contact(self.active_shape):
                    return False

        # Checking for corner contact with friendly shapes
        for shape in self.shapes:
            if shape.placed and shape.color == self.current_player:
                if shape.check_corner_contact(self.active_shape):
                    # Updating the grid squares that are now occupied
                    for square in considered_squares:
                        square.occupied = True
                    print("valid move.")
                    return True

        # Checking for corner contact with the initial spawning positions
        if self.spawn_placement_check():
            return True

        print('Invalid move - No corner contact between friendly shapes')
        return False

    def spawn_placement_check(self):
        """
            Potential shape placement needs to check if the move is in a spawn point.

        :return: True if active_shape is touching one of the outside corners
        """

        # Calculating coordinates if haven't already done so
        if len(self.corner_coordinates) == 0:
            # top-left coordinates
            tl_x = 9999999
            tl_y = 9999999
            # top-right coordinates
            tr_x = -1
            tr_y = 9999999
            # bottom-right coordinates
            br_x = -1
            br_y = -1
            # bottom-left coordinates
            bl_x = 999999
            bl_y = -1

            for square in self.grid_squares:
                # Checking for top left
                if square.x <= tl_x and square.y <= tl_y:
                    tl_x = square.x
                    tl_y = square.y
                # Checking top right
                if square.x >= tr_x and square.y <= tr_y:
                    tr_x = square.x2
                    tr_y = square.y
                # Checking bottom right
                if square.x >= br_x and square.y >= br_y:
                    br_x = square.x2
                    br_y = square.y2
                # Checking bottom left
                if square.x <= bl_x and square.y >= bl_y:
                    bl_x = square.x
                    bl_y = square.y2

            # All board squares evaluated.
            # Updating board with coordinates
            self.corner_coordinates.append((tl_x, tl_y))
            self.corner_coordinates.append((tr_x, tr_y))
            self.corner_coordinates.append((br_x, br_y))
            self.corner_coordinates.append((bl_x, bl_y))

        # Checking corners
        for square in self.active_shape.squares:
            if (square.x, square.y) in self.corner_coordinates:
                return True
            if (square.x, square.y2) in self.corner_coordinates:
                return True
            if (square.x2, square.y) in self.corner_coordinates:
                return True
            if (square.x2, square.y2) in self.corner_coordinates:
                return True

        return False


    # rotation or mirroring of the active shape
    def rotationEvent(self, event):
        if not self.active_shape:
            return

        print("about to event active shape rotate method")
        self.active_shape.rotate(event.keysym)
        print("exited active shape rotate method")
        # requres coordinates, but is only being used to redraw
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

        def check_face_contact(self, active_shape):
            """
            Evaluates each square in active_shape for face-to-face contact with
            the squares within the shaped this method is called from.
            Meant to be called when self or active_shape has already been played.

            :param active_shape: passed from Board
            :return: True in the event of surface contact

            """

            for active_square in active_shape.squares:
                for current_square in self.squares:
                    # shortening variable names for legibility
                    ax = active_square.x
                    ax2 = active_square.x2
                    ay = active_square.y
                    ay2 = active_square.y2

                    cx = current_square.x
                    cx2 = current_square.x2
                    cy = current_square.y
                    cy2 = current_square.y2

                    # Checking for contact on top of active squares
                    if ax == cx and ay == cy2:  # top left to bottom left corner check
                        if ax2 == cx2 and cy2:  # top right to bottom right corner check
                            print("Contact - top")
                            return True

                    # Checking for contact on right side of active squares
                    if ax2 == cx and ay == cy:       # top right to top left corner check
                        if ax2 == cx and ay2 == cy2: # bottom right to bottom left corner check
                            print("Contact - right")
                            return True

                    # Checking for contact on bottom of active squares
                    if ax == cx and ay2 == cy:        # bottom left to top left check
                        if ax2 == cx2 and ay2 == cy:  # bottom right to top right check
                            print('Contact - bottom')
                            return True

                    # Checking for contact on left of active squares
                    if ax == cx2 and ay == cy:          # top left to top right
                        if ax == cx2 and ay2 == cy2:    # bottom left to bottom right
                            print('Contact - left')
                            return True

            # No surface contact
            return False

        def check_corner_contact(self, active_shape):
            """
            Checks the squares in self.squares for corner contact with the squares in active_shape.squares

            Meant to be called when self or active_shape is a square already played.

            :param active_shape:  Square
            :return: True if corner contact is made
            """

            for active_square in active_shape.squares:
                for current_square in self.squares:
                    # shortening variable names for legibility
                    ax = active_square.x
                    ax2 = active_square.x2
                    ay = active_square.y
                    ay2 = active_square.y2

                    cx = current_square.x
                    cx2 = current_square.x2
                    cy = current_square.y
                    cy2 = current_square.y2

                    # Checking top left to bottom right
                    if ax == cx2 and ay == cy2:
                        print('top left ot bottom right contact')
                        return True
                    # Checking top right to bottom right contact
                    if ax2 == cx and ay == cy2:
                        print('top right to bottom left contact')
                        return True
                    # Checking bottom right to top left contact
                    if ax2 == cx and ay2 == cy:
                        print('bottom right to top left contact')
                        return True
                    # Checking bottom left to top right contact
                    if ax == cx2 and ay2 == cy:
                        print("bottom left:top right contact")
                        return True
            return False
