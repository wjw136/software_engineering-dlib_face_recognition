from src.DB.Database import Database
from src.utils.Log import studentlog
from src.utils.GlobalVariable import models
import numpy as np
from threading import Timer


class Face():  #基类，包含人脸编码，人脸识别
    def __init__(self):

        pass

    #为人脸编码
    def encodeface(self, rgbImage, raw_face):
        return np.array(
            models.encoder.compute_face_descriptor(rgbImage, raw_face))

    #计算人脸相似度，flaot值越小越相似
    def compare_faces(self, face_encoding, test_encoding, axis=0):
        return np.linalg.norm(face_encoding - test_encoding, axis=axis)#计算欧式距离

    #与数据库人脸对比，相似度小于0.5则认为是同一个人

    #每一段时间重置face_data值


#用于学生进入图书馆是别
class StudentRgFace(Face):
    def __init__(self):
        super().__init__()
        self.face_data = np.random.random(128).astype('float32')#初始化人脸编码，这个变量保存上一个人脸编码
        self.former_result = ""
        self.refreshthread = Timer(3, self.reset)
        self.refreshthread.setDaemon(True)
        self.refreshthread.start()
        student = Database()
        self.list_vector = []
        for i in student.c.execute("SELECT vector from student"):#查询数据库中所有人脸编码
            i = np.loads(i["vector"])
            self.list_vector.append(i)
      
        student.conn.close()
    def reset(self):
        self.face_data = np.random.random(128).astype('float32')
        self.refreshthread = Timer(3, self.reset)
        self.refreshthread.setDaemon(True)
        self.refreshthread.start()

    #主页面 识别版本
    def rg(self, img, rgbImage, raw_face,
           share):  #优化识别流程，识别成功后避免同一人频繁识别，频繁记录数据
        face_data = self.encodeface(rgbImage, raw_face)
        flag = self.compare_faces(face_data, self.face_data, axis=0)#计算欧式距离
        if flag < share.value:
            return self.former_result
        else:
            result = self.rg_face(face_data, share.value)
            if result:
                self.face_data = face_data#保存这次识别人脸编码，下次识别时比较是否是同一人
                student = Database()
                log = studentlog(result, img, student) # 记录识别log信息 以及识别时候的photo
                student.conn.close()
                self.former_result = "验证成功：" + log.item["user_name"]
                return self.former_result
            else:
                return "验证失败"

    # 首页登录版本
    def rgv2(self, img, rgbImage, raw_face,
           share):  #优化识别流程，识别成功后避免同一人频繁识别，频繁记录数据
        face_data = self.encodeface(rgbImage, raw_face)
        result = self.rg_face(face_data, share.value)
        if result == "请先注册用户":
            return "请先注册用户"
        elif result:
            student = Database()
            log = studentlog(result, img, student) # 记录识别log信息 以及识别时候的photo
            student.conn.close()
            return log.item["id_number"]
        else:
            return "验证失败"

    def rg_face(self, face_data, share):
        if len(self.list_vector) == 0:
            return "请先注册用户"
        distances = self.compare_faces(np.array(self.list_vector), face_data, axis=1)#计算欧式距离
        min_distance = np.argmin(distances)
        print("距离", distances[min_distance])
        if distances[min_distance] < share:
            tembyte = np.ndarray.dumps(self.list_vector[min_distance])
            return tembyte
        else:
            return False


# class AdminRgFace(Face):
#     def __init__(self):
#         super().__init__()
#
#     def rg_face(self, img, rgbImage, raw_face):
#         face_data = self.encodeface(rgbImage, raw_face)
#         admin = Database()
#         list_vector = []
#         list_user = admin.c.execute("SELECT vector,id_number from admin").fetchall ()# 查询数据库中的数据:
#         for i in list_user:
#             vector = np.loads(i["vector"])#把数据库中的vector（二进制）转换成ndarray
#             list_vector.append(vector)
#         if len(list_vector) == 0:
#             return False
#         distances = self.compare_faces(np.array(list_vector), face_data, axis=1)
#         min_distance = np.argmin(distances)
#         print("距离", distances[min_distance])
#         if distances[min_distance] < 0.4:
#             tembyte = np.ndarray.dumps(list_vector[min_distance])
#             adminlog(tembyte, img, admin)
#             id_number = list_user[min_distance]["id_number"]#返回管理员的id_number
#             admin.conn.close()  #关闭数据库连接
#             return id_number
#         else:
#             return False


# class AdminRgFace(Face):
#     def __init__(self):
#         super().__init__()
#         self.face_data = np.random.random(128).astype('float32')
#         self.refreshthread = Timer(10, self.reset)
#         self.refreshthread.setDaemon(True)
#         self.refreshthread.start()
#     def rg_face(self,img, rgbImage, raw_face,share):
#         face_data = self.encodeface(rgbImage, raw_face)
#         flag = self.compare_faces(face_data, self.face_data, axis=0)
#         if flag < 0.6:return ""
#         else:
#             admin = Database()
#             list_vector = []
#             for i in admin.c.execute("SELECT vector from admin"):
#                 i = np.loads(i[0])
#                 list_vector.append(i)
#             if len(list_vector) == 0:
#                 return False
#             distances = self.compare_faces(np.array(list_vector), face_data, axis=1)
#             min_distance = np.argmin(distances)
#             print("距离",distances[min_distance])
#             if distances[min_distance] < 0.4:
#                 share.value = True
#                 self.face_data = face_data
#                 tembyte = np.ndarray.dumps(list_vector[min_distance])
#                 adminlog(tembyte,img,admin)
#                 admin.conn.close()
#                 return "验证成功"
#             else:
#                 return  "验证失败"

#     def reset(self):
#         self.face_data = np.random.random(128).astype('float32')
#         self.refreshthread = Timer(10, self.reset)
#         self.refreshthread.setDaemon(True)
#         self.refreshthread.start()
