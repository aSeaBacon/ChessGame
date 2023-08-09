from PyQt6 import QtGui

class Piece():

    legalMoves = []
    isPinned = False
    pinningPieces = []
    image = None
    pieceName = ""
    possibleMoves = []
    checkingPieces = []
    attackedSquares = []

    def __init__(self,player,chessBoard, coords):
        self.player = player
        self.coords = coords
        self.chessBoard = chessBoard
        self.getImage()

    def getPossibleMoves(self):
        self.possibleMoves = []

    def getLegalMoves(self):
        self.legalMoves = []

    def getSquaresAttacked(self):
        self.attackedSquares = []

    def checkForPins(self):
        self.pinningPieces = []
        tempMoves = self.legalMoves[:]
        for row in self.chessBoard.squares:
            
            for square in row:

                if square.piece != None:

                    if square.piece.player != self.player and (square.piece.pieceName == "Bishop" or square.piece.pieceName == "Rook" or square.piece.pieceName == "Queen"):
                        square.piece.getPossibleMoves()
                        for direction in square.piece.possibleMoves:
                            if square.piece.player == "White" and self.chessBoard.kings[1].coords in direction:
                                lineOfAttack = self.chessBoard.createLine(square.piece.coords, self.chessBoard.kings[1].coords)
                                if self.coords in lineOfAttack:
                                    blockingPiecesCount = 0
                                    for coords in lineOfAttack:
                                        if self.chessBoard.squares[coords[0]][coords[1]].piece != None:
                                            blockingPiecesCount += 1
                                    if blockingPiecesCount == 1:
                                        self.pinningPieces.append(square.piece)
                                        break
                                
                            elif square.piece.player == "Black" and self.chessBoard.kings[0].coords in direction:
                                lineOfAttack = self.chessBoard.createLine(square.piece.coords, self.chessBoard.kings[0].coords)
                                if self.coords in lineOfAttack:
                                    blockingPiecesCount = 0
                                    for coords in lineOfAttack:
                                        if self.chessBoard.squares[coords[0]][coords[1]].piece != None:
                                            blockingPiecesCount += 1
                                    if blockingPiecesCount == 1:
                                        self.pinningPieces.append(square.piece)
                                        break

        for piece in self.pinningPieces:

            if self.player == "White":
                lineOfAttack = self.chessBoard.createLine(piece.coords, self.chessBoard.kings[0].coords, incLoc1=True)
            elif self.player == "Black":
                lineOfAttack = self.chessBoard.createLine(piece.coords, self.chessBoard.kings[1].coords, incLoc1=True)

            for move in self.legalMoves:
                if move not in lineOfAttack:
                    tempMoves.remove(move)

        return tempMoves

    def movesThatBlockCheck(self):

        if self.player == "White":
            if self.chessBoard.kings[0].isKingChecked:
                for piece in self.chessBoard.kings[0].checkingPieces:
                    if piece.pieceName == "Knight" or piece.pieceName == "Pawn":
                        for move in self.legalMoves[:]:
                            if move != piece.coords:
                                self.legalMoves.remove(move)
                    else:
                        lineOfAttack = self.chessBoard.createLine(piece.coords, self.chessBoard.kings[0].coords, incLoc1=True)
                        for move in self.legalMoves[:]:
                            if move not in lineOfAttack:
                                self.legalMoves.remove(move)


        elif self.player == "Black":
            if self.chessBoard.kings[1].isKingChecked:
                for piece in self.chessBoard.kings[1].checkingPieces:
                    if piece.pieceName == "Knight" or piece.pieceName == "Pawn":
                        for move in self.legalMoves[:]:
                            if move != piece.coords:
                                self.legalMoves.remove(move)
                    else:
                        lineOfAttack = self.chessBoard.createLine(piece.coords, self.chessBoard.kings[1].coords, incLoc1=True)
                        for move in self.legalMoves[:]:
                            if move not in lineOfAttack:
                                self.legalMoves.remove(move)
        
class ghostPawn(Piece):

    pieceName = "ghostPawn"
    
    def __init__(self, player,chessBoard, coords, pawn):
        self.player = player
        self.coords = coords
        self.chessBoard = chessBoard
        self.pawn = pawn
        self.getImage()

    def getImage(self):
        canvas = QtGui.QPixmap(self.chessBoard.squares[self.coords[0]][self.coords[1]].size())
        canvas.fill(QtGui.QColor(0,0,0,0))
        self.image = QtGui.QPixmap()

class Pawn(Piece):

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

        self.legalMoves = self.possibleMoves[:]

        #Check for pins
        self.legalMoves = self.checkForPins()

        #Check for moves that block checking pieces
        self.movesThatBlockCheck()

    def getSquaresAttacked(self):
        self.attackedSquares = []
        row = self.coords[0]
        col = self.coords[1]
        if self.player == "White":
            if col - 1 >= 0:
                self.attackedSquares.append((row-1, col-1))
            if col + 1 <= 7:
                self.attackedSquares.append((row-1, col+1))
        elif self.player == "Black":
            if col - 1 >= 0:
                self.attackedSquares.append((row+1, col-1))
            if col + 1 <=7:
                self.attackedSquares.append((row+1, col+1))
            
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
                if self.chessBoard.squares[move[0]][move[1]].piece == None or self.chessBoard.squares[move[0]][move[1]].piece.pieceName == "ghostPawn":
                    temp.append(move)
                elif self.chessBoard.squares[move[0]][move[1]].piece.player != self.player:
                    temp.append(move)
                    break
                else:
                    break
            self.legalMoves = self.legalMoves + temp

        #Check for pins
        self.legalMoves = self.checkForPins()

        #Check for moves to block checking pieces
        self.movesThatBlockCheck()

    def getSquaresAttacked(self):

        self.attackedSquares = []

        #Check for piece collisions
        for directionalMoves in self.possibleMoves:
            temp = []
            for move in directionalMoves:
                if self.chessBoard.squares[move[0]][move[1]].piece == None or self.chessBoard.squares[move[0]][move[1]].piece.pieceName == "ghostPawn" or self.chessBoard.squares[move[0]][move[1]].piece.pieceName == "King":
                    temp.append(move)
                elif self.chessBoard.squares[move[0]][move[1]].piece != None:
                    temp.append(move)
                    break
                else:
                    break
            self.attackedSquares = self.attackedSquares + temp

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
                if self.chessBoard.squares[move[0]][move[1]].piece == None or self.chessBoard.squares[move[0]][move[1]].piece.pieceName == "ghostPawn":
                    temp.append(move)
                elif self.chessBoard.squares[move[0]][move[1]].piece.player != self.player:
                    temp.append(move)
                    break
                else:
                    break
            self.legalMoves = self.legalMoves + temp

        #Check for Pins
        self.legalMoves = self.checkForPins()

        #check for moves that block checking pieces
        self.movesThatBlockCheck()

    def getSquaresAttacked(self):
        self.attackedSquares = []
        #Find piece collisions
        for directionalMoves in self.possibleMoves:
            temp = []
            for move in directionalMoves:
                if self.chessBoard.squares[move[0]][move[1]].piece == None or self.chessBoard.squares[move[0]][move[1]].piece.pieceName == "ghostPawn" or self.chessBoard.squares[move[0]][move[1]].piece.pieceName == "King":
                    temp.append(move)
                elif self.chessBoard.squares[move[0]][move[1]].piece != None:
                    temp.append(move)
                    break
                else:
                    break
            self.attackedSquares = self.attackedSquares + temp

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

    def getSquaresAttacked(self):
        self.attackedSquares = self.possibleMoves[:]

    def getLegalMoves(self):
        self.legalMoves = self.possibleMoves[:]

        #Check for pins
        self.legalMoves = self.checkForPins()

        #check for moves that block checking pieces
        self.movesThatBlockCheck()
      
class King(Piece):

    hasMoved = False
    isKingChecked = False
    canCastleKS = True
    canCastleQS = True
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

        #To do: Check if able to castle (possibly do in getLegalMoves to avoid conflict with getSquaresAttacked)
        #Possible issue, distinguish between legal/possible moves for pieces attacking a square
     
    def getLegalMoves(self):

        #No idea if this breaks after removing moves AFTER running canCastle
        self.legalMoves = []

        self.canCastle()

        tempMoves = self.possibleMoves[:]
        
        if self.canCastleKS:
            if self.player == "White":
                tempMoves.append((7,6))
            else:
                tempMoves.append((0,6))
        
        if self.canCastleQS:
            if self.player == "White":
               tempMoves.append((7,2))
            else:
                tempMoves.append((0,2))

        for row in self.chessBoard.squares:
            for square in row:
                if square.piece != None and square.piece.player != self.player:
                    square.piece.getSquaresAttacked()
                    for move in self.possibleMoves:
                        if move in square.piece.attackedSquares and move in tempMoves:
                            tempMoves.remove(move)

        self.legalMoves = tempMoves[:]

    def getSquaresAttacked(self):
        self.attackedSquares = self.possibleMoves[:]

    def getChecks(self):
        self.checkingPieces = []
        
        for row in self.chessBoard.squares:
            for square in row:
                if square.piece != None and square.piece.player != self.player:
                    square.piece.getSquaresAttacked()
                    if self.coords in square.piece.attackedSquares:
                        self.checkingPieces.append(square.piece)
        
        if len(self.checkingPieces) > 0:
            self.isKingChecked = True
        else:
            self.isKingChecked = False

    def canCastle(self):
        #Checks to see if castling is an option

        self.getChecks()

        self.canCastleKS = True
        self.canCastleQS = True

        if self.isKingChecked or self.hasMoved:
            self.canCastleKS = False
            self.canCastleQS = False
        
        else:
            if self.player == "White":
                #check king side castling
                kingRook = self.chessBoard.squares[7][7].piece
                if kingRook != None and kingRook.pieceName == "Rook" and kingRook.hasMoved == False and self.chessBoard.squares[7][6].piece == None and self.chessBoard.squares[7][5].piece == None:
                    #Check for pieces attacking squares in beween king and rook
                    for row in self.chessBoard.squares:
                        for square in row:
                            if square.piece != None and square.piece.player == "Black":
                                square.piece.getPossibleMoves()
                                square.piece.getSquaresAttacked()
                                if (7,6) in square.piece.attackedSquares or (7,5) in square.piece.attackedSquares:
                                    self.canCastleKS = False

                else:
                    self.canCastleKS = False

                #check quene side castling
                queenRook = self.chessBoard.squares[7][0].piece
                if queenRook != None and queenRook.pieceName == "Rook" and queenRook.hasMoved == False and self.chessBoard.squares[7][1].piece == None and self.chessBoard.squares[7][2].piece == None and self.chessBoard.squares[7][3].piece == None:
                    for row in self.chessBoard.squares:
                        for square in row:
                            if square.piece != None and square.piece.player == "Black":
                                square.piece.getPossibleMoves()
                                square.piece.getSquaresAttacked()
                                if (7,2) in square.piece.attackedSquares or (7,3) in square.piece.attackedSquares:
                                    self.CanCastleQS = False
                else:
                    self.canCastleQS = False
            
            elif self.player == "Black":
                #check king side castling
                kingRook = self.chessBoard.squares[0][7].piece
                if kingRook != None and kingRook.pieceName == "Rook" and kingRook.hasMoved == False and self.chessBoard.squares[0][6].piece == None and self.chessBoard.squares[0][5].piece == None:
                    #Check for pieces attacking squares in beween king and rook
                    for row in self.chessBoard.squares:
                        for square in row:
                            if square.piece != None and square.piece.player == "White":
                                square.piece.getPossibleMoves()
                                square.piece.getSquaresAttacked()
                                if (0,6) in square.piece.attackedSquares or (0,5) in square.piece.attackedSquares:
                                    self.CanCastleKS = False
                else:
                    self.canCastleKS = False
                #check quene side castling
                queenRook = self.chessBoard.squares[0][0].piece
                if queenRook != None and queenRook.pieceName == "Rook" and queenRook.hasMoved == False and self.chessBoard.squares[0][1].piece == None and self.chessBoard.squares[0][2].piece == None and self.chessBoard.squares[0][3].piece == None:
                    for row in self.chessBoard.squares:
                        for square in row:
                            if square.piece != None and square.piece.player == "White":
                                square.piece.getPossibleMoves()
                                square.piece.getSquaresAttacked()
                                if (0,2) in square.piece.attackedSquares or (0,3) in square.piece.attackedSquares:
                                    self.CanCastleQS = False
                else:
                    self.canCastleQS = False

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
                if self.chessBoard.squares[move[0]][move[1]].piece == None or self.chessBoard.squares[move[0]][move[1]].piece.pieceName == "ghostPawn":
                    temp.append(move)
                elif self.chessBoard.squares[move[0]][move[1]].piece.player != self.player:
                    temp.append(move)
                    break
                else:
                    break
            self.legalMoves = self.legalMoves + temp

        #Check for pins
        self.legalMoves = self.checkForPins()

        #check for moves that block checking pieces
        self.movesThatBlockCheck()

    def getSquaresAttacked(self):
        
        self.attackedSquares = []

        #Find piece collisions
        for directionalMoves in self.possibleMoves:
            temp = []
            for move in directionalMoves:
                if self.chessBoard.squares[move[0]][move[1]].piece == None or self.chessBoard.squares[move[0]][move[1]].piece.pieceName == "ghostPawn" or self.chessBoard.squares[move[0]][move[1]].piece.pieceName == "King":
                    temp.append(move)
                elif self.chessBoard.squares[move[0]][move[1]].piece != None:
                    temp.append(move)
                    break
                else:
                    break
            self.attackedSquares = self.attackedSquares + temp



