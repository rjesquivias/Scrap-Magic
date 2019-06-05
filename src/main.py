import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
import Themes

class QueryManager():
    def __init__(self):
        self._q = "" # text that will be searched for
        self._restrict_sr = 1 # 1 will search only in the provided subreddit, 0 will search all of reddit
        self._limit = 100 # limit the search results
        self._sort = "relevance" # hot/new/comments/relevance/top
        self._time = "all"
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

    def sortByTime(self, time):
        self._time = time

    def setSubreddit(self, sr):
        self._subreddit = sr

    def run(self):
        # craft query string
        queryString = 'https://www.reddit.com/r/' + self._subreddit + '/search.json?q=' + self._q + '&restrict_sr=' \
                    + str(self._restrict_sr) + '&limit=' + str(self._limit) + '&sort=' + self._sort + '&t=' + self._time 
        jsonResult = requests.get(queryString, headers = {'User-agent': 'RJ pyScraper'}).json()
        resultList = jsonResult['data']['children']
        return resultList

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._widget = MainWidget(self)
        self.setCentralWidget(self._widget)

        self.themeDict = dict()
        self.advancedSearchDict = dict()
        self.advancedSearchTimeDict = dict()

        fileMenu = self.menuBar().addMenu('File')
        self.themeMenu = self.menuBar().addMenu('Themes')
        self.advancedSearchMenu = self.menuBar().addMenu('Advanced Search')

        saveButton = QAction('Save', self)
        saveButton.triggered.connect(self.saveResults)
        fileMenu.addAction(saveButton)

        toggleDefaultThemeButton = QAction('Default', self)
        self.themeDict[toggleDefaultThemeButton.text()] = self.defaultTheme
        toggleDefaultThemeButton.setCheckable(True)
        toggleDefaultThemeButton.triggered.connect(self.toggleTheme)
        self.themeMenu.addAction(toggleDefaultThemeButton)

        toggleDarkButton = QAction('Dark', self)
        self.themeDict[toggleDarkButton.text()] = self.darkTheme
        toggleDarkButton.setCheckable(True)
        toggleDarkButton.triggered.connect(self.toggleTheme)
        toggleDarkButton.trigger()
        self.themeMenu.addAction(toggleDarkButton)

        newSearchButton = QAction("New", self)
        self.advancedSearchDict[newSearchButton.text()] = True
        newSearchButton.setCheckable(True)
        newSearchButton.triggered.connect(self.toggleAdvancedSearchType)
        newSearchButton.trigger()
        newSearchButton.setChecked(True)
        self.advancedSearchMenu.addAction(newSearchButton)

        hotSearchButton = QAction("Hot", self)
        self.advancedSearchDict[hotSearchButton.text()] = False
        hotSearchButton.setCheckable(True)
        hotSearchButton.triggered.connect(self.toggleAdvancedSearchType)
        self.advancedSearchMenu.addAction(hotSearchButton)

        topSearchButton = QAction("Top", self)
        self.advancedSearchDict[topSearchButton.text()] = False
        topSearchButton.setCheckable(True)
        topSearchButton.triggered.connect(self.toggleAdvancedSearchType)
        self.advancedSearchMenu.addAction(topSearchButton)

        relevantSearchButton = QAction("Relevant", self)
        self.advancedSearchDict[relevantSearchButton.text()] = False
        relevantSearchButton.setCheckable(True)
        relevantSearchButton.triggered.connect(self.toggleAdvancedSearchType)
        self.advancedSearchMenu.addAction(relevantSearchButton)
        self.advancedSearchMenu.addSeparator()

        week = QAction("Week", self)
        self.advancedSearchTimeDict[week.text()] = False
        week.setCheckable(True)
        week.triggered.connect(self.toggleAdvancedSearchTimeType)
        self.advancedSearchMenu.addAction(week)

        month = QAction("Month", self)
        self.advancedSearchTimeDict[month.text()] = False
        month.setCheckable(True)
        month.triggered.connect(self.toggleAdvancedSearchTimeType)
        self.advancedSearchMenu.addAction(month)

        year = QAction("Year", self)
        self.advancedSearchTimeDict[year.text()] = False
        year.setCheckable(True)
        year.triggered.connect(self.toggleAdvancedSearchTimeType)
        self.advancedSearchMenu.addAction(year)

        allTime = QAction("All", self)
        self.advancedSearchTimeDict[allTime.text()] = True
        allTime.setCheckable(True)
        allTime.triggered.connect(self.toggleAdvancedSearchTimeType)
        allTime.trigger()
        self.advancedSearchMenu.addAction(allTime)

        self.resize(1000, 400)

    def toggleTheme(self, checked):
        action = self.sender()
        if checked:
            (self.themeDict[action.text()])()
            for item in self.themeMenu.actions():
                if item.text() != action.text():
                    item.setChecked(False)
        else:
            action.setChecked(True)

    def toggleAdvancedSearchType(self, checked):
        action = self.sender()
        if checked:
            for item in self.advancedSearchMenu.actions():
                if item.text() in self.advancedSearchDict and item.text() != action.text():
                    item.setChecked(False)
                    self.advancedSearchDict[item.text()] = False
                elif item.text() in self.advancedSearchDict and item.text() == action.text():
                    self._widget.QManager.sortBy(action.text().lower())
                    self.advancedSearchDict[item.text()] = True
        else:
            action.setChecked(True)

    def toggleAdvancedSearchTimeType(self, checked):
        action = self.sender()
        if checked:
            for item in self.advancedSearchMenu.actions():
                if item.text() in self.advancedSearchTimeDict and item.text() != action.text():
                    item.setChecked(False)
                    self.advancedSearchTimeDict[item.text()] = False
                elif item.text() in self.advancedSearchTimeDict and item.text() == action.text():
                    self._widget.QManager.sortByTime(action.text().lower())
                    self.advancedSearchTimeDict[item.text()] = True
        else:
            action.setChecked(True)

    # TODO
    def saveResults(self):
        println("need to do");

    def darkTheme(self):
        self._widget.toggleTheme()
        p = self.palette()
        p.setColor(self.backgroundRole(), Themes.DarkTheme.background_color())
        self.setPalette(p)

    def defaultTheme(self):
        self._widget.toggleTheme()
        p = self.palette()
        p.setColor(self.backgroundRole(), Themes.DefaultTheme.background_color())
        self.setPalette(p)


class MainWidget(QWidget):

    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
    
        self.QManager = QueryManager()
        self.initUI()

    def initUI(self):
        self.resultList = []
        self.isDark = False
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

    def toggleTheme(self):

        bgCol = Themes.DefaultTheme.background_color_style() if self.isDark else Themes.DarkTheme.background_color_style()
        txtCol = Themes.DefaultTheme.text_color_style() if self.isDark else Themes.DarkTheme.text_color_style()
        edCol = Themes.DefaultTheme.textbox_color_style() if self.isDark else Themes.DarkTheme.textbox_color_style()
        borderCol = "border: 1px solid transparent"

        self.keyWords.setStyleSheet(txtCol)
        self.subreddit.setStyleSheet(txtCol)
        self.results.setStyleSheet(txtCol)

        p = self.palette()
        if (self.isDark):
            p.setColor(self.backgroundRole(), Themes.DefaultTheme.background_color())
            self.keyWordsEdit.setStyleSheet(edCol + txtCol + borderCol)
            self.subredditEdit.setStyleSheet(edCol + txtCol + borderCol)
            self.resultsBrowser.setStyleSheet(edCol + txtCol + borderCol)
        else:
            p.setColor(self.backgroundRole(), Themes.DarkTheme.background_color())
            self.keyWordsEdit.setStyleSheet(edCol + txtCol + borderCol)
            self.subredditEdit.setStyleSheet(edCol + txtCol + borderCol)
            self.resultsBrowser.setStyleSheet(edCol + txtCol + borderCol)
        self.setPalette(p)

        self.isDark = not self.isDark
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
        keyWordString = ""
        for keyword in keywordList:
            keyWordString += keyword
            keyWordString += "%20"

        # remove last 3 characters
        keyWordString = keyWordString[:-3]

        self.QManager.setSearchParam(keyWordString)
        self.QManager.setSubreddit(subredditList[0])
        self.resultList = self.QManager.run()
        self.updateResultsBrowser()

    def updateResultsBrowser(self):
        # Inherits the character format of the previous block. Need to clear the color/hyperlink
        self.resultsBrowser.setCurrentCharFormat(QTextCharFormat())
        self.resultsBrowser.setText('')

        self.resultList.sort(key=lambda result: int(result['data']['score']), reverse=True)
        for result in self.resultList:
           self.resultsBrowser.append('Title: ' + str(result['data']['title']))
           self.resultsBrowser.append('Score: ' + str(result['data']['score']))
           self.resultsBrowser.append('Upvotes: ' + str(result['data']['ups']))
           self.resultsBrowser.append('DownVotes: ' + str(result['data']['downs']))
           if self.isDark:
               self.resultsBrowser.append(
                    'Link: ' + '<a href="https://www.reddit.com' + str(result['data']['permalink']) + '">' +
                    '<span style="color: #1F9EE9;">' + 'https://www.reddit.com' + str(result['data']['permalink']) + '</span></a>')
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

