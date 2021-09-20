from pathlib import Path
from typing import List     # for better documentation of function return types

from library.adapters.repository import AbstractRepository
from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__inventory = BooksInventory()
        self.__publishers = []
        self.__authors = []
        self.__users = []
        self.__reviews = []

    def add_book(self, book: Book):
        if self.__inventory.find_book(book.book_id) is None:    # check if already in library
            self.__inventory.add_book(book, 0, 0)   # placeholder price + stock

    def get_books(self) -> List[Book]:
        return self.__inventory.get_books()

    def get_book(self, book_id: int) -> Book:
        return self.__inventory.find_book(book_id)

    def get_book_stock(self, book_id: int) -> int:
        return self.__inventory.find_stock_count(book_id)

    def get_book_price(self, book_id: int) -> int:
        return self.__inventory.find_price(book_id)

    def search_books_by_title(self, title: str) -> List[Book]:
        books = []
        if title is not None:
            books = [book for book in self.get_books() if title.lower() in book.title.lower()]
        return books


def load_books(data_path: Path, repo: MemoryRepository):    # makes list of book objects
    books_filename = str(Path(data_path) / "comic_books_excerpt.json")
    author_filename = str(Path(data_path) / "book_authors_excerpt.json")

    reader = BooksJSONReader(books_filename, author_filename)
    reader.read_json_files()
    books_list = reader.dataset_of_books

    for book in books_list:     # load the books into repo
        repo.add_book(book)


def load_users(data_path: Path, repo: MemoryRepository):
    pass


def load_reviews(data_path: Path, repo: MemoryRepository, users):
    pass


def populate(data_path: Path, repo: MemoryRepository):
    load_books(data_path, repo)
