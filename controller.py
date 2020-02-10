

class Controller(object):


    def __init__(self, model, view):
        self.boardModel = model
        self.boardView = view

        ##### init board
        ## Set listeners
        self.boardView.setMovementListener(self.mouseListener)
        self.boardView.setClickListener(self.clickListener)

        self.boardView.initScreen(self.boardModel.initScreen())

        ############################################
        ## Begin
        self.boardView.beginLoop()

    def mouseListener(self, event):
        view = self.boardView
        model = self.boardModel
        view.updateScreen(model.updateCoords(event.x, event.y))

    def clickListener(self, event):
        view = self.boardView
        model = self.boardModel
        view.updateScreen(model.clickEvent(event))

