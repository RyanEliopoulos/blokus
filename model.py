
"""


"""

class Board(object):

    def __init__(self):
        ## Board layout
        self.side_length    = 50
        self.columns        = 10
        self.rows           = 10
        self.padding        = 5         ## space between window edge and grid edge

        ## graphics
        self.grid_squares   = []        ## Square objects representing the grid
        self.shapes         = []        ## shape objects
        self.active_shape   = None      ## shape/game piece currently selected and moving

        ## Logic variables
        self.mouse_x        = -1
        self.mouse_y        = -1
        self.square_count   = 0

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
        for i in range(self.columns):  #
            for j in range(self.rows):  #
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
        print("dimensions")
        print(dimensions)
        return dimensions

    ## Processing mouse movement
    def updateCoords(self, new_x, new_y):

        ## initial movement on the board.  Prior position is undefined
        if self.mouse_x is None:   ## no previous movement to compare to..undefined delta
            self.mouse_x = new_x
            self.mouse_y = new_y
            return

        ## needs to provide [Int, {update_rectangle: options,}]
        ## to the canvas.itemconfigure()

        if self.active_shape is None:
            self.mouse_x = new_x
            self.mouse_y = new_y
            return                          ## nothing to really consider, then.

        ######
        #####
        ##### NEED TO CHECK IF SNAP TO GRID OR SMOOTH MOVEMENT!!



        ## Assuming smooth movement...

        x_diff = new_x - self.mouse_x
        y_diff = new_y - self.mouse_y

        print(f"x diff: {x_diff}, y diff: {y_diff}")
        self.active_shape.updateCoords(x_diff, y_diff)


        self.mouse_x = new_x
        self.mouse_y = new_y
        coords = []

        ### This should be calling a Board method that does all the validity checking and intejecting
        ### the occupoied space/out of bounds color
        for shape in self.shapes:
            shape_coords = shape.getCoords()
            for s_coord in shape_coords:
                coords.append(s_coord)

        print("coords")
        print(coords)
        return coords
        ##### If we have an active shape, the shape needs to update it's position - so
        ##### either smooth movement or check grid placement.

        ### We have an active shape. So, we have to determine how it moves/updates
        """
            Have to update all grid_squares and Shapes.
            Then pass new dimension list
        """



        ## return dimensions

    ## Processing mouse click
    def clickEvent(self, event):
        print(f"in click event with coords: {event.x}, {event.y}")
        ## evaluate implications of a mouse click here
        ## don't need to update view when this happens, right?

        if self.active_shape is None:
            ## check if click is within a shape.
            for shape in self.shapes:
                if shape.clicked(event.x, event.y) and not shape.placed:
                    print(f"new active shape: {shape}")
                    self.active_shape = shape
                    return

        else:
            self.active_shape = None
        ## Clicked while a shape was active

        # 1) Check if click in grid.  Snap

    class Square(object):

        def __init__(self, x, y, x2, y2, item_number, fill=''):
            self.x              = x
            self.y              = y
            self.x2             = x2
            self.y2             = y2
            self.item_number    = item_number  ## len(Board.grid_squares) + 1
            self.fill           = fill         ## create_rectangle(fill=)
            self.occupied       = False

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
            print("yaba daba doo")
            print(coords)
            return coords

        ## checks if current shape has just been selected
        def clicked(self, click_x, click_y):

            for square in self.squares:
                ## Check x axis
                if click_x > square.x and click_x < square.x2:
                    if click_y > square.y and click_y < square.y2:
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





