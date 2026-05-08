import os
import csv
from pathlib import Path


# ========================
# 1. Подсчет файлов в директории
# ========================
def count_files_in_directory(dir_path: str) -> int:
    path = Path(dir_path)
    if not path.is_dir():
        print(f"Ошибка: директория '{dir_path}' не существует.")
        return 0

    file_count = sum(1 for item in path.iterdir() if item.is_file())
    print(f"В директории '{dir_path}' находится файлов: {file_count}")
    return file_count


# ========================
# 2. Работа с CSV (чтение, сортировка, фильтрация)
# ========================
def load_posts(filepath: str) -> list[dict]:
    posts = []
    with open(filepath , mode='r' , encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['likes'] = int(row['likes'])
            posts.append(row)
    return posts


def display_posts(posts: list[dict] , title: str = "") -> None:
    if title:
        print(f"\n🔹 {title}")
    print(f"{'ID':<4} | {'Ник':<12} | {'Лайки':<6} | Текст")
    print("-" * 60)
    for p in posts:
        print(f"{p['id']:<4} | {p['nickname']:<12} | {p['likes']:<6} | {p['text']}")
    print()


def save_posts(filepath: str , posts: list[dict]) -> None:
    fieldnames = ['id' , 'nickname' , 'text' , 'likes']
    with open(filepath , mode='w' , encoding='utf-8' , newline='') as f:
        writer = csv.DictWriter(f , fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(posts)
    print(f"Данные успешно сохранены в '{filepath}'")


def create_sample_csv(filepath: str) -> None:
    sample_data = [
        {'id': 1 , 'nickname': 'alex_dev' , 'text': 'Изучаю Python, это круто!' , 'likes': 15} ,
        {'id': 2 , 'nickname': 'maria_code' , 'text': 'Кто знает, как работать с CSV?' , 'likes': 8} ,
        {'id': 3 , 'nickname': 'ivan_prog' , 'text': 'Выложил новый проект на GitHub' , 'likes': 42} ,
        {'id': 4 , 'nickname': 'anna_web' , 'text': 'Всем хорошего дня!' , 'likes': 23} ,
        {'id': 5 , 'nickname': 'dmitry_ai' , 'text': 'Нейросети меняют мир' , 'likes': 57}
    ]
    save_posts(filepath , sample_data)
    print(f" Файл '{filepath}' не найден. Создан тестовый набор данных.")


# ========================
# Основная программа
# ========================
def main():
    CSV_FILE = "data.csv"

    # --- ПУНКТ 1: Подсчет файлов ---
    print("=" * 60)
    print("1. ПОДСЧЕТ ФАЙЛОВ В ДИРЕКТОРИИ")
    print("=" * 60)
    dir_input = input("Введите путь к папке (Enter для текущей): ").strip() or "."
    count_files_in_directory(dir_input)

    # --- Подготовка данных ---
    if not os.path.exists(CSV_FILE):
        create_sample_csv(CSV_FILE)

    posts = load_posts(CSV_FILE)
    print(f"\nЗагружено записей из '{CSV_FILE}': {len(posts)}")

    # --- ПУНКТ 2.1: Сортировка по строковому полю (ник автора) ---
    print("=" * 60)
    print("2.1. СОРТИРОВКА ПО СТРОКОВОМУ ПОЛЮ (nickname)")
    print("=" * 60)
    sorted_by_nick = sorted(posts , key=lambda x: x['nickname'])
    display_posts(sorted_by_nick , "Отсортировано по нику (А-Я)")

    # --- ПУНКТ 2.2: Сортировка по числовому полю (количество лайков) ---
    print("=" * 60)
    print("2.2. СОРТИРОВКА ПО ЧИСЛОВОМУ ПОЛЮ (likes)")
    print("=" * 60)
    sorted_by_likes = sorted(posts , key=lambda x: x['likes'] , reverse=True)
    display_posts(sorted_by_likes , "Отсортировано по лайкам (по убыванию)")

    # --- ПУНКТ 2.3: Фильтрация по критерию ---
    print("=" * 60)
    print("2.3. ФИЛЬТРАЦИЯ ПО КРИТЕРИЮ (лайки > N)")
    print("=" * 60)
    try:
        threshold = int(input("Введите минимальное количество лайков: "))
        filtered_posts = [p for p in posts if p['likes'] > threshold]
        display_posts(filtered_posts , f"Посты с лайками > {threshold}")
    except ValueError:
        print("Введено не число. Фильтрация пропущена.")

    # --- ПУНКТ 3: Добавление и сохранение новых данных ---
    print("=" * 60)
    print("3. ДОБАВЛЕНИЕ НОВОГО ПОСТА И СОХРАНЕНИЕ В ФАЙЛ")
    print("=" * 60)
    new_id = max((p['id'] for p in posts) , default=0) + 1
    new_nick = input("Введите ник автора: ").strip()
    new_text = input("Введите текст поста: ").strip()

    while True:
        try:
            new_likes = int(input("Введите количество лайков: ").strip())
            break
        except ValueError:
            print("введите целое число.")

    new_post = {
        'id': new_id ,
        'nickname': new_nick ,
        'text': new_text ,
        'likes': new_likes
    }
    posts.append(new_post)

    # Сохраняем обновленный список обратно в файл
    save_posts(CSV_FILE , posts)
    display_posts(posts , "Итоговый список после добавления")

    print("Программа завершена.")


if __name__ == "__main__":
    main()