# ChessGame
Created Chess Game to learn PyQt6

Layout of application is:

MainWindow
  -ChessBoard
    -Squares
      -Pieces
  -MovesContainer
    -movesitem
  -DisplayBoard (Non interactable chessBoard)
    -DisplaySquare
  -PieceSelection (Stored with chessboard class, parent is set as main for display purposes)
    -PieceIcon
  -GameOverMessage (Stored with chessboard class, parent is set as main for display purposes)
