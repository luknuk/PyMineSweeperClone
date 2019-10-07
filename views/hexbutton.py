from PyQt5 import QtCore, QtGui, QtWidgets

"""
HexButton
.text = ""
.move(x, y)
"""
DEBUG = False


class HexGuiField(QtWidgets.QPushButton):
    textChanged = QtCore.pyqtSignal(str)

    def __init__(self, loc, parent):
        super(HexGuiField, self).__init__(parent)
        # Default values
        if DEBUG:
            self.setToolTip(str(loc))

        self.__text = ""
        self.loc = loc

        # A regular offset exists, to move the entire grid into the centre.
        self.offset = (6, 50)

        # If it's an odd row, we shift it right, by adding to offset.
        if loc[0] % 2:
            self.offset = (self.offset[0] + 15, self.offset[1])

        self.text_label = QtWidgets.QLabel()

        self.resize(29, 29)
        self.move(self.loc[1] * 29 + self.offset[0], self.loc[0] * 25 + self.offset[1])

        # Create the label
        self.text_label.setMinimumWidth(16)
        self.text_label.setMinimumHeight(16)
        self.text_label.setStyleSheet("""
                color: blue;
                font-weight: bold;
                """)
        # Centre the text in the hexagon
        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(2, 2, 0, 0)
        lay.addWidget(self.text_label, alignment=QtCore.Qt.AlignCenter)

        self.draw("#ebbd34")

    def draw(self, colour):
        # Create the hexagon shape
        # Get the SVG, set colour, make it the icon of the button.
        qimage = QtGui.QImage.fromData(self.svg_hexagon(QtGui.QColor(colour)))
        qicon = QtGui.QPixmap(qimage)
        self.setIcon(QtGui.QIcon(qicon))
        self.setIconSize(QtCore.QSize(30, 30))
        self.setStyleSheet(
            """
            margin: 0px;
            padding: 0px;
            position: absolute;
            border: none;
        """)


    def svg_hexagon(self, colour):
        svg_bytes = f'<svg xmlns="http://www.w3.org/2000/svg" width="31" height="31"><path stroke="none" fill="{colour.name()}" d="M12.5 1.2320508075689a6 6 0 0 1 6 0l7.856406460551 4.5358983848622a6 6 0 0 1 3 5.1961524227066l0 9.0717967697245a6 6 0 0 1 -3 5.1961524227066l-7.856406460551 4.5358983848622a6 6 0 0 1 -6 0l-7.856406460551 -4.5358983848623a6 6 0 0 1 -3 -5.1961524227066l0 -9.0717967697245a6 6 0 0 1 3 -5.1961524227066"></path></svg>'
        return bytearray(svg_bytes, encoding="utf-8")

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
        QLabel {
            font-weight:bold;
        """
        if colour is False:
            self.draw("#ccc")
            # Flatten the button, no text colour
            self.text_label.setStyleSheet(f"{style} }}")
        else:
            self.draw("#ccc")
            # Flatten the button and set text colour
            self.text_label.setStyleSheet(f"{style} color: {COLOURS[colour]} }}")

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, t):
        if t is "*":
            t = "💣"
        elif t.isnumeric():
            t = " "+t
        elif t is "f":
            t = "🚩"
        self.__text = t
        self.text_label.setText(t)



def test_main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()

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

    button = HexGuiField((0, 0), window)
    button.text = "💣"

    button = HexGuiField((0, 1), window)
    button.text = "🚩"

    button = HexGuiField((1, 0), window)
    button.text = " 8"

    button = HexGuiField((1, 1), window)
    button.text = ""

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    test_main()




