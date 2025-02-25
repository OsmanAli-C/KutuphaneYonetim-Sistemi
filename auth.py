from matplotlib.pyplot import title
from pymongo import MongoClient
import setup

class Auth():
    """
       Kullanıcı kayıt ve giriş işlemleri için bir sınıf.
       MongoDB 'users' koleksiyonu üzerinde işlem yapar.
    """

    def __init__(self, users):
        """
                Auth sınıfının kurucusu. Kullanıcı koleksiyonunu alır ve işlemleri başlatır.

                Args:
                    users (Collection): MongoDB 'users' koleksiyonu.
        """

        self.users = users

    def register(self, name, surname, email, password):
        """
                Yeni bir kullanıcıyı kaydeder.

                Args:
                    name (str): Kullanıcının adı.
                    surname (str): Kullanıcının soyadı.
                    email (str): Kullanıcının email adresi.
                    password (str): Kullanıcının şifresi.
                    borrowed (list): Kullanıcının ödünç aldığı kitaplar

                Returns:
                    str: Kayıt başarılıysa, aksi takdirde email'in zaten kayıtlı olduğu mesajını döndürür.
        """
        user = {
            "name": name.title(),
            "surname": surname.title(),
            "email": email,
            "password": password,
            "borrowed":[],
            #borrowed [
            # {'isbn': '1234567890123, 'borrow_date': '2024-12-14', 'last_due_date': '2024-12-29'}
            # ]
            "borrow_req": []#isbn numarası olacak sadece maximum 3-len(borrowed) kadar olabilir
        }

        if self.users.find_one({"email": email}):
           return False
        else:
            self.users.insert_one(user)
            return True

    def login(self, email, password):
        """
                Kullanıcı giriş işlemi.

                Args:
                    email (str): Kullanıcının email adresi.
                    password (str): Kullanıcının şifresi.

                Returns:
                    str: Giriş başarılıysa "giriş başarılı", şifre yanlışsa "yanlış şifre",
                    email kayıtlı değilse "bu epostya sahip kayıtlı kullanıcı yok" mesajını döndürür.
        """

        input_email = self.users.find_one({"email": email})
        if input_email:
            if input_email["password"] == password:
                if input_email["name"]=='banned' and input_email["surname"]=='banned':
                    return 'yasaklanmış kullanıcı'
                return "giriş başarılı"
            else:
                return "yanlış şifre"
        else:
            return ""

    def change_password(self, new_password, email):
        """kullanıcının şifresini değiştirir"""
        self.users.update_one({"email": email}, {"$set": {'password': new_password}})



    def ban(self, email):
        """email'i seçilen kullanıcıyı yasaklar ve mail gönderir"""
        if self.users.find_one({"email": email}):
            self.users.update_one({"email": email}, {"$set": {"name": 'banned', "surname": 'banned'}})

