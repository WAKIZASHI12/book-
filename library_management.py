
import json

class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        """
        Класс для представления книги.
        :param book_id: Уникальный идентификатор книги
        :param title: Название книги
        :param author: Автор книги
        :param year: Год издания книги
        :param status: Статус книги ("в наличии" или "выдана")
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        """Приведение объекта книги к словарю для сохранения в JSON."""
        return {
            "id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict):
        """Создание объекта книги из словаря."""
        return Book(data["id"], data["title"], data["author"], data["year"], data["status"])


class Library:
    def __init__(self, filename: str = "library.json"):
        """
        Класс для управления библиотекой.
        :param filename: Имя файла для сохранения данных библиотеки
        """
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        """Загрузка данных библиотеки из файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books(self):
        """Сохранение данных библиотеки в файл."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """Добавление книги в библиотеку."""
        new_id = max((book.book_id for book in self.books), default=0) + 1
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга с ID {new_id} успешно добавлена.")

    def delete_book(self, book_id: int):
        """Удаление книги из библиотеки."""
        for book in self.books:
            if book.book_id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с ID {book_id} успешно удалена.")
                return
        print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, **kwargs):
        """Поиск книг в библиотеке."""
        results = self.books
        for key, value in kwargs.items():
            results = [book for book in results if str(getattr(book, key, "")).lower() == str(value).lower()]
        if results:
            self.display_books(results)
        else:
            print("Книги по вашему запросу не найдены.")

    def display_books(self, books=None):
        """Отображение всех книг в библиотеке."""
        books = books or self.books
        if not books:
            print("Библиотека пуста.")
        else:
            for book in books:
                print(f"ID: {book.book_id}, Название: {book.title}, Автор: {book.author}, "
                      f"Год: {book.year}, Статус: {book.status}")

    def update_status(self, book_id: int, status: str):
        """Изменение статуса книги."""
        for book in self.books:
            if book.book_id == book_id:
                if status in ["в наличии", "выдана"]:
                    book.status = status
                    self.save_books()
                    print(f"Статус книги с ID {book_id} успешно обновлён.")
                else:
                    print("Некорректный статус. Используйте 'в наличии' или 'выдана'.")
                return
        print(f"Книга с ID {book_id} не найдена.")


def main():
    """Главная функция для работы с приложением."""
    library = Library()

    while True:
        print("\nДоступные действия:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Введите номер действия: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания книги: "))
            library.add_book(title, author, year)
        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            library.delete_book(book_id)
        elif choice == "3":
            field = input("Введите поле для поиска (title, author, year): ").strip()
            value = input("Введите значение для поиска: ").strip()
            library.search_books(**{field: value})
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            book_id = int(input("Введите ID книги для изменения статуса: "))
            status = input("Введите новый статус ('в наличии' или 'выдана'): ").strip()
            library.update_status(book_id, status)
        elif choice == "6":
            print("Выход из приложения.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
