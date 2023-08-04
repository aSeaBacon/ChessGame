from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QScrollArea
from PyQt6.QtCore import Qt, QSize
from chessboard import ChessBoard
from moves import movesContainer
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        scrollArea = QScrollArea()
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollArea.setWidgetResizable(True)
        scrollArea.setFixedSize(QSize(150,600))
        moves = movesContainer()
        scrollArea.setWidget(moves)

        self.setWindowTitle("Chess Game")
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.addWidget(ChessBoard(moves), 0, 0)
        layout.addWidget(scrollArea, 0, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)




app = QApplication([])

window = MainWindow()
window.show()

app.exec()

