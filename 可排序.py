import sys,requests,json,time,webbrowser,os,re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime, QObject,Qt,QTimer
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
titlepicurl = "https://i0.hdslb.com/bfs/garb/item/a49fe98adbefe6f03b18f538db696c504eb1ae4a.png@90w_90h.webp"
titlepicshow = requests.get(titlepicurl, headers=header)
mmm=[]
nnn = []
mmmdict = {"key": "-1"}
nnndict = {"key": "-1"}
subject_idurl='https://api.bilibili.com/x/garb/card/subject/list?subject_id=42'
try:
    actj_sons = requests.get(subject_idurl, headers=header).text
    act_dicts = json.loads(actj_sons)
    for i in range(0,10000):
        act_id=act_dicts['data']['subject_card_list'][i]['act_id']
        act_name=act_dicts['data']['subject_card_list'][i]['act_name']
        act_pic=act_dicts['data']['subject_card_list'][i]['act_pic']+'@328w_440h_1c.webp'
        mmm.append([int(i),str(act_id),act_name,act_pic])
except:
    pass
class MyThread(QThread):
    def __int__(self):
        super.__init__()
    def run(self):
        j = int(mmmdict['key'])
        try:
            fileName =re.sub('[:*?"<>|]', '-', mmm[j][2])
            os.mkdir(fileName)
            os.startfile(fileName)
            eachpic_url = r'https://api.bilibili.com/x/vas/dlc_act/act/item/list?act_id=' + str(mmm[j][1])
            eachpic_jsons = requests.get(eachpic_url, headers=header).text
            eachpic_dicts = json.loads(eachpic_jsons)
            for i in range(0, 10000):
                card_name = eachpic_dicts['data']['item_list'][i]['card_item']['card_name']
                try:
                    data = eachpic_dicts['data']['item_list'][i]['card_item']['video_list'][0]
                    video = requests.get(url=data, verify=False, headers=header)
                    filename = './' + fileName + '/' + card_name + '.mp4'
                    with open(filename, 'ab') as f:
                        f.write(video.content)
                    f.flush()
                    time.sleep(1)
                except:
                    pic = eachpic_dicts['data']['item_list'][i]['card_item']['card_img']
                    request.urlretrieve(pic, './' + fileName + '/' + card_name + '.png')
                    print(i + 1, card_name)
                    time.sleep(1)

        except:
            messagebox.showinfo('',fileName+'下载完成，请重新选择')
            mmmdict['key'] = '-1'
class NewMyThread(QThread):
    def __int__(self):
        super.__init__()
    def run(self):

        os.startfile(os.getcwd())
        i = int(nnndict['key'])
        card_name = nnn[i][1]
        try:
            data = nnn[i][2]
            video = requests.get(url=data, verify=False, headers=header)
            filename ='./' + card_name + '.mp4'
            with open(filename, 'ab') as f:
                f.write(video.content)
            f.flush()
            time.sleep(1)
        except:
            pic = nnn[i][3]
            request.urlretrieve(pic, './' + card_name + '.png')
            print(i + 1, card_name)
            time.sleep(1)
        messagebox.showinfo('',card_name+'下载完成，请重新选择')
        nnndict['key'] = '-1'
class Window(QMainWindow):
    def __init__(self,parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('收藏集图片下载 第二版')

        self.titlepic = QPixmap()
        self.titlepic.loadFromData(titlepicshow.content)
        self.setWindowIcon(QIcon(self.titlepic))

        self.setGeometry(1000, 500, 770, 550)
        self.setFixedSize(770, 550)

        self.centralwidget = QtWidgets.QWidget(self)

        self.label_card = QtWidgets.QLabel(self.centralwidget)
        self.label_card.setGeometry(QtCore.QRect(50, 50, 328, 440))
        self.label_card.setStyleSheet("background-color: rgb(150, 150, 150);")
        self.label_card.setAlignment(Qt.AlignCenter)
        self.label_card.setText("请选择收藏集")

        self.select_Box = QtWidgets.QComboBox(self.centralwidget)
        self.select_Box.setGeometry(QtCore.QRect(400, 50, 330, 50))
        self.select_Box.addItem("点击此按钮选择")
        for i in range(0, len(mmm)):
            self.select_Box.addItem("")
        for i in range(0, len(mmm)):
            self.select_Box.setItemText(i + 1, mmm[i][2])
        self.select_Box.setCurrentIndex(0)
        self.select_Box.setMaxVisibleItems(22)
        self.select_Box.currentIndexChanged.connect(self.select_change)

        self.btn_moren = QtWidgets.QPushButton(self)
        self.btn_moren.setGeometry(QtCore.QRect(400, 110, 150, 50))
        self.btn_moren.setText("默认排序")
        self.btn_moren.clicked.connect(self.moren_sort)
        self.btn_moren.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.moren=False

        self.btn_a_z= QtWidgets.QPushButton(self)
        self.btn_a_z.setGeometry(QtCore.QRect(580, 110, 150, 50))
        self.btn_a_z.setText("首字母排序")
        self.btn_a_z.clicked.connect(self.a_z_sort)
        self.btn_a_z.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.a_z = False

        self.btn_xiazai = QtWidgets.QPushButton(self)
        self.btn_xiazai.setGeometry(QtCore.QRect(400, 170, 328, 50))
        self.btn_xiazai.setText("全部下载")
        self.btn_xiazai.clicked.connect(self.handleDisplay)
        self.btn_xiazai.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.btn_each = QtWidgets.QPushButton(self)
        self.btn_each.setGeometry(QtCore.QRect(400,230, 328, 50))
        self.btn_each.setText("逐个下载")
        self.btn_each.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_each.clicked.connect(self.open_new_window)

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setGeometry(QtCore.QRect(400, 340, 328, 50))
        self.label1.setTextInteractionFlags(Qt.TextSelectableByMouse)
        font = self.label1.font()
        font.setBold(True)#加粗
        font.setPointSize(18)
        self.label1.setFont(font)
        self.label1.setText('作者@你看清楚了吗')
        self.label1.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setGeometry(QtCore.QRect(500, 340, 128, 200))
        self.label2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        font = self.label2.font()
        font.setBold(True)#加粗
        font.setPointSize(14)
        self.label2.setFont(font)
        self.label2.setText('点击直达\n←———')
        self.label2.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        self.btn_bili = QtWidgets.QPushButton(self)
        self.btn_bili.setGeometry(QtCore.QRect(400,390, 100, 100))
        self.btn_bili.setStyleSheet("background-color:rgba(255,255,255,255)")
        self.bili_pic = QPixmap()
        bili_url = "https://i2.hdslb.com/bfs/face/1f48fcebf4e8f6de510eaf83e4d42b898fe5e69c.jpg@200w_200h_1c.webp"
        bili_picshow = requests.get(bili_url, headers=header)
        self.bili_pic.loadFromData(bili_picshow.content)
        self.btn_bili.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_bili.setIconSize(QtCore.QSize(100, 100))
        icon = QtGui.QIcon()
        icon.addPixmap(self.bili_pic)
        self.btn_bili.setIcon(icon)
        self.btn_bili.clicked.connect(self.dak)

        self.setCentralWidget(self.centralwidget)

    def select_change(self, index):
        for i in range(0,len(mmm)):
            if index == i+1:
                mmmdict["key"] =str(i)
                self.image = QPixmap()
                image_url = mmm[i][3]
                req = requests.get(image_url, headers=header)
                self.image.loadFromData(req.content)
                self.label_card.setPixmap(self.image)

    def moren_sort(self):
        mmm.sort(key=lambda x:x[0], reverse=self.moren)
        for i in range(0,len(mmm)):
            self.select_Box.setItemText(i + 1, mmm[i][2])
        self.select_Box.setCurrentIndex(0)
        self.label_card.setAlignment(Qt.AlignCenter)
        self.label_card.setText("请选择收藏集")
        self.moren=not self.moren
        mmmdict['key'] = '-1'

    def a_z_sort(self):
        mmm.sort(key=lambda x:pinyin(x[2]), reverse=self.a_z)
        for i in range(0,len(mmm)):
            self.select_Box.setItemText(i + 1, mmm[i][2])
        self.select_Box.setCurrentIndex(0)
        self.label_card.setAlignment(Qt.AlignCenter)
        self.label_card.setText("请选择收藏集")
        self.a_z=not self.a_z
        mmmdict['key'] = '-1'

    def handleDisplay(self):
        if mmmdict['key']=='-1':
            messagebox.showerror('','请先选择')
        else:
            self.my_thread=MyThread()
            self.my_thread.start()
            self.label_card.setText("请选择收藏集")
            self.select_Box.setCurrentIndex(0)

    def dak(self):
        newurl='https://space.bilibili.com/353403349'
        webbrowser.open(newurl, new=1, autoraise=True)

    def open_new_window(self):
        if mmmdict['key']=='-1':
            messagebox.showerror('','请先选择')
        else:
            current_item = self.select_Box.currentText()
            self.new_window = NewWindow(current_item)
            self.new_window.show()
            self.hide()
            nnndict['key'] = '-1'


class NewWindow(QMainWindow):
    def __init__(self,item):
        super().__init__()

        self.setWindowTitle("逐个下载")

        self.titlepic = QPixmap()
        self.titlepic.loadFromData(titlepicshow.content)
        self.setWindowIcon(QIcon(self.titlepic))

        self.setGeometry(1000, 500, 770, 550)
        self.setFixedSize(770, 550)

        self.new_centralwidget = QtWidgets.QWidget(self)
        self.new_label_card = QtWidgets.QLabel(self.new_centralwidget)
        self.new_label_card.setGeometry(QtCore.QRect(50, 50, 328, 440))
        self.new_label_card.setStyleSheet("background-color: rgb(150, 150, 150);")
        self.new_label_card.setAlignment(Qt.AlignCenter)
        self.new_label_card.setText("请选择图片")

        self.new_select_Box = QtWidgets.QComboBox(self.new_centralwidget)
        self.new_select_Box.setGeometry(QtCore.QRect(400, 50, 330, 50))
        self.new_select_Box.addItem("点击此按钮选择图片")
        if item!='-1':
            act_url = 'https://api.bilibili.com/x/vas/dlc_act/act/item/list?act_id=' + str(
                mmm[int(mmmdict['key'])][1])
            try:
                req1 = requests.get(act_url, headers=header).text
                dicts1 = json.loads(req1)
                for i in range(0, 10000):
                    card_name = dicts1['data']['item_list'][i]['card_item']['card_name']
                    try:
                        video = dicts1['data']['item_list'][i]['card_item']['video_list'][0]
                    except:
                        video =''
                    pic = dicts1['data']['item_list'][i]['card_item']['card_img']
                    nnn.append([int(i),str(card_name), video, pic])
            except:
                pass
            for i in range(0, len(nnn)):
                self.new_select_Box.addItem("")
            for i in range(0, len(nnn)):
                self.new_select_Box.setItemText(i + 1, nnn[i][1])
        self.new_select_Box.setCurrentIndex(0)
        self.new_select_Box.setMaxVisibleItems(22)
        self.new_select_Box.currentIndexChanged.connect(self.new_select_change)

        self.new_btn_moren = QtWidgets.QPushButton(self)
        self.new_btn_moren.setGeometry(QtCore.QRect(400, 110, 150, 50))
        self.new_btn_moren.setText("默认排序")
        self.new_btn_moren.clicked.connect(self.new_moren_sort)
        self.new_btn_moren.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.new_moren = False

        self.new_btn_a_z = QtWidgets.QPushButton(self)
        self.new_btn_a_z.setGeometry(QtCore.QRect(580, 110, 150, 50))
        self.new_btn_a_z.setText("首字母排序")
        self.new_btn_a_z.clicked.connect(self.new_a_z_sort)
        self.new_btn_a_z.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.new_a_z = False

        self.new_btn_xiazai = QtWidgets.QPushButton(self)
        self.new_btn_xiazai.setGeometry(QtCore.QRect(400, 170, 328, 50))
        self.new_btn_xiazai.setText("下载")
        self.new_btn_xiazai.clicked.connect(self.new_handleDisplay)
        self.new_btn_xiazai.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.setCentralWidget(self.new_centralwidget)
    def new_select_change(self, index):
        for i in range(0,len(nnn)):
            if index == i+1:
                nnndict["key"] =str(i)
                self.pixmap = QPixmap()
                i = int(nnndict['key'])
                image_url = nnn[i][3]+'@328w_440h_1c.webp'
                req = requests.get(image_url, headers=header)
                self.pixmap.loadFromData(req.content)
                self.new_label_card.setPixmap(self.pixmap)

    def new_moren_sort(self):
        nnn.sort(key=lambda x:x[0], reverse=self.new_moren)
        for i in range(0,len(nnn)):
            self.new_select_Box.setItemText(i + 1, nnn[i][1])
        self.new_select_Box.setCurrentIndex(0)
        self.new_label_card.setAlignment(Qt.AlignCenter)
        self.new_label_card.setText("请选择图片")
        self.new_moren=not self.new_moren
        nnndict['key'] = '-1'

    def new_a_z_sort(self):
        nnn.sort(key=lambda x:pinyin(x[1]), reverse=self.new_a_z)
        for i in range(0,len(nnn)):
            self.new_select_Box.setItemText(i + 1, nnn[i][1])
        self.new_select_Box.setCurrentIndex(0)
        self.new_label_card.setAlignment(Qt.AlignCenter)
        self.new_label_card.setText("请选择图片")
        self.new_a_z=not self.new_a_z
        nnndict['key'] = '-1'

    def new_handleDisplay(self):
        if nnndict['key']=='-1':
            messagebox.showerror('','请先选择')
        else:
            self.new_my_thread=NewMyThread()
            self.new_my_thread.start()
            self.new_label_card.setText("请选择图片")
            self.new_select_Box.setCurrentIndex(0)
    def closeEvent(self, event):
        self.main_window = Window()
        self.main_window.show()
        mmmdict['key'] = '-1'
        nnn.clear()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

