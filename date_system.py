from datetime import datetime, timedelta
from add_remove import BookRemove
from auth import Auth
import mail_system
import pytz



def get_turkey_time():
    """Türkiye saatini ve tarihini döndürür."""
    tz = pytz.timezone('Europe/Istanbul')  # Türkiye saat dilimi
    turkey_time = datetime.now(tz)
    formatted_time = turkey_time.strftime("%Y-%m-%d")  # Yıl-Ay-Gün Saat:Dakika:Saniye
    return formatted_time

# Fonksiyon çağrısı

def get_future_date(days=15):
    """O anki Türkiye saatine göre belirli gün sonrasını döndürür."""
    tz = pytz.timezone('Europe/Istanbul')  # Türkiye saat dilimi
    turkey_time = datetime.now(tz)
    future_date = turkey_time + timedelta(days=days)  # Belirtilen gün kadar ekle
    formatted_date = future_date.strftime("%Y-%m-%d")  # Formatlı tarih
    return formatted_date

def last_chek_date(date_setting):
    """veritabanına en son gün kontrolünün ne zaman olduğunu işler"""
    td=get_turkey_time()
    date_setting.update_one(
        {"_id": "last_checked"},{"$set": {"date": td}},
        upsert=True
    )

def get_last_checked_date(date_setting):
    """Son kontrol edilen tarihi MongoDB'den alır."""
    result = date_setting.find_one({"_id": "last_checked"})
    return result["date"] if result else None


def check_users(users, books,target_date=0):
    """Tüm kullanıcıların belirtilen tarih bilgisini kontrol eder."""
    # Tüm kullanıcıları getir
    all_users = users.find()
    target_date=get_turkey_time()
    target_date=datetime.strptime(target_date, "%Y-%m-%d")

    for user in all_users:
        borrowed_books = user.get("borrowed", [])  # Kullanıcının borrowed bilgisi
        user_email = user.get("email")  # Kullanıcının e-postası

        for book in borrowed_books:
            # Ödünç alınan kitabın teslim tarihini kontrol et
            last_due_date = book.get("last_due_date")
            if last_due_date:
                due_date = datetime.strptime(last_due_date, "%Y-%m-%d")
                if due_date <= target_date:
                    auth_instance = Auth(users)
                    ban_message=(f"{book.get("author")} - {book.get('title')} kitabını zamanında teslim etmediğiniz için"
                                 f"hesabınız engellenmiştir")
                    mail_system.send_email(user_email, "Hesap Engeli", ban_message)
                    auth_instance.ban(user_email)
                    del_book=BookRemove(books=books, isbn=book.get("isbn"))
                    del_book.update_count(missing=-1,tor=-1)

def remind_user(users, books):
    """Tüm kullanıcıların belirtilen tarih bilgisini kontrol eder ve hatırlatma mesajı gönderir."""
    all_users = users.find()
    target_date=get_turkey_time()
    target_date=datetime.strptime(target_date, "%Y-%m-%d")

    for user in all_users:
        borrowed_books = user.get("borrowed", [])  # Kullanıcının borrowed bilgisi
        user_email = user.get("email")  # Kullanıcının e-postası

        for book in borrowed_books:
            # Ödünç alınan kitabın teslim tarihini kontrol et
            last_due_date = book.get("last_due_date")
            if last_due_date:
                due_date = datetime.strptime(last_due_date, "%Y-%m-%d") - timedelta(days=5)
                if due_date <= target_date and not user.get('br')==True:
                    remind_message=(f"{book.get("author")} - {book.get('title')} kitabının teslim süresine 5 gün "
                                 f"kalmıştır en geç {datetime.strftime(due_date, "%Y-%m-%d")} tarihine kadar"
                                    f"kitabı teslim ediniz.")
                    mail_system.send_email(user_email, "Kitap Teslim Hatırlatması", remind_message)
                    users.update_one({'email': user_email}, {'$set': {'br': True}})
