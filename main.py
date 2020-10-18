import controller
import model
import view


ourView = view.View(1000, 1000)
ourModel = model.Board()
ourController = controller.Controller(ourModel, ourView)

print("back at main yo")
# No reset mechanism exists to recycle already-existing resources.
while ourController.reset:
    ourView = view.View(1000, 1000)

    ourModel = model.Board()

    ourController = controller.Controller(ourModel, ourView)





