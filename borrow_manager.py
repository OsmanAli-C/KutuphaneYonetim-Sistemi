import pymongo
from debugpy.adapter.components import missing
import mail_system
from add_remove import BookRemove

class AskBorrow(object):

    def __init__(self, users, user, books, book):

        self.users = users
        self.user = user
        self.books = books
        self.book = book #kitap komple bilgiler



    def reload_user(self):
        """Kullanıcının bilgilerini yeniden yükler."""
        self.user = self.users.find_one({"email": self.user["email"]})

    def borrow_control(self):
        """kullanıcının aynı anda 3'ten fazla kitap isteğinde bulunup bulunmadığını kontrol eder"""
        self.reload_user()
        a = self.book['book_borrowed'] == False
        return len(self.user.get('borrowed')) + len(self.user.get('borrow_req'))<3 and a

    def request_borrow(self):
        """kitap isteğinde bulunulduğunda kullanıcının ve kitabın bilgilerine bunu işler"""
        if self.borrow_control():
            self.users.update_one(
                {'email': self.user['email']}, {'$push':{'borrow_req':self.book['isbn']}}
            )

            self.books.update_one(
                {'isbn': self.book['isbn']}, {'$set':{'requested_list': self.user['email']}},
            )

    def refuse_borrow(self):
        """kitap isteği ipta veya ret edildiğinde kullanıcı ve kitabın bilgilerine bunu işler"""
        self.users.update_one(
            {'email': self.user['email']}, {'$pull': {'borrow_req': self.book['isbn']}}
        )

        self.books.update_one(
            {'isbn': self.book['isbn']}, {'$set': {'requested_list': False}},
        )
        mail_system.send_email(
            self.user['email'],
            "Kitap İsteği İptali",
            f"{self.book.get("author")} - {self.book.get('title')} kitabını ödünç alma isteği"
            f" iptal edilmiştir"
        )


    def borrowing(self, take_date, last_date):
        """kitap alma isteği onaylandığında kullanıcının ve kitabın bilgilerine bunu işler"""
        if self.borrow_control() :
            self.users.update_one(
                {'email': self.user['email']},
                {
                    '$push': {
                        'borrowed': {
                            'isbn': self.book['isbn'],
                            'borrow_date': take_date,
                            'last_due_date': last_date
                        }
                    },
                    '$pull': {
                        'borrow_req': self.book['isbn']
                    }
                }

            )

            self.books.update_one(
                {'isbn': self.book['isbn']},
                {
                    '$set': {'requested_list': False, 'book_borrowed': self.user['email']}
                }
            )

            book_remove = BookRemove(self.books, self.book['isbn'])
            book_remove.update_count(tor=-1)




    def return_book(self, isbn):
        """kitap geri teslim edilmek istendiğinde kullanıcı ve kitabın bilgilerine bunu işler"""

        if self.book.get('isbn') == isbn.get('isbn'):
            self.user['borrowed'].remove(isbn)
            book_add = BookRemove(self.books, isbn.get('isbn'))
            book_add.update_count(tor=1)
            self.books.update_one(
                {'isbn': self.book['isbn']}, {'$set': {'requested_list': False, 'book_borrowed': False}},
            )
            self.users.update_one({'email': self.user.get('email')}, {'$pull': {'borrowed': isbn}})

            mail_system.send_email(
                self.user['email'],
                "Kitap Teslimi",
                f"{self.book.get("author")} - {self.book.get('title')} kitabı teslim edilmiştir"
            )
            self.users.update_one({'email': self.user.get('email')}, {'$set': {'br': False}})

            return True
        else:
            return False




