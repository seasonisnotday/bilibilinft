import sys,requests,json,time,webbrowser,os,re

from selenium import webdriver
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime, QObject,Qt
from PyQt5.QtGui import QBrush, QColor, QFont,QPalette,QPixmap,QPainter,QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from pypinyin import pinyin
from urllib import request
from tkinter import messagebox

import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}
mmm=[]
ind_dict = {"key": "-1"}
subject_idurl='https://api.bilibili.com/x/garb/card/subject/list?subject_id=42'
try:
    req = requests.get(subject_idurl, headers=header).text
    print(req)
    dicts = json.loads(req)
    for i in range(0,10000):
        act_id=dicts['data']['subject_card_list'][i]['act_id']
        act_name=dicts['data']['subject_card_list'][i]['act_name']
        act_pic=dicts['data']['subject_card_list'][i]['act_pic']+'@328w_440h_1c.webp'
        act=[str(act_id),act_name,act_pic]
        print(str(act))
        mmm.append(act)
except:
    pass
print(mmm)
class MyThread(QThread):
    def __int__(self):
        super.__init__()
    def run(self):
        try:
            fileName =re.sub('[\/:*?"<>|]', '-', mmm[int(ind_dict['key'])][1])
            os.mkdir(fileName)
            os.startfile(fileName)
            base_url = r'https://api.bilibili.com/x/vas/dlc_act/act/item/list?act_id=' + str(mmm[int(ind_dict['key'])][0])
            jsons = requests.get(base_url, headers=header).text
            dicts = json.loads(jsons)
            for i in range(0, 100, 1):
                uidlist = dicts['data']['item_list'][i]['card_item']['card_name']
                try:
                    data = dicts['data']['item_list'][i]['card_item']['video_list'][0]
                    print(data)
                    req = requests.get(url=data, verify=False, headers=header)
                    filename ='./'+fileName+'/' + uidlist + '.mp4'
                    with open(filename, 'ab') as f:
                        f.write(req.content)
                    f.flush()
                    time.sleep(1)
                except:
                    pic = dicts['data']['item_list'][i]['card_item']['card_img']
                    request.urlretrieve(pic, './' +fileName+'/' + uidlist + '.png')
                    print(i + 1, uidlist)
                    time.sleep(1)
        except:
            messagebox.showinfo('','下载完成，请重新选择')
class Window(QMainWindow):
    def __init__(self,parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('收藏集图片下载 第一版')
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)

        self.pixmap = QPixmap()
        image_url = "https://i0.hdslb.com/bfs/garb/item/a49fe98adbefe6f03b18f538db696c504eb1ae4a.png@90w_90h.webp"
        req = requests.get(image_url, headers=header)
        self.pixmap.loadFromData(req.content)
        self.setWindowIcon(QIcon(self.pixmap))

        self.setGeometry(1000, 500, 770, 550)
        self.setFixedSize(770, 550)
        self.setupUi(self)
    def setupUi(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 50, 328, 440))
        self.label.setStyleSheet("background-color: rgb(150, 150, 150);")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("请选择收藏集")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(400, 50, 330, 50))
        self.comboBox.addItem("点击此按钮选择")
        for i in range(0, len(mmm)):
            self.comboBox.addItem("")
        for i in range(0, len(mmm)):
            self.comboBox.setItemText(i + 1, mmm[i][1])
        self.comboBox.setCurrentIndex(0)
        self.comboBox.setMaxVisibleItems(22)
        self.comboBox.currentIndexChanged.connect(self.select_change)

        self.pushButton1 = QtWidgets.QPushButton(self)
        self.pushButton1.setGeometry(QtCore.QRect(400, 110, 150, 50))
        self.pushButton1.setStyleSheet("background-color:rgb(0,255,255)")
        self.pushButton1.setText("首字母a-z排序")
        self.pushButton1.clicked.connect(lambda:self.mingc(False))
        self.pushButton1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.pushButton2 = QtWidgets.QPushButton(self)
        self.pushButton2.setGeometry(QtCore.QRect(580, 110, 150, 50))
        self.pushButton2.setStyleSheet("background-color:rgb(0,255,255)")
        self.pushButton2.setText("首字母z-a排序")
        self.pushButton2.clicked.connect(lambda:self.mingc(True))
        self.pushButton2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.pushButtonxz = QtWidgets.QPushButton(self)
        self.pushButtonxz.setGeometry(QtCore.QRect(400, 170, 328, 50))
        self.pushButtonxz.setStyleSheet("background-color:rgb(0,255,255)")
        self.pushButtonxz.setText("下载")
        self.pushButtonxz.clicked.connect(self.handleDisplay)
        self.pushButtonxz.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setGeometry(QtCore.QRect(400, 240, 328, 50))
        self.label1.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label1.setStyleSheet("background-color:rgba(0,200,255,255)")
        font = self.label.font()
        font.setBold(True)#加粗
        font.setPointSize(18)
        self.label1.setFont(font)
        self.label1.setText('作者@你看清楚了吗')
        self.label1.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setGeometry(QtCore.QRect(600, 290, 128, 200))
        self.label2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label2.setStyleSheet("background-color:rgba(0,200,255,255)")
        font = self.label.font()
        font.setBold(True)#加粗
        font.setPointSize(14)
        self.label2.setFont(font)
        self.label2.setText('点击直达\n←———')
        self.label2.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(400,290, 200, 200))
        self.pushButton.setStyleSheet("background-color:rgba(255,255,255,255)")
        self.pixmap = QPixmap()
        image_url = "https://i2.hdslb.com/bfs/face/1f48fcebf4e8f6de510eaf83e4d42b898fe5e69c.jpg@200w_200h_1c.webp"
        req = requests.get(image_url, headers=header)
        self.pixmap.loadFromData(req.content)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setIconSize(QtCore.QSize(200, 200))
        icon = QtGui.QIcon()
        icon.addPixmap(self.pixmap)
        self.pushButton.setIcon(icon)
        self.pushButton.clicked.connect(self.dak)

        MainWindow.setCentralWidget(self.centralwidget)

    def select_change(self, index):
        for i in range(0,len(mmm)):
            if index == i+1:
                ind_dict["key"] =str(i)
                self.pixmap = QPixmap()
                image_url =mmm[i][2]
                req = requests.get(image_url, headers=header)
                self.pixmap.loadFromData(req.content)
                self.label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.label.setPixmap(self.pixmap)
    def mingc(self,reverse):
        mmm.sort(key=lambda x:pinyin(x[1]), reverse=reverse)
        for i in range(0,len(mmm)):
            self.comboBox.setItemText(i + 1, mmm[i][1])
        self.comboBox.setCurrentIndex(0)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("请选择收藏集")

    def handleDisplay(self):
        if ind_dict['key']=='-1':
            messagebox.showerror('','请先选择')
        else:
            self.my_thread=MyThread()
            self.my_thread.start()
            self.label.setText("请耐心等待")
    def dak(self):
        newurl='https://space.bilibili.com/353403349'
        webbrowser.open(newurl, new=1, autoraise=True)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

