# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PdVisualization.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1413, 822)
        mainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 20, 551, 741))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.graphicsView = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView.setGeometry(QtCore.QRect(20, 90, 511, 361))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView_3.setGeometry(QtCore.QRect(20, 540, 511, 171))
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_5.setGeometry(QtCore.QRect(20, 450, 511, 71))
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox_5)
        self.horizontalSlider.setGeometry(QtCore.QRect(20, 10, 421, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label = QtWidgets.QLabel(self.groupBox_5)
        self.label.setGeometry(QtCore.QRect(450, 10, 59, 16))
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox_5)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(90, 30, 311, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolButton_pause = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.toolButton_pause.setObjectName("toolButton_pause")
        self.horizontalLayout.addWidget(self.toolButton_pause)
        self.time_P = QtWidgets.QLabel(self.groupBox_5)
        self.time_P.setGeometry(QtCore.QRect(440, 40, 41, 17))
        self.time_P.setObjectName("time_P")
        self.entry_flist_1 = QtWidgets.QPlainTextEdit(self.groupBox)
        self.entry_flist_1.setEnabled(True)
        self.entry_flist_1.setGeometry(QtCore.QRect(20, 30, 481, 31))
        self.entry_flist_1.setLineWidth(1)
        self.entry_flist_1.setMidLineWidth(0)
        self.entry_flist_1.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        self.entry_flist_1.setCenterOnScroll(True)
        self.entry_flist_1.setObjectName("entry_flist_1")
        self.btn_flist_1 = QtWidgets.QPushButton(self.groupBox)
        self.btn_flist_1.setGeometry(QtCore.QRect(500, 30, 31, 31))
        self.btn_flist_1.setObjectName("btn_flist_1")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(19, 89, 511, 361))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.vbox = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setObjectName("vbox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(550, 20, 531, 741))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.groupBox_2)
        self.graphicsView_2.setGeometry(QtCore.QRect(20, 90, 491, 361))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.graphicsView_4 = QtWidgets.QGraphicsView(self.groupBox_2)
        self.graphicsView_4.setGeometry(QtCore.QRect(20, 540, 491, 171))
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.groupBox_12 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_12.setGeometry(QtCore.QRect(20, 450, 491, 71))
        self.groupBox_12.setTitle("")
        self.groupBox_12.setObjectName("groupBox_12")
        self.horizontalSlider_HC = QtWidgets.QSlider(self.groupBox_12)
        self.horizontalSlider_HC.setGeometry(QtCore.QRect(20, 10, 401, 22))
        self.horizontalSlider_HC.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_HC.setObjectName("horizontalSlider_HC")
        self.label_13 = QtWidgets.QLabel(self.groupBox_12)
        self.label_13.setGeometry(QtCore.QRect(430, 10, 59, 16))
        self.label_13.setObjectName("label_13")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_12)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(90, 30, 311, 41))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.toolButton_pause_HC = QtWidgets.QToolButton(self.horizontalLayoutWidget_4)
        self.toolButton_pause_HC.setObjectName("toolButton_pause_HC")
        self.horizontalLayout_4.addWidget(self.toolButton_pause_HC)
        self.time_HC = QtWidgets.QLabel(self.groupBox_12)
        self.time_HC.setGeometry(QtCore.QRect(420, 40, 51, 20))
        self.time_HC.setObjectName("time_HC")
        self.entry_flist_5 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.entry_flist_5.setEnabled(True)
        self.entry_flist_5.setGeometry(QtCore.QRect(20, 30, 461, 31))
        self.entry_flist_5.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        self.entry_flist_5.setObjectName("entry_flist_5")
        self.btn_flist_5 = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_flist_5.setGeometry(QtCore.QRect(480, 30, 31, 31))
        self.btn_flist_5.setObjectName("btn_flist_5")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_2)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(19, 89, 491, 361))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.vbox_HC = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.vbox_HC.setContentsMargins(0, 0, 0, 0)
        self.vbox_HC.setObjectName("vbox_HC")
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(1150, 40, 181, 51))
        self.btn_start.setObjectName("btn_start")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(1110, 130, 271, 601))
        self.textBrowser.setObjectName("textBrowser")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1413, 27))
        self.menubar.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "PD Walking Pattern Visualization"))
        self.groupBox.setTitle(_translate("mainWindow", "Patient"))
        self.label.setText(_translate("mainWindow", "Timer"))
        self.toolButton_pause.setText(_translate("mainWindow", "o"))
        self.time_P.setText(_translate("mainWindow", "00:00"))
        self.btn_flist_1.setText(_translate("mainWindow", "..."))
        self.groupBox_2.setTitle(_translate("mainWindow", "Health Control"))
        self.label_13.setText(_translate("mainWindow", "Timer"))
        self.toolButton_pause_HC.setText(_translate("mainWindow", "o"))
        self.time_HC.setText(_translate("mainWindow", "00:00"))
        self.btn_flist_5.setText(_translate("mainWindow", "..."))
        self.btn_start.setText(_translate("mainWindow", "Start Visualization"))
        self.textBrowser.setHtml(_translate("mainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.75385pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px;\"><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt; font-weight:600;\">Instruction</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px; font-family:\'Helvetica Neue\'; font-size:8pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px;\"><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt;\">This tool is used for visualizing human walking pattern. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px;\"><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt;\">The position data for animation is computed according to Accelerometer and Gyroscope data from sensors.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px; font-family:\'Helvetica Neue\'; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px;\"><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt;\">In signal display: </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px;\"><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt;\">3-color line is displaying the accelerometer data in coordinate axis.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px;\"><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt; font-weight:600; color:#bd180f;\">Red</span><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt;\"> is for </span><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt; font-weight:600; color:#bd180f;\">X</span><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt;\"> axis.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px;\"><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt; font-weight:600; color:#2315c1;\">Blue </span><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt;\">is for </span><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt; font-weight:600; color:#2315c1;\">Y</span><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt;\"> axis. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px;\"><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt; font-weight:600; color:#108e1e;\">Green</span><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt;\"> is for </span><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt; font-weight:600; color:#108e1e;\">Z</span><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt;\"> axis.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px; font-family:\'Helvetica Neue\'; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px;\"><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt; font-weight:600;\">Usage</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px;\"><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt;\">You could adjust  the angle of view with your mouse clicked in the animation viewport.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px;\"><span style=\" font-family:\'Helvetica Neue\'; font-size:8pt;\">You could rewind, pause or fast forward the process using Timer panel.</span><span style=\" font-family:\'.SF NS Text\'; font-size:8pt;\"> </span></p></body></html>"))
