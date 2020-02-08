

class Controller(object):


    def __init__(self, model, view):
        self.boardModel = model
        self.boardView = view

        ## Establish listener to update controller with mouse movements
        ## init
        self.boardView.setMovementListener(self.mouseListener)
        # Additional things here, like View.initGrid/initScreen?


        ############################################
        ## Begin
        self.boardView.beginLoop()

    def mouseListener(self, event):
        self.boardModel.updateCoords(event.x, event.y)



