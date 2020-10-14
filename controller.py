

class Controller(object):

    def __init__(self, model, view):
        self.boardModel = model
        self.boardView = view

        # Clunky way to tell main.py to instantiate a new instance of everything
        # so we can play again
        self.reset = False

        ##### init board
        ## Set listeners
        self.boardView.setMovementListener(self.mouseListener)
        self.boardView.setClickListener(self.clickListener)
        self.boardView.setKeyListener(self.keyListener)
        self.boardView.set_endgame_listener(self.endgame_listener)
        self.boardView.set_reset(self.reset_listener)

        self.boardView.initScreen(self.boardModel.initScreen())
        self.boardView.update_turn_indicator(self.boardModel.current_player)

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

        # Updating "current player" indicator, if applicable
        player_before_click = model.current_player
        updated_coordinates = model.clickEvent(event)
        if player_before_click != model.current_player:
            view.update_turn_indicator(model.current_player)

        view.updateScreen(updated_coordinates)

    def keyListener(self, event):
        view = self.boardView
        model = self.boardModel
        view.updateScreen(model.rotationEvent(event))
        print("key listener activated")
        print(event.keysym)

    def endgame_listener(self):
        print('in controller endgame listener')
        return self.boardModel.endgame()

    def reset_listener(self, reset_bool):
        self.reset = reset_bool
        print(self.reset)
        if self.reset:
            print("Resetting")
            self.boardView.root.destroy()
        else:
            print("exiting game")
            exit(0)