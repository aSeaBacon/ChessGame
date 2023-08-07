import typing
from PyQt6.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow, QGridLayout)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from square import Square
from itertools import cycle
from PyQt6.QtGui import QPalette, QColor, QPixmap

class movesContainer(QWidget):

    notationDict = {
        0 : "a",
        1 : "b",
        2 : "c",
        3 : "d",
        4 : "e",
        5 : "f",
        6 : "g",
        7 : "h"
    }

    clickedMove = None
    currentMove = None

    def __init__(self, main):
        super().__init__()

        self.moves = 0
        self.main = main
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("1. "), 0, 0)
        self.layout.addWidget(QLabel(""), 0, 1)
        self.layout.addWidget(QLabel(""), 0, 2)

        # for i in range(1,50):
        #     object = QLabel(str(i))
        #     self.layout.addWidget(object, i, 0)
        #     self.layout.addWidget(object, i, 1)
        #     self.layout.addWidget(object, i, 2)

        # self.moves = 100
        
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)



    def addMove(self, player, startCoords, endCoords, capture, check, checkMate, shortCastle, longCastle, pieceName, board, boardState):

        moveNotation = ""
        
        #Move num = moves % 2 + 1 (ie 5 moves -> move 3 (3 white, 2 black))
        #if moves % 2 == 1, create new moves line, else add to current moves line
        self.moves +=1 
        #Determine notation
        #All pieces except Knights and pawns use first letter of piece
        #All pieces except king need to check for any other piece of the same name that could have also made that move


        count = 0
        for row in board.squares:
            for square in row:
                if square.piece != None and square.piece.player == player and square.piece.pieceName == pieceName:
                    if endCoords in square.piece.possibleMoves:
                        count+=1
                        
        if count == 1:
            uniqueMove = False
        else:
            uniqueMove = True

        if pieceName == "Knight":

            if uniqueMove:
                if capture:
                    moveNotation = "Nx" + self.notationDict[endCoords[1]] + str(8 - endCoords[0])
                else:
                    moveNotation = "N" + self.notationDict[endCoords[1]] + str(8 - endCoords[0])

            else:
                if capture:
                    moveNotation = "N" + self.notationDict[startCoords[1]] + "x" + self.notationDict[endCoords[1]] + str(8 - endCoords[0])
                else:
                    moveNotation = "N" + self.notationDict[startCoords[1]] + self.notationDict[endCoords[1]] + str(8 - endCoords[0])
        

        elif pieceName == "Pawn":
            if capture:
                moveNotation = self.notationDict[startCoords[1]] + "x" + self.notationDict[endCoords[1]] + str(8 - endCoords[0])
            else:
                moveNotation = self.notationDict[endCoords[1]] + str(8 - endCoords[0])
        else:
            if uniqueMove:
                if capture:
                    moveNotation = pieceName[0] + "x" + self.notationDict[endCoords[1]] + str(8 - endCoords[0])
                else:
                    moveNotation = pieceName[0] + self.notationDict[endCoords[1]] + str(8 - endCoords[0])
            else:
                if capture:
                    moveNotation = pieceName[0] +  self.notationDict[startCoords[1]] + "x" + self.notationDict[endCoords[1]] + str(8 - endCoords[0])
                else:
                    moveNotation = pieceName[0] + self.normalGeometry[startCoords[1]] + self.notationDict[endCoords[1]] + str(8 - endCoords[0])


        if shortCastle:
            moveNotation = "O-O"
        elif longCastle:
            moveNotation = "O-O-O"

        if checkMate:
            moveNotation = moveNotation + "#"
        elif check:
            moveNotation = moveNotation + "+"


        print(moveNotation)

        if self.moves%2 != 0:
            self.currentMove = movesItem(moveNotation, self, boardState)
            self.layout.addWidget(QLabel(str(self.moves//2 + 1) + ". "), self.moves//2, 0)
            self.layout.addWidget(self.currentMove, self.moves//2, 1)
        else:
            self.currentMove = movesItem(moveNotation, self, boardState)
            self.layout.addWidget(self.currentMove, self.moves//2 - 1, 2)

    def clickedMove(self):

        if self.clickedMove == self.currentMove:
            # self.centralWidget().layout().itemAtPosition(0,1).widget().verticalScrollBar().rangeChanged.connect(self.scrollToBottom)
            self.main.centralWidget().layout().addWidget(self.main.currentBoard)
        else:
            self.main.centralWidget().layout().addWidget(self.clickedMove.display)

class movesItem(QLabel):

    clicked = pyqtSignal()
    board = None
    display = None

    def __init__(self, moveText, movesContainer, boardState):
        super().__init__()
        self.setText(moveText)
        self.movesContainer = movesContainer
        self.createBoard(boardState)
        self.clicked.connect(self.movesContainer.clickedMove)

    def mousePressEvent(self, event):
        self.movesContainer.clickedMove = self
        self.clicked.emit()

    def createBoard(self, boardState):
        boardArray = boardState.split(" ")
        self.display = DisplayBoard(boardArray)



class DisplayBoard(QWidget):

    def __init__(self, boardArray):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setSpacing(0)

        #Color codes used for squares on chessboard
        values = cycle(["#769656", "#eeeed2"])

        for i in range(8):
            squareColor = next(values)
            for j in range(8):
                piece = boardArray.pop(0)
                pieceColor = boardArray.pop(0)

                self.layout.addWidget(DisplaySquare(squareColor, piece, pieceColor))

class DisplaySquare(QLabel):

    def __init__(self, squareColor, piece, pieceColor):
        super().__init__()
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(squareColor))
        self.setPalette(palette)

        match piece:
            case "Pawn":
                if pieceColor=="White":
                    self.image = QtGui.QPixmap("ChessPieces\PawnW.png")
                else:
                    self.image = QtGui.QPixmap("ChessPieces\PawnB.png")
            case "Knight":
                if pieceColor == "White":
                    self.image = QtGui.QPixmap("ChessPieces\KnightW.png")
                else:
                    self.image = QtGui.QPixmap("ChessPieces\KnightB.png")
            case "Bishop":
                if pieceColor == "White":
                    self.image = QtGui.QPixmap("ChessPieces\BishopW.png")
                else:
                    self.image = QtGui.QPixmap("ChessPieces\BishopB.png")
            case "Rook":
                if pieceColor == "White":
                    self.image = QtGui.QPixmap("ChessPieces\RookW.png")
                else:
                    self.image = QtGui.QPixmap("ChessPieces\RookB.png")
            case "Queen":
                if pieceColor == "White":
                    self.image = QtGui.QPixmap("ChessPieces\QueenW.png")
                else:
                    self.image = QtGui.QPixmap("ChessPieces\QueenB.png")
            case "King":
                if pieceColor == "White":
                    self.image = QtGui.QPixmap("ChessPieces\KingW.png")
                else:
                    self.image = QtGui.QPixmap("ChessPieces\KingB.png")
            case _:
                self.image = QPixmap()

        self.setPixmap(self.image)



                
    

