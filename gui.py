import tkinter as tk
from math import lgamma
from tkinter import messagebox
from auth import Auth
from pymongo import MongoClient
from pymongo.network import command
import borrow_manager
import auth
from add_remove import BookInsert, BookRemove
import date_system
import mail_system
from dotenv import load_dotenv
import os


load_dotenv()

admin_mail = os.getenv("EMAIL")

class LibraryApp:
    def __init__(self,books, users, master):
        """Kullancı Arayüzüdür"""
        self.books = books
        self.users = users

        self.master = master
        self.master.title("IST Kütüphanesi")

        # Pencere boyutunu ayarla ve ortala
        self.master.geometry("900x600")
        self.master.configure(bg="#f0f0f0")  # Beyaza yakın gri arka plan
        self.master.minsize(900, 600)
        self.center_window(900, 600)  # Ortalamak için

        # Değişkenleri tanımla
        self.login_email = tk.StringVar()
        self.login_password = tk.StringVar()
        self.reg_name = tk.StringVar()
        self.reg_surname = tk.StringVar()
        self.reg_email = tk.StringVar()
        self.reg_password = tk.StringVar()

        # Frame'leri oluştur
        self.login_frame = tk.Frame(self.master, bg="lightgray")
        self.register_frame = tk.Frame(self.master, bg="lightgray")

        # Giriş ekranını kur
        self.setup_login_frame()

        # Kayıt ekranını kur
        self.setup_register_frame()

        # Başlangıçta login frame göster
        self.show_login_frame()

        #Tarih kısmı
        self.t_day=date_system.get_turkey_time()
        self.fif_day=date_system.get_future_date()

    def center_window(self, width, height):
        """Pencereyi ekranda ortalamak için boyut ve pozisyon ayarları."""
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def setup_login_frame(self):
        """Giriş ekranını oluştur."""
        tk.Label(
            self.login_frame,
            text="IST KÜTÜPHANESİ",
            bg="lightgray",
            fg="red",
            font=("Helvetica", 24, "bold")
        ).pack(pady=10)

        # E-posta ve Şifre alanlarını dikey ve yatay ortala
        form_frame = tk.Frame(self.login_frame, bg="lightgray")
        form_frame.pack(expand=True)

        tk.Label(form_frame, text="E-Posta:", bg="lightgray", fg="black", font=("Arial", 16)).grid(row=0, column=0, pady=10, padx=10)
        tk.Entry(form_frame, textvariable=self.login_email, font=("Arial", 14), width=30).grid(row=0, column=1, pady=10)

        tk.Label(form_frame, text="Şifre:", bg="lightgray", fg="black", font=("Arial", 16)).grid(row=1, column=0, pady=10, padx=10)
        tk.Entry(form_frame, textvariable=self.login_password, show="*", font=("Arial", 14), width=30).grid(row=1, column=1, pady=10)

        # Giriş yap butonu
        tk.Button(
            self.login_frame,
            text="Giriş Yap",
            command=self.login,
            bg="blue",
            fg="blue",  # Yazı rengi mavi
            font=("Arial", 16)
        ).pack(pady=10)

        # Sağ alt köşede Kayıt Ol
        register_label = tk.Label(
            self.login_frame,
            text="Kayıt Ol",
            bg="lightgray",
            fg="blue",
            font=("Arial", 14, "underline"),
            cursor="hand2"
        )
        register_label.pack(side="bottom", anchor="se", padx=20, pady=20)
        register_label.bind("<Button-1>", lambda e: self.show_register_frame())

    def setup_register_frame(self):
        """Kayıt ekranını oluştur."""
        tk.Label(
            self.register_frame,
            text="IST KÜTÜPHANESİ KAYIT",
            bg="lightgray",
            fg="red",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)

        # İsim ve Soyisim aynı satırda sola dayalı ve kutucuk üstünde yazı
        name_frame = tk.Frame(self.register_frame, bg="lightgray")
        name_frame.pack(anchor="w", padx=20, pady=10)

        tk.Label(name_frame, text="İsim:", bg="lightgray", fg="black", font=("Arial", 14)).grid(row=0, column=0, padx=10, sticky="w")
        tk.Entry(name_frame, textvariable=self.reg_name, font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)

        tk.Label(name_frame, text="Soyisim:", bg="lightgray", fg="black", font=("Arial", 14)).grid(row=0, column=1, padx=10, sticky="w")
        tk.Entry(name_frame, textvariable=self.reg_surname, font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=5)

        # E-posta alanı sola dayalı
        tk.Label(self.register_frame, text="E-Posta:", bg="lightgray", fg="black", font=("Arial", 14)).pack(anchor="w", padx=20)
        tk.Entry(self.register_frame, textvariable=self.reg_email, font=("Arial", 12), width=40).pack(anchor="w", padx=20, pady=5)

        # Şifre alanı sola dayalı
        tk.Label(self.register_frame, text="Şifre:", bg="lightgray", fg="black", font=("Arial", 14)).pack(anchor="w", padx=20)
        tk.Entry(self.register_frame, textvariable=self.reg_password, font=("Arial", 12), width=40, show="*").pack(anchor="w", padx=20, pady=5)

        # Butonlar sola dayalı
        tk.Button(
            self.register_frame,
            text="Kayıt Ol",
            command=self.register_user,
            bg="blue",
            fg="blue",  # Yazı rengi mavi
            font=("Arial", 14),
            width=15
        ).pack(anchor="w", padx=20, pady=5)

        tk.Button(
            self.register_frame,
            text="Giriş Ekranına Dön",
            command=self.show_login_frame,
            bg="white",
            fg="blue",  # Yazı rengi mavi
            font=("Arial", 14),
            width=15
        ).pack(anchor="w", padx=20)

    def handle_successful_login(self, email, password_):
        """Giriş başarılı olduğunda ekranı düzenler."""
        self.user = self.users.find_one({"email": email, "password": password_})
        self.login_frame.pack_forget()

        success_frame = tk.Frame(self.master, bg="lightgray")
        success_frame.pack(fill="both", expand=True)

        tk.Label(
            success_frame,
            text="Kütüphaneye Hoşgeldiniz",
            font=("Arial", 24, "bold"),
            bg="lightgray",
            fg="green"
        ).pack(expand=True)

    def show_wrong_password_message(self):
        """Yanlış şifre mesajını gösterir."""
        error_label = tk.Label(
            self.login_frame,
            text="Şifre Yanlış",
            font=("Arial", 10, "underline"),
            bg="lightgray",
            fg="red"
        )
        error_label.place(
            x=550,  # Şifre kutucuğunun yatay konumuna göre ayarlanabilir
            y=260  # Şifre kutucuğunun dikey konumuna göre ayarlanabilir
        )

    def show_banned_user_message(self):
        """Yanlış şifre mesajını gösterir."""
        error_label = tk.Label(
            self.login_frame,
            text="Yasaklı kullanıcı",
            font=("Arial", 10, "underline"),
            bg="lightgray",
            fg="red"
        )
        error_label.place(
            x=550,  # Şifre kutucuğunun yatay konumuna göre ayarlanabilir
            y=260  # Şifre kutucuğunun dikey konumuna göre ayarlanabilir
        )

    def show_user_not_found_message(self):
        """Kullanıcı bulunamadı mesajını gösterir."""
        no_user_label = tk.Label(
            self.login_frame,
            text="Böyle bir kullanıcı sistemde kayıtlı değil",
            font=("Arial", 12),
            bg="lightgray",
            fg="red"
        )
        no_user_label.pack(side="bottom", pady=10)

    def handle_successful_registration(self):
        """Kayıt başarılı olduğunda mesaj kutusunu göster ve giriş ekranına dön."""
        tk.messagebox.showinfo("Kayıt Durumu", "Kayıt başarılı!")
        self.show_login_frame()

    def show_email_already_used_message(self):
        """Ekranın sağında 'Bu email daha önce kullanılmış' mesajını göster."""
        error_label = tk.Label(
            self.register_frame,
            text="Bu email daha önce kullanılmış",
            font=("Arial", 12),
            bg="lightgray",
            fg="red"
        )
        error_label.place(
            x=600,  # Sağda konumlandırmak için yatay değer
            y=150  # Mesajın dikey konumu
        )

    def show_login_frame(self):
        self.register_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(fill="both", expand=True)

    def register_user(self):
        """Kullanıcı kayıt işlemi."""
        name = self.reg_name.get().strip()
        surname = self.reg_surname.get().strip()
        email = self.reg_email.get().strip()
        password_ = self.reg_password.get().strip()

        # Yasaklı isim kontrolü
        forbidden_names = ["admin", "banned"]
        if name.lower() in forbidden_names:
            self.show_forbidden_name_popup()
            return

        new_user = auth.Auth(self.users)

        # Kayıt işlemi
        if new_user.register(name, surname, email, password_):
            # Kayıt başarılıysa işlem
            self.handle_successful_registration()
        else:
            # Kayıt başarısızsa hata mesajını göster
            self.show_email_already_used_message()

    def show_forbidden_name_popup(self):
        """Yasaklı isimler için uyarı popup'ı."""
        tk.messagebox.showwarning(
            "Yasaklı İsim",
            "Kullanıcı ismi olarak 'Admin' veya 'Banned' kullanamazsınız."
        )

    def login(self):
        """Kullanıcı giriş işlemi."""
        email = self.login_email.get()
        password_ = self.login_password.get()
        login_try = auth.Auth(self.users).login(email, password_)

        # Giriş başarılıysa kitaplık sayfasını göster

        if login_try == "giriş başarılı" and email == admin_mail:
            self.clear_frame()
            self.setup_admin_tabs(active_tab="library")  # Admin sekmeleri göster
            self.show_library_section()  # Varsayılan olarak Kütüphane Yönetimi sekmesi açık

        elif login_try == "giriş başarılı":
            self.user = self.users.find_one({"email": email, "password": password_})

            # Ekranı temizle ve kitaplık sayfasını yükle
            self.clear_frame()
            self.setup_header()
            self.setup_tabs()
            self.setup_library_page()

        # Yanlış şifre
        elif login_try == "yanlış şifre":
            self.show_wrong_password_message()

        #Yasaklı kullanıcı
        elif login_try == "yasaklanmış kullanıcı":
            self.show_banned_user_message()

        # Kullanıcı bulunamadı
        else:
            self.show_user_not_found_message()

    def reload_user(self):
        """Kullanıcının bilgilerini yeniden yükler."""
        self.user = self.users.find_one({"email": self.user["email"]})


# --------------------------------------------------------------

    def setup_header(self):
        """Başlığı düzenler."""
        header_frame = tk.Frame(self.master, bg="lightgray")
        header_frame.pack(side="top", fill="x")

        tk.Label(
            header_frame,
            text="IST KÜTÜPHANESİ",
            font=("Helvetica", 24, "bold"),
            bg="lightgray",
            fg="red"
        ).pack(anchor="center", pady=10)

    def clear_frame(self):
        """Tüm mevcut widget'ları temizler."""
        for widget in self.master.winfo_children():
            widget.destroy()
        self.setup_header()
        self.master.update()

    def reset_all_filters(self):
        """Tüm filtreleri sıfırlar."""
        self.book_name_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.book_name_label.config(text="")
        self.author_label.config(text="")


# --------------------------------------------------------------
#KULLANICI SAYFASI

    def setup_library_page(self):
        """Kitaplık sayfasını düzenler (normal kullanıcı)."""
        self.clear_frame()  # Önceki çerçeveyi temizle
        self.setup_tabs("lib")  # Sekmeleri ekle

        # Sağ Kısım: Kitap Listesi
        right_frame = tk.Frame(self.master, bg="white")
        right_frame.pack(side="right", fill="both", expand=True)

        # Kitap Listesi (Listbox)
        self.book_listbox = tk.Listbox(right_frame, font=("Arial", 12), height=18, width=50)
        self.book_listbox.pack(pady=10, padx=20)

        # Sol Kısım: Kullanıcı için filtreleme
        left_frame = tk.Frame(self.master, bg="#FFFDD0", width=300)
        left_frame.pack(side="left", fill="y")
        self.setup_user_library_filters(left_frame)  # Kullanıcı için özel filtreleme alanını ekle

        # Sayfa Geçişi İçin Butonlar
        button_frame = tk.Frame(right_frame, bg="white")
        button_frame.pack(side="bottom", pady=10)

        # Seç Butonu
        select_button = tk.Button(
            right_frame,
            text="Seç",
            font=("Arial", 14),
            bg="blue",
            fg="blue",
            width=20,
            height=2,
            command=self.select_user_book
        )
        select_button.pack(pady=20)

        self.load_books()  # Kitapları yükle

    def user_reset_filter(self, filter_type):
        """Belirli bir filtreyi sıfırlar."""
        if filter_type == "book_name":
            self.user_book_name_entry.delete(0, tk.END)
            self.user_book_name_label.config(text="")
        elif filter_type == "author":
            self.user_author_entry.delete(0, tk.END)
            self.user_author_label.config(text="")

    def setup_tabs(self, chosen_tab="lib"):
        """Sekmeleri düzenler."""
        tabs_frame = tk.Frame(self.master, bg="lightgray")
        tabs_frame.pack(side="top", fill="x")

        if chosen_tab == "lib":
            self.lib_="darkblue"
            self.aco_="blue"
        elif chosen_tab == "aco":
            self.lib_ = "blue"
            self.aco_ = "darkblue"

        # Hesap Sekmesi
        tk.Button(
            tabs_frame,
            text="Hesap",
            font=("Arial", 14),
            bg="white",
            fg=self.aco_,
            command=self.setup_account_page  # Hesap sayfasını gösterir
        ).pack(side="left", padx=10)

        # Kütüphane Sekmesi
        tk.Button(
            tabs_frame,
            text="Kütüphane",
            font=("Arial", 14),
            bg="blue",
            fg=self.lib_,
            command=self.setup_library_page  # Kütüphane sayfasını gösterir
        ).pack(side="left", padx=10)

    def setup_account_page(self):
        """Hesap sekmesini düzenler."""

        # Kullanıcı bilgilerini güncelle
        self.reload_user()

        self.clear_frame()  # Mevcut içeriği temizle
        self.setup_tabs("aco")  # Sekmeleri yeniden yükle

        # Sol çerçeve: Kullanıcı bilgileri
        left_frame = tk.Frame(self.master, bg="#FFFDD0", width=300)
        left_frame.pack(side="left", fill="y")

        # Kullanıcı bilgilerini ayırmak için dikey çizgi
        separator = tk.Frame(self.master, bg="black", width=2)
        separator.pack(side="left", fill="y")

        # Bilgileri kısaltarak göster
        def shorten_text(text, limit=20):
            return text if len(text) <= limit else text[:17] + "..."

        user_info = {
            "Ad": shorten_text(self.user['name']),
            "Soyad": shorten_text(self.user['surname']),
            "E-posta": shorten_text(self.user['email'])
        }

        for key, value in user_info.items():
            tk.Label(
                left_frame,
                text=f"{key}: {value}",
                font=("Arial", 14),
                bg="#FFFDD0",
                fg="black"
            ).pack(anchor="w", padx=20, pady=10)

        tk.Button(
            left_frame,
            text="Şifre Değiştir",
            font=("Arial", 12),
            bg="#FFFDD0",
            fg="blue",
            command=self.change_password
        ).pack(anchor="s", pady=20, side="bottom")

        # İade/İptal Butonu
        tk.Button(
            left_frame,
            text="İade/İptal",
            font=("Arial", 12),
            bg="#FFFDD0",
            fg="blue",
            command=self.open_return_cancel_popup
        ).pack(anchor="s", pady=5)  # Şifre Değiştir'in hemen üstünde olacak

        # Sağ çerçeve: Sabit dikey çizgiler
        right_frame = tk.Frame(self.master, bg="#FFFDD0")
        right_frame.pack(side="right", fill="both", expand=True)

        # Canvas tanımla
        canvas = tk.Canvas(right_frame, bg="#FFFDD0", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        borrow_info = self.get_borrow_info()

        # Çizgiler ve metinlerin konumları
        lines = [
            {"x": 0.0, "text": ["1. Blok 1. Satır\ndeneme", "1. Blok 2. Satır", "1. Blok 3. Satır", "1. Blok 4. Satır",
                                "1. Blok 5. Satır"]},
            {"x": 1/3, "text": ["2. Blok 1. Satır", "2. Blok 2. Satır", "2. Blok 3. Satır", "2. Blok 4. Satır",
                                "2. Blok 5. Satır"]},
            {"x": 2/3, "text": ["3. Blok 1. Satır", "3. Blok 2. Satır", "3. Blok 3. Satır", "3. Blok 4. Satır",
                                "3. Blok 5. Satır"]},
        ]

        for index, item in enumerate(borrow_info):
            if index >= len(lines):
                # Güvenlik için, lines listesinin sınırlarını aşmamak için kontrol
                break

            if isinstance(item, dict) and 'isbn' in item:
                # 'borrowed' bilgisi
                isbn = item.get('isbn', "")
                book_data_account = self.books.find_one({"isbn": isbn})

                if book_data_account:
                    # Kitap bilgilerini al
                    title = shorten_text(book_data_account.get('title', 'Bilinmiyor'))
                    author = book_data_account.get('author', 'Bilinmiyor')
                    publisher = book_data_account.get('publisher', 'Bilinmiyor')
                    year = book_data_account.get('year', 'Bilinmiyor')
                    edition = book_data_account.get('edition', 'Bilinmiyor')

                    # Ödünç alma tarihlerini al
                    borrow_date = item.get('borrow_date', 'Bilinmiyor')
                    last_due_date = item.get('last_due_date', 'Bilinmiyor')

                    # 'text' listesini doldur
                    lines[index]['text'] = [
                        f"Başlık:\n {title}",
                        f"Yazar:\n {author}",
                        f"Yayınevi:\n {publisher}",
                        f"Yıl:\n {year}",
                        f"Baskı:\n {edition}",
                        f"ISBN:\n {isbn}",
                        # Eğer daha fazla satır gerekiyorsa, burada ekleyebilirsiniz
                        f"Ödünç Alma Tarihi:\n {borrow_date}",
                        f"Son Teslim Tarihi:\n {last_due_date}"
                    ]

                    # Eğer 'text' listesine ekstra bilgi eklemek isterseniz, multi-line string kullanabilirsiniz
                    # Örneğin:

                else:
                    # Kitap bulunamadıysa, boş stringlerle doldur
                    lines[index]['text'] = [""]

            elif isinstance(item, int) and item:
                # 'borrow_req' bilgisi (ISBN numarası)
                isbn = item
                book_data_account = self.books.find_one({"isbn": isbn})

                if book_data_account:
                    # Kitap bilgilerini al
                    title = shorten_text(book_data_account.get('title', 'Bilinmiyor'))
                    author = book_data_account.get('author', 'Bilinmiyor')
                    publisher = book_data_account.get('publisher', 'Bilinmiyor')
                    year = book_data_account.get('year', 'Bilinmiyor')
                    edition = book_data_account.get('edition', 'Bilinmiyor')

                    # 'text' listesini doldur
                    lines[index]['text'] = [
                        f"Başlık:\n {title}",
                        f"Yazar:\n {author}",
                        f"Yayınevi:\n {publisher}",
                        f"Yıl:\n {year}",
                        f"Baskı:\n {edition}",
                        f"ISBN:\n {isbn}"

                    ]
                else:
                    # Kitap bulunamadıysa, boş stringlerle doldur
                    lines[index]['text'] = [""]

            else:
                # Boş bilgi, 'text' listesini boş stringlerle doldur
                lines[index]['text'] = [""]

            # lines değişkeni artık güncellenmiş durumda
            # Bu noktada, lines değişkenini uygun şekilde kullanabilirsiniz
            # Örneğin, bir kullanıcı arayüzünde göstermek için döndürebilirsiniz

        # Canvas boyutunu yeniden hesaplama
        canvas.bind("<Configure>", lambda event: self.redraw_canvas(canvas, lines))

    def open_return_cancel_popup(self):
        """İade/İptal popup'ını açar."""
        popup = tk.Toplevel(self.master)
        popup.title("İade/İptal İşlemi")
        popup.geometry("500x200")
        popup.resizable(False, False)  # Boyut değiştirilemez
        popup.grab_set()

        # ISBN giriş etiketi ve kutusu
        tk.Label(
            popup,
            text="İade/İptal etmek istediğiniz kitabın ISBN numarasını girin:",
            font=("Arial", 12)
        ).pack(pady=10)

        isbn_entry = tk.Entry(popup, font=("Arial", 12), width=30)
        isbn_entry.pack(pady=5)

        # Onay butonu
        tk.Button(
            popup,
            text="Onayla",
            font=("Arial", 12),
            bg="blue",
            fg="blue",
            command=lambda: self.return_cancel(int(isbn_entry.get()), popup)
        ).pack(pady=10)

    def return_cancel(self, isbn, popup):
        """İade/İptal işlemi (şimdilik pass)."""
        full_book=self.books.find_one({"isbn": isbn})
        if not full_book:
            popup.destroy()  # Önce mevcut popup'ı kapat
            self.show_invalid_isbn_popup()  # Geçersiz ISBN popup'ını göster
            return

        bor_man = borrow_manager.AskBorrow(users=self.users, user=self.user, books=self.books, book=full_book)
        for user_isbn in self.user['borrow_req']:
            if isbn == user_isbn:
                bor_man.refuse_borrow()
                popup.destroy()
                self.show_confirmed_isbn_popup()
                self.setup_account_page()
                return
        for user_isbn in self.user['borrowed']:
            if isbn == user_isbn['isbn']:
                bor_man.return_book(user_isbn)
                popup.destroy()
                self.show_confirmed_isbn_popup()
                self.setup_account_page()
                return

        self.reload_user()

        popup.destroy()  # Önce mevcut popup'ı kapat
        self.show_invalid_isbn_popup()  # Geçersiz ISBN popup'ını göster

    def show_invalid_isbn_popup(self):
        """Geçersiz ISBN mesajını bir popup penceresinde gösterir."""
        popup = tk.Toplevel(self.master)
        popup.title("Geçersiz ISBN")
        popup.geometry("300x150")
        popup.resizable(False, False)  # Boyut değiştirilemez
        popup.grab_set()

        tk.Label(
            popup,
            text="Geçersiz ISBN numarası!",
            font=("Arial", 12),
            fg="red"
        ).pack(pady=20)

        tk.Button(
            popup,
            text="Tamam",
            font=("Arial", 12),
            bg="blue",
            fg="white",
            command=popup.destroy  # Popup'ı kapatır
        ).pack(pady=10)

    def show_confirmed_isbn_popup(self):
        """Geçersiz ISBN mesajını bir popup penceresinde gösterir."""
        popup = tk.Toplevel(self.master)
        popup.title("Onay")
        popup.geometry("300x150")
        popup.resizable(False, False)  # Boyut değiştirilemez
        popup.grab_set()

        tk.Label(
            popup,
            text="İşlem Tamamlandı",
            font=("Arial", 12),
            fg="red"
        ).pack(pady=20)

        tk.Button(
            popup,
            text="Tamam",
            font=("Arial", 12),
            bg="blue",
            fg="blue",
            command=popup.destroy  # Popup'ı kapatır
        ).pack(pady=10)

    def change_password(self):
        """Şifre değiştirme işlemi."""
        # Yeni bir popup oluştur
        popup = tk.Toplevel(self.master)
        popup.title("Şifre Değiştir")
        popup.geometry("500x200")
        popup.resizable(False, False)  # Boyut değiştirilmesin
        popup.grab_set()

        # Yeni şifre giriş etiketi
        tk.Label(
            popup,
            text="Yeni Şifre Girin:",
            font=("Arial", 12)
        ).pack(pady=10)

        # Yeni şifre giriş kutusu
        new_password_entry = tk.Entry(popup, font=("Arial", 12), width=30, show="*")
        new_password_entry.pack(pady=10)

        # Onay butonu
        def submit_password():
            new_password = new_password_entry.get().strip()

            if new_password:
                # Şifreyi değiştir
                ch_ps = Auth(self.users)
                ch_ps.change_password(new_password, self.user['email'])

                # Kullanıcı bilgilerini yenile
                self.reload_user()

                # Popup'ı kapat
                popup.destroy()
            else:
                messagebox.showwarning("Uyarı", "Lütfen bir şifre girin!")

        tk.Button(
            popup,
            text="Tamam",
            font=("Arial", 12),
            bg="blue",
            fg="white",
            command=submit_password
        ).pack(pady=20)

    def redraw_canvas(self, canvas, lines):
        """Canvas yeniden boyutlandırıldığında çizgileri ve metinleri günceller."""
        canvas.delete("all")  # Tüm öğeleri sil

        for line in lines:
            # Çizgiyi yeniden ekle
            canvas.create_line(line["x"] * canvas.winfo_width(), 0,
                               line["x"] * canvas.winfo_width(), canvas.winfo_height(),
                               fill="blue", width=2)

            # Metinleri yeniden ekle
            for idx, text in enumerate(line["text"]):
                canvas.create_text(
                    line["x"] * canvas.winfo_width() + 15,
                    30 + idx * 50,
                    text=text,
                    font=("Arial", 12),
                    anchor="w",
                    fill="black"
                )

    def get_borrow_info(self):
        """
        Kullanıcının 'borrowed' ve 'borrow_req' listelerinden en fazla üç eleman alır.
        'borrowed' listesindeki öğeler tam sözlük olarak, 'borrow_req' listesindeki
        öğeler ise sadece ISBN numarası olarak tuple'da yer alır. Toplam eleman sayısı
        üçe ulaşmazsa, kalan elemanlar boş string ("") ile doldurulur.

        Returns:
            tuple: Üç elemanlı bir tuple. İlk elemanlar 'borrowed' öğeleri (sözlük),
                   ardından 'borrow_req' öğeleri (string) gelir. Eksik kalan yerler
                   boş string ile doldurulur.
        """
        # 'borrowed' ve 'borrow_req' listelerini alıyoruz, yoksa boş liste atıyoruz
        borrowed = self.user.get('borrowed', [])
        borrow_req = self.user.get('borrow_req', [])
        result = []

        # 'borrowed' listesindeki her öğeyi ekle
        for item in borrowed:
            result.append(item)
            if len(result) == 3:
                break  # 3 eleman toplandıysa döngüden çık

        # 'borrow_req' listesinden öğeleri eklemeye devam et, 3'e kadar
        if len(result) < 3:
            for isbn in borrow_req:
                result.append(isbn)
                if len(result) == 3:
                    break

        # Eğer toplam eleman sayısı 3'e ulaşmadıysa, kalanları boş string ile doldur
        while len(result) < 3:
            result.append("")

        # Sonuç olarak 3 elemanlı bir tuple döndür
        return tuple(result)

    def create_book_widget(self, parent, book, book_type, y_start, y_end):
        """Borrowed veya Borrow Request kitabı için bilgileri belirtilen pozisyonda yerleştirir."""
        book_data = self.books.find_one({"isbn": book.get("isbn")})
        if not book_data:
            return

        # Kitap detaylarını al
        title = book_data.get("title", "Bilinmeyen")
        author = book_data.get("author", "Bilinmeyen")
        publisher = book_data.get("publisher", "Bilinmeyen")
        edition = book_data.get("edition", "Bilinmeyen")
        isbn = book_data.get("isbn", "Bilinmeyen")
        borrow_date = book.get("borrow_date", "")
        due_date = book.get("last_due_date", "")

        # Çerçeve içine bilgileri ekle
        frame = tk.Frame(parent, bg="white", highlightbackground="black", highlightthickness=1)
        frame.place(relx=0, rely=y_start, relwidth=1, relheight=(y_end - y_start))  # Pozisyona göre yerleştir

        tk.Label(
            frame,
            text=f"Kitap İsmi: {title}",
            font=("Arial", 12),
            bg="white",
            fg="black"
        ).pack(anchor="w", padx=10, pady=2)

        tk.Label(
            frame,
            text=f"Yazar: {author}",
            font=("Arial", 12),
            bg="white",
            fg="black"
        ).pack(anchor="w", padx=10, pady=2)

        tk.Label(
            frame,
            text=f"Yayınevi: {publisher}",
            font=("Arial", 12),
            bg="white",
            fg="black"
        ).pack(anchor="w", padx=10, pady=2)

        tk.Label(
            frame,
            text=f"Kaçıncı Baskı: {edition}",
            font=("Arial", 12),
            bg="white",
            fg="black"
        ).pack(anchor="w", padx=10, pady=2)

        tk.Label(
            frame,
            text=f"ISBN: {isbn}",
            font=("Arial", 12),
            bg="white",
            fg="black"
        ).pack(anchor="w", padx=10, pady=2)

        if book_type == "borrowed":
            tk.Label(
                frame,
                text=f"Ödünç Tarihi: {borrow_date}",
                font=("Arial", 12),
                bg="white",
                fg="black"
            ).pack(anchor="w", padx=10, pady=2)

            tk.Label(
                frame,
                text=f"Son Teslim Tarihi: {due_date}",
                font=("Arial", 12),
                bg="white",
                fg="black"
            ).pack(anchor="w", padx=10, pady=2)

    def create_empty_widget(self, parent):
        """Boş bir kutucuk oluşturur."""
        frame = tk.Frame(parent, bg="#FFFDD0", highlightbackground="black", highlightthickness=1)

    def setup_user_library_filters(self, left_frame):
        """Normal kullanıcılar için filtreleme alanını oluşturur."""
        # Ara Butonu
        tk.Button(
            left_frame,
            text="Ara",
            font=("Arial", 14),
            bg="#FFFDD0",  # Butonun arka planı krem
            highlightbackground="#FFFDD0",
            fg="blue",  # Yazı rengi mavi
            command=self.handle_user_search
        ).pack(pady=10, padx=10)

        # Tümünü Sıfırla Butonu
        tk.Button(
            left_frame,
            text="Tümünü Sıfırla",
            font=("Arial", 12),
            bg="#FFFDD0",
            highlightbackground="#FFFDD0",
            fg="blue",
            command=self.reset_all_filters
        ).pack(pady=10)

        # Kitap İsmi Filtreleme
        tk.Label(left_frame, text="Kitap İsmi:", font=("Arial", 12), bg="#FFFDD0").pack(anchor="w", padx=10)
        self.user_book_name_entry = tk.Entry(left_frame, font=("Arial", 12), width=30)
        self.user_book_name_entry.pack(pady=5, padx=10)

        # Kitap İsmi Sonuçları (Altındaki yazı)
        self.user_book_name_label = tk.Label(left_frame, text="", font=("Arial", 10), bg="#FFFDD0", fg="black")
        self.user_book_name_label.pack(anchor="w", padx=10)

        # Kitap İsmi Sıfırla Butonu
        self.book_name_reset = tk.Button(
            left_frame,
            text="Sıfırla",
            font=("Arial", 10),
            bg="#FFFDD0",
            highlightbackground="#FFFDD0",
            fg="blue",
            command=lambda: self.user_reset_filter("book_name")
        )
        self.book_name_reset.pack(anchor="e", padx=10)

        # Yazar Filtreleme
        tk.Label(left_frame, text="Yazar:", font=("Arial", 12), bg="#FFFDD0").pack(anchor="w", padx=10)
        self.user_author_entry = tk.Entry(left_frame, font=("Arial", 12), width=30)
        self.user_author_entry.pack(pady=5, padx=10)

        # Yazar Sonuçları (Altındaki yazı)
        self.user_author_label = tk.Label(left_frame, text="", font=("Arial", 10), bg="#FFFDD0",
                                     highlightbackground="#FFFDD0", fg="black")
        self.user_author_label.pack(anchor="w", padx=10)

        # Yazar Sıfırla Butonu
        self.author_reset = tk.Button(
            left_frame,
            text="Sıfırla",
            font=("Arial", 10),
            bg="#FFFDD0",
            highlightbackground="#FFFDD0",
            fg="blue",
            command=lambda: self.user_reset_filter("author")
        )
        self.author_reset.pack(anchor="e", padx=10)

        # Ödünç Alınabilir Filtre
        self.user_borrowable_var = tk.BooleanVar()
        tk.Checkbutton(
            left_frame,
            text="Kitap Ödünç Alınabilir",
            variable=self.user_borrowable_var,
            font=("Arial", 12),
            bg="#FFFDD0",
            fg="blue",
            command=self.handle_user_search
        ).pack(pady=10, anchor="w")

    def handle_user_search(self):
        """Normal kullanıcıların filtreleme işlemini uygular."""
        book_name = self.user_book_name_entry.get().strip()
        author = self.user_author_entry.get().strip()
        borrowable = self.user_borrowable_var.get()  # Ödünç alınabilir filtre

        # MongoDB sorgusu
        query = {}
        if book_name:
            query["title"] = {"$regex": book_name, "$options": "i"} # Büyük-küçük harf duyarsız
            self.user_book_name_label.config(text=f"Aradığınız: {book_name}")  # Kitap adını etikete yaz
        else:
            self.user_book_name_label.config(text="")  # Boş bırak

        if author:
            query["author"] = {"$regex": author, "$options": "i"}
            self.user_author_label.config(text=f"Aradığınız: {author}")  # Yazar adını etikete yaz
        else:
            self.user_author_label.config(text="")  # Boş bırak

        if borrowable:
            query["available"] = True
            query["book_borrowed"] = False
            query["requested_list"] = False

        self.books_data = list(self.books.find(query).sort("title", 1))  # Sorgu ve sıralama
        self.current_page = 0
        self.update_book_list()

    def select_user_book(self):
        """Kullanıcı seçilen kitabı görür."""
        selected_index = self.book_listbox.curselection()

        if not selected_index:
            messagebox.showwarning("Uyarı", "Lütfen bir kitap seçin!")
            return

        # Seçilen kitabın bilgilerini al
        selected_book = self.books_data[self.current_page * 20 + selected_index[0]]

        # Kitap bilgilerini gösteren popup
        book_popup = tk.Toplevel(self.master)
        book_popup.title("Kitap Detayları")
        book_popup.geometry("400x400")
        book_popup.resizable(False, False)
        book_popup.grab_set()

        # Kitap bilgilerini göster
        details = {
            "Kitap İsmi": selected_book["title"],
            "Yazar": selected_book["author"],
            "Yayıncı": selected_book["publisher"],
            "Basım Yılı": selected_book["year_published"],
            "Kaçıncı Baskı": selected_book["edition"],
            "ISBN": selected_book["isbn"]
        }

        for key, value in details.items():
            tk.Label(
                book_popup,
                text=f"{key}: {value}",
                font=("Arial", 12)
            ).pack(anchor="w", padx=20, pady=5)

        # Duruma göre buton veya mesaj ekle
        if not selected_book["available"]:
            tk.Label(
                book_popup,
                text="Bu kitap alınamaz",
                font=("Arial", 12),
                fg="red"
            ).pack(pady=20)
        elif selected_book["book_borrowed"] or selected_book["requested_list"]:
            tk.Label(
                book_popup,
                text="Bu kitap başkasında",
                font=("Arial", 12),
                fg="red"
            ).pack(pady=20)
        else:
            tk.Button(
                book_popup,
                text="Kitabı İste",
                font=("Arial", 12),
                bg="blue",
                fg="blue",
                command=lambda: self.requesting_book(selected_book, book_popup)  # Şimdilik pass geçecek
            ).pack(pady=20)

    def requesting_book(self, selected_book, popup):
        """Kitap isteme işlemini başlatır (şimdilik pass)."""
        self.reload_user()
        bor_man=borrow_manager.AskBorrow(self.users,self.user,self.books,selected_book)
        if bor_man.borrow_control():
            bor_man.request_borrow()
            self.show_confirmed_isbn_popup()
            self.reload_user()
            mail_system.send_email(
                self.user['email'],
                "Kitap İsteği",
                f"{selected_book.get('author')} - {selected_book.get('title')} kitabını ödünç alma isteğiniz "
                f"alınmıştır en kısa sürede dönüş yapılacaktır.")
            popup.destroy()  # Popup'ı kapat
        else:
            self.no_much_borrow()
            popup.destroy()

    def no_much_borrow(self):
        """Geçersiz ISBN mesajını bir popup penceresinde gösterir."""
        popup = tk.Toplevel(self.master)
        popup.title("Fazla Ödünç")
        popup.geometry("400x150")
        popup.resizable(False, False)  # Boyut değiştirilemez
        popup.grab_set()

        tk.Label(
            popup,
            text="3'ten fazla Kitap ödünç alınamaz",
            font=("Arial", 12),
            fg="red"
        ).pack(pady=20)

        tk.Button(
            popup,
            text="Tamam",
            font=("Arial", 12),
            bg="blue",
            fg="white",
            command=popup.destroy  # Popup'ı kapatır
        ).pack(pady=10)

# --------------------------------------------------------------
#ADMİN SAYFASI

    def setup_admin_tabs(self, active_tab="library"):
        """Admin sekmelerini düzenler."""
        tabs_frame = tk.Frame(self.master, bg="lightgray")
        tabs_frame.pack(side="top", fill="x")

        # Sekme renkleri
        member_tab_color = "darkblue" if active_tab == "members" else "blue"
        library_tab_color = "darkblue" if active_tab == "library" else "blue"
        approvals_tab_color = "darkblue" if active_tab == "approvals" else "blue"

        # Üyeler Sekmesi
        tk.Button(
            tabs_frame,
            text="Üyeler",
            font=("Arial", 14),
            bg="white",
            fg=member_tab_color,
            command=lambda: self.switch_to_admin_section("members")
        ).pack(side="left", padx=10)

        # Kütüphane Yönetimi Sekmesi
        tk.Button(
            tabs_frame,
            text="Kütüphane Yönetimi",
            font=("Arial", 14),
            bg="white",
            fg=library_tab_color,
            command=lambda: self.switch_to_admin_section("library")
        ).pack(side="left", padx=10)

        # Onaylar Sekmesi
        tk.Button(
            tabs_frame,
            text="Onaylar",
            font=("Arial", 14),
            bg="white",
            fg=approvals_tab_color,
            command=lambda: self.switch_to_admin_section("approvals")
        ).pack(side="left", padx=10)

    def switch_to_admin_section(self, section):
        """Admin sekmesine geçiş yapar."""
        self.clear_frame()  # Mevcut içeriği temizle
        self.setup_admin_tabs(active_tab=section)  # Sekmeleri yeniden yükle

        if section == "members":
            self.show_members_section()
        elif section == "library":
            self.show_library_section()
        elif section == "approvals":
            self.show_approvals_section()

#---
#KULLANICI SEKMESİ

    def show_members_section(self):
        """Üyeler sayfasını düzenler."""
        self.clear_frame()
        self.setup_admin_tabs(active_tab="members")  # Sekmeleri güncelle

        # Sol Kısım: Filtreleme
        left_frame = tk.Frame(self.master, bg="#FFFDD0", width=300)
        left_frame.pack(side="left", fill="y")
        self.setup_member_filters(left_frame)  # Filtreleme alanını ekle

        # Sağ Kısım: Kullanıcı Listesi
        right_frame = tk.Frame(self.master, bg="white")
        right_frame.pack(side="right", fill="both", expand=True)

        # Kullanıcı Listesi (Listbox)
        self.member_listbox = tk.Listbox(right_frame, font=("Arial", 12), height=20, width=50)
        self.member_listbox.pack(pady=8, padx=20)

        # Sayfa Geçişi İçin Butonlar
        button_frame = tk.Frame(right_frame, bg="white")
        button_frame.pack(side="bottom", pady=10)

        self.prev_button = tk.Button(
            button_frame,
            text="<",
            font=("Arial", 14),
            bg="lightgray",
            fg="blue",
            command=self.prev_page_members
        )
        self.prev_button.pack(side="left", padx=10)

        self.next_button = tk.Button(
            button_frame,
            text=">",
            font=("Arial", 14),
            bg="lightgray",
            fg="blue",
            command=self.next_page_members
        )
        self.next_button.pack(side="right", padx=10)

        # Seç Butonu
        select_button = tk.Button(
            right_frame,
            text="Seç",
            font=("Arial", 14),
            bg="blue",
            fg="blue",
            width=20,
            height=5,
            command=self.select_member
        )
        select_button.pack(pady=10)

        self.load_members()  # Kullanıcıları yükle

    def setup_member_filters(self, left_frame):
        """Üyeler sayfası için filtreleme alanını oluşturur."""
        # Ara Butonu
        tk.Button(
            left_frame,
            text="Ara",
            font=("Arial", 14),
            bg="#FFFDD0",
            fg="blue",
            command=self.filter_members
        ).pack(pady=10, padx=10)

        # Tümünü Sıfırla Butonu
        tk.Button(
            left_frame,
            text="Tümünü Sıfırla",
            font=("Arial", 12),
            bg="#FFFDD0",
            fg="blue",
            command=self.reset_member_filters
        ).pack(pady=10)

        # İsim Filtreleme
        tk.Label(left_frame, text="İsim:", font=("Arial", 12), bg="#FFFDD0").pack(anchor="w", padx=10)
        self.name_entry = tk.Entry(left_frame, font=("Arial", 12), width=30)
        self.name_entry.pack(pady=5, padx=10)

        # Soyisim Filtreleme
        tk.Label(left_frame, text="Soyisim:", font=("Arial", 12), bg="#FFFDD0").pack(anchor="w", padx=10)
        self.surname_entry = tk.Entry(left_frame, font=("Arial", 12), width=30)
        self.surname_entry.pack(pady=5, padx=10)

        # Özel Arama Butonu
        tk.Button(
            left_frame,
            text="Özel Arama",
            font=("Arial", 12),
            bg="#FFFDD0",
            fg="blue",
            command=self.open_member_search_popup
        ).pack(pady=20)

    def load_members(self):
        """Kullanıcı listesini yükler ve sıralar."""
        # 'banned' ve 'Admin' olmayan kullanıcıları filtrele
        self.members_data = list(
            self.users.find(
                {"name": {"$nin": ["banned", "Admin"]}}  # Bu isimlere sahip olmayan kullanıcıları al
            ).sort("name", 1)  # İsme göre sıralama
        )
        self.current_page = 0
        self.update_member_list()

    def update_member_list(self):
        """Sayfaya göre kullanıcı listesini günceller."""
        self.member_listbox.delete(0, tk.END)

        start = self.current_page * 20
        end = start + 20
        page_members = self.members_data[start:end]

        for member in page_members:
            member_info = f"{member['name']} {member['surname']} - {member['email']}"
            self.member_listbox.insert(tk.END, member_info)

        # Sayfa kontrolü
        if self.current_page == 0:
            self.prev_button.config(state="disabled", bg="gray")
        else:
            self.prev_button.config(state="normal", bg="lightgray")

        if end >= len(self.members_data):
            self.next_button.config(state="disabled", bg="gray")
        else:
            self.next_button.config(state="normal", bg="lightgray")

    def ban_member(self, confirm_popup, member_popup, email, borrowed_books):
        """Kullanıcıyı yasaklar ve ödünç alınan kitapları günceller."""
        confirm_popup.destroy()  # Onay popup'ını kapat

        # Borrowed doluysa kitapları güncelle
        if borrowed_books:
            for book in borrowed_books:
                isbn = book.get("isbn")
                if isbn:
                    book_remove = BookRemove(self.books, isbn)
                    book_remove.update_count(missing=-1, tor=-1)

        # Kullanıcıyı yasakla
        auth = Auth(self.users)
        ban_message = (f"hesabınız engellenmiştir")
        mail_system.send_email(email, "Hesap Engeli", ban_message)
        auth.ban(email)

        member_popup.destroy()  # Kullanıcı bilgilerini gösteren popup'ı kapat

        # Yasaklama işlemi tamamlandı mesajı
        success_popup = tk.Toplevel(self.master)
        success_popup.title("Başarılı")
        success_popup.geometry("300x150")
        success_popup.resizable(False, False)
        success_popup.grab_set()

        tk.Label(
            success_popup,
            text="Kullanıcı başarıyla yasaklandı!",
            font=("Arial", 12),
            fg="green"
        ).pack(pady=20)

        tk.Button(
            success_popup,
            text="Tamam",
            font=("Arial", 12),
            bg="blue",
            fg="blue",
            command=success_popup.destroy
        ).pack(pady=10)

    def show_member_popup(self, member, ban_command=None):
        """
        Bir kullanıcının bilgilerini gösteren popup'ı açar.

        Args:
            member (dict): Kullanıcı bilgilerini içeren sözlük.
            ban_command (function, optional): Yasaklama işlemini başlatan bir fonksiyon.
        """
        member_popup = tk.Toplevel(self.master)
        member_popup.title("Kullanıcı Bilgileri")
        member_popup.geometry("600x400")
        member_popup.resizable(False, False)
        member_popup.grab_set()

        # Kullanıcı bilgilerini göster
        tk.Label(
            member_popup,
            text="Kullanıcı Bilgileri:",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        for key, value in member.items():
            tk.Label(
                member_popup,
                text=f"{key.capitalize()}: {value}",
                font=("Arial", 12)
            ).pack(anchor="w", padx=20)

        #

    def select_member(self):
        """Seçili kullanıcının bilgilerini gösterir."""
        selected_index = self.member_listbox.curselection()

        if not selected_index:
            messagebox.showwarning("Uyarı", "Lütfen bir kullanıcı seçin!")
            return

        # Seçilen kullanıcının bilgilerini al
        selected_member = self.members_data[self.current_page * 20 + selected_index[0]]

        # Popup'ı göster ve yasaklama işlevini bağla
        self.show_member_popup(
            member=selected_member,
            ban_command=self.confirm_ban  # Yasaklama işlevini bağlantı olarak gönder
        )

    def confirm_ban(self, member_popup, member):
        """Kullanıcıyı yasaklama işlemi için onay alır."""
        # Yeni popup oluştur
        confirm_popup = tk.Toplevel(self.master)
        confirm_popup.title("Yasaklama Onayı")
        confirm_popup.geometry("400x200")
        confirm_popup.resizable(False, False)
        confirm_popup.grab_set()

        # Kullanıcıyı yasaklama onayı mesajı
        tk.Label(
            confirm_popup,
            text=f"{member['name']} {member['surname']} kullanıcısını yasaklamak istediğinize emin misiniz?",
            font=("Arial", 12),
            fg="red"
        ).pack(pady=20)

        # Evet ve Hayır butonları
        button_frame = tk.Frame(confirm_popup)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Evet",
            font=("Arial", 12),
            bg="gray",
            fg="blue",
            command=lambda: self.ban_member(confirm_popup, member_popup, member["email"], member.get("borrowed", []))
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Hayır",
            font=("Arial", 12),
            bg="gray",
            fg="blue",
            command=confirm_popup.destroy
        ).pack(side="right", padx=10)
        self.switch_to_admin_section("members")

    def filter_members(self):
        """İsim ve soyisim filtreleme işlemini uygular."""
        name_filter = self.name_entry.get().strip()  # İsim filtresi
        surname_filter = self.surname_entry.get().strip()  # Soyisim filtresi

        # MongoDB sorgusu
        query = {}
        if name_filter:
            query["name"] = {"$regex": name_filter, "$options": "i"}  # İsimde büyük/küçük harf duyarsız eşleşme
        if surname_filter:
            query["surname"] = {"$regex": surname_filter,
                                "$options": "i"}  # Soyisimde büyük/küçük harf duyarsız eşleşme

        self.members_data = list(self.users.find(query).sort("name", 1))  # İsim sıralaması
        self.current_page = 0
        self.update_member_list()  # Listeyi güncelle

    def reset_member_filters(self):
        """Tüm filtreleme girişlerini sıfırlar ve listeyi yeniden yükler."""
        self.name_entry.delete(0, tk.END)  # İsim filtresini sıfırla
        self.surname_entry.delete(0, tk.END)  # Soyisim filtresini sıfırla
        self.load_members()  # Tüm üyeleri yeniden yükle

    def prev_page_members(self):
        """Bir önceki sayfaya geçiş yapar."""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_member_list()  # Listeyi güncelle

    def next_page_members(self):
        """Bir sonraki sayfaya geçiş yapar."""
        if (self.current_page + 1) * 20 < len(self.members_data):
            self.current_page += 1
            self.update_member_list()  # Listeyi güncelle

    def open_member_search_popup(self):
        """Kullanıcı özel arama popup'ını açar."""
        popup = tk.Toplevel(self.master)
        popup.title("Özel Arama")
        popup.geometry("400x200")
        popup.resizable(False, False)  # Boyut değiştirilmesin
        popup.grab_set()

        # Email giriş etiketi ve kutusu
        tk.Label(
            popup,
            text="Kullanıcının email adresini girin:",
            font=("Arial", 12)
        ).pack(pady=10)

        email_entry = tk.Entry(popup, font=("Arial", 12), width=30)
        email_entry.pack(pady=5)

        # Onay butonu
        tk.Button(
            popup,
            text="Ara",
            font=("Arial", 12),
            bg="blue",
            fg="blue",
            command=lambda: self.search_member_by_email(email_entry.get(), popup)
        ).pack(pady=20)

    def search_member_by_email(self, email, popup):
        """Email adresine göre kullanıcı bilgilerini arar ve bilgileri gösterir."""
        popup.destroy()  # Arama popup'ını kapat

        # Kullanıcıyı veritabanında ara
        member = self.users.find_one({"email": email})

        if member:
            # Kullanıcı bilgilerini göster
            member_popup = tk.Toplevel(self.master)
            member_popup.title("Kullanıcı Detayları")
            member_popup.geometry("400x300")
            member_popup.resizable(False, False)
            member_popup.grab_set()

            tk.Label(
                member_popup,
                text="Kullanıcı Bilgileri:",
                font=("Arial", 14, "bold")
            ).pack(pady=10)

            for key, value in member.items():
                tk.Label(
                    member_popup,
                    text=f"{key.capitalize()}: {value}",
                    font=("Arial", 12)
                ).pack(anchor="w", padx=20)

            # Yasaklama butonu
            tk.Button(
                member_popup,
                text="Kullanıcıyı Yasakla",
                font=("Arial", 12),
                bg="red",
                fg="blue",
                command=lambda: self.confirm_ban(member_popup, member)  # Yasaklama işlemi için yeni popup
            ).pack(pady=20)
        else:
            # Kullanıcı bulunamadı mesajı
            messagebox.showwarning("Hata", "Bu email adresine sahip kullanıcı bulunamadı.")

# ----
# KÜTÜPAHNE SEKMESİ

    def reset_filter(self, filter_type):
        """Belirli bir filtreyi sıfırlar."""
        if filter_type == "book_name":
            self.book_name_entry.delete(0, tk.END)
            self.book_name_label.config(text="")
        elif filter_type == "author":
            self.author_entry.delete(0, tk.END)
            self.author_label.config(text="")

    def handle_search(self):
        """Filtreleme işlemini uygular."""
        book_name = self.book_name_entry.get().strip()
        author = self.author_entry.get().strip()

        # Kitap ve yazar verisi ile MongoDB sorgusu
        query = {}
        if book_name:
            query["title"] = {"$regex": book_name, "$options": "i"}  # Büyük-küçük harf duyarsız
            self.book_name_label.config(text=f"Aradığınız: {book_name}")  # Kitap adını etikete yaz
        else:
            self.book_name_label.config(text="")  # Boş bırak

        if author:
            query["author"] = {"$regex": author, "$options": "i"}
            self.author_label.config(text=f"Aradığınız: {author}")  # Yazar adını etikete yaz
        else:
            self.author_label.config(text="")  # Boş bırak

        self.books_data = list(self.books.find(query).sort("title", 1))  # Sorgu ve sıralama
        self.current_page = 0
        self.update_book_list()

    def show_library_section(self):
        """Kütüphane Yönetimi sayfasını düzenler."""
        self.clear_frame()
        self.setup_admin_tabs(active_tab="library")

        # Sol Kısım: Filtreleme
        left_frame = tk.Frame(self.master, bg="#FFFDD0", width=300)
        left_frame.pack(side="left", fill="y")
        self.setup_library_filters(left_frame)  # Filtreleme alanını ekle

        # Sağ Kısım: Kitap Listesi
        right_frame = tk.Frame(self.master, bg="white")
        right_frame.pack(side="right", fill="both", expand=True)

        # Kitap Listesi (Listbox)
        self.book_listbox = tk.Listbox(right_frame, font=("Arial", 12), height=18, width=50)
        self.book_listbox.pack(pady=10, padx=20)

        # Sol Alt Köşe: Kitap Ekle ve Kitap Çıkar Butonları
        bottom_frame = tk.Frame(left_frame, bg="#FFFDD0")
        bottom_frame.pack(side="bottom", pady=10)

        tk.Button(
            bottom_frame,
            text="Kitap Ekle",
            font=("Arial", 12),
            bg="#FFFDD0",
            highlightbackground="#FFFDD0",
            fg="blue",
            command=self.open_add_book_popup
        ).pack(side="left", padx=5)

        tk.Button(
            bottom_frame,
            text="Kitap Çıkar",
            font=("Arial", 12),
            bg="#FFFDD0",
            highlightbackground="#FFFDD0",
            fg="blue",
            command=self.open_remove_book_popup
        ).pack(side="right", padx=5)

        # Sayfa Geçişi İçin Butonlar
        button_frame = tk.Frame(right_frame, bg="white")
        button_frame.pack(side="bottom", pady=10)



        # Seç Butonu
        select_button = tk.Button(
            right_frame,
            text="Seç",
            font=("Arial", 14),
            bg="blue",
            fg="blue",
            width=20,
            height=2,
            command=self.select_book
        )
        select_button.pack(pady=20)

        self.load_books()  # Kitapları yükle

    def load_books(self):
        """Kitap listesini yükler ve sayfaya göre gösterir."""
        self.books_data = list(self.books.find().sort("title", 1))  # Kitapları title_'a göre sıralar
        self.current_page = 0
        self.update_book_list()

    def update_book_list(self):
        """Sayfaya göre kitap listesini günceller."""
        self.book_listbox.delete(0, tk.END)  # Listeyi temizle

        start = self.current_page * 20
        end = start + 20
        page_books = self.books_data[start:end]

        for book in page_books:
            # Kitap ismi ve yazarı birleştirerek listeye ekle
            book_info = f"{book['title']} - {book['author']}"
            self.book_listbox.insert(tk.END, book_info)

    def select_book(self):
        """Seçili kitabın bilgilerini gösterir."""
        selected_index = self.book_listbox.curselection()

        if not selected_index:
            messagebox.showwarning("Uyarı", "Lütfen bir kitap seçin!")
            return

        # Seçilen kitabın ISBN numarasını al
        selected_book = self.books_data[self.current_page * 20 + selected_index[0]]
        isbn = selected_book["isbn"]

        # ISBN kullanarak kitap bilgilerini göster
        self.handle_isbn_search(isbn, None)

    def open_add_book_popup(self):
        """Kitap ekleme popup'ını açar."""
        popup = tk.Toplevel(self.master)
        popup.title("Kitap Ekle")
        popup.geometry("400x600")
        popup.resizable(False, False)
        popup.grab_set()

        # Kitap Bilgilerini İsteyen Etiketler ve Giriş Kutuları
        labels = ["Kitap İsmi", "Yazar", "Yazıldığı Yıl", "Basım Yılı", "Yayıncı", "Kaçıncı Baskı"]
        entries = {}

        for idx, label in enumerate(labels):
            tk.Label(popup, text=label, font=("Arial", 12)).pack(pady=5, anchor="w", padx=10)
            entry = tk.Entry(popup, font=("Arial", 12))
            entry.pack(pady=5, padx=10)
            entries[label] = entry

        # Ödünç Alınabilir Kutusu
        available_var = tk.BooleanVar()
        tk.Checkbutton(
            popup,
            text="Ödünç Alınabilir mi?",
            variable=available_var,
            font=("Arial", 12)
        ).pack(pady=10, anchor="w", padx=10)

        # Onay Butonu
        tk.Button(
            popup,
            text="Ekle",
            font=("Arial", 12),
            bg="blue",
            fg="blue",
            command=lambda: self.add_book(entries, available_var, popup)
        ).pack(pady=20)

    def add_book(self, entries, available_var, popup):
        """Kitap ekleme işlemini gerçekleştirir."""
        # Girişlerden veri al
        title_ = entries["Kitap İsmi"].get()
        author = entries["Yazar"].get()
        year = int(entries["Yazıldığı Yıl"].get())
        published_year = int(entries["Basım Yılı"].get())
        publiser=entries["Yayıncı"].get()
        edition = entries["Kaçıncı Baskı"].get()
        available = available_var.get()

        # Kitabı ekle
        book = BookInsert(
            self.books, title_=title_, author=author, year=year, published_year=published_year,
            publisher=publiser, edition=edition, available=available
        )
        popup.destroy()  # İlk popup'ı kapat

        # ISBN ve Bilgileri Gösteren Yeni Popup
        isbn_popup = tk.Toplevel(self.master)
        isbn_popup.title("Kitap Bilgileri")
        isbn_popup.geometry("400x300")
        isbn_popup.resizable(False, False)
        isbn_popup.grab_set()

        tk.Label(isbn_popup, text="Kitap Eklendi!", font=("Arial", 14)).pack(pady=10)
        tk.Label(isbn_popup, text=f"Kitap İsmi: {title_}", font=("Arial", 12)).pack(pady=5)
        tk.Label(isbn_popup, text=f"Yazar: {author}", font=("Arial", 12)).pack(pady=5)
        tk.Label(isbn_popup, text=f"ISBN: {book.isbn_maker()}", font=("Arial", 12)).pack(pady=5)

        tk.Button(
            isbn_popup,
            text="Tamam",
            font=("Arial", 12),
            bg="blue",
            fg="blue",
            command=isbn_popup.destroy
        ).pack(pady=20)

        isbn_book_stock = self.books.find_one({"title": title_, "author": author})

        self.switch_to_admin_section("library")

    def setup_library_filters(self, left_frame):
        """Admin kitaplık filtreleme alanını oluşturur."""
        # Ara Butonu
        tk.Button(
            left_frame,
            text="Ara",
            font=("Arial", 14),
            bg="#FFFDD0",  # Butonun arka planı beyaz
            highlightbackground="#FFFDD0",
            fg="blue",  # Yazı rengi mavi
            command=self.handle_search
        ).pack(pady=10, padx=10)

        # Tümünü Sıfırla Butonu
        tk.Button(
            left_frame,
            text="Tümünü Sıfırla",
            font=("Arial", 12),
            bg="#FFFDD0",
            highlightbackground="#FFFDD0",
            fg="blue",
            command=self.reset_all_filters
        ).pack(pady=10)

        # Özel Arama Butonu
        tk.Button(
            left_frame,
            text="Özel Arama",
            font=("Arial", 12),
            bg="#FFFDD0",
            highlightbackground="#FFFDD0",
            fg="blue",
            command=self.open_isbn_search_popup
        ).pack(pady=20)

        # Kitap İsmi Filtreleme
        tk.Label(left_frame, text="Kitap İsmi:", font=("Arial", 12), bg="#FFFDD0").pack(anchor="w", padx=10)
        self.book_name_entry = tk.Entry(left_frame, font=("Arial", 12), width=30)  # Sınıf değişkeni olarak tanımlandı
        self.book_name_entry.pack(pady=5, padx=10)

        # Kitap İsmi Sonuçları (Altındaki yazı)
        self.book_name_label = tk.Label(left_frame, text="", font=("Arial", 10), bg="#FFFDD0", fg="black")
        self.book_name_label.pack(anchor="w", padx=10)

        # Kitap İsmi Sıfırla Butonu
        self.book_name_reset = tk.Button(
            left_frame,
            text="Sıfırla",
            font=("Arial", 10),
            bg="#FFFDD0",
            highlightbackground="#FFFDD0",
            fg="blue",
            command=lambda: self.reset_filter("book_name")
        )
        self.book_name_reset.pack(anchor="e", padx=10)

        # Yazar Filtreleme
        tk.Label(left_frame, text="Yazar:", font=("Arial", 12), bg="#FFFDD0", highlightbackground="#FFFDD0").pack(anchor="w", padx=10, pady=5)
        self.author_entry = tk.Entry(left_frame, font=("Arial", 12), width=30)  # Sınıf değişkeni olarak tanımlandı
        self.author_entry.pack(pady=5, padx=10)

        # Yazar Sonuçları (Altındaki yazı)
        self.author_label = tk.Label(left_frame, text="", font=("Arial", 10), bg="#FFFDD0", highlightbackground="#FFFDD0", fg="black")
        self.author_label.pack(anchor="w", padx=10)

        # Yazar Sıfırla Butonu
        self.author_reset = tk.Button(
            left_frame,
            text="Sıfırla",
            font=("Arial", 10),
            highlightbackground="#FFFDD0",
            bg="#FFFDD0",
            fg="blue",
            command=lambda: self.reset_filter("author")
        )
        self.author_reset.pack(anchor="e", padx=10)

    def open_isbn_search_popup(self):
        """Özel arama için ISBN sorgulama popup'ını açar."""

        def validate_input(action, value):
            if action == "1":  # Yeni karakter ekleniyorsa
                return value.isdigit()  # Sadece rakamlara izin ver
            return True


        popup = tk.Toplevel(self.master)
        popup.title("Özel Arama")
        popup.geometry("400x200")
        popup.resizable(False, False)  # Boyutu değiştirilemez
        popup.grab_set()

        # ISBN Giriş Etiketi ve Kutusu
        tk.Label(
            popup,
            text="ISBN Numarası Girin:",
            font=("Arial", 12),
            anchor="w"
        ).pack(pady=10, padx=20)

        validate_command = popup.register(validate_input)
        isbn_entry = tk.Entry(
            popup,
            font=("Arial", 12),
            width=30,
            validate="key",
            validatecommand=(validate_command, "%d", "%P")  # Sadece sayısal girişlere izin ver
        )
        isbn_entry.pack(pady=10, padx=20)


        # Onay Butonu
        tk.Button(
            popup,
            text="Ara",
            font=("Arial", 12),
            bg="blue",
            fg="blue",
            command=lambda: self.handle_isbn_search(isbn_entry.get(), popup)
        ).pack(pady=20)

    def handle_isbn_search(self, isbn, parent_popup):
        """ISBN numarasını kullanarak kitap bilgilerini arar."""
        try:
            isbn = int(isbn)  # ISBN numarasını int'e dönüştür
        except ValueError:
            # Geçersiz ISBN girişinde uyarı popup'ı
            if parent_popup:
                parent_popup.destroy()
            error_popup = tk.Toplevel(self.master)
            error_popup.title("Hata")
            error_popup.geometry("300x150")
            error_popup.resizable(False, False)
            error_popup.grab_set()

            tk.Label(
                error_popup,
                text="Geçersiz ISBN numarası!",
                font=("Arial", 12),
                fg="red"
            ).pack(pady=20)

            tk.Button(
                error_popup,
                text="Tamam",
                font=("Arial", 12),
                bg="blue",
                fg="blue",
                command=error_popup.destroy
            ).pack(pady=10)
            return

        # ISBN numarasını arama
        book = self.books.find_one({"isbn": isbn})

        # Eğer parent_popup varsa, onu kapat
        if parent_popup:
            parent_popup.destroy()

        # Kitap bilgilerini gösteren yeni popup
        result_popup = tk.Toplevel(self.master)
        result_popup.title("Arama Sonucu")
        result_popup.geometry("400x500")
        result_popup.resizable(False, False)  # Boyutu değiştirilemez
        result_popup.grab_set()

        if book:
            # Kitap bilgilerini listele
            tk.Label(
                result_popup,
                text="Kitap Bilgileri:",
                font=("Arial", 14, "bold")
            ).pack(pady=10)

            for key, value in book.items():
                tk.Label(
                    result_popup,
                    text=f"{key.capitalize()}: {value}",
                    font=("Arial", 12)
                ).pack(anchor="w", padx=20)
        else:
            # Kitap bulunamadı mesajı
            tk.Label(
                result_popup,
                text="Kitap Bulunamadı",
                font=("Arial", 14, "bold"),
                fg="red"
            ).pack(pady=10)

        # Tamam Butonu
        tk.Button(
            result_popup,
            text="Tamam",
            font=("Arial", 12),
            bg="blue",
            fg="blue",
            command=result_popup.destroy
        ).pack(pady=20)

    def open_remove_book_popup(self):
        """Kitap çıkarma işlemi için popup açar."""
        # Popup oluştur
        popup = tk.Toplevel(self.master)
        popup.title("Kitap Çıkar")
        popup.geometry("400x300")
        popup.resizable(False, False)  # Boyutu değiştirilmesin
        popup.grab_set()

        # ISBN giriş etiketi
        tk.Label(
            popup,
            text="Silmek istediğiniz kitabın ISBN numarasını girin:",
            font=("Arial", 12)
        ).pack(pady=10)

        # ISBN giriş kutusu
        isbn_entry = tk.Entry(popup, font=("Arial", 12), width=30)
        isbn_entry.pack(pady=5)

        # Hata mesajı için alan
        error_label = tk.Label(popup, text="", font=("Arial", 10), fg="red")
        error_label.pack(pady=5)

        # Onay butonu
        tk.Button(
            popup,
            text="ISBN Doğrula",
            font=("Arial", 12),
            bg="blue",
            fg="blue",
            command=lambda: self.verify_and_show_book(isbn_entry.get(), popup, error_label)
        ).pack(pady=10)

    def verify_and_show_book(self, isbn, popup, error_label):
        """ISBN doğrular ve kitabın bilgilerini gösterir."""
        try:
            isbn = int(isbn)  # ISBN'nin geçerli bir sayı olduğunu kontrol et
        except ValueError:
            error_label.config(text="Geçersiz ISBN numarası!")
            return

        # BookRemove sınıfı ile kontrol et
        book_remove = BookRemove(self.books, isbn)

        if not book_remove.book:
            error_label.config(text="Yanlış ISBN numarası!")
            return

        # Eğer kitap varsa, detayları göster ve silme onayı iste
        error_label.config(text="")  # Hata mesajını temizle
        popup.destroy()  # İlk popup'ı kapat

        confirm_popup = tk.Toplevel(self.master)
        confirm_popup.title("Kitap Detayları")
        confirm_popup.geometry("400x500")
        confirm_popup.resizable(False, False)
        confirm_popup.grab_set()

        # Kitap bilgilerini göster
        book_details = book_remove.book
        tk.Label(
            confirm_popup,
            text="Kitap Bilgileri:",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        for key, value in book_details.items():
            tk.Label(
                confirm_popup,
                text=f"{key.capitalize()}: {value}",
                font=("Arial", 12)
            ).pack(anchor="w", padx=20)

        # Bu kitabı silmek istediğinize emin misiniz?
        tk.Label(
            confirm_popup,
            text="Bu kitabı silmek istediğinize emin misiniz?",
            font=("Arial", 12),
            fg="red"
        ).pack(pady=20)

        # Evet ve Hayır butonları
        button_frame = tk.Frame(confirm_popup)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Evet",
            font=("Arial", 12),
            bg="blue",
            fg="blue",  # Yazı rengi mavi
            command=lambda: self.remove_book(confirm_popup, book_remove)
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Hayır",
            font=("Arial", 12),
            bg="gray",
            fg="blue",  # Yazı rengi mavi
            command=confirm_popup.destroy
        ).pack(side="right", padx=10)

    def remove_book(self, confirm_popup, book_remove):
        """Kitabı siler ve bir başarı mesajı gösterir."""
        # Kitabı sil
        book_remove.update_count(missing=-1, tor=-1)

        # Silme işlemini tamamla
        confirm_popup.destroy()  # Onay popup'ını kapat

        # Başarı mesajı popup'ı
        success_popup = tk.Toplevel(self.master)
        success_popup.title("Başarılı")
        success_popup.geometry("300x150")
        success_popup.resizable(False, False)
        success_popup.grab_set()

        tk.Label(
            success_popup,
            text="Kitap başarıyla silindi!",
            font=("Arial", 12),
            fg="green"
        ).pack(pady=20)

        tk.Button(
            success_popup,
            text="Tamam",
            font=("Arial", 12),
            bg="blue",
            fg="white",
            command=lambda: success_popup.destroy()
        ).pack(pady=10)
        self.switch_to_admin_section("library")

# ----
#ONAYLAR SEKMESİ

    def show_approvals_section(self):
        """Onaylar sekmesini düzenler."""
        self.clear_frame()  # Mevcut içeriği temizle
        self.setup_admin_tabs(active_tab="approvals")  # Sekmeleri güncelle

        # Sağ Kısım: Kitap Listesi
        right_frame = tk.Frame(self.master, bg="white")
        right_frame.pack(side="right", fill="both", expand=True)

        # Kitap Listesi (Listbox)
        self.approval_listbox = tk.Listbox(right_frame, font=("Arial", 12), height=20, width=50)
        self.approval_listbox.pack(pady=10, padx=20)

        # Sol Alt Köşe: Ara Butonu
        bottom_frame = tk.Frame(right_frame, bg="white")
        bottom_frame.pack(side="bottom", pady=10)

        tk.Button(
            bottom_frame,
            text="Seç",
            font=("Arial", 14),
            bg="blue",
            fg="blue",
            command=self.select_approval  # Onaylanacak kitabı seçmek için
        ).pack(pady=20)

        # Kitapları yükle
        self.load_approvals()

    def load_approvals(self):
        """Onaylanmayı bekleyen kitapları yükler."""
        # Tüm requested_list False olmayan kitapları al
        self.approval_data = list(self.books.find({"requested_list": {"$ne": False}}))
        self.update_approval_list()

    def update_approval_list(self):
        """Onaylanmayı bekleyen kitapları listeler."""
        self.approval_listbox.delete(0, tk.END)  # Listeyi temizle

        for book in self.approval_data:
            title = book["title"]
            requested_email = book["requested_list"]
            display_text = f"{title} - {requested_email}"
            self.approval_listbox.insert(tk.END, display_text)

    def select_approval(self):
        """Seçili kitabın detaylarını gösterir."""
        selected_index = self.approval_listbox.curselection()

        if not selected_index:
            messagebox.showwarning("Uyarı", "Lütfen bir kitap seçin!")
            return

        # Seçilen kitabın bilgilerini al
        selected_book = self.approval_data[selected_index[0]]

        # Popup'ı göster
        approval_popup = tk.Toplevel(self.master)
        approval_popup.title("Onay Detayları")
        approval_popup.geometry("400x500")
        approval_popup.resizable(False, False)
        approval_popup.grab_set()

        # Kitap bilgilerini göster
        book_details = {
            "Kitap İsmi": selected_book["title"],
            "Yazar": selected_book["author"],
            "Yayıncı": selected_book["publisher"],
            "Edisyon": selected_book["edition"],
            "ISBN": selected_book["isbn"],
            "Kopyalar": selected_book["copies"],
            "Stok": selected_book["stock"],
        }

        # E-posta bilgileri
        requested_email = selected_book["requested_list"]
        user = self.users.find_one({"email": requested_email})
        if user:
            user_details = {
                "Ad": user["name"],
                "Soyad": user["surname"],
                "E-posta": user["email"]
            }
        else:
            user_details = {"Hata": "Kullanıcı bilgileri bulunamadı"}

        tk.Label(approval_popup, text="Kitap Detayları:", font=("Arial", 14, "bold")).pack(pady=10)
        for key, value in book_details.items():
            tk.Label(approval_popup, text=f"{key}: {value}", font=("Arial", 12)).pack(anchor="w", padx=20)

        tk.Label(approval_popup, text="Kullanıcı Bilgileri:", font=("Arial", 14, "bold")).pack(pady=10)
        for key, value in user_details.items():
            tk.Label(approval_popup, text=f"{key}: {value}", font=("Arial", 12)).pack(anchor="w", padx=20)

        # Butonlar
        button_frame = tk.Frame(approval_popup)
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Kitabı Ver",
            font=("Arial", 12),
            bg="blue",
            fg="blue",
            command=lambda: self.book_given(approval_popup, selected_book, user)
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Kitabı Verme",
            font=("Arial", 12),
            bg="gray",
            fg="blue",
            command=lambda: self.book_not_given(approval_popup, selected_book, user)
        ).pack(side="right", padx=10)

    def book_given(self, popup, choosen_book, user):
        """Kitap verildi işlemini gerçekleştirir."""
        bor_man=borrow_manager.AskBorrow(self.users, user, self.books, choosen_book)
        popup.destroy()
        bor_man.borrowing(self.t_day, self.fif_day)
        self.switch_to_admin_section("approvals")
        give_note = \
            (f"Kitap alma isteğiniz kabul edilmiştir kitabınızı teslim alabilirsini, en geç {self.fif_day} tarihine "
             f"kitabı geri teslim ediniz")
        mail_system.send_email(user['email'], "Kitap İsteği Onayı", give_note)
        messagebox.showinfo("Onay", "Kitap başarıyla teslim edildi.")

    def book_not_given(self, popup, choosen_book, user):
        """Kitap verilmedi işlemini gerçekleştirir."""
        bor_man=borrow_manager.AskBorrow(self.users, user, self.books, choosen_book)
        popup.destroy()
        bor_man.refuse_borrow()
        self.switch_to_admin_section("approvals")





