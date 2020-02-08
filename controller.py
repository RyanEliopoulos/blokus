

class Controller(object):


    def __init__(self, model, view):
        self.boardModel = model
        self.boardView = view

        ## Establish listener to update controller with mouse movements
        self.boardView.setMovementListener(self.mouseListener)
        self.boardView.beginLoop()

    def mouseListener(self, event):
        print("do we get here?")
        self.boardModel.updateCoords(event.x, event.y)



