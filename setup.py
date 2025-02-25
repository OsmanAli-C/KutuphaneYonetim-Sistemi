from pymongo import MongoClient
import date_system
import time
import asyncio
import threading
import os
from dotenv import load_dotenv
from auth import Auth
from gui import admin_mail

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
admin_password = os.getenv("ADMIN_PASSWORD")


def run_setup():
    """
       setup.py'nin ana fonksiyonu.
       MongoDB'ye bağlanır, kütüphane sistemi için gerekli veritabanı ve koleksiyonları oluşturur.
       Eğer 'worked.txt' dosyası mevcut değilse, admin kullanıcı oluşturur.
       Fonksiyon başarıyla çalışırsa MongoDB client, books ve users koleksiyonlarını döndürür.

       Returns:
           tuple: (client, books, users)
               - client: MongoDB bağlantı nesnesi
               - books: kitaplar koleksiyonu
               - users: kullanıcılar koleksiyonu
    """
    try:
        print("setup başlatıyor")
        # Yerel MongoDB'ye bağlan
        client = MongoClient(mongo_uri)
        client.admin.command('ping')
        print("MongoDB bağlantısı başarılı.")

        # kütüphane veri tabanı oluştur
        db = client['library_system']

        # kitaplar koleksiyonu oluştur
        books = db['books']

        # kullanıcı koleksiyonu oluştur
        users = db['users']

        # Tarih koleksiyonu oluştur
        date_setting = db["date_system"]

        #En son girilen günü kaydeder
        date_system.last_chek_date(date_setting)



        print("setup başarılı")

        return client, books, users, date_setting

    except Exception as e:
        print("hata oluşt", e)

def background_checker(users, books):
    while True:
        date_system.check_users(users, books)
        date_system.remind_user(users, books)
        time.sleep(3600)

def admin_create(users):
    if not users.find_one({"name": "admin", "surname": "admin"}):
        add_admin = Auth(users)
        add_admin.register("admin", "admin",admin_mail, admin_password)



if __name__ == '__main__':
    client, books, users, date_setting = run_setup()

    thread = threading.Thread(target=background_checker, args=(users, books), daemon=True)
    thread.start()
