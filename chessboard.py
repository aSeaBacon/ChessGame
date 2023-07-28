from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtGui import QPalette, QColor, QPixmap, QPainter, QBrush
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from itertools import cycle
from pieces import Pawn, Rook, Bishop, Knight, King, Queen



class Square(QtWidgets.QLabel):

    clicked = pyqtSignal()

    def __init__(self, coords, color, piece=None):
        super().__init__()

        self.coords = coords
        self.piece = piece
        self.hightLight = False
        self.color = color

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window,QColor(self.color))
        self.setPalette(palette)

        if self.piece != None:
            self.setPixmap(self.piece.image)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.clicked.connect(self.squareClicked)

    def mousePressEvent(self, event):
        self.clicked.emit()

    # def squareClicked(self):
    #     print("Clicked:", self.coords, self.piece)
    #     canvas = QPixmap(self.width(), self.width())
    #     canvas.fill(QColor(255,255,0,127))
    #     self.setPixmap(canvas)
    #     self.setPalette(canvas)
    #     self.setPixmap(self.piece.image)
        

    #     # self.setPixmap(QPixmap("ChessPieces\RookW.png"))
        

        
        


class ChessBoard(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        layout.setSpacing(0)

        #Color codes used for squares on chessboard
        values = cycle(["#769656", "#eeeed2"])

        #Setsup initial gamestate, initalizing all squares/pieces
        for i in range(8):
            color = next(values)

            for j in range(8):
                color = next(values)

                if i == 0 or i ==1:
                    player = "Black"
                    if i == 1:
                        layout.addWidget(Square((i,j), color, Pawn(player)), i, j)
                    else:
                        match j:
                            case 0 | 7:
                                layout.addWidget(Square((i,j), color, Rook(player)), i, j)
                            case 1 | 6:
                                layout.addWidget(Square((i,j), color, Knight(player)), i, j)
                            case 2 | 5:
                                layout.addWidget(Square((i,j), color, Bishop(player)), i, j)
                            case 3:
                                layout.addWidget(Square((i,j), color, Queen(player)), i, j)
                            case 4:
                                layout.addWidget(Square((i,j), color, King(player)), i, j)

                elif i == 6 or i == 7:
                    player = "White"
                    if i == 6:
                        layout.addWidget(Square((i,j), color, Pawn(player)), i, j)
                    else:
                        match j:
                            case 0 | 7:
                                layout.addWidget(Square((i,j), color, Rook(player)), i, j)
                            case 1 | 6:
                                layout.addWidget(Square((i,j), color, Knight(player)), i, j)
                            case 2 | 5:
                                layout.addWidget(Square((i,j), color, Bishop(player)), i, j)
                            case 3:
                                layout.addWidget(Square((i,j), color, Queen(player)), i, j)
                            case 4:
                                layout.addWidget(Square((i,j), color, King(player)), i, j)
                else:
                    layout.addWidget(Square((i,j), color), i, j)

        self.setLayout(layout)
        self.setFixedSize(QSize(800,800))
        self.setGeometry(100,100,400,400)
