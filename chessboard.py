from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QColor, QFont, QPalette
from itertools import cycle
from pieces import Pawn, Rook, Bishop, Knight, King, Queen, ghostPawn
from square import Square
from moves import DisplayBoard    

class ChessBoard(QWidget):

    highlightedSquare = None
    clickedSquare = None
    currentPlayer = "White"
    hasGhostPawn = False
    ghostPawnLoc = None
    checkMate = False
    staleMate = False
    boardStates = []
    pieceChoiceMenu = None
    promoted = False
    moveLimitCounter = 0
    test=None

    #kings[0] -> White king
    #kings[1] -> black king
    kings = [None, None]

    def __init__(self, moves, main):
        super().__init__()

        self.moves = moves
        self.main = main
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
                                self.kings[1] = King(player, self, (i,j))
                                self.layout.addWidget(Square(self, (i,j), color, self.kings[1]), i, j)

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
                                self.kings[0] = King(player, self, (i,j))
                                self.layout.addWidget(Square(self, (i,j), color, self.kings[0]), i, j)
                else:
                    self.layout.addWidget(Square(self, (i,j), color), i, j)

        tempString = ""
        for row in self.squares:
            for square in row:
                if square.piece != None:
                    tempString = tempString + square.piece.pieceName + " " + square.piece.player
                else:
                    tempString = tempString + "None None"

                if square.coords != (7,7):
                    tempString = tempString + " "

        self.boardStates.append(tempString)

        self.setLayout(self.layout)
        self.setFixedSize(QSize(600,600))


        #Add all Squares objects to 8x8 array (squares) to make future access easier
        for i in range(8):
            tmpList = []
            for j in range(8):
                tmpList.append(self.layout.itemAtPosition(i,j).widget())
            self.squares.append(tmpList)

        #Calculate whites starting moves
        for row in self.squares:
            for square in row:
                if square.piece != None and square.piece.player == "White":
                    square.piece.getPossibleMoves()
                    square.piece.getLegalMoves()

    def squareClicked(self):

        if self.clickedSquare.piece != None and not (self.checkMate or self.staleMate):
            print(self.clickedSquare.piece.pieceName,":",self.clickedSquare.coords)
        elif not (self.checkMate or self.staleMate):
            print(None,":", self.clickedSquare.coords)

        if self.pieceChoiceMenu != None:
            self.pieceChoiceMenu.hide()
            self.pieceChoiceMenu = None
            self.squareClicked()
            return


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

    def promotion(self, piece):

        self.setHints(self.highlightedSquare, False)
        self.promoted = True

        match piece:
            case "Queen":
                self.highlightedSquare.piece = Queen(self.currentPlayer, self, self.clickedSquare.coords)
            case "Rook":
                self.highlightedSquare.piece = Rook(self.currentPlayer, self, self.clickedSquare.coords)
                self.highlightedSquare.piece.hasMoved = True
            case "Bishop":
                self.highlightedSquare.piece = Bishop(self.currentPlayer, self, self.clickedSquare.coords)
            case "Knight":
                self.highlightedSquare.piece = Knight(self.currentPlayer, self, self.clickedSquare.coords)

        self.pieceChoiceMenu.hide()
        self.pieceChoiceMenu = None

        self.movePiece()

    def movePiece(self):

        #Used for determining notation
        startCoords = self.highlightedSquare.coords
        endCoords = self.clickedSquare.coords
        capture = True if self.clickedSquare.piece != None and self.clickedSquare.piece.player != self.currentPlayer else False
        piece = self.highlightedSquare.piece.pieceName
        shortCastle = False
        longCastle = False

        #Incrementing/resetting move counter for 50 move rule
        if self.promoted or self.highlightedSquare.piece.pieceName == "Pawn" or capture:
            self.moveLimitCounter = 0
        else:
            self.moveLimitCounter+=1

        # if self.highlightedSquare.piece.pieceName == "King" and self.highlightedSquare.piece.canCastle and self.clickedSquare.coords in [(7,6), (7,2), (0,6), (0,2)]:
        if self.highlightedSquare.piece.pieceName == "King" and ((self.highlightedSquare.piece.canCastleKS and self.clickedSquare.coords in [(7,6), (0,6)]) or (self.highlightedSquare.piece.canCastleQS and self.clickedSquare.coords in [(7,2), (0,2)])):
            match self.clickedSquare.coords:
                case (0,2):
                    longCastle = True
                    self.highlightedSquare.piece.hasMoved = True
                    self.squares[0][0].piece.hasMoved = True

                    #Move king
                    self.clickedSquare.piece = self.highlightedSquare.piece
                    self.clickedSquare.piece.coords = self.clickedSquare.coords
                    self.clickedSquare.updateSquare()
                    self.setHints(self.highlightedSquare, False)
                    self.highlightedSquare.piece = None
                    self.highlightedSquare.isHighlighted = False
                    self.highlightedSquare.updateSquare()
                    self.highlightedSquare = None

                    #Move Rook
                    self.squares[0][3].piece = self.squares[0][0].piece
                    self.squares[0][3].piece.coords = self.squares[0][3].coords
                    self.squares[0][3].updateSquare()
                    self.squares[0][0].piece = None
                    self.squares[0][0].updateSquare()

                case (0,6):
                    shortCastle = True
                    self.highlightedSquare.piece.hasMoved = True
                    self.squares[0][7].piece.hasMoved = True

                    #Move king
                    self.clickedSquare.piece = self.highlightedSquare.piece
                    self.clickedSquare.piece.coords = self.clickedSquare.coords
                    self.clickedSquare.updateSquare()
                    self.setHints(self.highlightedSquare, False)
                    self.highlightedSquare.piece = None
                    self.highlightedSquare.isHighlighted = False
                    self.highlightedSquare.updateSquare()
                    self.highlightedSquare = None

                    #Move Rook
                    self.squares[0][5].piece = self.squares[0][7].piece
                    self.squares[0][5].piece.coords = self.squares[0][5].coords
                    self.squares[0][5].updateSquare()
                    self.squares[0][7].piece = None
                    self.squares[0][7].updateSquare()
                case (7,2):
                    longCastle = True
                    self.highlightedSquare.piece.hasMoved = True
                    self.squares[7][0].piece.hasMoved = True

                    #Move king
                    self.clickedSquare.piece = self.highlightedSquare.piece
                    self.clickedSquare.piece.coords = self.clickedSquare.coords
                    self.clickedSquare.updateSquare()
                    self.setHints(self.highlightedSquare, False)
                    self.highlightedSquare.piece = None
                    self.highlightedSquare.isHighlighted = False
                    self.highlightedSquare.updateSquare()
                    self.highlightedSquare = None

                    #Move Rook
                    self.squares[7][3].piece = self.squares[7][0].piece
                    self.squares[7][3].piece.coords = self.squares[7][3].coords
                    self.squares[7][3].updateSquare()
                    self.squares[7][0].piece = None
                    self.squares[7][0].updateSquare()

                case (7,6):
                    shortCastle = True
                    self.highlightedSquare.piece.hasMoved = True
                    self.squares[7][7].piece.hasMoved = True

                    #Move king
                    self.clickedSquare.piece = self.highlightedSquare.piece
                    self.clickedSquare.piece.coords = self.clickedSquare.coords
                    self.clickedSquare.updateSquare()
                    self.setHints(self.highlightedSquare, False)
                    self.highlightedSquare.piece = None
                    self.highlightedSquare.isHighlighted = False
                    self.highlightedSquare.updateSquare()
                    self.highlightedSquare = None

                    #Move Rook
                    self.squares[7][5].piece = self.squares[7][7].piece
                    self.squares[7][5].piece.coords = self.squares[7][5].coords
                    self.squares[7][5].updateSquare()
                    self.squares[7][7].piece = None
                    self.squares[7][7].updateSquare()

            if self.hasGhostPawn and self.squares[self.ghostPawnLoc[0]][self.ghostPawnLoc[1]].piece != None and self.squares[self.ghostPawnLoc[0]][self.ghostPawnLoc[1]].piece.player != self.currentPlayer:
                self.squares[self.ghostPawnLoc[0]][self.ghostPawnLoc[1]].piece = None
                self.hasGhostPawn = False
                self.ghostPawnLoc = None

        #Pawn promotion

        elif self.highlightedSquare.piece.pieceName == "Pawn" and (self.clickedSquare.coords[0] == 0 or self.clickedSquare.coords[0] == 7):

            self.pieceChoiceMenu = PieceSelection(self, self.clickedSquare.coords, self.clickedSquare, self.main)
            self.pieceChoiceMenu.show()
            return
                
        else:

            if self.highlightedSquare.piece.pieceName in ["Pawn", "King", "Rook"]:
                #check for enabling en pessant
                if self.highlightedSquare.piece.pieceName == "Pawn" and self.highlightedSquare.piece.hasMoved == False and self.clickedSquare.piece == None:
                    if self.hasGhostPawn:
                        if self.squares[self.ghostPawnLoc[0]][self.ghostPawnLoc[1]].piece != None and self.squares[self.ghostPawnLoc[0]][self.ghostPawnLoc[1]].piece.pieceName == "ghostPawn":
                            self.squares[self.ghostPawnLoc[0]][self.ghostPawnLoc[1]].piece = None
                    if abs(self.highlightedSquare.coords[0] - self.clickedSquare.coords[0]) == 2:
                        self.hasGhostPawn = True
                        if self.currentPlayer == "White":
                            self.squares[5][self.highlightedSquare.coords[1]].piece = ghostPawn(self.currentPlayer, self,(5,self.highlightedSquare.coords[1]), self.highlightedSquare.piece)
                            self.ghostPawnLoc = (5, self.highlightedSquare.coords[1])
                        else:
                            self.squares[2][self.highlightedSquare.coords[1]].piece = ghostPawn(self.currentPlayer, self,(2,self.highlightedSquare.coords[1]), self.highlightedSquare.piece)
                            self.ghostPawnLoc = (2, self.highlightedSquare.coords[1])
                #check if executing en pessant
                elif self.highlightedSquare.piece.pieceName == "Pawn" and self.hasGhostPawn and self.clickedSquare.piece != None and self.clickedSquare.piece.pieceName == "ghostPawn":
                    tempPawn = self.squares[self.ghostPawnLoc[0]][self.ghostPawnLoc[1]].piece.pawn
                    tempCoords = tempPawn.coords
                    self.squares[tempCoords[0]][tempCoords[1]].piece = None
                    self.squares[tempCoords[0]][tempCoords[1]].updateSquare()
                    self.hasGhostPawn = False
                    self.ghostPawnLoc = None

                self.highlightedSquare.piece.hasMoved = True


            if self.hasGhostPawn and self.squares[self.ghostPawnLoc[0]][self.ghostPawnLoc[1]].piece != None and self.squares[self.ghostPawnLoc[0]][self.ghostPawnLoc[1]].piece.player != self.currentPlayer:
                if self.squares[self.ghostPawnLoc[0]][self.ghostPawnLoc[1]].piece.pieceName == "ghostPawn":
                    self.squares[self.ghostPawnLoc[0]][self.ghostPawnLoc[1]].piece = None
                self.hasGhostPawn = False
                self.ghostPawnLoc = None


            self.clickedSquare.piece = self.highlightedSquare.piece
            self.clickedSquare.piece.coords = self.clickedSquare.coords
            self.clickedSquare.updateSquare()
            self.setHints(self.highlightedSquare, False)
            self.highlightedSquare.piece = None
            self.highlightedSquare.isHighlighted = False
            self.highlightedSquare.updateSquare()
            self.highlightedSquare = None


        if self.currentPlayer == "White":
            for row in self.squares:
                for square in row:
                    if square.piece != None and square.piece.player =="White":
                        square.piece.getPossibleMoves()
                        square.piece.getSquaresAttacked()

            self.kings[1].getPossibleMoves()
            self.kings[1].getLegalMoves()
            self.kings[1].getChecks()
            self.currentPlayer = "Black"
        else:
            for row in self.squares:
                for square in row:
                    if square.piece != None and square.piece.player =="Black":
                        square.piece.getPossibleMoves()
                        square.piece.getSquaresAttacked()
            self.kings[0].getPossibleMoves()
            self.kings[0].getLegalMoves()
            self.kings[0].getChecks()
            self.currentPlayer = "White"

        #Create string to represent boardstate
        #"PieceName player PieceName player None None pieceName player ... pieceName player"
        tempString = ""
        for row in self.squares:
            for square in row:
                if square.piece != None:
                    tempString = tempString + square.piece.pieceName + " " + square.piece.player
                else:
                    tempString = tempString + "None None"

                if square.coords != (7,7):
                    tempString = tempString + " "
        
        drawByRep = False
        self.boardStates.append(tempString)
        if self.boardStates.count(tempString) == 3:
            drawByRep = True

        isCheckmate = True
        isStalemate = True

        for row in self.squares:
            for square in row:
                if square.piece != None and square.piece.player == self.currentPlayer and square.piece.pieceName != "King":
                    square.piece.getPossibleMoves()
                    square.piece.getLegalMoves()
                    if len(square.piece.legalMoves) > 0:
                        isCheckmate = False
                        isStalemate = False
        
        if (isCheckmate or isStalemate) and self.currentPlayer == "White" and len(self.kings[0].legalMoves) > 0:
            isCheckmate = False
            isStalemate = False

        if (isCheckmate or isStalemate) and self.currentPlayer == "Black" and len(self.kings[1].legalMoves) > 0:
            isCheckmate = False
            isStalemate = False

        if (isCheckmate or isStalemate):
            if self.currentPlayer == "White":
                if self.kings[0].isKingChecked:
                    self.checkMate = True
                    print("CHECKMATE")
                    print("Black wins!")
                    gameOver = GameOverMessage(self.main, self, "Checkmate\n Black Wins!")
                    gameOver.show()
                else:
                    self.staleMate = True
                    print("STALEMATE")
                    print("Game is a tie")
                    gameOver = GameOverMessage(self.main, self, "Stalemate\n Game is a draw.")
                    gameOver.show()
            else:
                if self.kings[1].isKingChecked:
                    self.checkMate = True
                    print("CHECKMATE")
                    print("White wins!")
                    gameOver = GameOverMessage(self.main, self, "Checkmate\n White Wins!")
                    gameOver.show()
                else:
                    self.staleMate = True
                    print("STALEMATE")
                    print("Game is a tie")
                    gameOver = GameOverMessage(self.main, self, "Stalemate\n Game is a draw.")
                    gameOver.show()

        if drawByRep:
            print("DRAW BY REPETITION")
            print("Game is a draw")
            gameOver = GameOverMessage(self.main, self, "Draw by Repetition\n Game is a draw.")
            gameOver.show()
            boardArray = tempString.split(" ")
            finalBoard = DisplayBoard(boardArray)
            self.moves.main.centralWidget().layout().itemAtPosition(0,0).widget().removeWidget(self)
            self.moves.main.centralWidget().layout().itemAtPosition(0,0).widget().insertWidget(0, finalBoard)
            self.moves.main.centralWidget().layout().itemAtPosition(0,0).widget().setCurrentWidget(finalBoard)

        if self.moveLimitCounter == 100:
            print("DRAW BY FIFTY-MOVE RULE")
            print("Game is a draw")
            gameOver = GameOverMessage(self.main, self, "Draw by Fifty-Move Rule\n Game is a draw.")
            gameOver.show()
            boardArray = tempString.split(" ")
            finalBoard = DisplayBoard(boardArray)
            self.moves.main.centralWidget().layout().itemAtPosition(0,0).widget().removeWidget(self)
            self.moves.main.centralWidget().layout().itemAtPosition(0,0).widget().insertWidget(0, finalBoard)
            self.moves.main.centralWidget().layout().itemAtPosition(0,0).widget().setCurrentWidget(finalBoard)

        #Draw by insufficient material
        if self.insufficientMaterial():
            print("Draw by insufficent material")
            print("Game is a draw")
            gameOver = GameOverMessage(self.main, self, "Draw by insufficent material\n Game is a draw")
            gameOver.show()
            boardArray = tempString.split(" ")
            finalBoard = DisplayBoard(boardArray)
            self.moves.main.centralWidget().layout().itemAtPosition(0,0).widget().removeWidget(self)
            self.moves.main.centralWidget().layout().itemAtPosition(0,0).widget().insertWidget(0, finalBoard)
            self.moves.main.centralWidget().layout().itemAtPosition(0,0).widget().setCurrentWidget(finalBoard)

        if self.currentPlayer == "White":
            self.moves.addMove("Black", startCoords, endCoords, capture, self.kings[0].isKingChecked, isCheckmate, shortCastle, longCastle, self.promoted, piece, self, tempString)
        else:
            self.moves.addMove("White", startCoords, endCoords, capture, self.kings[1].isKingChecked, isCheckmate, shortCastle, longCastle, self.promoted, piece, self, tempString)

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

    def insufficientMaterial(self):
        
        whiteKnights = 0
        whiteBishops = 0
        blackKnights = 0
        blackBishops = 0

        for row in self.squares:
            for square in row:
                if square.piece!=None:
                    match square.piece.pieceName:
                        case "Pawn" | "Queen" | "Rook":
                            return False
                        case "Bishop":
                            if square.piece.player == "White":
                                whiteBishops +=1
                            else:
                                blackBishops +=1
                        case "Knight":
                            if square.piece.player == "White":
                                whiteKnights +=1
                            else:
                                blackKnights +=1

        if (whiteBishops <= 1 or blackBishops <=1) and (whiteKnights == 0 and blackKnights == 0):
            return True
        if (whiteBishops == 0 and blackBishops == 0) and (whiteKnights <= 1 and blackKnights <= 1):
            return True
        if whiteKnights == 2 and whiteBishops == 0 and blackBishops == 0 and blackKnights == 0:
            return True
        if blackKnights == 2 and whiteBishops == 0 and blackBishops == 0 and whiteKnights == 0:
            return True
        
        return False

class PieceSelection(QWidget):

    close = pyqtSignal()
    
    def __init__(self, board, coords, square, main):
        super().__init__(main)
        layout = QVBoxLayout()
        self.board = board
        if coords[0] == 0:
            layout.addWidget(PieceIcon(QPixmap("ChessPieces\QueenW.png"), square, board, "Queen"))
            layout.addWidget(PieceIcon(QPixmap("ChessPieces\RookW.png"), square, board, "Rook"))
            layout.addWidget(PieceIcon(QPixmap("ChessPieces\BishopW.png"), square, board, "Bishop"))
            layout.addWidget(PieceIcon(QPixmap("ChessPieces\KnightW.png"), square, board, "Knight"))

        elif coords[0] == 7:
            layout.addWidget(PieceIcon(QPixmap("ChessPieces\QueenB.png"), square))
            layout.addWidget(PieceIcon(QPixmap("ChessPieces\RookB.png"), square))
            layout.addWidget(PieceIcon(QPixmap("ChessPieces\BishopB.png"), square))
            layout.addWidget(PieceIcon(QPixmap("ChessPieces\KnightB.png"), square))

        self.closeButton = QPushButton()
        self.closeButton.setAutoFillBackground(True)
        self.closeButton.setText("x")
        palette = self.closeButton.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(211,211,211))
        self.closeButton.setPalette(palette)
        font = QFont()
        font.setPixelSize(18)
        font.setBold(True)
        self.closeButton.setFont(font)
        self.closeButton.setFixedSize(square.width(),square.height()//2)
        self.closeButton.setContentsMargins(0,0,0,0)
        self.closeButton.clicked.connect(self.closeMenu)
        if coords[0] == 0:
            layout.addWidget(self.closeButton)
        elif coords[0] == 7:
            layout.insertWidget(0, self.closeButton)
        layout.setContentsMargins(0,0,0,0)

        self.setLayout(layout)
        self.setFixedSize(square.width(), square.height()*4 + square.height()//2)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255,255,255))
        self.setPalette(palette)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        if coords[0] == 0:
            self.move(square.pos())
        elif coords[0] == 7:
            self.move(board.squares[coords[0]-3][coords[1]].pos().x(), board.squares[coords[0]-3][coords[1]].pos().y() - square.height()//2)

    def closeMenu(self):
        self.hide()
        self.board.pieceChoiceMenu = None

class PieceIcon(QLabel):
    
    clicked = pyqtSignal()

    def __init__(self, image, square, board, piece):
        super().__init__()
        self.board = board
        self.piece = piece
        self.setFixedSize(square.size())
        self.setPixmap(image)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clicked.connect(self.pieceSeleceted)

    def mousePressEvent(self, event):
        self.clicked.emit()

    def pieceSeleceted(self):
        self.board.promotion(self.piece)

class GameOverMessage(QWidget):
    def __init__(self, main, board, message):
        super().__init__(main)

        font = QFont()
        font.setPixelSize(18)
        font.setBold(True)

        layout = QVBoxLayout()



        self.messageLabel = QLabel()
        self.messageLabel.setText(message)
        self.messageLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.messageLabel.setFont(font)

        self.closeButton = QPushButton("x")
        self.closeButton.setFont(font)
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setFixedSize(25,25)
        self.closeButton.setStyleSheet("border: none;")
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.closeButton)
        layout.addLayout(buttonLayout)
        layout.addWidget(self.messageLabel)
        layout.setContentsMargins(0,0,0,0)

        self.setLayout(layout)

        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(200, 200, 200, 255))
        self.setPalette(palette)
        self.setLayout(layout)
        self.setAutoFillBackground(True)
        self.setFixedSize(300, 100)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.move(board.width()//2 - self.width()//2, board.height()//2 - self.height()//2)

