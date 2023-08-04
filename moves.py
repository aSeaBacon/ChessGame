import typing
from PyQt6.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt6.QtCore import Qt, QSize
from PyQt6 import QtCore, QtWidgets, uic
from square import Square

class movesContainer(QWidget):

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



    def addMove(self, startCoords, endCoords, capture, pieceName, board):
        
        #Move num = moves % 2 + 1 (ie 5 moves -> move 3 (3 white, 2 black))
        #if moves % 2 == 1, create new moves line, else add to current moves line
        self.moves +=1 
        #Determine notation
        #All pieces except Knights and pawns use first letter of piece
        #All pieces except king need to check for any other piece of the same name that could have also made that move

        if pieceName == "Knight":
            pass
        elif pieceName == "Pawn":
            pass
        else:
            pass


