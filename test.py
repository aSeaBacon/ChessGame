# import sys

# from PyQt6.QtCore import QSize, Qt
# from PyQt6.QtGui import QAction, QIcon, QPixmap
# from PyQt6.QtWidgets import (
#     QApplication,
#     QCheckBox,
#     QLabel,
#     QMainWindow,
#     QStatusBar,
#     QToolBar,
# )

# # class MainWindow(QMainWindow):
# #     def __init__(self):
# #         super().__init__()

# #         self.setWindowTitle("My App")

# #         label = QLabel("Hello!")
# #         label.setAlignment(Qt.AlignmentFlag.AlignCenter)

# #         self.setCentralWidget(label)

# #         toolbar = QToolBar("My main toolbar")
# #         toolbar.setIconSize(QSize(16, 16))
# #         self.addToolBar(toolbar)

# #         button_action = QAction(QIcon(QPixmap("ChessPiece\BishopB.png").scaled(16,16)), "&Your button", self)
# #         button_action.setStatusTip("This is your button")
# #         button_action.triggered.connect(self.onMyToolBarButtonClick)
# #         button_action.setCheckable(True)
# #         toolbar.addAction(button_action)

# #         toolbar.addSeparator()

# #         button_action2 = QAction(QIcon(QPixmap("ChessPiece\QueenB.png")), "Your &button2", self)
# #         button_action2.setStatusTip("This is your button2")
# #         button_action2.triggered.connect(self.onMyToolBarButtonClick)
# #         button_action2.setCheckable(True)
# #         toolbar.addAction(button_action2)

# #         toolbar.addWidget(QLabel("Hello"))
# #         toolbar.addWidget(QCheckBox())

# #         self.setStatusBar(QStatusBar(self))

# #         menu = self.menuBar()

# #         file_menu = menu.addMenu("&File")
# #         file_menu.addAction(button_action)
# #         file_menu.addSeparator()
# #         file_menu.addAction(button_action2)

# #     def onMyToolBarButtonClick(self, s):
# #         print("click", s)


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

#         button_action = QAction(QIcon(QPixmap("ChessPieces\BishopB.png")), "&Your button", self)
#         button_action.setStatusTip("This is your button")
#         button_action.triggered.connect(self.onMyToolBarButtonClick)
#         button_action.setCheckable(True)
#         toolbar.addAction(button_action)

#         toolbar.addSeparator()

#         button_action2 = QAction(QIcon("bug.png"), "Your &button2", self)
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


# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec()

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

class MessageWidget(QWidget):
    def __init__(self, message):
        super().__init__()

        self.setWindowTitle("Message Widget")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        self.close_button.setMaximumWidth(50)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)
        layout.addWidget(self.message_label)
        self.setLayout(layout)

        # self.layout().setAlignment(self.close_button, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    message = "Hello, this is a centered message!"
    widget = MessageWidget(message)
    widget.show()

    sys.exit(app.exec())