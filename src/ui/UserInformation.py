
from .ImageView import ImageView
from src.DB.Database import Database
from .ImageView import ShowImage
from src.DB.Creatuser import CreatUser
from PyQt5.QtCore import Qt,pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QGroupBox,QPushButton,\
QMessageBox, QMenu,QWidget
from src.utils.ImgPath import get_img_path
from .UpdatePwd import UpdatePwd
from .ShowStudentLog import ShowStudentLog
from .ShowStudentUser import ShowStudentUser
class StudentInformation(QWidget):
    def __init__(self,id_number):
        super().__init__()
        self.id_number = id_number
        self.setGeometry(300, 300,400, 380)
        self.setWindowTitle('用户信息')
        self.setWindowIcon(QIcon('resources/用户信息.png'))
        self.setWindowModality(Qt.ApplicationModal)
        

        self.Hlayout_base = QHBoxLayout()
        self.Hlayout_choice=QHBoxLayout()
        self.Vhlayout = QVBoxLayout()
        
        #self.linnedit.setFixedSize(400,15)
        
        self.grou_base = QGroupBox(self)
        self.grou_choice = QGroupBox(self)
        self.img = ImageView("./resources/bg.jpg",Qt.black)
        self.qlabel1 = QLabel(self)
        self.qlabel2 = QLabel(self)
        self.qlabel3 = QLabel(self)
        self.qlabel4 = QLabel(self)
        self.Hlayout_base.addWidget(self.qlabel1)
        self.Hlayout_base.addWidget(self.qlabel2)
        self.Hlayout_base.addWidget(self.qlabel3)
        self.Hlayout_base.addWidget(self.qlabel4)
        self.qlabel1.setText("用户ID：{}".format(self.id_number))
        self.btn1 = QPushButton()
        self.btn1 = QPushButton(objectName="GreenButton")
       
        self.btn2 = QPushButton()
        self.btn2 = QPushButton(objectName="GreenButton")
        
        self.btn1.setText("修改图片")
        self.btn1.clicked.connect(lambda:self.img_event())
        self.btn2.setText("修改密码")
        self.btn2.clicked.connect(self.update_pwd)
        self.btn3 = QPushButton()
        self.btn3 = QPushButton(objectName="GreenButton")
        self.btn3.clicked.connect(self.browse)
        self.btn3.setText("登录日志")


        self.Hlayout_choice.addWidget(self.btn1)
        self.Hlayout_choice.addWidget(self.btn2)
        self.Hlayout_choice.addWidget(self.btn3)
        if self.id_number == "12345678910" :
           self.btn4 = QPushButton()
           self.btn4 = QPushButton(objectName="GreenButton")
           self.btn4.setText("用户管理")
           self.btn4.clicked.connect(self.root)
           self.Hlayout.addWidget(self.btn4)
        self.grou_base.setLayout(self.Hlayout_base)
        self.grou_choice.setLayout(self.Hlayout_choice)
        self.Vhlayout.addWidget(self.grou_base)
        self.Vhlayout.addWidget(self.grou_choice)
        self.Vhlayout.addWidget(self.img)
        self.grou_base.setMaximumSize(600,40)
        self.grou_choice.setMaximumSize(600, 40)
        self.setLayout(self.Vhlayout)

        #设置图片
        self.Vhlayout.itemAt(2).widget().deleteLater()
        img_path = "img_information/student/{0}/{1}.jpg".format(str(self.id_number), str(self.id_number))
        show_imag = ShowImage(img_path, Qt.WhiteSpaceMode)
        self.Vhlayout.addWidget(show_imag)
        self.sex_dict = {0: '女生', 1: '男生'}
        self.complete_info()


    def complete_info(self):
        result=Database().c.execute(
            "select id_number,user_name,gender,count from student where id_number ={0} ".format(
                self.id_number)).fetchall()
        self.qlabel2.setText('性别: {}'.format(self.sex_dict[int(result[0]['gender'])]))
        self.qlabel3.setText('用户名: {}'.format(result[0]['user_name']))
        self.qlabel4.setText('识别次数: {}'.format(result[0]['count']))

    def update_pwd(self):
        self.pwd_dialog = UpdatePwd(self.id_number)
        self.pwd_dialog.exec_()
    def browse(self):
        result = Database().c.execute("select rowid,id_number,log_time from student_log_time where id_number = {0}  order by log_time desc".format(self.id_number)).fetchall()
        if len(result)!= 0:
            
            self.result = ShowStudentLog(result,[ '用户ID', '登录时间',"图片" ])
            self.Vhlayout.itemAt(1).widget().deleteLater()
            self.Vhlayout.addWidget(self.result)
        else: 
            QMessageBox.critical(self, 'Wrong', '不存在用户')
            return
    def img_event(self):
       path = get_img_path(self)
       if path:
          vector = CreatUser().get_vector(self.id_number,path,"student")
          database = Database()
          database.c.execute("update student set vector = ? where id_number = {0}".format(self.id_number),(vector,))
          database.conn.commit()
          database.conn.close()
          QMessageBox.information(self, 'Success', '修改成功')
          self.Vhlayout.itemAt(1).widget().deleteLater()
          img_path = "img_information/student/{0}/{1}.jpg".format(str(self.id_number), str(self.id_number))
          show_imag = ShowImage(img_path, Qt.WhiteSpaceMode)
          self.Vhlayout.addWidget(show_imag)
   
    def root(self):
        result = Database().c.execute("select id_number,password    from student ").fetchall()
        self.result = ShowStudentUser(result,[ '用户ID', '密码',"图片" ])
        self.Vhlayout.itemAt(1).widget().deleteLater()
        self.Vhlayout.addWidget(self.result)
        pass
#密码修改窗口

