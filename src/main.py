"""
    Written in Python 3
"""






import controller
import model
import view


# This sizes don't actually matter because the window will
# full screen itself.
ourView = view.View(1000, 1000)
ourModel = model.Board()
ourController = controller.Controller(ourModel, ourView)

# No reset mechanism exists to recycle already-existing resources.
# So, this loop will re-instantiate the game board until the players decide
# they no longer wish to play a new game.
while ourController.reset:
    ourView = view.View(1000, 1000)
    ourModel = model.Board()
    ourController = controller.Controller(ourModel, ourView)





