from PyQt6 import QtGui

class Pawn():
    def __init__(self, player):
        if player=="White":
            self.image = QtGui.QPixmap("ChessPieces\PawnW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\PawnB.png")

class Rook():
    def __init__(self, player):
        if player=="White":
            self.image = QtGui.QPixmap("ChessPieces\RookW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\RookB.png")

class Knight():
    def __init__(self, player):
        if player=="White":
            self.image = QtGui.QPixmap("ChessPieces\KnightW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\KnightB.png")

class Bishop():
    def __init__(self, player):
        if player=="White":
            self.image = QtGui.QPixmap("ChessPieces\BishopW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\BishopB.png")

class Queen():
    def __init__(self, player):
        if player=="White":
            self.image = QtGui.QPixmap("ChessPieces\QueenW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\QueenB.png")
    
class King():
    def __init__(self, player):
        if player=="White":
            self.image = QtGui.QPixmap("ChessPieces\KingW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\KingB.png")