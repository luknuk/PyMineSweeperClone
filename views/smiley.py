from PyQt5 import QtCore, QtGui, QtWidgets

DEBUG = False


class SmileyButton(QtWidgets.QPushButton):
    textChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(SmileyButton, self).__init__(parent)
        # Default values

        self.__state = ""

        self.text_label = QtWidgets.QLabel()

        self.resize(46, 40)
        self.move(5, 48)

        self.setStyleSheet("""
        QPushButton{
              border-width: 2px;
              border-style: solid;
              border-color: #fff, rgb(117, 117, 117), rgb(117, 5, 117), #fff;
              background-color: rgb(200, 200, 200);
            }
        QPushButton:hover:!pressed
            {
              background-color: rgb(185, 185, 185);
            }""")

        # Create the label
        self.text_label.setMinimumWidth(32)
        self.text_label.setMinimumHeight(32)
        self.text_label.setStyleSheet("""
                color: blue;
                font-weight: bold;
                font-size: 28pt;
                """)
        # Centre the text in the hexagon
        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(4, 5, 0, 0)
        lay.addWidget(self.text_label, alignment=QtCore.Qt.AlignCenter)

    def left_click(self, func):
        # Connects passed function to left click event listener
        self.clicked.connect(lambda: func())

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        if state is 0:
            s = "😄"
        elif state is 1:
            s = "😬"
        elif state is 2:
            s = "😵"
        elif state is 3:
            s = "😎"

        self.__state = s
        self.text_label.setText(s)



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


    button = SmileyButton(window)
    button.state = 0

    #button = SmileyButton(window)
    #button.state = 4

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    test_main()




