import random

from matplotlib.pyplot import title
from prompt_toolkit.key_binding.bindings.named_commands import capitalize_word
from pymongo import MongoClient

class BookInsert():
    """
        Yeni kitap ekleme işlemlerini gerçekleştiren sınıf.
        Kitap bilgilerini alır ve MongoDB koleksiyonuna ekler.
        Ayrıca aynı başlık ve yazara sahip kitapların kopyalarını günceller.
    """

    def __init__(self, books, title_, author, year, published_year, publisher, edition, available=True):
        """
        BookInsert sınıfını başlatır.

        Args:
            books (Collection): MongoDB'deki books koleksiyonu.
            title_ (str): Kitap başlığı.
            author (str): Kitap yazarı.
            year (int): Kitabın yayınlandığı yıl.
            published_year (int): Kitabın yayımlandığı yıl (detaylı bilgi için).
            publisher (str): Kitabın yayınevi.
            edition (str): Kitabın baskısı.
            available (bool): Kitap ödünç alınabilir mi? Varsayılan: True.
        """

        self.books = books
        self.title_ = title_.title()
        self.author = author.title()
        self.year = year
        self.available = available
        self.published_year = published_year
        self.publisher = publisher.title()
        self.edition = edition
        self.add_book()



    def isbn_maker(self):
        """
        Kitap için rastgele bir ISBN numarası üretir.
        Daha önce kullanılmamış benzersiz bir ISBN numarası döndürür.

        Returns:
            int: Üretilen benzersiz ISBN numarası.
        """

        isbn = random.randint(10 ** 12, 10 ** 13 - 1)
        while self.books.find_one({'isbn': isbn}):
            isbn = random.randint(10 ** 12, 10 ** 13 - 1)

        return isbn


    def add_book(self):
        """
        Yeni bir kitap ekler ve aynı başlık/yazara sahip kitapların kopyalarını günceller.

        Returns:
            str: Kitap ekleme işleminin sonucu.
        """
        if self.books.find_one({'title': self.title_, 'author': self.author}):
            existing_book = self.books.find_one({'title': self.title_, 'author': self.author},
                                                {'copies': 1, 'stock': 1})

            if existing_book:
                self.count_ = existing_book.get('copies', 0)  # 'copies' al, yoksa 0
                self.book_stock_ = existing_book.get('stock', 0)  # 'stock' al, yoksa 0
        else:
            self.count_ = 0
            self.book_stock_ = 0

        book = {
            'title': self.title_,
            'author': self.author,
            'year': self.year,
            'year_published': self.published_year,
            'publisher': self.publisher,
            'edition': self.edition,
            'isbn': self.isbn_maker(),
            'copies': self.count_,
            'stock': self.book_stock_,
            'book_borrowed': False,
            'available': self.available,#True ise ödünç alınabilir False ise sadece kütüphanede incelenebilir
            'requested_list': False
        }
        self.books.insert_one(book)
        self.books.update_many(
            {'title': self.title_, 'author': self.author},
            {'$inc': {'copies': 1, 'stock': 1}}
            )
        return 'Kitap ekleme işlemi başarılı'


class BookRemove():
    """
    Kitap silme işlemlerini gerçekleştiren sınıf.
    ISBN numarasına göre kitap siler ve kopya sayısını günceller.
    """

    def __init__(self, books, isbn):
        """
        BookRemove sınıfını başlatır ve belirtilen ISBN numarasına göre kitabı siler.

        Args:
            books (Collection): MongoDB'deki books koleksiyonu.
            isbn (int): Silinecek kitabın ISBN numarası.
            missing (int): copies'ten eksiltilecek değer. Varsayılan: -1.
        """

        self.books = books
        self.isbn = isbn
        self.book=books.find_one({'isbn': isbn})
        if not self.book:
            return "Yanlış ISBN numarası"


    def update_count(self, missing=0, tor=0):
        """
        kitabın stock ve copies değerlerini günceller
        """

        book_i=self.books.find_one({'isbn': self.isbn}, {'title': 1, 'author': 1})



        self.books.update_many(
            {'title': book_i['title'], 'author': book_i['author']},
            {'$inc': {'copies': missing, 'stock': tor}}
            )

        if tor == -1 and missing == -1:
            self.books.delete_one({'isbn': self.isbn})
            return  "Kitap kütüphane kitaplığından silindi"


