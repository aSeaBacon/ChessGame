import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("My App")

#         label = QLabel("Hello!")
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         self.setCentralWidget(label)

#         toolbar = QToolBar("My main toolbar")
#         toolbar.setIconSize(QSize(16, 16))
#         self.addToolBar(toolbar)

#         button_action = QAction(QIcon(QPixmap("ChessPiece\BishopB.png").scaled(16,16)), "&Your button", self)
#         button_action.setStatusTip("This is your button")
#         button_action.triggered.connect(self.onMyToolBarButtonClick)
#         button_action.setCheckable(True)
#         toolbar.addAction(button_action)

#         toolbar.addSeparator()

#         button_action2 = QAction(QIcon(QPixmap("ChessPiece\QueenB.png")), "Your &button2", self)
#         button_action2.setStatusTip("This is your button2")
#         button_action2.triggered.connect(self.onMyToolBarButtonClick)
#         button_action2.setCheckable(True)
#         toolbar.addAction(button_action2)

#         toolbar.addWidget(QLabel("Hello"))
#         toolbar.addWidget(QCheckBox())

#         self.setStatusBar(QStatusBar(self))

#         menu = self.menuBar()

#         file_menu = menu.addMenu("&File")
#         file_menu.addAction(button_action)
#         file_menu.addSeparator()
#         file_menu.addAction(button_action2)

#     def onMyToolBarButtonClick(self, s):
#         print("click", s)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon(QPixmap("ChessPieces\BishopB.png")), "&Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("bug.png"), "Your &button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)
        file_menu.addSeparator()
        file_menu.addAction(button_action2)

    def onMyToolBarButtonClick(self, s):
        print("click", s)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()