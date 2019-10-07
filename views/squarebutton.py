from PyQt5 import QtCore, QtGui, QtWidgets

DEBUG = False

class SquareGuiField(QtWidgets.QPushButton):
    textChanged = QtCore.pyqtSignal(str)

    def __init__(self, loc, parent):
        super(SquareGuiField, self).__init__(parent)
        # Default values
        if DEBUG:
            self.setToolTip(str(loc))
        self.text = " "
        self.loc = loc
        self.offset = (6, 50)
        self.init()


    def init(self):
        self.move(self.loc[1]*24+self.offset[0], self.loc[0]*24+self.offset[1])
        self.resize(24, 24)
        self.setFlat(False)
        # Set starting stylesheet
        self.setStyleSheet("""
            QPushButton:hover{
              background-color: rgb(185, 185, 185);
            }
            QPushButton{
              width: 16px; height: 16px;
              border-width: 2px;
              border-style: solid;
              border-color: #fff, rgb(117, 117, 117), rgb(117, 5, 117), #fff;
              background-color: rgb(200, 200, 200);
            }
        """)

    def left_click(self, func):
        # Connects passed function to left click event listener
        self.clicked.connect(lambda *args, loc=self.loc: func(loc))

    def right_click(self, func):
        # Connects passed function to right click event listener
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda *args, loc=self.loc: func(loc))

    def flatten(self, colour=False):
        '''
        
        :param colour: False, 1-9
        :return: No value
        '''
        COLOURS = {
            1: "blue",
            2: "green",
            3: "red",
            4: "navy",
            5: "maroon",
            6: "turqoise",
            7: "purple",
            8: "grey"
        }
        style = """
        QPushButton {
              width: 20px; height: 20px;
              border: 0.5px solid;
              border-color: rgb(117, 117, 117);
              font-size:16pt;
              font-weight: bold;
              background-color: rgb(200, 200, 200);
        """
        if colour is False:
            # Flatten the button, no text colour
            self.setStyleSheet(f"{style} }}")
        else:
            # Flatten the button and set text colour
            self.setStyleSheet(f"{style} color: {COLOURS[colour]} }}")

    # Set and get text.
    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, t):
        if t is "*":
            t = "💣"
        elif t is "f":
            t = "🚩"
        self.__text = t
        self.setText(t)
