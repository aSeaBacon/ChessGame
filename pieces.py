from PyQt6 import QtGui

class Pawn():
    def __init__(self, player):
        if player=="White":
            self.image = QtGui.QPixmap("ChessPieces\PawnW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\PawnB.png")

        self.legalMoves = [(5,5), (4,5)]
        self.player = player

class Rook():
    def __init__(self, player):
        if player=="White":
            self.image = QtGui.QPixmap("ChessPieces\RookW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\RookB.png")

        self.legalMoves = []
        self.player = player

class Knight():
    def __init__(self, player):
        if player=="White":
            self.image = QtGui.QPixmap("ChessPieces\KnightW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\KnightB.png")
        
        self.legalMoves = []
        self.player = player

class Bishop():
    def __init__(self, player):
        if player=="White":
            self.image = QtGui.QPixmap("ChessPieces\BishopW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\BishopB.png")

        self.legalMoves = []
        self.player = player

class Queen():
    def __init__(self, player):
        if player=="White":
            self.image = QtGui.QPixmap("ChessPieces\QueenW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\QueenB.png")

        self.legalMoves = []
        self.player = player
    
class King():
    def __init__(self, player):
        if player=="White":
            self.image = QtGui.QPixmap("ChessPieces\KingW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\KingB.png")

        self.legalMoves = []
        self.player = player