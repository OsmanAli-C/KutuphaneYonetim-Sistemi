import setup
import tkinter as tk
from gui import LibraryApp
import threading
from pymongo import MongoClient

if __name__ == "__main__":
    client, books, users, date_setting = setup.run_setup()
    setup.admin_create(users)
    thread = threading.Thread(target=setup.background_checker, args=(users, books), daemon=True)
    thread.start()
    root = tk.Tk()
    app = LibraryApp(books, users, root)  # Parametrelerle sınıfı başlat
    root.mainloop()
