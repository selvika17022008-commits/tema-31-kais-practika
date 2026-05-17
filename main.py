import json
import os

DB_FILE = "books.json"


def load_books():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_books(books):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)


# --- Ветка feature/add-book ---
def add_book():
    author = input("Введите автора: ")
    title = input("Введите название книги: ")

    books = load_books()
    for book in books:
        if book['author'] == author and book['title'] == title:
            print("Ошибка: Такая книга уже есть!")
            return

    try:
        rating = int(input("Введите оценку (1-5): "))
        if not (1 <= rating <= 5):
            raise ValueError
    except ValueError:
        print("Ошибка: оценка должна быть целым числом от 1 до 5.")
        return

    date = input("Введите дату прочтения (например, 2023-10-25): ")

    books = load_books()
    books.append({
        "author": author,
        "title": title,
        "rating": rating,
        "date": date
    })
    save_books(books)
    print("Книга успешно добавлена!")


# --- Ветка feature/list-and-stats ---
def show_all_books():
    books = load_books()
    if not books:
        print("Список книг пуст.")
        return
    for idx, book in enumerate(books, 1):
        print(f"{idx}. {book['author']} — '{book['title']}' ({book['rating']}/5), прочитано: {book['date']}")


def show_average_rating():
    books = load_books()
    if not books:
        print("Нет данных для расчета.")
        return
    avg = sum(book['rating'] for book in books) / len(books)
    print(f"Средняя оценка всех книг: {avg:.2f}")


def show_author_stats():
    books = load_books()
    if not books:
        print("Нет данных.")
        return
    stats = {}
    for book in books:
        author = book['author']
        stats[author] = stats.get(author, 0) + 1
    print("Статистика по авторам:")
    for author, count in stats.items():
        print(f"{author}: {count} кн.")


# --- Ветка feature/delete ---
def delete_book():
    show_all_books()
    books = load_books()
    if not books:
        return
    try:
        choice = int(input("Введите номер книги для удаления: "))
        if 1 <= choice <= len(books):
            removed = books.pop(choice - 1)
            save_books(books)
            print(f"Книга '{removed['title']}' удалена.")
        else:
            print("Неверный номер.")
    except ValueError:
        print("Введите число.")


def main():
    while True:
        print("\n--- Трекер прочитанных книг ---")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            show_all_books()
        elif choice == "3":
            show_average_rating()
        elif choice == "4":
            show_author_stats()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()