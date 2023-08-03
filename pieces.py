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
        row = self.coords[0]
        col = self.coords[1]

        if self.player=="White":
            #Forward moves
            if self.chessBoard.squares[row - 1][col].piece == None:
                self.possibleMoves.append((row-1, col))
            if not self.hasMoved and self.chessBoard.squares[row - 1][col].piece == None and self.chessBoard.squares[row - 2][col].piece == None:
                self.possibleMoves.append((row-2, col))
            #Left capture
            if col - 1 >= 0  and self.chessBoard.squares[row - 1][col-1].piece != None and self.chessBoard.squares[row - 1][col-1].piece.player != self.player:
                self.possibleMoves.append((row - 1, col - 1))
            #Right capture
            if col + 1 <= 7  and self.chessBoard.squares[row - 1][col+1].piece != None and self.chessBoard.squares[row - 1][col+1].piece.player != self.player:
                self.possibleMoves.append((row - 1, col + 1))

        elif self.player=="Black":
            #Forward moves
            if self.chessBoard.squares[row + 1][col].piece == None:
                self.possibleMoves.append((row + 1, col))
            if not self.hasMoved and self.chessBoard.squares[row + 1][col].piece == None and self.chessBoard.squares[row + 2][col].piece == None:
                self.possibleMoves.append((row + 2, col))
            #Left (from white's perspective) capture
            if col - 1 >= 0  and self.chessBoard.squares[row + 1][col-1].piece != None and self.chessBoard.squares[row + 1][col-1].piece.player != self.player:
                self.possibleMoves.append((row + 1, col - 1))
            #Right (from white's perspective) capture
            if col + 1 <= 7  and self.chessBoard.squares[row + 1][col+1].piece != None and self.chessBoard.squares[row + 1][col+1].piece.player != self.player:
                self.possibleMoves.append((row + 1, col + 1))

    def getLegalMoves(self):

        self.legalMoves = []
        tempMoves = self.possibleMoves[:]

        # if self.chessBoard.isKingChecked:
        #     for piece in self.chessBoard.checkingPieces:
        #         if piece.pieceName == "Knight":
        #             for move in tempMoves:
        #                 if move != piece.coords:
        #                     tempMoves.remove(move)
        #         else:
        #             blockingSquares = self.chessBoard.createLine(self.chessBoard.checkedKing.coords, piece.coords, incLoc2=True)
        #             for move in tempMoves:
        #                 if move not in blockingSquares:
        #                     tempMoves.remove(move)
        
        # if self.isPinned:
        #     for piece in self.pinningPieces:
        #         blockingSquares = self.chessBoard.createLine(self.coords, piece.coords, inclLoc2 = True)
        #         for move in tempMoves:
        #             if move not in blockingSquares:
        #                 tempMoves.remove(move)
        
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

        #possibleMoves[0] -> North
        #possibleMoves[1] -> East
        #possibleMoves[2] -> South
        #possibleMoves[3] -> West

        row = self.coords[0]
        col = self.coords[1]

        #North:
        self.possibleMoves.append(self.chessBoard.createLine(self.coords, (0, col), incLoc2=True))
        
        #East:
        self.possibleMoves.append(self.chessBoard.createLine(self.coords, (row, 7), incLoc2=True))

        #South:
        self.possibleMoves.append(self.chessBoard.createLine(self.coords, (7, col), incLoc2=True))

        #West
        self.possibleMoves.append(self.chessBoard.createLine(self.coords, (row, 0), incLoc2=True))

    def getLegalMoves(self):

        self.legalMoves = []
        
        #Find piece collisions
        for directionalMoves in self.possibleMoves:
            temp = []
            for move in directionalMoves:
                if self.chessBoard.squares[move[0]][move[1]].piece == None:
                    temp.append(move)
                elif self.chessBoard.squares[move[0]][move[1]].piece.player != self.player:
                    temp.append(move)
                    break
                else:
                    break
            self.legalMoves = self.legalMoves + temp
        
            

class Bishop(Piece):

    pieceName = "Bishop"

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\BishopW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\BishopB.png")

    def getPossibleMoves(self):
        self.possibleMoves = []

        #possibleMoves[0] -> NE
        #possibleMoves[1] -> SE
        #possibleMoves[2] -> SW
        #possibleMoves[3] -> NW

        row = self.coords[0]
        col = self.coords[1]

        #NE direction
        if row + col < 7:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (0, row+col), incLoc2=True))
        elif row + col > 7:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (row+col-7,7), incLoc2=True))
        elif row + col == 7:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (0,7), incLoc2=True))
            
        #SE direction
        if row == col:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (7,7), incLoc2=True))
        elif row > col:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (7, col + 7-row), incLoc2=True))
        elif row < col:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (row + 7-col,7), incLoc2=True))

        #SW direction
        if row + col < 7:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (row+col,0), incLoc2=True))
        elif row + col > 7:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (7,col+row-7), incLoc2=True))
        elif row + col == 7:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (7,0), incLoc2=True))

        # #NW direction
        if row == col:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (0,0), incLoc2=True))
        elif row > col:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (row-col,0), incLoc2=True))
        elif row < col:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (0,col-row), incLoc2=True))

    def getLegalMoves(self):
        self.legalMoves = []

        #Find piece collisions
        for directionalMoves in self.possibleMoves:
            temp = []
            for move in directionalMoves:
                if self.chessBoard.squares[move[0]][move[1]].piece == None:
                    temp.append(move)
                elif self.chessBoard.squares[move[0]][move[1]].piece.player != self.player:
                    temp.append(move)
                    break
                else:
                    break
            self.legalMoves = self.legalMoves + temp

class Knight(Piece):

    pieceName = "Knight"

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\KnightW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\KnightB.png")

    def getPossibleMoves(self):
        self.possibleMoves = []
        row = self.coords[0]
        col = self.coords[1]


        #2N -> 1W/1E
        if row - 2 >= 0:
            if col - 1 >= 0:
                self.possibleMoves.append((row - 2, col - 1))
            if col + 1 <= 7:
                self.possibleMoves.append((row - 2, col + 1))

        #2E -> 1N/1S
        if col + 2 <= 7:
            if row - 1 >=0:
                self.possibleMoves.append((row - 1, col + 2))
            if row + 1 <= 7:
                self.possibleMoves.append((row + 1, col + 2))

        #2S -> 1E/1W
        if row + 2 <= 7:
            if col + 1 <= 7:
                self.possibleMoves.append((row + 2, col + 1))
            if col - 1 >= 0:
                self.possibleMoves.append((row + 2, col - 1))
            
        #2W -> 1S/1N
        if col - 2 >= 0:
            if row + 1 <= 7:
                self.possibleMoves.append((row + 1, col - 2))
            if row - 1 >= 0:
                self.possibleMoves.append((row - 1, col - 2))

        #Remove any squares containing friendly piece
        for move in self.possibleMoves[:]:
            if self.chessBoard.squares[move[0]][move[1]].piece != None and self.chessBoard.squares[move[0]][move[1]].piece.player == self.player:
                self.possibleMoves.remove(move)

    def getLegalMoves(self):
        self.legalMoves = self.possibleMoves[:]
        
class King(Piece):

    hasMoved = False
    isKingChecked = False
    canCastle = False
    pieceName = "King"
    checkingPieces = []

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\KingW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\KingB.png")

    def getPossibleMoves(self):
        self.possibleMoves = []

        row = self.coords[0]
        col = self.coords[1]

        #Generates move by 1 square in every direction (order is NW -> N -> NE -> W -> E -> SW -> S -> SE)
        self.possibleMoves = [(row + x,col + y) for x in range(-1,2) if (row + x) >=0 and (row + x) <=7 for y in range(-1, 2) if (col+y) >= 0 and (col+y) <= 7]
        self.possibleMoves.remove((row,col))

        #Remove any squares occupied by friendly pieces
        for move in self.possibleMoves[:]:
            if self.chessBoard.squares[move[0]][move[1]].piece != None and self.chessBoard.squares[move[0]][move[1]].piece.player == self.player:
                self.possibleMoves.remove(move)

        #To do: Check if able to castle
        
    def getLegalMoves(self):
        self.legalMoves = self.possibleMoves[:]

class Queen(Piece):

    pieceName = "Queen"

    def getImage(self):
        if self.player=="White":
            self.image = QtGui.QPixmap("ChessPieces\QueenW.png")
        else:
            self.image = QtGui.QPixmap("ChessPieces\QueenB.png")

    def getPossibleMoves(self):
        self.possibleMoves = []

        row = self.coords[0]
        col = self.coords[1]

        #possibleMoves[0] -> N
        #possibleMoves[1] -> NE
        #possibleMoves[2] -> E
        #possibleMoves[3] -> SE
        #possibleMoves[4] -> S
        #possibleMoves[5] -> SW
        #possibleMoves[6] -> W
        #possibleMoves[7] -> NW


        #North:
        self.possibleMoves.append(self.chessBoard.createLine(self.coords, (0, col), incLoc2=True))

        #NE direction
        if row + col < 7:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (0, row+col), incLoc2=True))
        elif row + col > 7:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (row+col-7,7), incLoc2=True))
        elif row + col == 7:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (0,7), incLoc2=True))

        #East:
        self.possibleMoves.append(self.chessBoard.createLine(self.coords, (row, 7), incLoc2=True))
            
        #SE direction
        if row == col:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (7,7), incLoc2=True))
        elif row > col:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (7, col + 7-row), incLoc2=True))
        elif row < col:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (row + 7-col,7), incLoc2=True))

        #South:
        self.possibleMoves.append(self.chessBoard.createLine(self.coords, (7, col), incLoc2=True))

        #SW direction
        if row + col < 7:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (row+col,0), incLoc2=True))
        elif row + col > 7:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (7,col+row-7), incLoc2=True))
        elif row + col == 7:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (7,0), incLoc2=True))

        #West
        self.possibleMoves.append(self.chessBoard.createLine(self.coords, (row, 0), incLoc2=True))

        # #NW direction
        if row == col:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (0,0), incLoc2=True))
        elif row > col:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (row-col,0), incLoc2=True))
        elif row < col:
            self.possibleMoves.append(self.chessBoard.createLine(self.coords, (0,col-row), incLoc2=True))


    def getLegalMoves(self):

        self.legalMoves = []

        #Find piece collisions
        for directionalMoves in self.possibleMoves:
            temp = []
            for move in directionalMoves:
                if self.chessBoard.squares[move[0]][move[1]].piece == None:
                    temp.append(move)
                elif self.chessBoard.squares[move[0]][move[1]].piece.player != self.player:
                    temp.append(move)
                    break
                else:
                    break
            self.legalMoves = self.legalMoves + temp

