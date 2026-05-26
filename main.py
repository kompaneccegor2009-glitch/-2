import tkinter as tk
from tkinter import ttk, messagebox
import json

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")

        # Создаем интерфейс
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название книги").grid(row=0, column=0)
        self.book_title = tk.Entry(self.root)
        self.book_title.grid(row=0, column=1)

        tk.Label(self.root, text="Автор").grid(row=1, column=0)
        self.book_author = tk.Entry(self.root)
        self.book_author.grid(row=1, column=1)

        tk.Label(self.root, text="Жанр").grid(row=2, column=0)
        self.book_genre = tk.Entry(self.root)
        self.book_genre.grid(row=2, column=1)

        tk.Label(self.root, text="Количество страниц").grid(row=3, column=0)
        self.book_pages = tk.Entry(self.root)
        self.book_pages.grid(row=3, column=1)

        # Кнопка добавления книги
        add_button = tk.Button(self.root, text="Добавить книгу", command=self.add_book)
        add_button.grid(row=4, columnspan=2)

        # Таблица для отображения книг
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Genre", "Pages"), show='headings')
        for col in ("Title", "Author", "Genre", "Pages"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=5, columnspan=2)

        # Поля для фильтрации
        self.filter_genre = tk.Entry(self.root)
        self.filter_genre.grid(row=6, column=1)
        tk.Button(self.root, text="Фильтровать по жанру", command=self.filter_books).grid(row=6, column=0)

        self.filter_pages = tk.Entry(self.root)
        self.filter_pages.grid(row=7, column=1)
        tk.Button(self.root, text="Фильтровать по страницам", command=self.filter_books_by_pages).grid(row=7, column=0)

    def add_book(self):
        title = self.book_title.get()
        author = self.book_author.get()
        genre = self.book_genre.get()
        pages = self.book_pages.get()

        if not (title and author and genre and pages):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        try:
            pages = int(pages)
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
            return

        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        }

        self.load_data()
        self.books.append(new_book)
        self.save_data()
        self.update_tree()
        self.clear_form()

    def filter_books(self):
        genre = self.filter_genre.get()
        self.update_tree(genre=genre)

    def filter_books_by_pages(self):
        try:
            min_pages = int(self.filter_pages.get())
            self.update_tree(min_pages=min_pages)
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
            return

    def load_data(self):
        try:
            with open('books.json', 'r') as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def save_data(self):
        with open('books.json', 'w') as f:
            json.dump(self.books, f)

    def update_tree(self, genre=None, min_pages=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for book in self.books:
            if genre and book['genre'] != genre:
                continue
            if min_pages and book['pages'] < min_pages:
                continue

            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def clear_form(self):
        self.book_title.delete(0, tk.END)
        self.book_author.delete(0, tk.END)
        self.book_genre.delete(0, tk.END)
        self.book_pages.delete(0,