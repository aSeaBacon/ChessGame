from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QPalette, QColor, QPixmap, QPainter, QBrush, QPen
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QPoint, QPointF
from itertools import cycle
from pieces import Pawn, Rook, Bishop, Knight, King, Queen
from square import Square        


class ChessBoard(QWidget):

    highlightedSquare = None
    clickedSquare = None
    currentPlayer = "White"
    isKingChecked = False
    checkingPieces = []
    checkedKing = None

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
                        self.layout.addWidget(Square(self, (i,j), color, Pawn(player, self, (i,j))), i, j)
                    else:
                        match j:
                            case 0 | 7:
                                self.layout.addWidget(Square(self, (i,j), color, Rook(player, self, (i,j))), i, j)
                            case 1 | 6:
                                self.layout.addWidget(Square(self, (i,j), color, Knight(player, self, (i,j))), i, j)
                            case 2 | 5:
                                self.layout.addWidget(Square(self, (i,j), color, Bishop(player, self, (i,j))), i, j)
                            case 3:
                                self.layout.addWidget(Square(self, (i,j), color, Queen(player, self, (i,j))), i, j)
                            case 4:
                                self.layout.addWidget(Square(self, (i,j), color, King(player, self, (i,j))), i, j)

                elif i == 6 or i == 7:
                    player = "White"
                    if i == 6:
                        self.layout.addWidget(Square(self, (i,j), color, Pawn(player, self, (i,j))), i, j)
                    else:
                        match j:
                            case 0 | 7:
                                self.layout.addWidget(Square(self, (i,j), color, Rook(player, self, (i,j))), i, j)
                            case 1 | 6:
                                self.layout.addWidget(Square(self, (i,j), color, Knight(player, self, (i,j))), i, j)
                            case 2 | 5:
                                self.layout.addWidget(Square(self, (i,j), color, Bishop(player, self, (i,j))), i, j)
                            case 3:
                                self.layout.addWidget(Square(self, (i,j), color, Queen(player, self, (i,j))), i, j)
                            case 4:
                                self.layout.addWidget(Square(self, (i,j), color, King(player, self, (i,j))), i, j)
                else:
                    self.layout.addWidget(Square(self, (i,j), color), i, j)

        self.setLayout(self.layout)
        self.setFixedSize(QSize(600,600))

        #Add all Squares objects to 8x8 array (squares) to make future access easier
        for i in range(8):
            tmpList = []
            for j in range(8):
                tmpList.append(self.layout.itemAtPosition(i,j).widget())
            self.squares.append(tmpList)

    def squareClicked(self):
        print(self.clickedSquare.piece,":",self.clickedSquare.coords)
        #Either white occupied, black occupied or empty square is clicked

        #Player clicks empty square
        if self.clickedSquare.piece == None:
            #Currently selected square exists AND new square is a legal move for the selected piece
            if self.highlightedSquare != None and self.clickedSquare.coords in self.highlightedSquare.piece.legalMoves:
                self.movePiece()
            #Currently selected square exists but click square is not a legal move for selected piece
            elif self.highlightedSquare != None:
                self.highlightedSquare.isHighlighted = False
                self.highlightedSquare.updateSquare()
                self.setHints(self.highlightedSquare, False)
                self.highlightedSquare = None

        #Player clicks one of their peices
        elif self.clickedSquare.piece.player == self.currentPlayer:
            #Recalculate legal moves
            self.clickedSquare.piece.getPossibleMoves()
            self.clickedSquare.piece.getLegalMoves()
            print(self.clickedSquare.piece.pieceName, ":",self.clickedSquare.piece.legalMoves)
            #Clicked square is currently highlighted
            if self.clickedSquare == self.highlightedSquare:
                self.clickedSquare.isHighlighted = False
                self.clickedSquare.updateSquare()
                self.setHints(self.clickedSquare, False)
                self.highlightedSquare = None

            #Another Square is currently highlighted
            elif self.highlightedSquare != None:
                self.selectNewSquare()

            #No currently highlighted Square
            else:
                self.highlightedSquare = self.clickedSquare
                self.clickedSquare.isHighlighted = True
                self.clickedSquare.updateSquare()
                self.setHints(self.clickedSquare, True)

        #Player clicks one of opponents pieces           
        else:
            if self.highlightedSquare != None:
                #Player has a selected piece and can capture clicked piece
                if self.clickedSquare.coords in self.highlightedSquare.piece.legalMoves:
                    self.movePiece()
                #If player can't capture, just deselect currently selected piece
                else:
                    self.highlightedSquare.isHighlighted = False
                    self.highlightedSquare.updateSquare()
                    self.setHints(self.highlightedSquare, False)
                    self.highlightedSquare = None
            

    def setHints(self, square, flag):
        for coords in square.piece.legalMoves:
            i, j = coords[0], coords[1]
            self.squares[i][j].hasHint = flag
            self.squares[i][j].updateSquare()

    def movePiece(self):

        if self.highlightedSquare.piece.pieceName in ["Pawn", "King", "Rook"]:
            self.highlightedSquare.piece.hasMoved = True
        self.clickedSquare.piece = self.highlightedSquare.piece
        self.clickedSquare.piece.coords = self.clickedSquare.coords
        self.clickedSquare.updateSquare()
        self.setHints(self.highlightedSquare, False)
        self.highlightedSquare.piece = None
        self.highlightedSquare.isHighlighted = False
        self.highlightedSquare.updateSquare()
        self.highlightedSquare = None

        if self.currentPlayer == "White":
            self.currentPlayer = "Black"
        else:
            self.currentPlayer = "White"

    def selectNewSquare(self):

        #Highlight clicked square
        self.clickedSquare.isHighlighted = True
        self.clickedSquare.updateSquare()

        #Remove highlight from previously highlighted square
        self.highlightedSquare.isHighlighted = False
        self.highlightedSquare.updateSquare()

        #Remove hints from previously highlighted square
        self.setHints(self.highlightedSquare, False)

        #Add hints for clicked square
        self.setHints(self.clickedSquare, True)

        #Set clicked square as highlighted square
        self.highlightedSquare = self.clickedSquare

    def createLine(self, loc1, loc2, incLoc1=False, incLoc2=False):

        #Generates points from starting position to ending position in order
        #i.e a:(1,0) b:(4,0)
        #    a->b = [(2,0), (3,0)]
        #    b->a = [(3,0), (2,0)]

        points = []
        if loc1[0] == loc2[0]:
            if loc2[1] > loc1[1]:
                for i in range(1, loc2[1] - loc1[1]):
                    points.append((loc1[0], loc1[1] + i))
            else:
                for i in range(1, loc1[1] - loc2[1]):
                    points.append((loc1[0], loc1[1] - i))

        else:
            m = (loc2[1] - loc1[1]) // (loc2[0] - loc1[0])
            if loc2[0] > loc1[0]:
                for x in range(1, loc2[0] - loc1[0]):
                    points.append((loc1[0] + x, loc1[1] + x*m))
            else:
                for x in range(1, loc1[0] - loc2[0]):
                    points.append((loc1[0] - x, loc1[1] - x*m))

        if incLoc1 and loc1!=loc2:
            points.append(loc1)

        if incLoc2 and loc1!=loc2:
            points.append(loc2)

        return points

    

        # print(self.layout.itemAtPosition(0,0).widget().coords)
        # self.setGeometry(100,100,400,400)
