import typing
from PyQt6.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt6.QtCore import Qt, QSize
from PyQt6 import QtCore, QtWidgets, uic
from square import Square

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

    def __init__(self):
        super().__init__()

        self.moves = 0

        scrollArea = QScrollArea()
        self.layout = QVBoxLayout()

        for i in range(1,50):
            object = QLabel("1.   e4   e5")
            self.layout.addWidget(object)
        
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)



    def addMove(self, startCoords, endCoords, capture, check, castle, pieceName, board):

        moveNotation = ""
        
        #Move num = moves % 2 + 1 (ie 5 moves -> move 3 (3 white, 2 black))
        #if moves % 2 == 1, create new moves line, else add to current moves line
        self.moves +=1 
        #Determine notation
        #All pieces except Knights and pawns use first letter of piece
        #All pieces except king need to check for any other piece of the same name that could have also made that move

        if pieceName == "Knight":
            count = 0
            for row in board.squares:
                for square in row:
                    if square.piece != None and square.piece.pieceName == pieceName:
                        if endCoords in square.piece.legalMoves:
                            count+=1
            if count == 1:
                uniqueMove = True
            else:
                uniqueMove = False

            if uniqueMove:
                if capture:
                    moveNotation = "Nx" + str(self.notationDict[endCoords[1]]) + str(endCoords[1])
                else:
                    moveNotation = "N" + str(self.notationDict[endCoords[1]]) + str(endCoords[1])

            if check:
                moveNotation = moveNotation + "+"
        

        elif pieceName == "Pawn":
            pass
        else:
            pass


        print(moveNotation)


