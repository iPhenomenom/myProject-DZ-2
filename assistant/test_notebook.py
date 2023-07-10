import time

from notebook_classes import *
from random import sample, randint

some_data = """
    This indicates that a Person object has private fields named name and birth
    Date, and that it has public methods named getName, setName and isBirthday. 
    A Book object has private fields named title and authors. A Book object 
    also has public methods named getTitle, getAuthors and addAuthor.

The examples below also model a Person class and Book class, but only shows 
fields or methods as needed for illustration.
Use Relationships 
    """


def get_test_notebook():
    notebook = NoteBook()
    # add 100 notes with some randome data
    for n in range(100):
        # for title take from 3 to 7 samples of strings
        title = ' '.join(sample([d for d in some_data.split()], randint(3, 7)))
        # content is a bit longer
        content = ' '.join(sample([d for d in some_data.split()],
                                  randint(10, len(some_data.split()) - 1)))
        notebook.add_note(Note(Title(title), Content(content)))

    return notebook


if (choice := int(input("1 - test add/del tags/notes\n"
                        "2 - test search\n"
                        "3 - pagination: "))) == 1:
    notebook = NoteBook()

    note = Note(Title("Note1"), Content("Some content\
        blabla ewr rwe rw erw er 23r2 3r "))

    note1 = Note(Title("Note1"), Content("Some content\
        blabla ewr rwe rw erw er 23r2 3r "))

    notebook.add_note(note)
    notebook.add_note(note1)

    for i in range(4):
        tag = Tag(f"tag{i}")
        if i % 2:
            tag.add_note(note)
        else:
            tag.add_note(note1)

        notebook.add_tag(tag)

    tag = Tag("tag0")
    tag.add_note(note1)

    notebook.add_tag(tag)

    for v, tag in notebook.tags.items():
        print(tag.notes)

    notebook.clear_note_tags(1)

    for v, tag in notebook.tags.items():
        print(tag.notes)
elif choice == 2:
    notebook = get_test_notebook()

    notebook.add_tag(Tag("bomba"), 99)

    print(notebook.get_by_tag(Tag("bomba"), False))
    print(notebook.search("Relationships Date", False))
    print(notebook.search_by_id(77))
elif choice == 3:
    for page_n, page in enumerate(get_test_notebook().search("Relationships Date")):
        print(f"================ PAGE: {page_n} =================\n")
        print(page)
        time.sleep(1)