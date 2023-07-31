from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPalette, QColor, QPixmap, QPainter, QBrush, QPen
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QPoint



class Square(QLabel):

    clicked = pyqtSignal()
    isHighlighted = False
    hasHint = False

    def __init__(self, chessBoard, coords, color, piece=None):
        super().__init__()

        self.coords = coords
        self.piece = piece
        self.color = color
        self.chessBoard = chessBoard

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(self.color))
        self.setPalette(palette)
        self.updateSquare()

        self.clicked.connect(self.chessBoard.squareClicked)

    def mousePressEvent(self, event):
        #This line seems to break this function
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
        painter.drawPixmap(point, self.piece.image)
        painter.end()
        self.setPixmap(canvas)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def removeHighlight(self):
        self.clear()
        if self.piece != None:
            self.setPixmap(self.piece.image)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def addHint(self):
        self.clear()
        canvas = QPixmap(self.size())
        canvas.fill(QColor(0,0,0,0))
        r = self.width()//6
        painter = QPainter(canvas)
        center = QPoint(self.height()//2, self.width()//2)
        brush = QBrush(Qt.BrushStyle.SolidPattern)
        brush.setColor(QColor(0,0,0,25))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(brush)
        painter.drawEllipse(center, r, r)
        self.setPixmap(canvas)
        painter.end()

    def removeHint(self):
        self.clear()

    def updateSquare(self):
        if self.piece != None:
            if self.isHighlighted:
                self.addHighlight()
            else:
                self.clear()
                self.setPixmap(self.piece.image)
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        else:
            if self.hasHint:
                self.addHint()
            else:
                self.clear()
    

