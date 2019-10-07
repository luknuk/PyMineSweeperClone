#!/usr/bin/env python

# FBS Compiling
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys, os

# Import concurrency
from worker import Worker, WorkerSignals

# Import game controllers
from board import Board
from field import Field

# Import view libraries
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
from score import Scores

# Import buttons
from views.squarebutton import SquareGuiField
from views.hexbutton import HexGuiField
from views.smiley import SmileyButton

# Import load/save functionality
import save_state as save

# Web browser for showing Wikipedia
import webbrowser


class MainApplication(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainApplication, self).__init__(*args, **kwargs)
        # Tell the application that we don't have a menu
        self.restart = False
        self.from_save = False
        self.first_move = True

        # Default start mode
        self.difficulty = "beginner"
        self.mode = "classic"
        self.start()


    def start(self):
        '''
        Starts the game.
        :param mode: (mode, difficulty)
        :return:
        '''

        # If only the difficulty is supplied, use previous game mode.
        self.counter = 0
        # Set number of flags to 0
        self.flags = 0

        if self.restart:
            # Clean up memory
            for b in self.buttons:
                b.deleteLater()

            # Initialise a brand new Board
            self.board = Board(self.difficulty, self.mode)
        else:
            # If fresh start; try and load a serialised board object.
            save_obj = self.load()
            if save_obj:
                try:
                    # Use the existing one
                    self.board = save_obj["board"]
                    self.difficulty = self.board.difficulty
                    self.mode = self.board.mode
                    self.from_save = True
                except AttributeError:
                    print("The savefile is not compatible")
                    raise
                try:
                    self.counter = save_obj["counter"]
                    self.flags = save_obj["flags"]
                except KeyError:
                    # The savefile is incompatible with this version of the game, so remove it.
                    save.destroy()
                    self.close()
            else:
                # Create a new one
                self.board = Board(self.difficulty, self.mode)

        self.total_mines = self.board.get_total_number_of_mines()

        self.close()

        # Create new Thread pool
        self.threadpool = QThreadPool()

        self.buttons = []


        # If loss is true, the GUIFields are not clickable
        self.loss = False

        # Start the timer
        self.start_timer()

        # Initialise the UI
        self.initUI()

    def change_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.start()

    def change_mode(self, mode):
        self.mode = mode
        self.start()



    def initUI(self):
        '''
        Paints the UI
        :return:
        '''

        # Minesweeper window
        self.title = f"Minesweeper ({self.difficulty.capitalize()})"
        self.setWindowTitle(self.title)

        sizes = {
            # mode_difficulty: (x, y, centre)
            # Classic mode
            ("classic", "beginner"): (252, 249),
            ("classic", "intermediate"): (396, 369),
            ("classic", "expert"): (732, 440),
            # Hexagon mode
            ("hexagon", "beginner"): (316, 260),
            ("hexagon", "intermediate"): (488, 386),
            ("hexagon", "expert"): (896, 460)
        }
        size = sizes[(self.mode, self.difficulty)]

        # Set the size
        self.width = size[0]
        self.height = size[1]
        self.center = size[0]/2
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)




        if not self.restart:
            self.restart = True

            def add_action(text, parent, func, arg=False):
                '''
                Private method to create a new toolbar action.
                :param text: Text to display.
                :param parent: Pass MainApplication object
                :param func: lambda to execute upon click
                :param arg: One single argument to pass
                :return: The new action object
                '''
                _action = QAction(text.capitalize(), parent)
                if not arg:
                    _action.triggered.connect(lambda: func())
                else:
                    _action.triggered.connect(lambda *arg, v=arg: func(v))
                return _action

            def web(url):
                # Opens webpage
                return webbrowser.open(url)

            # Top-level toolbar
            menubar = self.menuBar()

            # Add the action to the relevant menus, by surrounding them in menu.addAction()
            menubar.addAction(add_action("new game", self, self.start))

            menu_mode = menubar.addMenu("Gamemode")
            menu_mode.addAction(add_action("play classic mode", self, self.change_mode, "classic"))
            menu_mode.addAction(add_action("play hexagon mode", self, self.change_mode, "hexagon"))

            menu_difficulty = menubar.addMenu("Difficulty")
            menu_difficulty.addAction(add_action("beginner", self, self.change_difficulty, "beginner"))
            menu_difficulty.addAction(add_action("intermediate", self, self.change_difficulty, "intermediate"))
            menu_difficulty.addAction(add_action("expert", self, self.change_difficulty, "expert"))

            menu_scores = menubar.addMenu("Highscores")
            menu_scores.addAction(add_action("beginner", self, self.view_highscores, "beginner"))
            menu_scores.addAction(add_action("intermediate", self, self.view_highscores, "intermediate"))
            menu_scores.addAction(add_action("expert", self, self.view_highscores, "expert"))

            menu_help = menubar.addMenu('Help')
            menu_help.addAction(add_action("Tutorial", self, web, "https://en.wikipedia.org/wiki/Minesweeper_(video_game)"))
            menu_help.addAction(add_action("Developer", self, web, "https://ldmartin.com"))

            # Display unflagged mines
            self.unflagged_mines = display(self)
            self.unflagged_mines.make()

            # Display timer
            self.time_display = display(self)
            self.time_display.make()

            self.create_smiley_button()

        # Resize the two displays.
        self.unflagged_mines.move(6, 6)
        self.time_display.move(int(self.width - 66), 6)

        self.time_display.setText("000")

        self.unflagged_mines.setText(f"{(self.total_mines - self.flags):0>3}")

        self.smiley.move(self.center-24, 6)

        positions = []
        for row in range(self.board.r):
            for col in range(self.board.c):
                positions.append((row, col))

        if self.mode == "classic":
            gui_field = SquareGuiField
        elif self.mode == "hexagon":
            gui_field = HexGuiField

        self.buttons = []
        for position in positions:
            self.buttons.append(gui_field(position, self))
            self.buttons[-1].left_click(self.click_field)
            self.buttons[-1].right_click(self.flag_field)

        if self.from_save:
            self.update_fields(self.board.get_board())

        # Set it to a class variable
        self.show()


    def start_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def create_smiley_button(self):
        """
        Handles the smiley button
        :return:
        """
        self.smiley = SmileyButton(self)
        self.smiley.state = 0
        self.smiley.left_click(self.start)

    def update_fields(self, board):
        """
        Updates all the fields on the board
        :param board:
        :return:
        """

        if not board:
            print("Error: Board.update_fields() could not access Board")
            return
        # Need to count flags
        self.flags = 0
        # Before we count, there are no blank squares
        blanks = False
        # By default, we haven't lost yet
        loss = False

        for f, b in zip(board, self.buttons):
            if f is False:
                b.text = ""
                # There are still blanks, so player can't win.
                blanks = True
            elif f is "f":
                b.text = "f"
                self.flags += 1
            elif f is "*":
                b.text = "*"
                b.flatten()
                # We've lost
                loss = True
            elif f is 0:
                b.text = ""
                b.flatten()
            else:
                # Number
                b.flatten(int(f))
                b.text = str(f)

        # Check for win condition (player must flag all mines and clear all tiles)
        if self.total_mines - self.flags == 0 and blanks is False:
            # Destroy the save
            save.destroy()
            self.show_win()
        elif loss:
            # Destroy the save
            save.destroy()
            self.show_loss()
        else:
            # If this isn't the winning move, we can save the game.
            self.save_state()

    def view_highscores(self, difficulty):
        '''
        View a list of high scores, given the difficulty
        :param difficulty:
        :return:
        '''

        w = QMessageBox(self)

        sc = Scores()
        # name, points, difficulty
        raw_data = sc.get_highscores(self.mode, difficulty)

        if not raw_data:
            w.setText(f"There are no high scores for {self.mode.capitalize()} Minesweeper on {difficulty.capitalize()} difficulty.")
        else:
            # Show score list
            scores = ""
            for row in raw_data:
                if scores == "":
                    w.setText(f"Top score for {self.mode.capitalize()} Minesweeper on {difficulty.capitalize()} difficulty is {row[1]} by {row[0].capitalize()}.")
                scores += f"{row[0].capitalize()}\t\t{row[1]}\n"

            if scores == "":
                w.setText(f"There are no high scores in this difficulty level.")
            w.setDetailedText(scores)
        w.exec_()


    def show_loss(self):
        '''
        Show message upon loss, and restart the game
        :return:
        '''
        self.loss = True

        # Make the smiley show the lose state.
        self.smiley.state = 2

    def show_win(self):
        '''
        Show message upon victory, and ask if user wants to be put in high scores list.
        :return:
        '''
        # Make the smiley show the win state.
        self.smiley.state = 3
        result = QMessageBox.question(self, "You won!",
                                      f"Thank you for playing Minesweeper.\nYour score is: {self.counter}\nWould you like to record it in the high scores?")
        if result == 16384:
            # yes
            self.record_score()
        elif result == 65536:
            #no
            pass

        # Restart game
        self.start()

    def record_score(self):
        '''
        Record the high score in list of high scores
        :return:
        '''
        text, okPressed = QInputDialog.getText(self, "Record your score", "Your name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            # Record the score
            sc = Scores()
            # name, points, difficulty
            sc.write_highscore(text, self.counter, self.mode, self.difficulty)
            sc.save()
            print("Score recorded")
        return


    def refreshUI(self):
        '''
        Refreshes the other parts of the UI
        :return:
        '''
        mines_left = int(self.total_mines - self.flags)
        self.unflagged_mines.setText(f"{mines_left:0>3}")

    def click_field(self, loc):
        '''
        Registers a click, passes location to board.reveal() through a worker.
        :param button:
        :return:
        '''
        # Guard: Player must still be playing
        if self.loss:
            return

        # Make the smiley show the pressing state.
        self.smiley.state = 1

        # Create a new worker, and pass it the click field
        # Pass the reference to the board.reveal method, with loc as an argument
        worker = Worker(self.board.reveal, loc)
        # We update the button when the result comes back.
        worker.signals.result.connect(self.update_fields)
        # We update the entire UI when the thread is finished.
        worker.signals.finished.connect(self.refreshUI)
        self.threadpool.start(worker)

    def flag_field(self, loc):
        '''
        Registers a right click, passes location to board.flag() through a worker.
        :param button:
        :return:
        '''
        # Guard: Player must still be playing
        if self.loss:
            return
        # Create a new worker, and pass it the click field
        # Pass the reference to the board.reveal method, with loc as an argument
        worker = Worker(self.board.flag, loc)
        # We update the button when the result comes back.
        worker.signals.result.connect(self.update_fields)
        # We update the entire UI when the thread is finished.
        worker.signals.finished.connect(self.refreshUI)
        self.threadpool.start(worker)

    def recurring_timer(self):
        if self.loss is False:
            self.counter += 1
            self.time_display.setText(f"{self.counter:0>3}")
            # Makes the smiley go back to state 0.
            self.smiley.state = 0

    def save_state(self):
        """
        Creates a new worker to save the Board state
        :return:
        """
        save_obj = {
            "board": self.board,
            "counter": self.counter,
            "flags": self.flags
        }
        # We don't need anything back from it.
        worker = Worker(save.save, save_obj)
        self.threadpool.start(worker)

    def load(self):
        # See if there's a save file.
        save_obj = save.load()
        if save_obj:
            return save_obj
        else:
            return False



class display(QLabel):
    def make(self):
        self.setText("000")
        self.resize(60, 40)
        self.setStyleSheet("""
                  border-width: 0px;
                  border-style: solid;
                  color: rgb(71, 71, 71);
                  text-align: center;
                  padding: 6px 5px 4px 5px;
                  font-size: 24px;
                  font-family: Arial;
                  font-weight: bold;
                  border-color: rgb(66, 66, 66), rgb(117, 117, 117), rgb(117, 117, 117), rgb(66, 66, 66);
                  background-color: #ccc;
        """)

if __name__ == '__main__':
    # Instantiate Application Context
    # appctxt = ApplicationContext()

    app = QApplication(sys.argv)
    ex = MainApplication()

    # Invoke appctxt.app.exec_()
    #exit_code = appctxt.app.exec_()
    #sys.exit(exit_code)
    sys.exit(app.exec_())