from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtGui import QPalette, QColor, QPixmap, QPainter, QBrush, QPen
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QPoint
from itertools import cycle
from pieces import Pawn, Rook, Bishop, Knight, King, Queen



class Square(QtWidgets.QLabel):

    clicked = pyqtSignal()

    def __init__(self, chessBoard, coords, color, piece=None):
        super().__init__()

        self.coords = coords
        self.piece = piece
        self.highLight = False
        self.color = color
        self.chessBoard = chessBoard

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window,QColor(self.color))
        self.setPalette(palette)

        if self.piece != None:
            self.setPixmap(self.piece.image)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.clicked.connect(self.chessBoard.squareClicked)

    def mousePressEvent(self, event):
        self.chessBoard.clickedSquare = self
        self.clicked.emit()

    # def squareClicked(self):
    #     if self.highLight and self.coords == self.chessBoard.currentSquare:
    #         self.removeHighLight()
    #     elif self.highLight == False and self.chessBoard.currentSquare == None:
    #         self.highLightSquare()
    #     else:
    #         pass

    #     if self.piece == None:
    #         self.addHint()
        

    def highlightSquare(self):
        if self.piece != None:
            canvas = QPixmap(self.size())
            canvas.fill(QColor(255,255,0,127))
            painter = QPainter(canvas)
            point = QPoint((self.width() - self.piece.image.width())//2 , (self.height() - self.piece.image.height())//2)
            painter.drawPixmap(point, self.piece.image)
            painter.end()
            self.setPixmap(canvas)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def removeHighlight(self):
        if self.piece != None:
            self.clear()
            self.setPixmap(self.piece.image)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.clear()
            

    def addHint(self):
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
        if self.piece == None:
            self.clear()
        else:
            self.clear()
            self.setPixmap(self.piece.image)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        
        


class ChessBoard(QWidget):

    highlightedSquare = None
    currentPlayer = "White"
    clickedSquare = None

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.squares = []

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
                        self.layout.addWidget(Square(self, (i,j), color, Pawn(player)), i, j)
                    else:
                        match j:
                            case 0 | 7:
                                self.layout.addWidget(Square(self, (i,j), color, Rook(player)), i, j)
                            case 1 | 6:
                                self.layout.addWidget(Square(self, (i,j), color, Knight(player)), i, j)
                            case 2 | 5:
                                self.layout.addWidget(Square(self, (i,j), color, Bishop(player)), i, j)
                            case 3:
                                self.layout.addWidget(Square(self, (i,j), color, Queen(player)), i, j)
                            case 4:
                                self.layout.addWidget(Square(self, (i,j), color, King(player)), i, j)

                elif i == 6 or i == 7:
                    player = "White"
                    if i == 6:
                        self.layout.addWidget(Square(self, (i,j), color, Pawn(player)), i, j)
                    else:
                        match j:
                            case 0 | 7:
                                self.layout.addWidget(Square(self, (i,j), color, Rook(player)), i, j)
                            case 1 | 6:
                                self.layout.addWidget(Square(self, (i,j), color, Knight(player)), i, j)
                            case 2 | 5:
                                self.layout.addWidget(Square(self, (i,j), color, Bishop(player)), i, j)
                            case 3:
                                self.layout.addWidget(Square(self, (i,j), color, Queen(player)), i, j)
                            case 4:
                                self.layout.addWidget(Square(self, (i,j), color, King(player)), i, j)
                else:
                    self.layout.addWidget(Square(self, (i,j), color), i, j)

        self.setLayout(self.layout)
        self.setFixedSize(QSize(600,600))

        for i in range(8):
            tmpList = []
            for j in range(8):
                tmpList.append(self.layout.itemAtPosition(i,j).widget())
            self.squares.append(tmpList)

    def squareClicked(self):

        #Either white occupied, black occupied or empty square is clicked

        if self.clickedSquare.piece == None:
            if self.highlightedSquare != None and self.clickedSquare.coords in self.highlightedSquare.piece.legalMoves:
                self.clickedSquare.piece = self.highlightedSquare.piece
                self.clickedSquare.updateSquare()
                self.highlightedSquare.piece = None
                self.highlightedSquare.updateSquare()
                self.highlightedSquare = None
            elif self.highlightedSquare != None:
                self.highlightedSquare.removeHighlight()
                self.highlightedSquare = None

        elif self.clickedSquare.piece.player == self.currentPlayer:
            #Either:
            #   A square is highlighted, so need to remove old highlight and highlight new square
            #   Highlighted square is clicked, so remove highlight on that square
            #   No square is highlighted, so highlight clicked square
            if self.clickedSquare == self.highlightedSquare:
                self.clickedSquare.removeHighlight()
                self.highlightedSquare = None

            elif self.highlightedSquare != None:
                self.highlightedSquare.removeHighlight()
                self.clickedSquare.highlightSquare()
                self.highlightedSquare = self.clickedSquare

            else:
                self.highlightedSquare = self.clickedSquare
                self.clickedSquare.highlightSquare()
        else:
            pass

        # print(self.layout.itemAtPosition(0,0).widget().coords)
        # self.setGeometry(100,100,400,400)
