# coding=utf-8

import re #正则
import math
from decimal import getcontext, Decimal

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets 


class OpenFile(QtWidgets.QMainWindow):  
    def __init__(self, parent= None):  
        QtWidgets.QWidget.__init__(self)  
          
        self.setGeometry(500, 500, 400, 300)  
        #setGeometry是resize()和move()的合体,前面位置后面尺寸
        self.setWindowTitle('直流电法')  
        self.textEdit = QTextEdit()  
        self.setCentralWidget(self.textEdit)  
          
        self.statusBar()  
        self.setFocus()  
        #窗口左上角logo
        icon = QIcon()
        icon.addPixmap(QPixmap("logo.ico"),QIcon.Normal)
        self.setWindowIcon(icon)
        exit = QAction(QIcon('icons/Blue_Flower.ico'), 'Open', self)  
        exit.setShortcut('Ctrl+O')  
        exit.setStatusTip('Open new file')  
          
        exit.triggered.connect(self.showDialog)  
          
        menubar = self.menuBar()  
        file = menubar.addMenu('&File')  
        file.addAction(exit)  
          
    def showDialog(self):  
            filename,  _ = QFileDialog.getOpenFileName(self, 'Open file', './')  
            if filename:  
                file = open(filename)  
                # data = file.read()   
                # self.textEdit.setText(data)  
                data=self.arrChange(file)
                result=self.electric_processing(data)
                nPos=filename.rfind('.')
                mPos=filename.rfind('/')
                res_file=open(filename[mPos+1:nPos]+'.dat','w')
                for i in range(len(result)):
                    res_file.write(str(result[i][0])+','+str(result[i][1])+','+str(result[i][2])+'\r\n')
                #当前日期
                now = QDate.currentDate().toString(Qt.ISODate)
                #当前时间
                time = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)
                self.textEdit.setText('成功生成文件'+filename[mPos+1:nPos]+'.dat  Time:'+now+' '+time)
    def arrChange(self,file):
            arr = []
            for line in file.readlines()[7:]:
                line = line.strip()
                # fields=re.split(r'\s+',line)
                temp = re.split(r'\s+', line)
                arr.append(list(temp))
                #print("读取的数据为: %s" % (line))
            file.close()
            new_arr=[]
            i=0
            for i in range(len(arr)):
                temp=[]
                temp.append(arr[i][5])
                temp.append(arr[i][6])
                temp.append(arr[i][9])
                new_arr.append(temp)
            return new_arr
    def electric_processing(self,data):
        num=0
        result=[]
        temp=0
        for i in range(len(data)):
            res=[]
            if(num<3):
                temp=temp+float(data[i][2])
                num=num+1
                if(num==3):
                    if(float(data[i][2])<=0):
                        break
                    temp=math.log10(temp)
                    temp = Decimal(temp).quantize(Decimal('0.00'))
                    res.append(data[i-2][0])
                    res.append(4)
                    res.append(float(temp))
                    result.append(res)
                    num=0
                    temp=0
        temp_start=result[0].copy()
        temp_stop=result[len(result)-1].copy()
        for i in [1,7]:
            temp_start[1]=i
            result.append(temp_start.copy())
            temp_stop[1]=i
            result.append(temp_stop.copy())
        return result
if __name__ == "__main__":  
    import sys  
    app = QApplication(sys.argv)  
    qb = OpenFile()  
    qb.show()  
    sys.exit(app.exec_())  