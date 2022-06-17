import cv2
from src.utils.GlobalVariable import models
from src.model.Face import StudentRgFace


#此用于面部特征计算进程
# 自动进行普通识别=> 消费者模型
def process_student_rg(Q1, Q2, share):
    face_rg = StudentRgFace()
    while True:
        while not Q1.empty():
            img = Q1.get()
            rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(rgbImage, cv2.COLOR_RGB2GRAY)
            location_faces = models.detector(gray)
            if len(location_faces) == 1:
                raw_face = models.predictor(gray, location_faces[0])
                result = face_rg.rg(img, rgbImage, raw_face, share)
                Q2.put(result)

        #time.sleep(1)


# def process_admin_rg(Q1, share):
#     face_rg = AdminRgFace()
#     while True:
#         while not Q1.empty():
#             img = Q1.get()
#             rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             gray = cv2.cvtColor(rgbImage, cv2.COLOR_RGB2GRAY)
#             location_faces = models.detector(gray)
#             if len(location_faces) == 1:
#                 raw_face = models.predictor(gray, location_faces[0])
#                 result = face_rg.rg_face(img, rgbImage, raw_face,share)
