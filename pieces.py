from PyQt6 import QtGui

class Piece():

    legalMoves = []
    isPinned = False
    pinningPieceLoc = ()
    image = None
    pieceName = None

    def __init__(self,player,chessBoard, coords):
        self.player = player
        self.coords = coords
        self.chessBoard = chessBoard
        self.getImage()

    def getLegalMoves(self):
        pass

class Pawn(Piece):

    # legalMoves = [(4,5), (5,5)]
    hasMoved = False
    pieceName = "Pawn"

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\PawnW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\PawnB.png")

    def getLegalMoves(self):

        self.legalMoves = []
        i = self.coords[0]
        j = self.coords[1]

        #Pawn Moves:
        #    4#
        # 3# 2# 1#
        if self.player=="White":
            #1
            if (j+1) < 8 and self.chessBoard.squares[i-1][j+1].piece != None and self.chessBoard.squares[i-1][j+1].piece.player != self.player:
                self.legalMoves.append((i-1, j+1))
            #2
            if self.chessBoard.squares[i-1][j].piece == None:
                self.legalMoves.append((i-1, j))
            #3
            if (j-1) >= 0 and self.chessBoard.squares[i-1][j-1].piece != None and self.chessBoard.squares[i-1][j-1].piece.player != self.player:
                self.legalMoves.append((i-1, j-1))
            #4
            if not self.hasMoved and self.chessBoard.squares[i-2][j].piece == None and self.chessBoard.squares[i-1][j].piece == None:
                self.legalMoves.append((i-2, j))

        elif self.player=="Black":
            #1
            if (j+1) < 8 and self.chessBoard.squares[i+1][j+1].piece != None and self.chessBoard.squares[i+1][j+1].piece.player != self.player:
                self.legalMoves.append((i+1, j+1))
            #2
            if self.chessBoard.squares[i+1][j].piece == None:
                self.legalMoves.append((i+1, j))
            #3
            if (j-1) >= 0 and self.chessBoard.squares[i+1][j-1].piece != None and self.chessBoard.squares[i+1][j-1].piece.player != self.player:
                self.legalMoves.append((i+1, j-1))
            #4
            if not self.hasMoved and self.chessBoard.squares[i+2][j].piece == None and self.chessBoard.squares[i+1][j].piece == None:
                self.legalMoves.append((i+2, j))
                    


        

class Rook(Piece):
    
    hasMoved = False
    
    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\RookW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\RookB.png")

class Bishop(Piece):

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\BishopW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\BishopB.png")

class Knight(Piece):

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\KnightW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\KnightB.png")

class King(Piece):

    hasMoved = False

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\KingW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\KingB.png")

class Queen(Piece):

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\QueenW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\QueenB.png")

