from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional


# ============================================================
#  МОДЕЛЬ ПРЕДМЕТНОЙ ОБЛАСТИ
#  Посты + коллекция постов
# ============================================================


class Post:
    """Одна запись из CSV."""

    __slots__ = ("id", "nickname", "text", "likes")
    _allowed_fields = {"id", "nickname", "text", "likes"}

    def __init__(self, id: int, nickname: str, text: str, likes: int) -> None:
        # Все значения записываются через __setattr__.
        self.id = id
        self.nickname = nickname
        self.text = text
        self.likes = likes

    def __setattr__(self, name: str, value: Any) -> None:
        if name not in self._allowed_fields:
            raise AttributeError(f"Поле '{name}' недоступно для записи")

        if name == "id":
            value = int(value)
            if value <= 0:
                raise ValueError("id должен быть положительным целым числом")
        elif name == "nickname":
            value = str(value).strip()
            if not value:
                raise ValueError("nickname не может быть пустым")
        elif name == "text":
            value = str(value).strip()
            if not value:
                raise ValueError("text не может быть пустым")
        elif name == "likes":
            value = int(value)
            if value < 0:
                raise ValueError("likes не может быть отрицательным")

        object.__setattr__(self, name, value)

    def __iter__(self) -> Iterator[Any]:
        # Позволяет распаковывать объект как кортеж.
        yield self.id
        yield self.nickname
        yield self.text
        yield self.likes

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, nickname={self.nickname!r}, "
            f"text={self.text!r}, likes={self.likes})"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "nickname": self.nickname,
            "text": self.text,
            "likes": self.likes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Post":
        return cls(
            id=data["id"],
            nickname=data["nickname"],
            text=data["text"],
            likes=data["likes"],
        )


class FeaturedPost(Post):
    """Наследник класса Post.

    Используется для демонстрации наследования: такие посты
    считаются 'выделенными', если лайков достаточно много.
    """

    POPULAR_LIMIT = 50

    @staticmethod
    def is_featured(likes: int) -> bool:
        return int(likes) >= FeaturedPost.POPULAR_LIMIT

    def __repr__(self) -> str:
        base = super().__repr__()[:-1]
        return base + f", featured={self.is_featured(self.likes)})"


class CollectionBase:
    """Базовый класс коллекции."""

    def __init__(self, items: Optional[Iterable[Any]] = None) -> None:
        self._items: list[Any] = []
        if items is not None:
            for item in items:
                self._items.append(item)

    def __iter__(self) -> Iterator[Any]:
        return self._iter_items()

    def _iter_items(self) -> Iterator[Any]:
        # Генератор
        for item in self._items:
            yield item

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={len(self._items)})"


class PostCollection(CollectionBase):
    """Коллекция постов с сортировкой, фильтрацией и CSV-операциями."""

    CSV_FIELDS = ("id", "nickname", "text", "likes")

    def __init__(self, posts: Optional[Iterable[Post]] = None) -> None:
        super().__init__(posts)

    def add_post(self, post: Post) -> None:
        if not isinstance(post, Post):
            raise TypeError("В коллекцию можно добавлять только объекты Post")
        self._items.append(post)

    def max_id(self) -> int:
        return max((post.id for post in self._items), default=0)

    def sort_by_nickname(self) -> list[Post]:
        return sorted(self._items, key=lambda post: post.nickname)

    def sort_by_likes(self, reverse: bool = True) -> list[Post]:
        return sorted(self._items, key=lambda post: post.likes, reverse=reverse)

    def filter_by_likes(self, threshold: int) -> Iterator[Post]:
        # Генератор
        for post in self._items:
            if post.likes > threshold:
                yield post

    def filter_by_nickname(self, fragment: str) -> Iterator[Post]:
        # Генератор
        fragment = fragment.lower().strip()
        for post in self._items:
            if fragment in post.nickname.lower():
                yield post

    def to_dicts(self) -> list[dict[str, Any]]:
        return [post.to_dict() for post in self._items]

    def display(self, title: str = "") -> None:
        if title:
            print(f"\n🔹 {title}")
        print(f"{'ID':<4} | {'Ник':<12} | {'Лайки':<6} | Текст")
        print("-" * 70)
        for post in self._items:
            print(f"{post.id:<4} | {post.nickname:<12} | {post.likes:<6} | {post.text}")
        print()

    @staticmethod
    def load_csv(filepath: str | Path) -> "PostCollection":
        path = Path(filepath)
        posts: list[Post] = []

        with path.open(mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                posts.append(
                    Post(
                        id=int(row["id"]),
                        nickname=row["nickname"],
                        text=row["text"],
                        likes=int(row["likes"]),
                    )
                )
        return PostCollection(posts)

    @staticmethod
    def save_csv(filepath: str | Path, posts: Iterable[Post]) -> None:
        path = Path(filepath)
        with path.open(mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(PostCollection.CSV_FIELDS))
            writer.writeheader()
            for post in posts:
                writer.writerow(post.to_dict())

    @staticmethod
    def create_sample_csv(filepath: str | Path) -> None:
        sample = PostCollection(
            [
                Post(1, "alex_dev", "Изучаю Python, это круто!", 15),
                Post(2, "maria_code", "Кто знает, как работать с CSV?", 8),
                Post(3, "ivan_prog", "Выложил новый проект на GitHub", 12),
                Post(4, "anna_web", "Всем хорошего дня!", 23),
                Post(5, "dmitry_ai", "Нейросети меняют мир", 50),
                Post(6 , "oleg_po" , "Архитектура .xml" , 28) ,

            ]
        )
        PostCollection.save_csv(filepath, sample)


class DirectoryInspector:
    """Работа с каталогами."""

    @staticmethod
    def count_files_in_directory(dir_path: str | Path) -> int:
        path = Path(dir_path)
        if not path.is_dir():
            print(f"Ошибка: директория '{path}' не существует.")
            return 0

        file_count = sum(1 for item in path.iterdir() if item.is_file())
        print(f"В директории '{path}' находится файлов: {file_count}")
        return file_count

    @staticmethod
    def iter_files(dir_path: str | Path) -> Iterator[Path]:
        # Генератор
        path = Path(dir_path)
        if path.is_dir():
            for item in path.iterdir():
                if item.is_file():
                    yield item


# ============================================================
#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================


def read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Введите целое число.")


# ============================================================
#  ОСНОВНАЯ ПРОГРАММА
# ============================================================


def main() -> None:
    csv_file = Path("data.csv")

    print("=" * 60)
    print("1. ПОДСЧЕТ ФАЙЛОВ В ДИРЕКТОРИИ")
    print("=" * 60)
    dir_input = input("Введите путь к папке (Enter для текущей): ").strip() or "."
    DirectoryInspector.count_files_in_directory(dir_input)

    # Создаём тестовый файл, если его нет
    if not csv_file.exists():
        PostCollection.create_sample_csv(csv_file)
        print(f"Файл '{csv_file}' не найден. Создан тестовый набор данных.")

    posts = PostCollection.load_csv(csv_file)
    print(f"\nЗагружено записей из '{csv_file}': {len(posts)}")

    print("=" * 60)
    print("2.1. СОРТИРОВКА ПО СТРОКОВОМУ ПОЛЮ (nickname)")
    print("=" * 60)
    sorted_by_nick = PostCollection(posts.sort_by_nickname())
    sorted_by_nick.display("Отсортировано по нику (А-Я)")

    print("=" * 60)
    print("2.2. СОРТИРОВКА ПО ЧИСЛОВОМУ ПОЛЮ (likes)")
    print("=" * 60)
    sorted_by_likes = PostCollection(posts.sort_by_likes(reverse=True))
    sorted_by_likes.display("Отсортировано по лайкам (по убыванию)")

    print("=" * 60)
    print("2.3. ФИЛЬТРАЦИЯ ПО КРИТЕРИЮ (лайки > N)")
    print("=" * 60)
    threshold = read_int("Введите минимальное количество лайков: ")
    filtered_posts = PostCollection(posts.filter_by_likes(threshold))
    filtered_posts.display(f"Посты с лайками > {threshold}")

    print("=" * 60)
    print("3. ДОБАВЛЕНИЕ НОВОГО ПОСТА И СОХРАНЕНИЕ В ФАЙЛ")
    print("=" * 60)
    new_id = posts.max_id() + 1
    new_nick = input("Введите ник автора: ").strip()
    new_text = input("Введите текст поста: ").strip()
    new_likes = read_int("Введите количество лайков: ")

    new_post = Post(new_id, new_nick, new_text, new_likes)
    posts.add_post(new_post)

    PostCollection.save_csv(csv_file, posts)
    posts.display("Итоговый список после добавления")

    print("Программа завершена.")


if __name__ == "__main__":
    main()
