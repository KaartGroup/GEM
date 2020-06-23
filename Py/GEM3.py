#!/usr/bin/env python
import argparse
import json
import requests
import urllib
import httpbin
import string
import github
from github import Github
import os
import sys
import logging
import re
from enum import Enum, auto
import PyQt5
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QGridLayout,
    QWidget,
    QStatusBar,
    QMenuBar,
    QMenu,
    QApplication,
    QAction,
)
from PyQt5.QtWidgets import QPushButton, QMessageBox, QTabWidget
from PyQt5.QtCore import QSize
import time

##################################################
__author__ = "Chris Gousset"
__copyright__ = "N/A"
__credits__ = ["Louis Morales", "Zack LaVergne"]
__license__ = "N/A"
__version__ = "2.1pyi"
__maintainer__ = "Chris Gousset"
__email__ = "chris.gousset@kaart.com"
__status__ = "Development"

#########################################
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception as e:
        logger.exception(e)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#########################################

###########################################
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError as e:
    # TODO: We are detecting that QString doesn't exist?
    logger.exception(e)

    def _fromUtf8(s):
        return s


try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)


except AttributeError as e:
    # TODO: We are detecting that something doesn't exist?
    logger.exception(e)

    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


###############################################


class MapCSSParseExceptionType(Enum):
    UNKNOWN = auto()
    UNKNOWN_USER = auto()


class MapCSSParseException(Exception):
    """
    Thrown when there is an issue parsing the mapcss
    """

    def __init__(
        self,
        message: str,
        exception_type: MapCSSParseExceptionType = MapCSSParseExceptionType.UNKNOWN,
    ):
        self.exception_type = exception_type
        super().__init__(message)


class TABMOD(QAbstractTableModel):
    def __init__(
        self, GEMarray, headers=[], parent=None,
    ):
        QAbstractTableModel.__init__(self, parent)
        self.GEMarraydata = GEMarray
        self.headers = headers
        self.thumbSize = 64

    def resizePixmap(self, mult):
        self.thumbSize = self.thumbSize * mult
        self.reset()

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def rowCount(self, parent):
        return 50

    def columnCount(self, parent):
        return 4

    def data(self, index, role):
        row = index.row()
        column = index.column()
        value = self.GEMarraydata[row][column]
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            if column == 0:
                try:
                    value = self.GEMarraydata[row][column]
                    self.dataChanged.emit(index, index)
                    return str(value)
                except Exception as e:
                    logger.exception(e)
            if column == 1:
                try:
                    value = self.GEMarraydata[row][column]
                    self.dataChanged.emit(index, index)
                    return str(value)
                except Exception as e:
                    logger.exception(e)
        if role == QtCore.Qt.DecorationRole:
            row = index.row()
            column = index.column()

            if column == 2:
                pix = QtGui.QPixmap(25, 15)
                value = self.GEMarraydata[row][column]
                pix.fill(value)
                self.dataChanged.emit(index, index)
                icon = QtGui.QIcon(pix)

                return icon

            if column == 3:
                Sicon = self.GEMarraydata[row][column]
                self.dataChanged.emit(index, index)
                return Sicon

    def setData(self, index, value, role: int):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            if column == 0:
                try:
                    value = self.GEMarraydata[row][column]
                    self.dataChanged.emit(index, index)
                    return str(value)
                except Exception as e:
                    logger.exception(e)
            if column == 1:
                try:
                    value = self.GEMarraydata[row][column]
                    self.dataChanged.emit(index, index)
                    return str(value)
                except Exception as e:
                    logger.exception(e)
        if role == QtCore.Qt.DecorationRole:
            row = index.row()
            column = index.column()
            if column == 2:
                pix = QtGui.QPixmap(25, 15)
                value = self.GEMarraydata[row][column]
                pix.fill(value)

                self.dataChanged.emit(index, index)
                icon = QtGui.QIcon(pix)
                return icon
            if column == 3:
                Sicon = self.GEMarraydata[row][column]
                self.dataChanged.emit(index, index)
                return Sicon
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section < len(self.headers):
                    return self.headers[section]


#####################################################
Model = TABMOD

clear = QtGui.QColor(0, 0, 0, 0)
red = QtGui.QColor(255, 0, 0)


class EDITORINFO(object):
    def __init__(self):
        self.NAME = ""
        self.UID = ""
        self.USERNAME = ""
        self.TITLE = ""
        self.GITACCESS = False
        self.LINECOLORTEXT = ""
        self.NODECOLORTEXT = ""
        self.LINECOLORUI = ""
        self.NODECOLORUI = ""
        self.ICONSIZE = 10
        self.LINEWIDTH = 5
        self.ICONSHAPE = ""
        self.ICONSHAPELINK = ""


###############################################


class CONFIRMPOPUP(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setGeometry(900, 100, 300, 80)
        self.setWindowTitle("CONFIRMATION")
        self.POPHOME()

    def POPHOME(self):
        self.LABEL = QtWidgets.QLabel(self)
        self.LABEL.setText("Enter administrator password:")
        self.LABEL.resize(300, 20)
        self.LABEL.move(13, 5)

        self.PASSFIELD = QtWidgets.QLineEdit(self)
        self.PASSFIELD.setEchoMode(self.PASSFIELD.Password)
        self.PASSFIELD.resize(275, 20)
        self.PASSFIELD.move(12, 30)

        self.CONFIRM = QPushButton(self)
        self.CONFIRM.setText("CONFIRM")
        self.CONFIRM.resize(150, 25)
        self.CONFIRM.move(5, 50)
        self.CONFIRM.clicked.connect(self.CONFIRMED_clicked)

        self.CANCEL = QPushButton(self)
        self.CANCEL.setText("CANCEL")
        self.CANCEL.resize(150, 25)
        self.CANCEL.move(145, 50)
        self.CANCEL.clicked.connect(self.CANCEL_clicked)
        self.show()

    def CONFIRMED_clicked(self):
        TESTPASS = self.PASSFIELD.text()

        if TESTPASS == one.ADMINPASS:
            one.GITPUSH_GO()
        self.close()

    def CANCEL_clicked(self):
        self.close()


############################################
class MAINWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setGeometry(720, 300, 680, 500)
        self.setWindowTitle("GEM - GUI Editor for Mapcss")
        self.MWHOME(self)
        self.output_file_dir = os.path.expanduser("~/Documents")

    def MWHOME(self, MAINWindow):

        MAINWindow.setObjectName(_fromUtf8("MAINWindow"))
        self.ADMINPASS = "**********"
        self.repoGO = False
        self.GOREMOVEALL = False
        self.TEAMNAMETEXT = ""
        self.SETUPENTRYBLOCK = ""
        self.SETTINGBLOCK = ""
        self.NODEENTRYBLOCK = ""
        self.WAYENTRYBLOCK = ""
        self.MASTEROUTPUTBLOCK = ""
        self.WHITE = "#FFFFFF"
        self.EDITORNODECOLORUI = "#FFFFFF"
        self.TEAMLINECOLORTEXT = "#47D608"
        self.TEAMNODECOLORTEXT = "orange"
        self.TEAMLINECOLORUI = "#47D608"
        self.TEAMNODECOLORUI = "#ffaa00"
        self.LINEWIDTH = 5
        self.ICONSIZE = 10
        self.TEAMICONSHAPE = "Circle"
        self.FOLDER = os.getcwd()
        self.NRSELECT = ""
        self.GUMSELECT = ""
        self.GUMusercount = 0
        self.usercount = 0
        self.tempcount = 1
        self.TEMPUSERS = {}
        for j in range(100):
            self.TEMPUSERS[str(j)] = 0

        self.GUMTEMPUSERS = {}
        for j in range(100):
            self.GUMTEMPUSERS[str(j)] = 0
        self.ADDUSERS = []
        self.GUMADDUSERS = []
        self.filters = ""
        self.select_filters = "MAPCSS (*.mapcss)"
        self.directory = os.getcwd()
        self.SELTEXT = ""
        self.TEMPEDITORICONSHAPE = ""
        self.TEMPLINECOLORTEXT = ""
        self.TEMPNODECOLORTEXT = ""
        self.GOEDIT = False
        self.TABS = QTabWidget(self)
        self.TABS.resize(670, 460)
        self.TABS.move(5, 25)
        self.TAB1 = QWidget()
        self.TAB2 = QWidget()
        self.TABS.addTab(self.TAB1, "GEM")
        self.PULLUSER = ""
        # ###############################TABLE BUTTONS############################## #

        self.TABLE = QtWidgets.QTableView(self.TAB1)
        self.TABLE.resize(400, 330)
        self.TABLE.move(255, 30)
        self.TABLE.clicked.connect(self.SETNR)

        self.REMOVE = QtWidgets.QPushButton(self.TAB1)
        self.REMOVE.setText("REMOVE")
        self.REMOVE.resize(110, 25)
        self.REMOVE.move(250, 367)
        self.REMOVE.clicked.connect(self.REMOVE_clicked)

        self.REMOVEALL = QPushButton(self.TAB1)
        self.REMOVEALL.setText("REMOVE ALL")
        self.REMOVEALL.resize(110, 25)
        self.REMOVEALL.move(250, 392)
        self.REMOVEALL.clicked.connect(self.REMOVEALL_clicked)

        self.EXPORT = QPushButton(self.TAB1)
        self.EXPORT.setText("EXPORT")
        self.EXPORT.resize(110, 25)
        self.EXPORT.move(350, 392)
        self.EXPORT.clicked.connect(self.EXPORT_clicked)

        self.IMPORT = QPushButton(self.TAB1)
        self.IMPORT.setText("IMPORT")
        self.IMPORT.resize(110, 25)
        self.IMPORT.move(350, 367)
        self.IMPORT.clicked.connect(self.IMPORTGO)

        self.RESTACK = QPushButton(self.TAB1)
        self.RESTACK.setText("RESTACK")
        self.RESTACK.resize(110, 25)
        self.RESTACK.move(550, 367)
        self.RESTACK.clicked.connect(self.RESTACK_clicked)

        self.MOVEUP = QPushButton(self.TAB1)
        self.MOVEUP.setText("MOVE UP")
        self.MOVEUP.resize(110, 25)
        self.MOVEUP.move(450, 367)
        self.MOVEUP.clicked.connect(self.MOVEUP_clicked)

        self.MOVEDOWN = QPushButton(self.TAB1)
        self.MOVEDOWN.setText("MOVE DOWN")
        self.MOVEDOWN.resize(110, 25)
        self.MOVEDOWN.move(450, 392)
        self.MOVEDOWN.clicked.connect(self.MOVEDOWN_clicked)
        # #####################################TEAM SETTINGS######################### #
        self.groupBox = QtWidgets.QGroupBox(self.TAB1)

        self.groupBox.setGeometry(QtCore.QRect(5, 30, 245, 40))

        self.TEAMNAMELABEL = QtWidgets.QLabel(self.groupBox)
        self.TEAMNAMELABEL.setText("Team Name")
        self.TEAMNAMELABEL.resize(250, 20)
        self.TEAMNAMELABEL.move(10, 5)

        self.TEAMNAME = QtWidgets.QLineEdit(self.groupBox)
        self.TEAMNAME.resize(130, 20)
        self.TEAMNAME.move(105, 8)
        # #####################################HIGHLIGHT SETTINGS#################### #
        self.groupBox3 = QtWidgets.QGroupBox(self.TAB1)
        self.groupBox3.setGeometry(QtCore.QRect(5, 75, 245, 120))

        self.NOTUPLOADEDLABEL = QtWidgets.QLabel(self.groupBox3)
        self.NOTUPLOADEDLABEL.setText("Highlight non-uploaded additions")
        self.NOTUPLOADEDLABEL.resize(250, 20)
        self.NOTUPLOADEDLABEL.move(10, 5)

        self.TEAMLINECOLOR = QPushButton(self.groupBox3)
        self.TEAMLINECOLOR.setText("LINE COLOR")
        self.TEAMLINECOLOR.resize(110, 25)
        self.TEAMLINECOLOR.move(3, 30)
        self.TEAMLINECOLOR.clicked.connect(self.TEAMLINECOLOR_clicked)

        self.TEAMLINECOLORICON = QtWidgets.QLabel(self.groupBox3)
        self.TEAMLINECOLORICON.move(110, 37)
        self.pix = QtGui.QPixmap(15, 15)
        self.pix.fill(QColor(self.WHITE))
        self.TEAMLINECOLORICON.setPixmap(self.pix)

        self.LINEWIDTHLABEL = QtWidgets.QLabel(self.groupBox3)
        self.LINEWIDTHLABEL.setText("Line Width")
        self.LINEWIDTHLABEL.resize(250, 20)
        self.LINEWIDTHLABEL.move(130, 34)

        self.TEAMLINEWIDTHSPIN = QtWidgets.QSpinBox(self.groupBox3)
        self.TEAMLINEWIDTHSPIN.setRange(1, 20)
        self.TEAMLINEWIDTHSPIN.setValue(self.LINEWIDTH)
        self.TEAMLINEWIDTHSPIN.move(200, 34)

        self.TEAMNODECOLOR = QPushButton(self.groupBox3)
        self.TEAMNODECOLOR.setText("NODE COLOR")
        self.TEAMNODECOLOR.resize(110, 25)
        self.TEAMNODECOLOR.move(3, 55)
        self.TEAMNODECOLOR.clicked.connect(self.TEAMNODECOLOR_clicked)

        self.TEAMNODECOLORICON = QtWidgets.QLabel(self.groupBox3)
        self.TEAMNODECOLORICON.move(110, 62)
        self.pix = QtGui.QPixmap(15, 15)
        self.pix.fill(QColor(self.WHITE))
        self.TEAMNODECOLORICON.setPixmap(self.pix)

        self.ICONSIZELABEL = QtWidgets.QLabel(self.groupBox3)
        self.ICONSIZELABEL.setText("Node Size")
        self.ICONSIZELABEL.resize(250, 20)
        self.ICONSIZELABEL.move(130, 59)

        self.TEAMICONSIZESPIN = QtWidgets.QSpinBox(self.groupBox3)
        self.TEAMICONSIZESPIN.setRange(10, 50)
        self.TEAMICONSIZESPIN.setValue(self.ICONSIZE)
        self.TEAMICONSIZESPIN.move(200, 60)

        self.ICONSHAPELABEL = QtWidgets.QLabel(self.groupBox3)
        self.ICONSHAPELABEL.setText("Node Shape  -")
        self.ICONSHAPELABEL.resize(250, 20)
        self.ICONSHAPELABEL.move(10, 84)

        self.TEAMICONSHAPEBOX = QtWidgets.QComboBox(self.groupBox3)
        self.TEAMICONSHAPEBOX.activated.connect(self.TEAMSHAPESELECT)
        self.TEAMICONSHAPEBOX.blockSignals(False)
        self.TEAMICONSHAPEBOX.resize(138, 20)
        self.TEAMICONSHAPEBOX.addItem("Circle")
        self.TEAMICONSHAPEBOX.addItem("Triangle")
        self.TEAMICONSHAPEBOX.addItem("Square")
        self.TEAMICONSHAPEBOX.addItem("Pentagon")
        self.TEAMICONSHAPEBOX.addItem("Hexagon")
        self.TEAMICONSHAPEBOX.addItem("Heptagon")
        self.TEAMICONSHAPEBOX.addItem("Octagon")
        self.TEAMICONSHAPEBOX.addItem("Nonagon")
        self.TEAMICONSHAPEBOX.addItem("Decagon")
        self.TEAMICONSHAPEBOX.move(105, 85)

        # ##############################EDITOR SETTINGS############################## #

        self.groupBox2 = QtWidgets.QGroupBox(self.TAB1)
        self.groupBox2.setGeometry(QtCore.QRect(5, 200, 245, 220))

        self.EDITSETTINGSLABEL = QtWidgets.QLabel(self.groupBox2)
        self.EDITSETTINGSLABEL.setText("Editor Settings:")
        self.EDITSETTINGSLABEL.resize(250, 20)
        self.EDITSETTINGSLABEL.move(10, 5)

        self.EDITNAMELABEL = QtWidgets.QLabel(self.groupBox2)
        self.EDITNAMELABEL.setText("Editor Name")
        self.EDITNAMELABEL.resize(250, 20)
        self.EDITNAMELABEL.move(10, 25)

        self.EDITORNAME = QtWidgets.QLineEdit(self.groupBox2)
        self.EDITORNAME.resize(130, 20)
        self.EDITORNAME.move(105, 25)

        self.EDITIDLABEL = QtWidgets.QLabel(self.groupBox2)
        self.EDITIDLABEL.setText("Editor User ID")
        self.EDITIDLABEL.resize(250, 20)
        self.EDITIDLABEL.move(10, 50)

        self.EDITORID = QtWidgets.QLineEdit(self.groupBox2)
        self.EDITORID.resize(130, 20)
        self.EDITORID.move(105, 50)

        self.ADD = QPushButton(self.groupBox2)
        self.ADD.setText("ADD")
        self.ADD.resize(80, 25)
        self.ADD.move(5, 75)
        self.ADD.clicked.connect(self.ADD_clicked)

        self.CLEAR = QPushButton(self.groupBox2)
        self.CLEAR.setText("CLEAR")
        self.CLEAR.resize(80, 25)
        self.CLEAR.move(83, 75)
        self.CLEAR.clicked.connect(self.CLEAR_clicked)

        self.EDIT = QPushButton(self.groupBox2)
        self.EDIT.setText("EDIT")
        self.EDIT.resize(80, 25)
        self.EDIT.move(160, 75)
        self.EDIT.clicked.connect(self.EDIT_clicked)

        self.EDITORLINECOLOR = QPushButton(self.groupBox2)
        self.EDITORLINECOLOR.setText("LINE COLOR")
        self.EDITORLINECOLOR.resize(110, 25)
        self.EDITORLINECOLOR.move(5, 105)
        self.EDITORLINECOLOR.clicked.connect(self.EDITORLINECOLOR_clicked)

        self.EDITORLINECOLORICON = QtWidgets.QLabel(self.groupBox2)
        self.EDITORLINECOLORICON.move(115, 112)
        self.pix = QtGui.QPixmap(15, 15)
        self.pix.fill(QColor(self.WHITE))
        self.EDITORLINECOLORICON.setPixmap(self.pix)

        self.EDITORLINEWIDTHLABEL = QtWidgets.QLabel(self.groupBox2)
        self.EDITORLINEWIDTHLABEL.setText("Line Width")
        self.EDITORLINEWIDTHLABEL.resize(75, 20)
        self.EDITORLINEWIDTHLABEL.move(135, 110)

        self.EDITORLINEWIDTHSPIN = QtWidgets.QSpinBox(self.groupBox2)
        self.EDITORLINEWIDTHSPIN.setRange(1, 20)
        self.EDITORLINEWIDTHSPIN.setValue(self.LINEWIDTH)
        self.EDITORLINEWIDTHSPIN.move(200, 110)

        self.EDITORNODECOLOR = QPushButton(self.groupBox2)
        self.EDITORNODECOLOR.setText("NODE COLOR")
        self.EDITORNODECOLOR.resize(110, 25)
        self.EDITORNODECOLOR.move(5, 134)
        self.EDITORNODECOLOR.clicked.connect(self.EDITORNODECOLOR_clicked)

        self.EDITORNODECOLORICON = QtWidgets.QLabel(self.groupBox2)
        self.EDITORNODECOLORICON.move(115, 141)
        self.pix = QtGui.QPixmap(15, 15)
        self.pix.fill(QColor(self.WHITE))
        self.EDITORNODECOLORICON.setPixmap(self.pix)

        self.EDITORNODESIZELABEL = QtWidgets.QLabel(self.groupBox2)
        self.EDITORNODESIZELABEL.setText("Node Size")
        self.EDITORNODESIZELABEL.resize(75, 20)
        self.EDITORNODESIZELABEL.move(135, 137)

        self.EDITORNODESIZESPIN = QtWidgets.QSpinBox(self.groupBox2)
        self.EDITORNODESIZESPIN.setRange(10, 50)
        self.EDITORNODESIZESPIN.setValue(10)
        self.EDITORNODESIZESPIN.move(200, 137)

        self.TOGGLELABEL = QtWidgets.QLabel(self.groupBox2)
        self.TOGGLELABEL.setText("Toggle UID in Style Settings menu")
        self.TOGGLELABEL.resize(250, 15)
        self.TOGGLELABEL.move(12, 165)

        self.TOGGLECHECK = QtWidgets.QCheckBox(self.groupBox2)
        self.TOGGLECHECK.move(220, 165)

        self.EDITORICONSHAPELABEL = QtWidgets.QLabel(self.groupBox2)
        self.EDITORICONSHAPELABEL.setText("Node Shape  -")
        self.EDITORICONSHAPELABEL.resize(250, 20)
        self.EDITORICONSHAPELABEL.move(12, 190)

        self.EDITORICONSHAPEBOX = QtWidgets.QComboBox(self.groupBox2)
        self.EDITORICONSHAPEBOX.activated.connect(self.EDITORSHAPESELECT)
        self.EDITORICONSHAPEBOX.blockSignals(False)
        self.EDITORICONSHAPEBOX.resize(135, 20)
        self.EDITORICONSHAPEBOX.addItem("Circle")
        self.EDITORICONSHAPEBOX.addItem("Triangle")
        self.EDITORICONSHAPEBOX.addItem("Square")
        self.EDITORICONSHAPEBOX.addItem("Pentagon")
        self.EDITORICONSHAPEBOX.addItem("Hexagon")
        self.EDITORICONSHAPEBOX.addItem("Heptagon")
        self.EDITORICONSHAPEBOX.addItem("Octagon")
        self.EDITORICONSHAPEBOX.addItem("Nonagon")
        self.EDITORICONSHAPEBOX.addItem("Decagon")
        self.EDITORICONSHAPEBOX.move(105, 190)
        self.CIRCLE = resource_path("//circle.png")
        self.SQUARE = resource_path("//square.png")
        self.TRIANGLE = resource_path("//triangle.png")
        self.PENTAGON = resource_path("//pentagon.png")
        self.HEXAGON = resource_path("//hexagon.png")
        self.HEPTAGON = resource_path("//heptagon.png")
        self.OCTAGON = resource_path("//octagon.png")
        self.NONAGON = resource_path("//nonagon.png")
        self.DECAGON = resource_path("//decagon.png")

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        exitAct = QAction(QIcon("exit.png"), " &Quit", self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.setStatusTip("Exit GEM")
        exitAct.triggered.connect(self.closeEvent)
        FILE = menubar.addMenu("&File")
        GITPULL = FILE.addMenu("Git Pull")
        GITPUSH = QAction(" &Git Push", self)
        GITPUSH.setStatusTip("Export .Mapcss to Github")
        GITPUSH.triggered.connect(self.CONFIRMPUSH)
        GITPUSH = FILE.addAction(GITPUSH)
        FILE.addAction(exitAct)
        git = Github("AUTH TOKEN")
        try:
            org = git.get_user("Kaart-labs")
            self.repo = org.get_repo("GEM")
            self.contents = self.repo.get_contents("")
            self.pulllist = {}
            self.pullcount = 0
            self.pullcountlist = []
            for i in self.contents:
                i = str(i)
                i = i.split('"')
                i = i[1]

                if "mapcss" in i:
                    i = i.split(".")
                    i = i[0]
                    self.pullcount += 1
                    self.pullcountlist.append(self.pullcount)
                    self.pulllist[self.pullcount] = i
            self.PULLS = []
            for j in range(self.pullcount):
                TEXT = self.pulllist[j + 1]
                ACT = str("ACT%s" % (j))
                ACT = QAction(" &Pull %s Paintstyle from Github" % (TEXT), self)
                ACT.setStatusTip("Import .Mapcss from Github")
                GITPULL.addAction(ACT)
                self.PULLS.append(ACT)

            for j in self.PULLS:
                j.triggered.connect(self.GITPULL_clicked)

        except github.BadCredentialsException as error:
            logger.exception(error)

        # ########################################################################### #
        self.retranslateUi(MAINWindow)

    # ########################################################################### #

    def retranslateUi(self, MAINWindow):

        self.GEMheaders = [
            "NAME",
            "USER ID",
            "LINE HIGHLIGHT",
            "NODE HIGHLIGHT",
        ]
        self.rowcount = 50
        self.colcount = 4
        self.GEMarray = [
            [str(""), str(""), QtGui.QColor(clear), QtGui.QColor(clear),]
            for j in range(self.rowcount)
        ]
        self.tablemodel = Model(self.GEMarray, self.GEMheaders, self)
        self.TABLE.setModel(self.tablemodel)
        self.TABLE.resizeRowsToContents()
        self.TABLE.resizeColumnsToContents()

    #############################################
    def resource_path(relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception as e:
            logger.exception(e)
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # ########################   GEM: EDITOR FUNCTIONS   ###################### #
    def closeEvent(self, event):
        self.setParent(None)
        self.deleteLater()
        self.close()

    #############

    def CONFIRMPUSH(self):
        self.passdialog = CONFIRMPOPUP()
        self.passdialog.show()

    def GITPULL_clicked(self):
        SENDER = self.sender()
        TEXT = SENDER.text()
        TEXT = TEXT.replace(" &Pull ", "")
        TEXT = TEXT.replace(" Paintstyle from Github", "")
        git = Github("AUTH TOKEN")
        org = git.get_user("Kaart-labs")
        self.repo = org.get_repo("GEM")
        self.contents = self.repo.get_contents("%s.mapcss" % (TEXT))
        self.c = self.contents.decoded_content
        self.IMPULLGO(self.c)

    def GITPUSH_GO(self):
        self.USERENTRYBLOCK = ""
        self.MASTERENTERYTEXT = ""
        self.OUTUSERS = 0
        self.EXPORT_clicked(True)
        NAME = "QAQC_%s.mapcss" % (self.TEAMNAME.text())
        try:
            self.contents = self.repo.get_contents(NAME)
            self.c = self.contents.decoded_content
            self.repo.update_file(
                self.contents.path, "GEM", self.OUTPUSHTEXT, self.contents.sha
            )
        except Exception as error:
            logger.exception(error)
            self.repo.create_file(NAME, "GEM", self.OUTPUSHTEXT)

    ##########
    def RESTACK_clicked(self):
        for i in range(50):
            self.GEMarray[i][0] = ""
            self.GEMarray[i][1] = ""
            self.GEMarray[i][2] = clear
            self.GEMarray[i][3] = clear
            count = 0
            self.RESTACKUSERS = {}
        for i in self.TEMPUSERS.values():
            if i != "" and type(i) != int:
                self.GEMarray[count][0] = i.NAME
                self.GEMarray[count][1] = i.UID
                self.GEMarray[count][2] = i.LINECOLORUI
                self.GEMarray[count][3] = i.icon
                self.RESTACKUSERS[str(count)] = i
                count += 1
                self.usercount = count
        self.TEMPUSERS = {}
        self.TEMPUSERS = self.RESTACKUSERS

    def MOVEUP_clicked(self):
        if self.NRSELECT != "":
            MOVETO = int(int(self.NRSELECT) - 1)
            MOVEFROM = int(self.NRSELECT)
            if MOVETO != int(-1):
                if str(MOVETO) in self.TEMPUSERS.keys():
                    if self.TEMPUSERS[str(MOVETO)] == 0:
                        self.GEMGEMarray[(MOVETO)][0] = self.TEMPUSERS[
                            str(MOVEFROM)
                        ].NAME
                        self.GEMGEMarray[(MOVETO)][1] = self.TEMPUSERS[
                            str(MOVEFROM)
                        ].UID
                        self.GEMGEMarray[(MOVETO)][2] = self.TEMPUSERS[
                            str(MOVEFROM)
                        ].LINECOLORUI
                        self.GEMGEMarray[(MOVETO)][3] = self.TEMPUSERS[
                            str(MOVEFROM)
                        ].icon
                        self.GEMGEMarray[(MOVEFROM)][0] = ""
                        self.GEMGEMarray[(MOVEFROM)][1] = ""
                        self.GEMGEMarray[(MOVEFROM)][2] = clear
                        self.GEMGEMarray[(MOVEFROM)][3] = clear
                        self.TEMPUSERS[str(MOVETO)] = self.TEMPUSERS[str(MOVEFROM)]
                        self.TEMPUSERS[str(MOVEFROM)] = 0
                        self.SETNR()

                    else:
                        if str(MOVEFROM) in self.TEMPUSERS.keys():
                            self.MOVETOUSER = self.TEMPUSERS[str(MOVEFROM)]
                            self.MOVEFROMUSER = self.TEMPUSERS[str(MOVETO)]
                            self.GEMGEMarray[(MOVEFROM)][0] = self.MOVEFROMUSER.NAME
                            self.GEMGEMarray[(MOVEFROM)][1] = self.MOVEFROMUSER.UID
                            self.GEMGEMarray[(MOVEFROM)][
                                2
                            ] = self.MOVEFROMUSER.LINECOLORUI
                            self.GEMarray[(MOVEFROM)][3] = self.MOVEFROMUSER.icon
                            self.GEMarray[(MOVETO)][0] = self.MOVETOUSER.NAME
                            self.GEMarray[(MOVETO)][1] = self.MOVETOUSER.UID
                            self.GEMarray[(MOVETO)][2] = self.MOVETOUSER.LINECOLORUI
                            self.GEMarray[(MOVETO)][3] = self.MOVETOUSER.icon
                            self.TEMPUSERS[str(MOVETO)] = self.MOVETOUSER
                            self.TEMPUSERS[str(MOVEFROM)] = self.MOVEFROMUSER
                            self.SETNR()

    def MOVEDOWN_clicked(self):
        if self.NRSELECT != "":
            MOVETO = int(int(self.NRSELECT) + 1)
            MOVEFROM = int(self.NRSELECT)

            if str(MOVETO) in self.TEMPUSERS.keys():
                if self.TEMPUSERS[str(MOVETO)] == 0:
                    self.GEMarray[(MOVETO)][0] = self.TEMPUSERS[str(MOVEFROM)].NAME
                    self.GEMarray[(MOVETO)][1] = self.TEMPUSERS[str(MOVEFROM)].UID
                    self.GEMarray[(MOVETO)][2] = self.TEMPUSERS[
                        str(MOVEFROM)
                    ].LINECOLORUI
                    self.GEMarray[(MOVETO)][3] = self.TEMPUSERS[str(MOVEFROM)].icon
                    self.GEMarray[(MOVEFROM)][0] = ""
                    self.GEMarray[(MOVEFROM)][1] = ""
                    self.GEMarray[(MOVEFROM)][2] = clear
                    self.GEMarray[(MOVEFROM)][3] = clear
                    self.TEMPUSERS[str(MOVETO)] = self.TEMPUSERS[str(MOVEFROM)]
                    self.TEMPUSERS[str(MOVEFROM)] = 0
                    self.SETNR()
                else:
                    self.MOVETOUSER = self.TEMPUSERS[str(MOVEFROM)]
                    self.MOVEFROMUSER = self.TEMPUSERS[str(MOVETO)]
                    self.GEMarray[(MOVEFROM)][0] = self.MOVEFROMUSER.NAME
                    self.GEMarray[(MOVEFROM)][1] = self.MOVEFROMUSER.UID
                    self.GEMarray[(MOVEFROM)][2] = self.MOVEFROMUSER.LINECOLORUI
                    self.GEMarray[(MOVEFROM)][3] = self.MOVEFROMUSER.icon
                    self.GEMarray[(MOVETO)][0] = self.MOVETOUSER.NAME
                    self.GEMarray[(MOVETO)][1] = self.MOVETOUSER.UID
                    self.GEMarray[(MOVETO)][2] = self.MOVETOUSER.LINECOLORUI
                    self.GEMarray[(MOVETO)][3] = self.MOVETOUSER.icon
                    self.TEMPUSERS[str(MOVETO)] = self.MOVETOUSER
                    self.TEMPUSERS[str(MOVEFROM)] = self.MOVEFROMUSER
                    self.SETNR()

    def EDITORLINECOLOR_clicked(self):
        color = QtWidgets.QColorDialog.getColor()
        clr = color.name()
        colr = ""
        for i in clr:
            colr += str(i)

        if colr != "#000000":
            if self.NRSELECT != "":
                self.TEMPUSERS[str(self.NRSELECT)].LINECOLORTEXT = colr
                self.TEMPUSERS[str(self.NRSELECT)].LINECOLORUI = color
                self.pix.fill(QColor(self.TEMPUSERS[str(self.NRSELECT)].LINECOLORUI))
                self.EDITORLINECOLORICON.setPixmap(self.pix)
                self.GEMarray[self.NRSELECT][2] = QtGui.QColor(
                    self.TEMPUSERS[str(self.NRSELECT)].LINECOLORUI
                )
            else:
                self.TEMPLINECOLORTEXT = colr
                self.TEMPLINECOLORUI = color
                self.pix.fill(QColor(self.TEMPLINECOLORUI))
                self.EDITORLINECOLORICON.setPixmap(self.pix)
                self.EDITORLINECOLORICON.repaint()

    def EDITORNODECOLOR_clicked(self):
        color = QtWidgets.QColorDialog.getColor()
        clr = color.name()
        colr = ""
        for i in clr:
            colr += str(i)
        if colr != "#000000":
            if self.NRSELECT != "":
                self.TEMPUSERS[str(self.NRSELECT)].NODECOLORTEXT = colr
                self.TEMPUSERS[str(self.NRSELECT)].NODECOLORUI = color
                self.pix.fill(QColor(self.TEMPUSERS[str(self.NRSELECT)].NODECOLORUI))
                self.EDITORNODECOLORICON.setPixmap(self.pix)
                self.EDITORNODECOLORDISPLAY(self.NRSELECT)

            else:
                self.TEMPNODECOLORTEXT = colr
                self.TEMPNODECOLORUI = color
                self.pix.fill(QColor(self.TEMPNODECOLORUI))
                self.EDITORNODECOLORICON.setPixmap(self.pix)
                self.EDITORNODECOLORICON.repaint()

    # ###########################   TEAM FUNCTIONS   #############################

    def TEAMLINECOLOR_clicked(self):
        color = QtWidgets.QColorDialog.getColor()

        clr = color.name()
        colr = ""
        for i in clr:
            colr += str(i)
        if colr != "#000000":
            self.TEAMLINECOLORTEXT = colr
            self.TEAMLINECOLORUI = color
            self.pix.fill(QColor(self.TEAMLINECOLORUI))
            self.TEAMLINECOLORICON.setPixmap(self.pix)

    def TEAMNODECOLOR_clicked(self):
        color = QtWidgets.QColorDialog.getColor()
        clr = color.name()
        colr = ""
        for i in clr:
            colr += str(i)
        if colr != "#000000":
            self.TEAMNODECOLORTEXT = colr
            self.TEAMNODECOLORUI = color
            self.pix.fill(QColor(self.TEAMNODECOLORUI))
            self.TEAMNODECOLORICON.setPixmap(self.pix)

    def ADD_clicked(self):
        if self.NRSELECT == "":
            ENAME = self.EDITORNAME.text()
            ENAME = ENAME.strip()
            EUID = self.EDITORID.text()
            EUID = EUID.strip()
            if ENAME and EUID.strip():
                ECLASS = EDITORINFO()
                ECLASS.NAME = ENAME
                ECLASS.UID = EUID
                if self.TEMPLINECOLORTEXT.strip():
                    ECLASS.LINECOLORTEXT = self.TEMPLINECOLORTEXT
                    ECLASS.LINECOLORUI = self.TEMPLINECOLORUI
                else:
                    ECLASS.LINECOLORTEXT = "#b600ff"
                    ECLASS.LINECOLORUI = QColor(ECLASS.LINECOLORTEXT)

                if self.TEMPNODECOLORTEXT.strip():
                    ECLASS.NODECOLORTEXT = self.TEMPNODECOLORTEXT
                    ECLASS.NODECOLORUI = self.TEMPNODECOLORUI
                else:
                    ECLASS.NODECOLORTEXT = "#4648ff"
                    ECLASS.NODECOLORUI = ECLASS.NODECOLORUI

                if self.TEMPEDITORICONSHAPE.strip():

                    ECLASS.ICONSHAPE = self.TEMPEDITORICONSHAPE
                else:
                    ECLASS.ICONSHAPE = "Circle"
                ECLASS.LINEWIDTH = str(self.EDITORLINEWIDTHSPIN.value())
                ECLASS.ICONSIZE = str(self.EDITORNODESIZESPIN.value())
                if str(self.usercount) in self.TEMPUSERS.keys():
                    if self.TEMPUSERS[str(self.usercount)] != 0:
                        self.usercount += 1

                self.TEMPUSERS[str(self.usercount)] = ECLASS
                self.GEMarray[self.usercount][0] = str(ECLASS.NAME)
                self.GEMarray[self.usercount][1] = str(ECLASS.UID)
                self.GEMarray[self.usercount][2] = QColor(ECLASS.LINECOLORUI)
                self.EDITORNODECOLORDISPLAY((self.usercount))

                self.ADDUSERS.append(ECLASS)
                self.EDITORNAME.setText("")
                self.EDITORID.setText("")
                self.EDITORNAME.repaint()
                self.EDITORID.repaint()
                self.usercount += 1
                self.pix.fill(QColor(self.WHITE))
                self.EDITORNODECOLORICON.setPixmap(self.pix)
                self.EDITORLINECOLORICON.setPixmap(self.pix)
                self.EDITORNODECOLORICON.repaint()
                self.EDITORLINECOLORICON.repaint()

        if self.NRSELECT != "":
            ENAME = self.EDITORNAME.text()
            ENAME = ENAME.strip()
            EUID = self.EDITORID.text()
            EUID = EUID.strip()
            if ENAME and EUID.strip():
                self.TEMPUSERS[str(self.EDITORSELECT)].NAME = ENAME
                self.TEMPUSERS[str(self.EDITORSELECT)].UID = EUID
                self.TEMPUSERS[
                    str(self.EDITORSELECT)
                ].ICONSHAPE = self.EDITORICONSHAPEBOX.currentText()
                self.TEMPUSERS[str(self.EDITORSELECT)].LINEWIDTH = str(
                    self.EDITORLINEWIDTHSPIN.value()
                )
                self.TEMPUSERS[str(self.EDITORSELECT)].ICONSIZE = str(
                    self.EDITORNODESIZESPIN.value()
                )

                if self.GOEDIT is True:
                    self.GEMarray[self.EDITORSELECT][0] = str(
                        self.TEMPUSERS[str(self.EDITORSELECT)].NAME
                    )
                    self.GEMarray[self.EDITORSELECT][1] = str(
                        self.TEMPUSERS[str(self.EDITORSELECT)].UID
                    )
                    self.EDITORNODECOLORDISPLAY(self.EDITORSELECT)
                else:
                    self.GEMarray[self.usercount][0] = str(
                        self.TEMPUSERS[str(self.EDITORSELECT)].NAME
                    )
                    self.GEMarray[self.usercount][1] = str(
                        self.TEMPUSERS[str(self.EDITORSELECT)].UID
                    )
                    self.EDITORNODECOLORDISPLAY((self.usercount))

                self.EDITORNAME.setText("")
                self.EDITORID.setText("")
                self.EDITORNAME.repaint()
                self.EDITORID.repaint()
                self.NRSELECT = ""
                self.EDITORSELECT = None
                self.ADD.setText("ADD")
                self.pix.fill(QColor(self.WHITE))
                self.EDITORNODECOLORICON.setPixmap(self.pix)
                self.EDITORLINECOLORICON.setPixmap(self.pix)
                self.EDITORLINECOLORICON.repaint()
                self.EDITORNODECOLORICON.repaint()
                self.NRSELECT = ""

    def GETTEAMSHAPETEXT(self):
        if self.TEAMICONSHAPE == "Circle":
            self.TEAMICONSHAPEBOX.setCurrentIndex(0)
            self.TEAMICONSHAPEBOX.repaint()
        if self.TEAMICONSHAPE == "Triangle":
            self.TEAMICONSHAPEBOX.setCurrentIndex(1)
            self.TEAMICONSHAPEBOX.repaint()
        if self.TEAMICONSHAPE == "Square":
            self.TEAMICONSHAPEBOX.setCurrentIndex(2)
            self.TEAMICONSHAPEBOX.repaint()
        if self.TEAMICONSHAPE == "Pentagon":
            self.TEAMICONSHAPEBOX.setCurrentIndex(3)
            self.TEAMICONSHAPEBOX.repaint()
        if self.TEAMICONSHAPE == "Hexagon":
            self.TEAMICONSHAPEBOX.setCurrentIndex(4)
            self.TEAMICONSHAPEBOX.repaint()
        if self.TEAMICONSHAPE == "Heptagon":
            self.TEAMICONSHAPEBOX.setCurrentIndex(5)
            self.TEAMICONSHAPEBOX.repaint()
        if self.TEAMICONSHAPE == "Octagon":
            self.TEAMICONSHAPEBOX.setCurrentIndex(6)
            self.TEAMICONSHAPEBOX.repaint()
        if self.TEAMICONSHAPE == "Nonagon":
            self.TEAMICONSHAPEBOX.setCurrentIndex(7)
            self.TEAMICONSHAPEBOX.repaint()
        if self.TEAMICONSHAPE == "Decagon":
            self.TEAMICONSHAPEBOX.setCurrentIndex(8)
            self.TEAMICONSHAPEBOX.repaint()

    def GETEDITORSHAPETEXT(self):
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "Circle":
            self.EDITORICONSHAPEBOX.setCurrentIndex(0)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "Triangle":
            self.EDITORICONSHAPEBOX.setCurrentIndex(1)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "Square":
            self.EDITORICONSHAPEBOX.setCurrentIndex(2)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "Pentagon":
            self.EDITORICONSHAPEBOX.setCurrentIndex(3)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "Hexagon":
            self.EDITORICONSHAPEBOX.setCurrentIndex(4)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "Heptagon":
            self.EDITORICONSHAPEBOX.setCurrentIndex(5)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "Octagon":
            self.EDITORICONSHAPEBOX.setCurrentIndex(6)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "Nonagon":
            self.EDITORICONSHAPEBOX.setCurrentIndex(7)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "Decagon":
            self.EDITORICONSHAPEBOX.setCurrentIndex(8)
            self.EDITORICONSHAPEBOX.repaint()

    # ############################   EXPORT BLOCK   ############################ #

    def TEAMSHAPESELECT(self):
        self.TEAMICONSHAPE = self.TEAMICONSHAPEBOX.currentText()

    def EDITORSHAPESELECT(self):
        self.TEMPEDITORICONSHAPE = self.EDITORICONSHAPEBOX.currentText()

    def EXPORT_clicked(self, ISPUSH):
        self.RESTACK_clicked()
        self.TITLEENTRYBLOCK = str(self.TEAMNAME.text())
        self.TITLEENTRYBLOCK = self.TITLEENTRYBLOCK.strip()
        if self.TITLEENTRYBLOCK.strip():
            if ISPUSH is not True:
                default_name = str(
                    self.output_file_dir + ("/QAQC_%s.mapcss" % (self.TITLEENTRYBLOCK))
                )
                self.OUTFILE = QtWidgets.QFileDialog.getSaveFileName(
                    self, directory=default_name
                )
            else:
                default_name = str("QAQC_%s.mapcss" % (self.TITLEENTRYBLOCK))

            self.SETUPENTRYBLOCK = ""
            self.SETTINGBLOCK = ""
            self.NODEENTRYBLOCK = ""
            self.WAYENTRYBLOCK = ""
            self.MASTEROUTPUTBLOCK = ""
            self.LINEWIDTH = str(self.TEAMLINEWIDTHSPIN.value())
            self.ICONSIZE = str(self.TEAMICONSIZESPIN.value())
            for i in self.ADDUSERS:
                if i != "":
                    if i.UID[-1] == " ":
                        i.UID = i.UID[:-1]
                    if " " in i.UID:
                        self.SPACESETTINGENTRY(i.NAME, i.UID)
                    else:
                        self.SETTINGENTRY(i.NAME, i.UID)
                    self.SETUPENTRY(i.NAME, i.UID)

                    self.NODEENTRY(i.NAME, i.ICONSIZE, i.ICONSHAPE, i.NODECOLORTEXT)
                    self.WAYDENTRY(i.NAME, i.LINECOLORTEXT, i.LINEWIDTH)
            self.MASTEROUTPUT(True)

    def SETUPENTRY(self, name, uid):

        if self.TOGGLECHECK.isChecked():
            self.SETUPENTRYBLOCK += """setting::user_%s {
            type:boolean;
            label:tr("Turn User %s On/Off");
            default:true;
            }\n""" % (
                name,
                name,
            )
        else:
            self.SETUPENTRYBLOCK += """setting::user_%s {
            type:boolean;
            label:tr("Turn User %s On/Off");
            default:true;
            }\n""" % (
                name,
                uid,
            )

    def SPACESETTINGENTRY(self, name, uid):
        self.SETTINGBLOCK += """*[osm_user_name() == \\"%s\\"][setting("user_%s")] {
  set .%s;
}\n""" % (
            uid,
            name,
            name,
        )

    def SETTINGENTRY(self, name, uid):
        return self.SPACESETTINGENTRY(name, uid)

    def NODEENTRY(self, name, iconsize, iconshape, nodecolor):
        self.NODEENTRYBLOCK += """node.%s{
  symbol-size: %s;
  symbol-shape: %s;
  symbol-stroke-color: %s;
  symbol-stroke-width: 3px;
  symbol-fill-opacity: 0.5;
  z-index: -5;
}""" % (
            name,
            iconsize,
            iconshape,
            nodecolor,
        )

    def WAYDENTRY(self, name, color, width):
        self.WAYENTRYBLOCK += """way.%s{
  z-index: -10;
  casing-color: %s;
  casing-width: %s;
  casing-opacity: 0.6;
  /*
  text: eval(concat("Highway type =", " ", tag("highway")));
  text-offset: -20;
  */
}""" % (
            name,
            color,
            width,
        )

    def MASTEROUTPUT(self, ISPUSH):
        try:
            path = self.OUTFILE[0]
        except Exception as e:
            logger.exception(e)

        OUTPUT = """meta {
  title: "QC Style For %s Team";
  description: "Highlights features that were created/modified by users";
  watch-modified: true;
  version: "1.5";
  icon: "http://uncrate.com/p/2016/02/smart-kart.jpg";

}
/* Notes

1.0 Added styles -- provided by Jenn -- and users -- Ian -- 3/11/2019

1.1 Configured styles -- Louis -- 3/13/2019

1.2 Configured style colors and highlighting -- Ian -- 3/15/2019

1.3 Simplified user lines -- Louis -- 3/18/2019

1.4 Adjusted user, style lines and appearances -- 3/20/2019

1.5 Alphabetized users, added new users, added tips, simplified node highlight & node modified overlays -- Louis,Ian,AndrewP -- 5/15/2019

Tips:

A setting should be created for each separate user:

setting::user_aaron {
  type: boolean;
  label: tr("Turn User Aaron On/Off");
  default: false;
}

-- after :: comes your setting "class" which can be named as you will. Our example show user_aaron
-- Type: boolean; should always exist
-- label: tr("Anything you want to put here") -> This is what shows up under setting in JOSM
-- Default: false -> the setting will remain disabled on launch until a user enables it

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


at which point, it becomes necessary to create a selector statement for your user:

*[osm_user_name() == "vespax"][setting("user_aaron")] {
  set .aaron;
}

-- * denotes what you are selecting, in this case, every element type in OSM
-- [osm_user_name() == "user:vespax"] -> this is necessary and should be constructed as such.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to construct time stamps, you can use the following:

(performance)
For the performance path, you will need to convert the date to seconds since the epoch.
On Mac OS X, you can use the following command, replacing "2016-02-20" with the appropriate date
$ date -j -u -f "%Y-%m-%d %T" "2016-02-20 00:00:00" "+%s"
String: "[osm_timestamp() > 1455926400]" can be modified in several ways.
"[osm_timestamp() > 1455926400]" shows all edits after that time
"[osm_timestamp() < 1455926400]" shows all edits prior to that time
"[osm_timestamp() == 1455926400]" shows all edits that occurred at precisely that time
"[osm_timestamp() > 1455926400][osm_timestamp() < 1456012800]" shows edits made on 2016-02-20

(ease of use)
String: "[eval(JOSM_search("timestamp:2016-02-20/"))]" can be modified in several ways
"timestamp:2016-02-20/" -- Shows all edits edited after date
"timestamp:2016-02-20/2016-02-22" -- Shows all edits after 02-20 but before 02-22
"timestamp:2016-02/ Day and Month can be removed to widen the range of edits shown, example here shows all edits starting in FEB2016.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So, a timestamped search would look like this:

*[osm_user_name() == "IndianaJones737"][eval(JOSM_search("timestamp:2016-03-14/2016-03-15"))] {
  casing-width: 10;
  casing-color: green;
  casing-opacity: 0.2;
}

-- set .aaron; -> this is setting the class for this statement. This allows us to call it out later on. Classes
can be set like that or as so -> set aaron;

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

way.aaron, & node.aaron,

-- This shows that we are looking for all ways/nodes which meet the "aaron" class. The comma here denotes
that there is another selector we would like to call out after "aaron"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


{
  z-index: -10;
  casing-color: lime;
  casing-width: 10;
  casing-opacity: 0.3;


}

-- This is our code block which will style up whatever we called out as a selector

*/

/* Create Settings */


/* User Settings */

%s




/* Tracking Selectors -- Way and node style BEFORE they are uploaded */

node:modified::modified_layer {
    symbol-shape: %s;
    symbol-size: %s;
    symbol-stroke-color: %s;
    symbol-stroke-width: 3px;
    symbol-fill-opacity: 0.5;
    z-index: -5;
}

way:modified::modified_layer,
node:modified < way::modified_layer {
    width: 6;
    color: transparent;
    opacity: 0;
    casing-width: %s;
    casing-color: %s;
    casing-opacity: 0.7;
    z-index: -5;
}

/* QC Styles */


/* User specific styles */

%s


/* This is how you search for someone with a space in their name

*[osm_user_name() == "Hector Vector"))] {
  set .jman;
}

*/

/* Styling of ways and nodes once they belong to "history" for each individual user */


%s
/*NODESTYLE*/

%s


node:selected::selected_layer {
    symbol-shape: circle;
    symbol-size: 22;
    symbol-stroke-color: #DF2E08;
    symbol-stroke-width: 3px;
    symbol-fill-opacity: 0.5;
    z-index: -5;
}""" % (
            self.TITLEENTRYBLOCK,
            self.SETUPENTRYBLOCK,
            self.TEAMICONSHAPE,
            self.ICONSIZE,
            self.TEAMNODECOLORTEXT,
            self.LINEWIDTH,
            self.TEAMLINECOLORTEXT,
            self.SETTINGBLOCK,
            self.WAYENTRYBLOCK,
            self.NODEENTRYBLOCK,
        )  # noqa: E501

        if ISPUSH != True:
            if path.strip():
                with open(path, "w+") as OUT:
                    OUT.writelines(OUTPUT)
        else:
            self.OUTPUSHTEXT = OUTPUT

    ##############################################################################

    def CLEAR_clicked(self):
        try:
            self.NRSELECT = ""
            self.EDITORNAME.setText("")
            self.EDITORID.setText("")
            self.EDITORID.repaint()
            self.EDITORNAME.repaint()
            self.ADD.setText("ADD")
            self.ADD.repaint()
            self.SELTEXT = ""
            self.pix.fill(QColor(self.WHITE))
            self.EDITORNODECOLORICON.setPixmap(self.pix)
            self.EDITORLINECOLORICON.setPixmap(self.pix)
            self.EDITORNODECOLORICON.repaint()
            self.EDITORLINECOLORICON.repaint()
            self.TEMPEDITORICONSHAPE = ""

        except Exception as e:
            logger.exception(e)

    def REMOVE_clicked(self):
        self.dialog = QMessageBox.question(
            self,
            "PyQt5 message",
            "Are you sure you want to remove this editor?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if self.dialog == QMessageBox.Yes:
            one.REMOVE_GO()

    def REMOVEALL_clicked(self):
        self.GOREMOVEALL = True
        self.dialog = QMessageBox.question(
            self,
            "PyQt5 message",
            "Are you sure you want to remove all editors?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if self.dialog == QMessageBox.Yes:
            one.REMOVEALL_GO()

    def REMOVEALL_GO(self):
        try:
            self.usercount = 0
            self.ADDUSERS = []
            self.TEMPUSERS = {}
            self.pix.fill(QColor(self.WHITE))
            self.TEAMNODECOLORICON.setPixmap(self.pix)
            self.TEAMLINECOLORICON.setPixmap(self.pix)
            self.TEAMLINEWIDTHSPIN.setValue(0)
            self.TEAMICONSIZESPIN.setValue(0)
            self.TEAMNAME.setText("")
            self.TEAMNAME.repaint()
            self.TEAMNODECOLORICON.repaint()
            self.TEAMLINECOLORICON.repaint()
            for i in range(0, 50):
                self.GEMarray[i][0] = str("")
                self.GEMarray[i][1] = str("")
                self.GEMarray[i][2] = QtGui.QColor(clear)
                self.GEMarray[i][3] = QtGui.QColor(clear)
            self.GOREMOVEALL = False
        except Exception as e:
            logger.exception(e)

    def REMOVE_GO(self):
        for ix in self.TABLE.selectedIndexes():
            column = ix.column()
            dat = ix.data()
            row = ix.row()
            if dat is not None:
                self.NRSELECT = row
            else:
                self.NRSELECT = ""
            try:
                self.ADDUSERS[int(self.NRSELECT)] = ""

            except Exception as e:
                logger.exception(e)
            try:
                self.TEMPUSERS[str(self.NRSELECT)] = 0
            except Exception as e:
                logger.exception(e)
            self.GEMarray[self.NRSELECT][0] = str("")
            self.GEMarray[self.NRSELECT][1] = str("")
            self.GEMarray[self.NRSELECT][2] = QtGui.QColor(clear)
            self.GEMarray[self.NRSELECT][3] = QtGui.QColor(clear)
            self.NRSELECT = ""
            self.usercount -= 1

    def SETNR(self):
        for ix in self.TABLE.selectedIndexes():
            column = ix.column()
            dat = ix.data()
            row = ix.row()
            if dat != "":
                self.NRSELECT = row
            else:
                self.NRSELECT = ""

    def EDIT_clicked(self):
        for ix in self.TABLE.selectedIndexes():
            column = ix.column()
            dat = ix.data()
            row = ix.row()
            if dat != "":
                self.NRSELECT = row

                self.ADD.setText("UPDATE")
                self.ADD.repaint()
            else:
                self.NRSELECT = ""
        if self.NRSELECT != "":
            if type(self.TEMPUSERS[str(self.NRSELECT)]) != str:
                self.GOEDIT = True
                self.EDITORNAME.setText(self.TEMPUSERS[str(self.NRSELECT)].NAME)
                self.EDITORID.setText(self.TEMPUSERS[str(self.NRSELECT)].UID)
                self.EDITORNAME.repaint()
                self.EDITORID.repaint()
                self.pix.fill(QColor(self.TEMPUSERS[str(self.NRSELECT)].NODECOLORUI))
                self.EDITORNODECOLORICON.setPixmap(self.pix)
                self.EDITORNODECOLORICON.repaint()
                self.pix.fill(QColor(self.TEMPUSERS[str(self.NRSELECT)].LINECOLORUI))
                self.EDITORLINECOLORICON.setPixmap(self.pix)
                self.EDITORLINECOLORICON.repaint()
                self.GETEDITORSHAPETEXT()
                self.EDITORLINEWIDTHSPIN.setValue(
                    int(self.TEMPUSERS[str(self.NRSELECT)].LINEWIDTH)
                )
                self.EDITORNODESIZESPIN.setValue(
                    int(self.TEMPUSERS[str(self.NRSELECT)].ICONSIZE)
                )
                self.EDITORLINEWIDTHSPIN.repaint()
                self.EDITORNODESIZESPIN.repaint()
                self.EDITORSELECT = self.NRSELECT

    @staticmethod
    def get_index_parsed_users(parsed_users: dict, user_key: str) -> str:
        """
        Parse a user dict to find the index key. It assumes that the user_key
        is unique in the dict. The primary purpose is if someone used different
        methods for determining the `set .class` in the mapcss file.
        """
        if user_key in parsed_users:
            return user_key
        for user in parsed_users:
            for key in parsed_users[user]:
                if parsed_users[user][key] == user_key:
                    return user
        return None

    @staticmethod
    def parse_team_from_mapcss(mapcss_text: str) -> str:
        title = re.findall(r"title: \"(.*?)\"", mapcss_text)
        title = title[0] if isinstance(title, list) else title
        teamname = re.findall(r".*For\s?(.*?)\s?Team.*?", title) if title else None
        teamname = teamname[0] if isinstance(teamname, list) else teamname
        return teamname

    @staticmethod
    def parse_users_from_mapcss(mapcss_text: str, parsed_users: dict = {}) -> dict:
        for i in re.finditer(
            r"\*\s*(\[\s*osm_user_name\s*\(\s*\)|\[\s*setting\(\s*\"user_.*?\"\s*\)).*?}",  # noqa: E501
            mapcss_text,
        ):
            temp = i.group()
            username = re.findall(r"osm_user_name\(\)\s*==\s*\\?\"?(.*?)\\?\"?\"", temp)
            if len(username) != 1:
                username = re.findall(r"user:\\?\"?(.*?)\\?\"?\"", temp)
            personname = re.findall(r"setting\(\s*\"user_(.*?)\"", temp)
            if len(username) == 1 and len(personname) == 1:
                parsed_users[username[0]] = {"name": personname[0]}
        return parsed_users

    @staticmethod
    def parse_line_colors_from_mapcss(mapcss_text: str, parsed_users: dict) -> dict:
        """
        This method parses way information from a mapcss file.
        >>> mapcss = "way.Dain { z-index: -10; casing-color: #B108D6; casing-width: 7; casing-opacity: 0.6; }"
        >>> MAINWindow.parse_line_colors_from_mapcss(mapcss, {})
        Traceback (most recent call last):
            ...
        MapCSSParseException: Unknown user: Dain
        >>> users = {"Dain": {}}
        >>> MAINWindow.parse_line_colors_from_mapcss(mapcss, users)
        {'Dain': {'casing-color': '#B108D6', 'casing_width': '7'}}
        """
        WAYSETTINGSBLOCK = re.findall(r"way\..*?}", mapcss_text)
        for i in WAYSETTINGSBLOCK:
            color = re.findall(r"casing-color:\s*([#A-Za-z0-9]+)\s*;", i)[0]
            width = re.findall(r"casing-width:\s*([0-9px]+)\s*;", i)[0]
            for user in re.findall(r"way\.(.*?)\s*[,{]", i):
                # MAINWindow since this is the current class...
                key = MAINWindow.get_index_parsed_users(parsed_users, user)
                if key in parsed_users:
                    parsed_users[key]["casing-color"] = color
                    parsed_users[key]["casing_width"] = width
                else:
                    logger.debug(WAYSETTINGSBLOCK)
                    logger.debug(parsed_users)
                    raise MapCSSParseException(
                        "Unknown user: " + user,
                        exception_type=MapCSSParseExceptionType.UNKNOWN_USER,
                    )
        return parsed_users

    @staticmethod
    def parse_node_colors_from_mapcss(mapcss_text: str, parsed_users: dict) -> dict:
        """
        This method parses node information from a mapcss file.
        >>> mapcss = "node.Aaron { symbol-size: 15; symbol-shape: triangle; symbol-stroke-color: blue; symbol-stroke-width: 3px; symbol-fill-opacity: 0.5; z-index: -5; }"
        >>> MAINWindow.parse_node_colors_from_mapcss(mapcss, {})
        Traceback (most recent call last):
            ...
        MapCSSParseException: Unknown user: Aaron
        >>> users = {"Aaron": {}}
        >>> MAINWindow.parse_node_colors_from_mapcss(mapcss, users)
        {'Aaron': {'symbol-size': '15', 'symbol-shape': 'triangle', 'symbol-stroke-color': 'blue', 'symbol-stroke-width': '3px'}}
        """
        NODESETTINGSBLOCK = re.findall(r"node\..*?}", mapcss_text)
        for i in NODESETTINGSBLOCK:
            size = re.findall(r"symbol-size:\s*([0-9px]+)\s*;", i)[0]
            shape = re.findall(r"symbol-shape:\s*([#A-Za-z0-9]+)\s*;", i)[0]
            color = re.findall(r"symbol-stroke-color:\s*([#A-Za-z0-9]+)\s*;", i)[0]
            width = re.findall(r"symbol-stroke-width:\s*([0-9px]+)\s*;", i)[0]
            for user in re.findall(r"node\.(.*?)\s*[,{]", i):
                # MAINWindow since this is the current class...
                key = MAINWindow.get_index_parsed_users(parsed_users, user)
                if key in parsed_users:
                    parsed_users[key]["symbol-size"] = size
                    parsed_users[key]["symbol-shape"] = shape
                    parsed_users[key]["symbol-stroke-color"] = color
                    parsed_users[key]["symbol-stroke-width"] = width
                else:
                    logger.debug(NODESETTINGSBLOCK)
                    logger.debug(parsed_users)
                    raise MapCSSParseException(
                        "Unknown user: " + user,
                        exception_type=MapCSSParseExceptionType.UNKNOWN_USER,
                    )
        return parsed_users

    def parse_mapcss_text(self, INFILETEXT: str) -> dict:
        # parsed_users = {user_class: {name: user_name, ...}}
        parsed_users = {}
        original_text = str(INFILETEXT)
        # Remove all comments from the original text (this just makes some
        # regexes easier). While the replaces/substitutions could be squashed
        # together, this is more readable in my opinion
        text_no_newline = original_text.replace("\n", " ")
        text_no_newline = re.sub(
            r"//.*?\n",
            "",
            re.sub(r"//.*?\\n", " ", re.sub(r"/\*.*?\*/", " ", text_no_newline)),
        )

        self.TEAMNAME.setText(self.parse_team_from_mapcss(text_no_newline))

        parsed_users = self.parse_users_from_mapcss(
            text_no_newline, parsed_users=parsed_users
        )

        self.TEAMLINECOLORTEXT = re.findall(
            r"way:modified.*?casing-color:\s?([#0-9A-Za-z]*)", text_no_newline
        )
        self.TEAMLINECOLORTEXT = (
            self.TEAMLINECOLORTEXT[0]
            if isinstance(self.TEAMLINECOLORTEXT, list)
            else self.TEAMLINECOLORTEXT
        )
        self.TEAMNODECOLORTEXT = re.findall(
            r"node:modified.*?symbol-stroke-color:\s?([#0-9A-Za-z]*)", text_no_newline,
        )
        self.TEAMNODECOLORTEXT = (
            self.TEAMNODECOLORTEXT[0]
            if isinstance(self.TEAMNODECOLORTEXT, list)
            else self.TEAMNODECOLORTEXT
        )
        self.TEAMLINECOLORUI = QtGui.QColor(self.TEAMLINECOLORTEXT)
        self.TEAMNODECOLORUI = QtGui.QColor(self.TEAMNODECOLORTEXT)
        self.LINEWIDTH = re.findall(
            r"way:modified.*?casing-width\s?:\s?([0-9px]+)", text_no_newline
        )
        self.LINEWIDTH = (
            self.LINEWIDTH[0] if isinstance(self.LINEWIDTH, list) else self.LINEWIDTH
        )
        self.ICONSIZE = re.findall(
            r"node:modified.*?symbol-size:\s?([0-9px]+)", text_no_newline
        )
        self.ICONSIZE = (
            self.ICONSIZE[0] if isinstance(self.ICONSIZE, list) else self.ICONSIZE
        )
        self.TEAMICONSHAPE = re.findall(
            r"node:modified.*?symbol-shape:\s?([a-zA-Z]+)", text_no_newline
        )
        self.TEAMICONSHAPE = (
            self.TEAMICONSHAPE[0]
            if isinstance(self.TEAMICONSHAPE, list)
            else self.TEAMICONSHAPE
        )

        parsed_users = self.parse_line_colors_from_mapcss(text_no_newline, parsed_users)
        parsed_users = self.parse_node_colors_from_mapcss(text_no_newline, parsed_users)

        return parsed_users

    def construct_table(self, parsed_users: dict):
        for user in parsed_users:
            CONSTRUCTOR = str(self.usercount)
            CONSTRUCTOR = EDITORINFO()
            NAME = parsed_users[user]["name"]
            CONSTRUCTOR.NAME = NAME
            CONSTRUCTOR.UID = user
            CONSTRUCTOR.LINECOLORUI = QtGui.QColor(parsed_users[user]["casing-color"])
            CONSTRUCTOR.NODECOLORUI = QtGui.QColor(
                parsed_users[user]["symbol-stroke-color"]
            )
            CONSTRUCTOR.LINECOLORTEXT = parsed_users[user]["casing-color"]
            CONSTRUCTOR.NODECOLORTEXT = parsed_users[user]["symbol-stroke-color"]
            CONSTRUCTOR.ICONSIZE = parsed_users[user]["symbol-size"]
            CONSTRUCTOR.LINEWIDTH = parsed_users[user]["symbol-stroke-width"]
            CONSTRUCTOR.ICONSHAPE = parsed_users[user]["symbol-shape"]
            self.TEMPUSERS[str(self.usercount)] = CONSTRUCTOR
            self.ADDUSERS.append(CONSTRUCTOR)
            self.GEMarray[self.usercount][0] = str(CONSTRUCTOR.NAME)
            self.GEMarray[self.usercount][1] = str(CONSTRUCTOR.UID)
            self.GEMarray[self.usercount][2] = QtGui.QColor(CONSTRUCTOR.LINECOLORUI)
            self.EDITORNODECOLORDISPLAY(self.usercount)
            self.pix.fill(QColor(self.TEAMNODECOLORUI))
            self.TEAMNODECOLORICON.setPixmap(self.pix)
            self.TEAMNODECOLORICON.repaint()
            self.TEAMLINEWIDTHSPIN.setValue(int(self.LINEWIDTH))
            self.TEAMICONSIZESPIN.setValue(int(self.ICONSIZE))
            self.pix.fill(QColor(self.TEAMLINECOLORUI))
            self.TEAMLINECOLORICON.setPixmap(self.pix)
            self.TEAMLINECOLORICON.repaint()
            self.usercount += 1
            self.TABLE.resizeRowsToContents()
            self.TABLE.resizeColumnsToContents()
            self.GETTEAMSHAPETEXT()

    def IMPULLGO(self, PULL):
        parsed_users = self.parse_mapcss_text(str(PULL))
        self.construct_table(parsed_users)

    def IMPORTGO(self):
        try:
            infile = QtWidgets.QFileDialog.getOpenFileName(
                self, self.filters, self.output_file_dir, self.select_filters
            )
            infile = str(infile[0])
            global INKML
            with open(infile, "r+") as reader:
                infile_text = reader.read()
        except Exception as e:
            logger.exception(e)
        try:
            self.IMPORT_clicked(infile_text)
        except Exception as e:
            logger.exception(e)

    def IMPORT_clicked(self, PULL):
        parsed_users = self.parse_mapcss_text(str(PULL))
        self.construct_table(parsed_users)

    def EDITORNODECOLORDISPLAY(self, count):

        if self.TEMPUSERS[str(count)].ICONSHAPE == "Circle":
            pixmap = QtGui.QPixmap(self.CIRCLE)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "Square":
            pixmap = QtGui.QPixmap(self.SQUARE)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "Triangle":
            pixmap = QtGui.QPixmap(self.TRIANGLE)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "Pentagon":
            pixmap = QtGui.QPixmap(self.PENTAGON)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "Hexagon":
            pixmap = QtGui.QPixmap(self.HEXAGON)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "Heptagon":
            pixmap = QtGui.QPixmap(self.HEPTAGON)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "Octagon":
            pixmap = QtGui.QPixmap(self.OCTAGON)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "Nonagon":
            pixmap = QtGui.QPixmap(self.NONAGON)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)

            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "Decagon":
            pixmap = QtGui.QPixmap(self.DECAGON)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon


# ################################   MAIN LOOP   ########################### #
def main(args):
    parser = argparse.ArgumentParser(description="Modify MapCSS files for QC purposes")
    parser.add_argument(
        "--test", action="store_true", required=False, help="Run doctests"
    )
    parser.add_argument(
        "-f", "--file", required=False, help="A file to open the program with"
    )
    parsed_args = parser.parse_args()
    if parsed_args.test:
        import doctest

        doctest.testmod()
    else:
        app = QtWidgets.QApplication(args)
        global one
        one = MAINWindow()
        one.show()
        if parsed_args.file is not None:
            mapcss_file = parsed_args.file
            if isinstance(mapcss_file, str):
                mapcss_file = [mapcss_file]
            for mfile in mapcss_file:
                with open(mfile, "r") as f:
                    one.IMPORT_clicked(f.read())
        sys.exit(app.exec_())
        if self.EXIT == 1:
            sys.exit(0)
        sys._excepthook = sys.excepthook
        sys.excepthook = exception_hook


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    try:
        sys._excepthook(exctype, value, traceback)
    except Exception as error:
        logger.exception(error)
    sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
