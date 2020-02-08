


class Board(object):

    def __init__(self):
        self.mouse_x = None
        self.mouse_y = None


    def updateCoords(self, new_x, new_y):
        self.mouse_x = new_x
        self.mouse_y = new_y

        print(f"new coords: {new_x}, {new_y}")
        ## here it would need to evaluate the implications of the new coords
