__author__ = "Andrew Rechnitzer"
__copyright__ = "Copyright (C) 2018-2020 Andrew Rechnitzer"
__credits__ = ["Andrew Rechnitzer"]
__license__ = "AGPLv3"

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QBrush, QIcon, QPixmap, QResizeEvent, QTransform, QPalette
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QGridLayout,
    QListView,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QToolButton,
)
from .uiFiles.ui_test_view import Ui_TestView
from .examviewwindow import ExamViewWindow
from .useful_classes import SimpleMessage


class SourceList(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setViewMode(QListWidget.IconMode)
        self.setAcceptDrops(False)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setFlow(QListView.LeftToRight)
        self.setIconSize(QSize(128, 128))
        self.setSpacing(16)
        self.setWrapping(False)
        self.itemDoubleClicked.connect(self.viewImage)
        self.originalItems = {}
        self.potentialItems = {}

    def addOriginalItem(self, p, pfile):
        name = str(p)
        self.addItem(QListWidgetItem(QIcon(pfile), name))
        self.originalItems[name] = pfile

    def addPotentialItem(self, p, pfile):
        name = str(p)
        self.potentialItems[name] = pfile

    def removeItem(self):
        cr = self.currentRow()
        ci = self.takeItem(cr)
        if ci is None:
            return None
        self.setCurrentItem(None)
        return ci.text()

    def returnItem(self, name):
        if name in self.originalItems:
            self.addItem(QListWidgetItem(QIcon(self.originalItems[name]), name))
        elif name in self.potentialItems:
            it = QListWidgetItem(QIcon(self.potentialItems[name]), name)
            it.setBackground(QBrush(Qt.darkGreen))
            self.addItem(it)
        else:
            return
        self.sortItems()

    def viewImage(self, qi):
        self.parent.viewImage(self.originalItems[qi.text()])


class SinkList(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setViewMode(QListWidget.IconMode)
        self.setFlow(QListView.LeftToRight)
        self.setAcceptDrops(False)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setFlow(QListView.LeftToRight)
        # self.setResizeMode(QListView.Adjust)
        self.setIconSize(QSize(128, 128))
        self.setSpacing(16)
        self.setWrapping(False)
        self.originalItems = {}
        self.potentialItems = {}
        self.itemDoubleClicked.connect(self.viewImage)

    def addOriginalItem(self, p, pfile):
        name = str(p)
        it = QListWidgetItem(QIcon(pfile), name)
        it.setBackground(QBrush(Qt.green))
        self.addItem(it)
        self.originalItems[name] = pfile

    def addPotentialItem(self, p, pfile):
        name = str(p)
        self.potentialItems[name] = pfile

    def removeItem(self):
        cr = self.currentRow()
        ci = self.currentItem()
        if ci is None:
            return None
        elif self.count() == 1:  # cannot remove all pages
            return None
        # elif ci.text() in self.originalItems:
        # return None
        else:
            ci = self.takeItem(cr)
            self.setCurrentItem(None)
            return ci.text()

    def appendItem(self, name):
        if name is None:
            return
        if name in self.potentialItems:
            ci = QListWidgetItem(QIcon(self.potentialItems[name]), name)
        else:
            ci = QListWidgetItem(QIcon(self.originalItems[name]), name)
            ci.setBackground(QBrush(Qt.darkGreen))
        self.addItem(ci)
        self.setCurrentItem(ci)

    def shuffleLeft(self):
        cr = self.currentRow()
        if cr in [-1, 0]:
            return
        ci = self.takeItem(cr)
        self.insertItem(cr - 1, ci)
        self.setCurrentRow(cr - 1)

    def shuffleRight(self):
        cr = self.currentRow()
        if cr in [-1, self.count() - 1]:
            return
        ci = self.takeItem(cr)
        self.insertItem(cr + 1, ci)
        self.setCurrentRow(cr + 1)

    def reverseOrder(self):
        rc = self.count()
        for n in range(rc // 2):
            # swap item[n] with item [rc-n-1]
            ri = self.takeItem(rc - n - 1)
            li = self.takeItem(n)
            self.insertItem(n, ri)
            self.insertItem(rc - n - 1, li)

    def rotateImage(self, angle=90):
        ci = self.currentItem()
        name = ci.text()
        rot = QTransform()
        rot.rotate(angle)

        if name in self.potentialItems:
            rname = self.potentialItems[name]
        else:
            rname = self.originalItems[name]

        cpix = QPixmap(rname)
        npix = cpix.transformed(rot)
        npix.save(rname, format="PNG")

        ci.setIcon(QIcon(rname))

    def viewImage(self, qi):
        if qi.text() in self.originalItems:
            self.parent.viewImage(self.originalItems[qi.text()])
        else:
            self.parent.viewImage(self.potentialItems[qi.text()])

    def getNameList(self):
        nList = []
        for r in range(self.count()):
            nList.append(self.item(r).text())
        return nList


class RearrangementViewer(QDialog):
    def __init__(self, parent, testNumber, pageData, pageFiles):
        super().__init__()
        self.parent = parent
        self.testNumber = testNumber
        self.numberOfPages = len(pageFiles)

        self.setupUI()
        self.pageData = pageData
        self.pageFiles = pageFiles
        self.nameToIrefNFile = {}
        # note pagedata  triples [name, image-ref, true/false]
        self.populateList()

    def setupUI(self):

        self.scrollA = QScrollArea()
        self.listA = SourceList(self)
        self.scrollA.setWidget(self.listA)
        self.scrollA.setWidgetResizable(True)
        self.scrollB = QScrollArea()
        self.listB = SinkList(self)
        self.scrollB.setWidget(self.listB)
        self.scrollB.setWidgetResizable(True)

        self.appendB = QToolButton()
        self.appendB.setArrowType(Qt.DownArrow)
        self.appendB.setText("Add Page")
        self.appendB.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.removeB = QToolButton()
        self.removeB.setArrowType(Qt.UpArrow)
        self.removeB.setText("Remove Page")
        self.removeB.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.sLeftB = QToolButton()
        self.sLeftB.setArrowType(Qt.LeftArrow)
        self.sLeftB.setText("Shift Left")
        self.sLeftB.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.sRightB = QToolButton()
        self.sRightB.setArrowType(Qt.RightArrow)
        self.sRightB.setText("Shift Right")
        self.sRightB.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.reverseB = QPushButton("Reverse Order")
        self.rotateB = QPushButton("Rotate Page (local copy only)")

        self.closeB = QPushButton("Close")
        self.acceptB = QPushButton("Accept new layout")

        self.permute = [False]

        hb1 = QHBoxLayout()
        hb1.addWidget(self.appendB)
        hb1.addWidget(self.removeB)
        hb2 = QHBoxLayout()
        hb2.addWidget(self.sLeftB)
        hb2.addWidget(self.sRightB)

        hb3 = QHBoxLayout()
        hb3.addWidget(self.rotateB)
        hb3.addWidget(self.reverseB)
        hb3.addWidget(self.acceptB)
        hb3.addWidget(self.closeB)

        allPages = QLabel("All Pages in Exam")
        allPages.setAlignment(Qt.AlignCenter)
        thisQuestion = QLabel("Pages for this Question")
        thisQuestion.setAlignment(Qt.AlignCenter)

        vb0 = QVBoxLayout()
        vb0.addWidget(allPages)
        vb0.addWidget(self.scrollA)
        vb0.addLayout(hb1)
        vb0.addWidget(thisQuestion)
        vb0.addWidget(self.scrollB)
        vb0.addLayout(hb2)
        vb0.addLayout(hb3)

        self.setLayout(vb0)
        self.resize(QSize(self.parent.width() / 2, self.parent.height() * 2 / 3))

        self.closeB.clicked.connect(self.close)
        self.sLeftB.clicked.connect(self.shuffleLeft)
        self.sRightB.clicked.connect(self.shuffleRight)
        self.reverseB.clicked.connect(self.reverseOrder)
        self.rotateB.clicked.connect(self.rotateImage)
        self.sRightB.clicked.connect(self.shuffleRight)
        self.appendB.clicked.connect(self.sourceToSink)
        self.removeB.clicked.connect(self.sinkToSource)
        self.acceptB.clicked.connect(self.doShuffle)

    def populateList(self):
        for k in range(len(self.pageData)):
            self.nameToIrefNFile[self.pageData[k][0]] = [
                self.pageData[k][1],
                self.pageFiles[k],
            ]
            if self.pageData[k][2]:  # is a question page
                self.listA.addPotentialItem(self.pageData[k][0], self.pageFiles[k])
                self.listB.addOriginalItem(self.pageData[k][0], self.pageFiles[k])
            else:
                self.listA.addOriginalItem(self.pageData[k][0], self.pageFiles[k])
                self.listB.addPotentialItem(self.pageData[k][0], self.pageFiles[k])

    def sourceToSink(self):
        self.listB.appendItem(self.listA.removeItem())

    def sinkToSource(self):
        self.listA.returnItem(self.listB.removeItem())

    def shuffleLeft(self):
        self.listB.shuffleLeft()

    def shuffleRight(self):
        self.listB.shuffleRight()

    def reverseOrder(self):
        self.listB.reverseOrder()

    def rotateImage(self):
        self.listB.rotateImage()

    def viewImage(self, fname):
        page = ShowExamPage(self, fname)

    def doShuffle(self):
        msg = SimpleMessage(
            "Are you sure you want to shuffle pages. This will erase all your annotations and relaunch the annotator."
        )
        if msg.exec() == QMessageBox.No:
            return

        self.permute = []
        for n in self.listB.getNameList():
            self.permute.append(self.nameToIrefNFile[n])
            # return pairs of [iref, file]
        print(self.permute)
        self.accept()


class ShowExamPage(QDialog):
    def __init__(self, parent, fname):
        super(ShowExamPage, self).__init__()
        self.setParent(parent)
        self.setWindowFlags(Qt.Dialog)
        grid = QGridLayout()
        self.testImg = ExamViewWindow(fname)
        self.closeButton = QPushButton("&Close")
        grid.addWidget(self.testImg, 1, 1, 6, 6)
        grid.addWidget(self.closeButton, 7, 7)
        self.setLayout(grid)
        self.closeButton.clicked.connect(self.closeWindow)

        self.show()

    def closeEvent(self, event):
        self.closeWindow()

    def closeWindow(self):
        self.close()


class OriginalScansViewer(QWidget):
    def __init__(self, parent, testNumber, pageData, pages):
        super().__init__()
        self.parent = parent
        self.testNumber = testNumber
        self.numberOfPages = len(pages)
        self.pageList = pages
        # note pagedata  triples [name, image-ref, true/false]
        self.pageNames = [x[0] for x in pageData]
        self.ui = Ui_TestView()
        self.ui.setupUi(self)
        self.connectButtons()
        self.tabs = {}
        self.buildTabs()
        self.setWindowTitle("Original scans of test {}".format(self.testNumber))
        self.show()

    def connectButtons(self):
        self.ui.prevGroupButton.clicked.connect(self.previousTab)
        self.ui.nextGroupButton.clicked.connect(self.nextTab)
        self.ui.closeButton.clicked.connect(self.closeWindow)
        self.ui.maxNormButton.clicked.connect(self.swapMaxNorm)

    def buildTabs(self):
        for k in range(0, self.numberOfPages):
            self.tabs[k] = ExamViewWindow(self.pageList[k])
            self.ui.groupViewTabWidget.addTab(
                self.tabs[k], "Page {}".format(self.pageNames[k])
            )

    def nextTab(self):
        t = self.ui.groupViewTabWidget.currentIndex() + 1
        if t >= self.ui.groupViewTabWidget.count():
            t = 0
        self.ui.groupViewTabWidget.setCurrentIndex(t)

    def previousTab(self):
        t = self.ui.groupViewTabWidget.currentIndex() - 1
        if t < 0:
            t = self.ui.groupViewTabWidget.count() - 1
        self.ui.groupViewTabWidget.setCurrentIndex(t)

    def swapMaxNorm(self):
        """Toggles the window size between max and normal"""
        if self.windowState() != Qt.WindowMaximized:
            self.setWindowState(Qt.WindowMaximized)
        else:
            self.setWindowState(Qt.WindowNoState)

    def closeEvent(self, event):
        self.closeWindow()

    def closeWindow(self):
        self.close()


class GroupView(QDialog):
    def __init__(self, fnames):
        super(GroupView, self).__init__()
        grid = QGridLayout()
        self.testImg = ExamViewWindow(fnames)
        self.closeButton = QPushButton("&Close")
        self.maxNormButton = QPushButton("Max/Norm")
        grid.addWidget(self.testImg, 1, 1, 6, 6)
        grid.addWidget(self.closeButton, 7, 7)
        grid.addWidget(self.maxNormButton, 1, 7)
        self.setLayout(grid)
        self.closeButton.clicked.connect(self.closeWindow)
        self.maxNormButton.clicked.connect(self.swapMaxNorm)

        self.show()

    def swapMaxNorm(self):
        """Toggles the window size between max and normal"""
        if self.windowState() != Qt.WindowMaximized:
            self.setWindowState(Qt.WindowMaximized)
        else:
            self.setWindowState(Qt.WindowNoState)

    def closeEvent(self, event):
        self.closeWindow()

    def closeWindow(self):
        self.close()


class WholeTestView(QDialog):
    def __init__(self, fnames):
        super(WholeTestView, self).__init__()
        self.pageList = fnames
        self.numberOfPages = len(fnames)
        grid = QGridLayout()
        self.pageTabs = QTabWidget()
        self.tabs = {}
        self.closeButton = QPushButton("&Close")
        self.maxNormButton = QPushButton("&Max/Norm")
        self.pButton = QPushButton("&Previous")
        self.nButton = QPushButton("&Next")
        grid.addWidget(self.pageTabs, 1, 1, 6, 6)
        grid.addWidget(self.pButton, 7, 1)
        grid.addWidget(self.nButton, 7, 2)
        grid.addWidget(self.closeButton, 7, 7)
        grid.addWidget(self.maxNormButton, 1, 7)
        self.setLayout(grid)
        self.pButton.clicked.connect(self.previousTab)
        self.nButton.clicked.connect(self.nextTab)
        self.closeButton.clicked.connect(self.closeWindow)
        self.maxNormButton.clicked.connect(self.swapMaxNorm)

        self.setMinimumSize(500, 500)

        self.show()
        self.buildTabs()

    def swapMaxNorm(self):
        """Toggles the window size between max and normal"""
        if self.windowState() != Qt.WindowMaximized:
            self.setWindowState(Qt.WindowMaximized)
        else:
            self.setWindowState(Qt.WindowNoState)

    def closeEvent(self, event):
        self.closeWindow()

    def closeWindow(self):
        self.close()

    def nextTab(self):
        t = self.pageTabs.currentIndex() + 1
        if t >= self.pageTabs.count():
            t = 0
        self.pageTabs.setCurrentIndex(t)

    def previousTab(self):
        t = self.pageTabs.currentIndex() - 1
        if t < 0:
            t = self.pageTabs.count() - 1
        self.pageTabs.setCurrentIndex(t)

    def buildTabs(self):
        for k in range(0, self.numberOfPages):
            self.tabs[k] = ExamViewWindow(self.pageList[k])
            self.pageTabs.addTab(self.tabs[k], "{}".format(k + 1))


class SelectTestQuestion(QDialog):
    def __init__(self, info, gn=None):
        super(SelectTestQuestion, self).__init__()
        self.setModal(True)
        self.setWindowTitle("View another test")
        self.iL = QLabel("From which test do you wish to view the current question?")
        self.ab = QPushButton("&Accept")
        self.ab.clicked.connect(self.accept)
        self.cb = QPushButton("&Cancel")
        self.cb.clicked.connect(self.reject)

        fg = QFormLayout()
        self.tsb = QSpinBox()
        self.tsb.setRange(1, info["numberToProduce"])
        self.tsb.setValue(1)
        fg.addRow("Select test:", self.tsb)
        if gn is not None:
            self.gsb = QSpinBox()
            self.gsb.setRange(1, info["numberOfQuestions"])
            self.gsb.setValue(gn)
            fg.addRow("Select question:", self.gsb)
            self.iL.setText("Which test/group do you wish to view?")
        grid = QGridLayout()
        grid.addWidget(self.iL, 0, 1, 1, 3)
        grid.addLayout(fg, 1, 1, 3, 3)
        grid.addWidget(self.ab, 4, 1)
        grid.addWidget(self.cb, 4, 3)
        self.setLayout(grid)
