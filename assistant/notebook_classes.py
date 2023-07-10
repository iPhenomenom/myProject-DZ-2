from collections import UserDict
import pickle
import os
import re
from math import ceil


# батьківський клас у якому прописані __init__, @property, @setter,
# які наслідують класи Tag, Title, Content
class Field:
    def __init__(self, value) -> None:
        self.value = value


class Title(Field):  # заголовок
    def __init__(self, value: str) -> None:
        super().__init__(value)


class Content(Field):  # основний зміст нотатки
    def __init__(self, value: str) -> None:
        super().__init__(value)


class Note:
    def __init__(self, title: Title, content: Content):
        self.title = title
        self.content = content
        self.id = 0

    def __str__(self):
        return (f"ID: {self.id}\n"
                f"+{'-' * (len(self.title.value) + 4)}+\n"
                f"|{self.title.value:^{len(self.title.value) + 4}}|\n"
                f"+{'-' * (len(self.title.value) + 4)}+\n"
                f"{self.content.value}")


class Tag(Field):  # тег
    def __init__(self, value):
        super().__init__(value)
        self.notes = []

    def add_note(self, note: Note):
        self.notes.append(note.id)


class NoteBook(UserDict):  # контейнер для нотаток

    def __init__(self, init_list: list[Note] = None):
        init_dict = {n.id: n for n in init_list} if init_list else None
        super().__init__(init_dict)
        self.__max_note_id = self.__get_max_note_id()
        self.tags: dict[str, Tag] = {}
        self.__address_db_file = "note_book_data.dat"
        self.per_page = 3

    def __get_max_note_id(self):
        # start with 0
        # if a first note is added it will have id = 1
        note_id = 0

        if len(self.data) > 0:
            note_id = max([note.id for note in self.data.values()])

        return note_id

    def __paginate(self, notes: list[Note]):
        if not notes:
            return {}

        if self.per_page <= 0:
            self.per_page = 3
            print("Bad per_page value, set to default = 3")

        self.per_page = len(notes) \
            if self.per_page > len(notes) else self.per_page

        ci = 0
        for _ in range(ceil(len(notes) / self.per_page)):
            yield NoteBook(notes[ci:ci + self.per_page])
            ci += self.per_page

    def __str__(self):
        return "\n\n".join([str(v) for v in self.data.values()])

    def add_note(self, note: Note):  # додає нотатку в словник ключем якого є id
        self.__max_note_id += 1
        note.id = self.__max_note_id
        self.data[note.id] = note

    def del_note(self, note_id):  # видаляє нотатки по id
        self.data.pop(note_id)
        return self.data

    def overwrite_note(self, note_id: int, new_note: Note):
        new_note.id = note_id
        self.data[note_id] = new_note

    def add_tag(self, tag: Tag, note_id=None):
        if note_id is not None and note_id > 0:
            tag.add_note(self.data[note_id])

        if tag.value not in self.tags.keys():
            self.tags[tag.value] = tag
        else:
            self.tags[tag.value].notes.extend(tag.notes)
            self.tags[tag.value].notes = list(set(self.tags[tag.value].notes))

    def del_tag(self, tag: Tag):
        self.tags.pop(tag.value, None)

    def untag_note(self, tag, note_id):
        try:
            for note in self.tags[tag.value].notes:
                if note == note_id:
                    self.tags[tag.value].notes.remove(note)
                    break
        except KeyError:
            return False

    def clear_note_tags(self, note_id):
        for tag in self.tags.values():
            self.untag_note(tag, note_id)

    def search(self, text: str, paginate=True):  # пошук нотаток
        # first let's get notes by tag
        result_list = list(self.get_by_tag(Tag(text), False).values())
        pattern = re.compile(f".*{text}.*")
        for note in self.data.values():
            if pattern.search(note.title.value + note.content.value):
                result_list.append(note)

        unique = list(set(result_list))
        unique.sort(key=lambda x: x.id)
        return self.__paginate(unique) if paginate else NoteBook(unique)

    # redundant method because Notebook is UserDict derrivative
    # we can use Notebook()[note_id] instead
    def search_by_id(self, note_id):
        for n_id, note in self.data.items():
            if n_id == note_id:
                return note
        else:
            print("Note not found")

    # this method guarantees to return Notebook
    def get_by_tag(self, tag: Tag, paginate=True):  # пошук по тегу
        result = NoteBook()
        if tag.value in self.tags.keys():
            result = [self.data[n] for n in self.tags[tag.value].notes]
            result = self.__paginate(result) if paginate else NoteBook(result)
        return result

    def get_all(self, paginate=True):  # повертає усі нотатки
        if not paginate:
            return self
        return self.__paginate(list(self.data.values()))

    def save_to_file(self):  # зберігає у файлі
        with open(self.__address_db_file, "wb") as file:
            if file.writable():
                picle_prepared_data = {
                    "data": self.data,
                    "__max_note_id": self.__max_note_id,
                    "tags": self.tags,
                    "per_page": self.per_page,
                    "__address_db_file": self.__address_db_file
                }
                pickle.dump(picle_prepared_data, file)
            else:
                print(f"Cannot save to {self.__address_db_file} file!")
                return False
        return True

    def load_from_file(self):  # завантажує з файлу
        if not os.path.isfile(self.__address_db_file):
            print("Database file was not found!")
            return False

        with open(self.__address_db_file, 'rb') as file:
            if file.readable():
                restored_data = pickle.load(file)
                self.data = restored_data["data"]
                self.__max_note_id = restored_data["__max_note_id"]
                self.tags = restored_data["tags"]
                self.per_page = restored_data["per_page"]
                self.__address_db_file = restored_data["__address_db_file"]
            else:
                print(f"Cannot read from {self.__address_db_file} file!")
                return False
        return True