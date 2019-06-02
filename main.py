import os
import sys
import json

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTabBar,
                             QFrame, QStackedLayout, QTabWidget)

from PyQt5.QtGui import QIcon, QWindow, QImage
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *


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

        # TODO: define 'About' Window

        self.tabbar = QTabBar(movable=True, tabsClosable=True)

        self.tabbar.setCurrentIndex(0)

        # Keep track of tabs
        self.tabCounter = 0
        self.tabs = []

        # Define Address Bar
        self.toolbar = QWidget()
        self.toolbarLayout = QHBoxLayout()
        self.addressBar = AddressBar()

        self.addressBar.returnPressed.connect(self.BrowseTo)

        self.toolbar.setLayout(self.toolbarLayout)
        self.toolbarLayout.addWidget(self.addressBar)

        #Add new tab
        self.addTabButton = QPushButton("+")

        self.toolbarLayout.addWidget(self.addTabButton)

        # Set main view
        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)

        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.container)

        self.setLayout(self.layout)

        # Connecting buttons to methods:
        self.tabbar.tabCloseRequested.connect(self.closeTab)
        self.addTabButton.clicked.connect(self.addTab)
        self.tabbar.tabBarClicked.connect(self.SwitchTab)

        self.addTab()

        self.show()

    def addTab(self):
        i = self.tabCounter

        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()
        self.tabs[i].setObjectName("tab" + str(i))

        # Open web view
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("http://www.google.com"))

        self.tabs[i].content.titleChanged.connect(lambda: self.setTabText(i))

        # Add web view to tabs layout
        self.tabs[i].layout.addWidget(self.tabs[i].content)

        # Set top level tab from [] to layout
        self.tabs[i].setLayout(self.tabs[i].layout)

        # Add tab to top level StackedWidget
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])

        self.tabbar.addTab("New Tab")
        self.tabbar.setTabData(i, {"object": "tab" + str(i), "initial": i})

        self.tabbar.setCurrentIndex(i)

        self.tabCounter += 1

    def SwitchTab(self, i):
        tab_data = self.tabbar.tabData(i)
        print("tab", tab_data)

        tab_content = self.findChild(QWidget, tab_data)
        print(tab_content)
        self.container.layout.setCurrentWidget(tab_content)

    def BrowseTo(self):
        address = self.addressBar.text()

        i = self.tabbar.currentIndex()
        tab = self.tabbar.tabData(i)["object"]
        wv = self.findChild(QWidget, tab).content

        if "http" not in address:
            if "." not in address:
                url = "https://www.google.com/search?q=" + address
            else:
                url = "http://" + address
        else:
            url = address

            # TODO: when url is clicked on page, get it and put to addressbar

        wv.load(QUrl.fromUserInput(url))

        self.addressBar.setText(url)

    def setTabText(self, i):
        tab_name = self.tabs[i].objectName()

        print(tab_name)

        count = 0
        running = True

        while running:
            tab_data_name = self.tabbar.tabData(count)

            if count >= 99:
                running = False

            if tab_name == tab_data_name["object"]:
                newTitle = self.findChild(QWidget, tab_name).content.title()
                self.tabbar.setTabText(count, newTitle)
                running = False
            else:
                count += 1

    def closeTab(self, i):
        self.tabbar.removeTab(i)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()

    sys.exit(app.exec_())