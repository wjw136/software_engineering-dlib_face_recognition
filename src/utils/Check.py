from src.DB.Database import Database
from src.utils.MyMd5 import MyMd5
import datetime
def check_user_id(user_id):

    if not user_id.isdigit() or len(user_id) > 100:
     
        return False
    return True


def check_user_pwd(user_pwd):
    if len(user_pwd) < 6 or len(user_pwd) > 13:
            return False
    return True

def verifye_pwd(user_id,user_pwd):
    admin = Database()
    user = admin.c.execute(
                "select id_number,salt, password,gender  from student where id_number = {} "
                .format(user_id)).fetchall()

    if len(user) == 0:
      return False

    elif len(user) == 1:
        item = user[0]
        pass_word = MyMd5().create_md5(user_pwd, item["salt"])
        if pass_word == item["password"]:
            return item["id_number"]
        else:return False
    else: return False              
   
# QMessageBox.information(parent, 'Information', '警告 username or Password')