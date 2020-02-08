
"""

    All decisions are made here. So all screen dimensions/information will originate here.

"""

class Board(object):

    def __init__(self):
        ## Board layout
        self.side_length    = 50
        self.columns        = 10
        self.rows           = 10
        self.padding        = 5

        ## graphics
        self.shapes         = []
        self.active_shape   = None
        self.squares        = []
        self.active_square  = None

        ## In motion variables
        self.mouse_x = None
        self.mouse_y = None

    ##
    def initShapes(self):
        """

            Incomplete. just the one PoC
        :return:
        """
        new_shape = self.Shape(700, 600, ['X', 'D', 'R'], 'red', self.side_length)
        other_shape = self.Shape(700, 300, ['X', 'U', 'U', 'U'], 'red', self.side_length)
        self.shapes.append(new_shape)
        self.shapes.append(other_shape)

    ## Build out initial screen state
    def initScreen(self):

        """
            Builds out the squares comprising the screen graphics.  Grid squares are computed,
            then the Shape square coordinate list is appended and returned to the view.

        :return: List of lists: x, y, x2, y2, (fill color string). Feeds into the view
        """
        dimensions = []

        ## First take care of grid
        for i in range(self.columns):  #
            for j in range(self.rows):  #
                ### Top left corning position (x, y, <>, <>) and bottom right corning (<>, <>, x, y)#
                sl = self.side_length
                padding = self.padding
                dimensions.append((
                                    i * sl + padding,         ## x
                                    j * sl + padding,         ## y
                                    (i+1) * sl + padding,     ## x2
                                    (j + 1) * sl + padding,   ## y2
                                     ""))               ## fill value: empty string = empty square

        ## Now add the shapes squares constructed earlier
        for shape in self.shapes:
            dimensions += shape.squares

        return dimensions

    ## Processing mouse movement
    def updateCoords(self, new_x, new_y):
        self.mouse_x = new_x
        self.mouse_y = new_y

        print(f"new coords: {new_x}, {new_y}")
        ## here it would need to evaluate the implications of the new coords

    ## Processing mouse click
    def clickEvent(self, event):
        print(f"in click event with coords: {event.x}, {event.y}")
        ## evaluate implications of a mouse click here

    class Shape(object):

        def __init__(self, anchor_x, anchor_y, build_order, shape_color, side_length):
            """

            :param anchor_x: x origin of initial square
            :param anchor_y: y origin of the initial square
            :param build_order: list of letters indicating direction to move
            :param side_length: square side length
            """
            self.squares = []

            for direction in build_order:
                if direction == 'U':
                    anchor_y = anchor_y - side_length
                elif direction == 'D':
                    anchor_y = anchor_y + side_length
                elif direction == 'L':
                    anchor_x = anchor_x - side_length
                elif direction == 'R':
                    anchor_x = anchor_x + side_length

                self.squares.append([anchor_x,
                                    anchor_y,
                                    anchor_x + side_length,
                                    anchor_y + side_length,
                                    shape_color])


