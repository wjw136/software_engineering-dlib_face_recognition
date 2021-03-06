from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QPoint,pyqtSlot
from  PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QVBoxLayout,QMenu,QHeaderView,QMessageBox, QDialog
from PyQt5 import QtWidgets
from src.ui.ImageView import ShowImage
from src.DB.Database import Database
import os
class ShowStudentLog(QDialog):
    def __init__(self,information,str_list_column ):
        super().__init__()
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("学生日志")
        self.setWindowIcon(QIcon("resources/日志.png"))
        self.resize(300,400)
        self.information = information
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键显示上菜单
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)#禁止用户编辑单元格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#表示均匀拉直表头
        # self.qlineedit = QLineEdit()
        # self.qlineedit.setPlaceholderText('Please enter your usernumber')
        # self
        self.tableWidget.customContextMenuRequested[QPoint].connect(self.context_menu)#菜单右键槽函数
        self.tableWidget.cellDoubleClicked.connect(self.on_tableWidget_cellDoubleClicked)
        self.VBoxLayout = QVBoxLayout()
        self.VBoxLayout.addWidget(self.tableWidget)
        self.setLayout(self.VBoxLayout)
        columncout = len(str_list_column)
        self.tableWidget.setColumnCount(columncout)#根据数据量确定列数
        self.tableWidget.setHorizontalHeaderLabels(str_list_column)
        self.set_information()
    def set_information(self):
        row = 0
        self.tableWidget.setRowCount(0)
        for i in self.information:
            self.tableWidget.insertRow(row)
            log_time = QTableWidgetItem(i["log_time"])
            # 什么都不加 平级就是项目根目录 因为是path是相对于入口文件的位置 和 import不一样
            imag_path = "img_information/student/{0}/{1}.jpg".format(i["id_number"],i["log_time"])
            img_item =  QTableWidgetItem()
            img_item.setIcon(QIcon(imag_path))
            id_number = QTableWidgetItem(i['id_number'])

            self.tableWidget.setItem(row, 0,id_number)
            self.tableWidget.setItem(row, 1,log_time)
            self.tableWidget.setItem(row, 2,img_item)
            row = row + 1
            self.tableWidget.setRowCount(row)
      
           
    def on_tableWidget_cellDoubleClicked(self, row, column):#双击槽函数 self.tableWidget.cellDoubleClicked.connect()
        imag_path = "img_information/student/{0}/{1}.jpg".format(str(self.information[row]["id_number"]),str(self.information[row]["log_time"]))
        show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
        show_imag.exec_()

    @pyqtSlot(QPoint)
    def context_menu(self,pos):
        pop_menu = QMenu()
        #菜单事件信号
        delete_event = pop_menu.addAction("删除")
        imageView_event = pop_menu.addAction("查看图片")
        item = self.tableWidget.itemAt(pos)
        if item != None:
            row = item.row()
            action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))#显示菜单列表，pos为菜单栏坐标位置
            if action == delete_event:
                r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if r == QMessageBox.No:
                   return
                database =  Database()
                database.c.execute("delete from student_log_time where rowid  = {0}".format(self.information[row]["rowid"])).fetchall()
                imag_path = "img_information/student/{0}/{1}.jpg".format(str(self.information[row]["id_number"]),str(self.information[row]["log_time"]))
                os.remove(imag_path)
                database.conn.commit()
                database.conn.close()
                self.tableWidget.removeRow(row) 
                self.information.remove(self.information[row])#删除信息列表

            elif action == imageView_event:
                imag_path = "img_information/student/{0}/{1}.jpg".format(str(self.information[row]["id_number"]),str(self.information[row]["log_time"]))
               
                show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
                show_imag.exec_()


