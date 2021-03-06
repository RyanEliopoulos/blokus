"""
                So obviously the model knows each squareID. It knows tkinters generation algorithms.
"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class View(object):

    def __init__(self, height, width):
        # Build tk components
        self.root           = self._initRoot(height, width)
        self.mainframe      = self._initFrame(height, width)
        self.canvas         = self._initCanvas(height, width)
        self.turn_indicator = None  # Label widget belonging to mainframe

        # callback functions
        self.endgame_listener = None
        self.reset_function = None
        self.skipturn_listener = None

        # Working variables
        self.button_var = IntVar(value=2)  # radio button value for player count

    # Used at creation
    def _initRoot(self, height, width):
        new_root = Tk()
        new_root.title("Blockus")
        new_root.state('zoomed')        # Like pressing the square in the top right of Windows.
        new_root.columnconfigure(0, weight=1)
        new_root.rowconfigure(0, weight=1)
        return new_root
    # Used at creation
    def _initFrame(self, height, width):
        new_frame = ttk.Frame(self.root, height=height, width=width)
        new_frame.grid(column=0, row=0, sticky=(N, S, W, E))
        new_frame.bind('<Configure>', self.resize_adjustment)
        new_frame.grid_propagate(False)  # Prevents widget resizing from affecting widget's children
        return new_frame
    # Used at creation
    def _initCanvas(self, height, width):
        new_canvas = Canvas(self.mainframe, height=height, width=width, scrollregion=(0, 0, 1000, 1200))
        new_canvas.grid(column=0, row=1, sticky=(N, S, E, W))

        # Adding vertical scrollbar
        vbar = Scrollbar(self.root)
        vbar.grid(column=1, row=0, sticky=(N, S, E, W))
        vbar.config(command=new_canvas.yview)
        new_canvas.config(yscrollcommand=vbar.set)

        # Adding horizontal scrollbar
        hbar = Scrollbar(self.root, orient=HORIZONTAL)
        hbar.grid(column=0, row=1, sticky=(N, S, E, W))
        hbar.config(command=new_canvas.xview)
        new_canvas.config(xscrollcommand=hbar.set)
        return new_canvas

    # Binding controller method to mouse movement
    def setMovementListener(self, listener):
        self.root.bind('<Motion>', listener)

    # Controller method to call on click
    def setClickListener(self, listener):
        self.root.bind('<Button-1>', listener)

    # listen for
    def setKeyListener(self, listener):
        self.root.bind('<Right>', listener)
        self.root.bind('<Left>', listener)
        self.root.bind('<Up>', listener)
        self.root.bind('<Down>', listener)

    def set_endgame_listener(self, listener):
        self.endgame_listener = listener

    def set_reset(self, controller_reset_function):
        self.reset_function = controller_reset_function

    def set_skipturn_listener(self, listener):
        print("In set skipturn in view")
        self.skipturn_listener = listener

    def reset(self, reset_bool):
        self.reset_function(reset_bool)

    def endgame(self):
        print("In view endgame")
        end_game_message = self.endgame_listener()
        print(end_game_message)
        #  Need to update the screen now instead of printing to console
        end_game_message += "\n\nWould you like to play again?"

        if messagebox.askyesno("Game Over", end_game_message):
            # reset board somehow here.
            print("got the first string (I guess)")
            self.reset(True)
        else:
            self.reset(False)

    def update_turn_indicator(self, current_player):
        self.turn_indicator.config(text=current_player + ' is the current player', foreground=current_player)

    # Initial screen state.
    def initScreen(self, squares):
        """
        :param squares: list of coordinates and options used in canvas.create_rectangle.
                        Perhaps x,y,a,b, (fill string)
        :return: None
        """
        for opts in squares:
            new_item = self.canvas.create_rectangle(opts[0], opts[1], opts[2], opts[3], fill=opts[4])
            #print(new_item)

        # Constructing game end button
        button = Button(self.mainframe, text="End Game", command=self.endgame)
        button.grid(column=1, row=0, stick=(N, S, E, W))

        # Constructing the skip turn button
        skip_turn_button = Button(self.mainframe, text="Skip Turn", command=self.skipturn_listener)
        skip_turn_button.grid(column=2, row=0, stick=(N, S, E, W))

        # Constructing "current player" indicator
        self.turn_indicator = Label(self.mainframe, text="Stand In")
        self.turn_indicator.grid(column=0, row=0)

        print(f'root height is {self.root.winfo_height()}')
        print(f'root width is {self.root.winfo_width()}')

    # Update the square positions on screen
    def updateScreen(self, squares):
        if squares is None:
            return
        for square in squares:
            # This keeps growing longer...I guess this is why dicts are better??
            x = square[0]
            y = square[1]
            x2 = square[2]
            y2 = square[3]
            fill = square[4]
            item_number = square[5]
            bring_fore = square[6]      # Bool indicating square at top layer.

            #print(f'this is a square {square}')
            self.canvas.itemconfigure(item_number, fill=fill)
            self.canvas.coords(item_number, x, y, x2, y2)
            if bring_fore:
                self.canvas.tag_raise(item_number)

    def build_player_inquiry(self, controller_count_callback):
        """
            Attach 3 radio buttons and a messagebox.askyesno to the canvas.
            Return the results
        :return: integer in range (2, 4) inclusive
        """

        first_button = Radiobutton(master=self.canvas, text="2 Player", variable=self.button_var, value=2)
        first_button.grid(column=0, row=0, sticky=(N, S, E, W))

        second_button = Radiobutton(master=self.canvas, text="3 Player", variable=self.button_var, value=3)
        second_button.grid(column=1, row=0, sticky=(N, S, E, W))

        third_button = Radiobutton(master=self.canvas, text="4 Player", variable=self.button_var, value=4)
        third_button.grid(column=2, row=0, sticky=(N, S, E, W))

        ok_button = Button(master=self.canvas, text='OK', command=controller_count_callback)
        ok_button.grid(column=0, row=1, sticky=(N, S, E, W))

    def get_button_var(self):
        return self.button_var.get()

    def playercount_teardown(self):
        """
            Clears screen to make room for board and pieces.
        """
        executioners_list = self.canvas.winfo_children()
        for item in executioners_list:
            item.destroy()

        # Need to resize these for some reason, otherwise they are tiny.
        # Event generation doesn't work without having manually adjusted these widgets first.
        self.mainframe.configure(height=1000, width=1000)
        self.canvas.configure(height=1000, width=1000)
        # This results in resize_adjustment being called and provides the correct sizing
        self.root.event_generate('<Configure>', when='tail')

    def resize_adjustment(self, event):
        """
            This method is bound to the frame widget. As the root window resizes, so too does the frame.
            This method causes the canvas, held within the frame, to resize accordingly. This is primarily
            to ensure the scroll bars work as expected if the window shrinks.
        """

        # Grabbing widget handles
        frame = event.widget
        frame_height = frame.winfo_height()
        frame_width = frame.winfo_width()
        children = frame.winfo_children()
        canvas = children[0]
        print('frame stats:', frame_height, frame_width)
        # Preparing to adjust canvas size
        canvas_padding_x: float
        canvas_padding_y: float

        if self.turn_indicator is None:   # User has yet to select the # of players.
            ok_button = canvas.winfo_children()[3]
            canvas_padding_x = ok_button.winfo_width() * 2  # Anticipating board layout with 2 buttons
            canvas_padding_y = ok_button.winfo_height()
        else:   # Game board is instantiated. Final buttons have spawned.
            end_game_button = children[1]
            skip_turn_button = children[2]
            canvas_padding_x = end_game_button.winfo_width() + skip_turn_button.winfo_width()
            canvas_padding_y = end_game_button.winfo_height()  # both buttons are the same height and in the same row.

        print('padding:', canvas_padding_x, canvas_padding_y)
        # Calculating padding for the canvas between the frame
        canvas.config(height=frame_height-canvas_padding_y
                      , width=frame_width-canvas_padding_x)
        print('canvas stats:', canvas.winfo_height(), canvas.winfo_width())

    # Begin main program loop
    def beginLoop(self):
        self.root.mainloop()

