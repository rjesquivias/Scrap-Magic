import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests

col_white = "color: rgb(255, 255, 255);"
col_gray = "color: rgb(66, 67, 68);"
col_black = "color: rgb(0, 0, 0);"
background_gray = "background-color: rgb(66, 67, 68);"
background_white = "background-color: rgb(255, 255, 255);"

class QueryManager():
    def __init__(self):
        self._q = "" # text that will be searched for
        self._restrict_sr = 1 # 1 will search only in the provided subreddit, 0 will search all of reddit
        self._limit = 100 # limit the search results
        self._sort = "new" # hot/new/comments/relevance/top
        self._subreddit = ""

    def setSearchParam(self, query):
        self._q = query

    def restrictSubreddit(self):
        self._restrict_sr = 1

    def unrestrictSubreddit(self):
        self._restrict_sr = 0

    def setLimit(self, lim):
        self._limit = lim

    def sortBy(self, type):
        self._sort = type

    def setSubreddit(self, sr):
        self._subreddit = sr

    def run(self):
        # craft query string
        queryString = 'https://www.reddit.com/r/' + self._subreddit + '/search.json?q=' + self._q + '&restrict_sr=' \
                      + str(self._restrict_sr) + '&limit=' + str(self._limit) + '&sort=' + self._sort
        jsonResult = requests.get(queryString, headers = {'User-agent': 'RJ pyScraper'}).json()
        resultList = jsonResult['data']['children']
        return resultList

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._widget = MainWidget(self)
        self.setCentralWidget(self._widget)

        fileMenu = self.menuBar().addMenu('File')
        themeMenu = self.menuBar().addMenu('Themes')

        saveButton = QAction('Save', self)
        saveButton.triggered.connect(self.saveResults)
        fileMenu.addAction(saveButton)

        toggleDefaultThemeButton = QAction('Default', self)
        toggleDefaultThemeButton.triggered.connect(self.defaultTheme)
        themeMenu.addAction(toggleDefaultThemeButton)

        toggleNigerianButton = QAction('Nigerian', self)
        toggleNigerianButton.triggered.connect(self.darkTheme)
        themeMenu.addAction(toggleNigerianButton)

        self.resize(1000, 400)

    def darkTheme(self):
        if not self._widget.isNigerian:
            self._widget.toggleNigerianTheme()
            p = self.palette()
            p.setColor(self.backgroundRole(), Qt.black)
            self.setPalette(p)

    def defaultTheme(self):
        if self._widget.isNigerian:
            self._widget.toggleNigerianTheme()
            p = self.palette()
            p.setColor(self.backgroundRole(), Qt.white)
            self.setPalette(p)

    # TODO
    def saveResults(self):
        println("need to do");

class MainWidget(QWidget):

    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)

        self.QManager = QueryManager()
        self.initUI()

    def initUI(self):
        self.resultList = []
        self.isNigerian = False
        self.keyWords = QLabel('Key Words')
        self.subreddit = QLabel('Subreddit')
        self.results = QLabel('Results')

        self.keyWordsEdit = QLineEdit()
        self.subredditEdit = QLineEdit()
        self.resultsBrowser = QTextBrowser()
        self.resultsBrowser.setOpenExternalLinks(True)


        searchBtn = QPushButton('Search')
        searchBtn.clicked.connect(self.search)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.keyWords, 1, 0)
        grid.addWidget(self.keyWordsEdit, 1, 1)

        grid.addWidget(self.subreddit, 2, 0)
        grid.addWidget(self.subredditEdit, 2, 1)

        grid.addWidget(self.results, 3, 0)
        grid.addWidget(self.resultsBrowser, 3, 1)

        grid.addWidget(searchBtn, 4, 1)

        self.setLayout(grid)
        self.resize(500, 150)
        self.center()
        self.setWindowTitle('RScraper')
        self.setWindowIcon(QIcon(os.getcwd() + '\scraper.png'))

        self.show()

    def toggleNigerianTheme(self):

        bgCol = col_black if self.isNigerian else col_white
        txtCol = col_black if self.isNigerian else col_white
        edCol = col_white if self.isNigerian else col_gray

        self.keyWords.setStyleSheet(bgCol)
        self.subreddit.setStyleSheet(bgCol)
        self.results.setStyleSheet(bgCol)

        p = self.palette()
        if (self.isNigerian):
            p.setColor(self.backgroundRole(), Qt.white)
            self.keyWordsEdit.setStyleSheet(background_white + txtCol)
            self.subredditEdit.setStyleSheet(background_white + txtCol)
            self.resultsBrowser.setStyleSheet(background_white + txtCol)
        else:
            p.setColor(self.backgroundRole(), Qt.black)
            self.keyWordsEdit.setStyleSheet(background_gray + txtCol)
            self.subredditEdit.setStyleSheet(background_gray + txtCol)
            self.resultsBrowser.setStyleSheet(background_gray + txtCol)
        self.setPalette(p)

        self.isNigerian = not self.isNigerian
        self.updateResultsBrowser()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def search(self):
        # Get contents of keyWordsEdit
        keywordList = self.keyWordsEdit.text().split()
        # Get contents of subredditEdit
        subredditList = self.subredditEdit.text().split()

        if keywordList and subredditList: # Both lists must be non-empty
            self.queryReddit(keywordList, subredditList)

    def queryReddit(self, keywordList, subredditList):
        self.QManager.setSearchParam(keywordList[0])
        self.QManager.setSubreddit(subredditList[0])
        self.resultList = self.QManager.run()
        self.updateResultsBrowser()

    def updateResultsBrowser(self):
        self.resultsBrowser.setText("")
        for result in self.resultList:
           self.resultsBrowser.append('Title: ' + str(result['data']['title']))
           self.resultsBrowser.append('Score: ' + str(result['data']['score']))
           self.resultsBrowser.append('Upvotes: ' + str(result['data']['ups']))
           self.resultsBrowser.append('DownVotes: ' + str(result['data']['downs']))
           if self.isNigerian:
               self.resultsBrowser.append('Link: ' + '<a href="https://www.reddit.com' + str(result['data']['permalink']) + '">' +
                                          '<span style="color: red;">' + 'https://www.reddit.com' + str(result['data']['permalink']) + '</span></a>')
           else:
               self.resultsBrowser.append(
                   'Link: ' + '<a href="https://www.reddit.com' + str(result['data']['permalink']) + '">' +
                   '<span style="color: blue;">' + 'https://www.reddit.com' + str(result['data']['permalink']) + '</span></a>')
           self.resultsBrowser.append('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    scraperWindow = MainWindow()
    scraperWindow.show()
    sys.exit(app.exec_())

