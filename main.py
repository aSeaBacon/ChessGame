from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QScrollArea, QStackedWidget
from PyQt6.QtCore import Qt, QSize
from chessboard import ChessBoard
from moves import movesContainer
        

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        moves = movesContainer(self)
        self.currentBoard = ChessBoard(moves, self)


        self.scrollArea = QScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedSize(QSize(150,600))
        self.scrollArea.setWidget(moves)
        self.scrollArea.verticalScrollBar().rangeChanged.connect(self.scrollToBottom)

        # scrollArea.scroll

        self.setWindowTitle("Chess Game")

        stackedWidget = QStackedWidget()
        stackedWidget.addWidget(self.currentBoard)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.addWidget(stackedWidget, 0, 0)
        layout.addWidget(self.scrollArea, 0, 1)
        layout.setContentsMargins(0,0,0,0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.centralWidget().layout().itemAtPosition(0,1).widget().verticalScrollBar().rangeChanged.connect(self.scrollToBottom)
        
    def scrollToBottom(self, minVal = None, maxVal = None):
        # self.scrollArea.verticalScrollBar().maximum()
        self.centralWidget().layout().itemAtPosition(0,1).widget().verticalScrollBar().setValue(
            self.centralWidget().layout().itemAtPosition(0,1).widget().verticalScrollBar().maximum()
        )



app = QApplication([])

window = MainWindow()
window.show()

app.exec()

