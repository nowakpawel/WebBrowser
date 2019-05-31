import os
import sys
import json

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTabBar,
                             QFrame, QStackedLayout, QTabWidget)

from PyQt5.QtGui import QIcon, QWindow, QImage
from PyQt5.QtCore import *


class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        self.selectAll()


class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Simple Web Browser")
        self.setBaseSize(1366, 768)
        self.createApp()

    def createApp(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.hlaouyt = QHBoxLayout()
        self.hlaouyt.addStretch(0)

        # create 'About/Close buttons
        self.aboutbutton = QPushButton("About")
        self.closebutton = QPushButton("Close")
        self.hlaouyt.addWidget(self.aboutbutton)
        self.hlaouyt.addWidget(self.closebutton)

        self.closebutton.clicked.connect(self.closeApp)
        # TODO: define 'About' Window
        # TODO: first create laouyt, than connect all buttons

        self.tabbar = QTabBar(movable=True, tabsClosable=True)
        self.tabbar.tabCloseRequested.connect(self.closeTab)

        self.tabbar.addTab("Tab 1")
        self.tabbar.addTab("Tab 2")

        self.tabbar.setCurrentIndex(0)

        # Define Address Bar
        self.toolbar = QWidget()
        self.toolbarLayout = QHBoxLayout()
        self.addressBar = AddressBar()

        self.toolbar.setLayout(self.toolbarLayout)
        self.toolbarLayout.addWidget(self.addressBar)

        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.toolbar)
        self.layout.addLayout(self.hlaouyt)

        self.setLayout(self.layout)

        self.show()

    def closeApp(self):
        QApplication.exit(0)

    def closeTab(self, i):
        self.tabbar.removeTab(i)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()

    sys.exit(app.exec_())