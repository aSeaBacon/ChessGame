from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPalette, QColor, QPixmap, QPainter, QBrush, QPen
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QPoint
from pieces import Pawn, Rook, Bishop, Knight, King, Queen
from chessboard import ChessBoard

class Square(QLabel):

    clicked = pyqtSignal()
    isHighlighted = False
    hasHint = False

    def __init__(self, chessBoard, coords, color, piece=None):
        super().__init()

        self.coords = coords
        self.piece = piece
        self.color = color
        self.chessBoard = chessBoard

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(self.color))
        self.setPalette(palette)

        self.clicked.connect(self.chessBoard.squareClicked)

    def mousePressEvent(self, event):
        #No idea if this line is needed
        # super().__init__()
        self.chessBoard.clickedSquare = self
        self.clicked.emit()

    def addHighlight(self):
        self.clear()
        canvas = QPixmap(self.size())
        #50% transparent yellow color used for highlight
        canvas.fill(QColor(255,255,0,127))
        point = QPoint((self.width() - self.piece.image.width())//2, (self.height() - self.piece.image.height())//2)
        painter = QPainter(canvas)