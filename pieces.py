from PyQt6 import QtGui

class Piece():

    legalMoves = []
    isPinned = False
    pinningPieces = []
    image = None
    pieceName = ""
    possibleMoves = []

    def __init__(self,player,chessBoard, coords):
        self.player = player
        self.coords = coords
        self.chessBoard = chessBoard
        self.getImage()

    def getPossibleMoves(self):
        pass

    def getLegalMoves(self):
        pass

    def createLine(self, loc1, loc2, incLoc1=False, incLoc2=False):

        #Generates points from starting position to ending position in order
        #i.e a:(1,0) b:(4,0)
        #    a->b = [(2,0), (3,0)]
        #    b->a = [(3,0), (2,0)]

        #(x1,y1), (x2, y2)
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
            
class Pawn(Piece):

    # legalMoves = [(4,5), (5,5)]
    hasMoved = False
    pieceName = "Pawn"

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\PawnW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\PawnB.png")

    def getPossibleMoves(self):

        self.possibleMoves = []
        i = self.coords[0]
        j = self.coords[1]

        #Pawn Moves:
        #    4#
        # 3# 2# 1#
        #   pawn
        if self.player=="White":
            #1
            if (j+1) < 8 and self.chessBoard.squares[i-1][j+1].piece != None and self.chessBoard.squares[i-1][j+1].piece.player != self.player:
                self.possibleMoves.append((i-1, j+1))
            #2
            if self.chessBoard.squares[i-1][j].piece == None:
                self.possibleMoves.append((i-1, j))
            #3
            if (j-1) >= 0 and self.chessBoard.squares[i-1][j-1].piece != None and self.chessBoard.squares[i-1][j-1].piece.player != self.player:
                self.possibleMoves.append((i-1, j-1))
            #4
            if not self.hasMoved and self.chessBoard.squares[i-2][j].piece == None and self.chessBoard.squares[i-1][j].piece == None:
                self.possibleMoves.append((i-2, j))

        elif self.player=="Black":
            #1
            if (j+1) < 8 and self.chessBoard.squares[i+1][j+1].piece != None and self.chessBoard.squares[i+1][j+1].piece.player != self.player:
                self.possibleMoves.append((i+1, j+1))
            #2
            if self.chessBoard.squares[i+1][j].piece == None:
                self.possibleMoves.append((i+1, j))
            #3
            if (j-1) >= 0 and self.chessBoard.squares[i+1][j-1].piece != None and self.chessBoard.squares[i+1][j-1].piece.player != self.player:
                self.possibleMoves.append((i+1, j-1))
            #4
            if not self.hasMoved and self.chessBoard.squares[i+2][j].piece == None and self.chessBoard.squares[i+1][j].piece == None:
                self.possibleMoves.append((i+2, j))

    def getLegalMoves(self):

        self.legalMoves = []
        tempMoves = self.possibleMoves[:]

        if self.chessBoard.isKingChecked:
            for piece in self.chessBoard.checkingPieces:
                if piece.pieceName == "Knight":
                    for move in tempMoves:
                        if move != piece.coords:
                            tempMoves.remove(move)
                else:
                    blockingSquares = self.createLine(self.chessBoard.checkedKing.coords, piece.coords, incLoc2=True)
                    for move in tempMoves:
                        if move not in blockingSquares:
                            tempMoves.remove(move)
        
        if self.isPinned:
            for piece in self.pinningPieces:
                blockingSquares = self.createLine(self.coords, piece.coords, inclLoc2 = True)
                for move in tempMoves:
                    if move not in blockingSquares:
                        tempMoves.remove(move)
        
        self.legalMoves = tempMoves[:]

class Rook(Piece):
    
    hasMoved = False
    pieceName = "Rook"
    
    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\RookW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\RookB.png")

    def getPossibleMoves(self):
        self.possibleMoves = []

        #Upward Moves:
        for move in self.createLine(self.coords, (0, self.coords[1]), incLoc2=True):
            if self.chessBoard.squares[move[0]][move[1]].piece == None:
                self.possibleMoves.append(move)
            elif self.chessBoard.squares[move[0]][move[1]].piece.player != self.player:
                self.possibleMoves.append(move)
                break
            else:
                break
        
        #Right Moves:
        for move in self.createLine(self.coords, (self.coords[0], 7), incLoc2=True):
            if self.chessBoard.squares[move[0]][move[1]].piece == None:
                self.possibleMoves.append(move)
            elif self.chessBoard.squares[move[0]][move[1]].piece.player != self.player:
                self.possibleMoves.append(move)
                break
            else:
                break

        #Downward Moves:
        for move in self.createLine(self.coords, (7, self.coords[1]), incLoc2=True):
            if self.chessBoard.squares[move[0]][move[1]].piece == None:
                self.possibleMoves.append(move)
            elif self.chessBoard.squares[move[0]][move[1]].piece.player != self.player:
                self.possibleMoves.append(move)
                break
            else:
                break

        #Left Moves
        for move in self.createLine(self.coords, (self.coords[0], 0), incLoc2=True):
            if self.chessBoard.squares[move[0]][move[1]].piece == None:
                self.possibleMoves.append(move)
            elif self.chessBoard.squares[move[0]][move[1]].piece.player != self.player:
                self.possibleMoves.append(move)
                break
            else:
                break

    def getLegalMoves(self):
        self.legalMoves = self.possibleMoves[:]

        


class Bishop(Piece):

    pieceName = "Bishop"

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\BishopW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\BishopB.png")

class Knight(Piece):

    pieceName = "Knight"

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\KnightW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\KnightB.png")

class King(Piece):

    hasMoved = False
    pieceName = "King"

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\KingW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\KingB.png")

class Queen(Piece):

    pieceName = "Queen"

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\QueenW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\QueenB.png")

