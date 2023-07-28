from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from chessboard import ChessBoard
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chess")
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.addWidget(ChessBoard())


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)




app = QApplication([])

window = MainWindow()
window.show()

app.exec()

