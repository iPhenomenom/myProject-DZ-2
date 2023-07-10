from notebook_classes import *
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt

GOOD_BYE_MSG = "Good bye!"
COMMAND_ARGS_MAX_COUNT = 1
INDEX_NOT_FOUND = -1
UNKNOWN_TAG = "Not tagged"

notebook = NoteBook()


def show_paginated(notebook: NoteBook, per_page):
    notebook.per_page = per_page
    all_notes = list(notebook.get_all())
    for n, page in enumerate(notebook.get_all(), start=1):
        print(f"Page-{n}:")
        print(page)

        if n < len(all_notes):
            try:
                answer = input("Continue? [Y/n]: ")
            except (EOFError, KeyboardInterrupt):
                answer = "n"

            if answer == "n":
                break


def split_by_len_line(text: str, length: int, split_list: list = None) -> list:
    '''recursively splits the text by the specified length.
    returns a list of text chunks of approximately the same length.
    fucking recursion! I worked with her all night'''
    if split_list is None:
        split_list = []

    if len(text) <= length:
        split_list.append(text)
        return split_list
    else:
        index = length
        while index > 0 and text[index] != ' ':
            index -= 1
        split_list.append(text[:index])
        return split_by_len_line(text[index+1:], length, split_list)


def make_line_longer(line: str, num_of_space: int) -> str:
    '''increases the string length by adding spaces between words'''
    words = line.split(" ")
    result = "  ".join(words[:num_of_space+1])
    others = " ".join(words[num_of_space+1:])
    result += f" {others}"
    return result


def content_format(text: str, length = 80) -> str:
    '''formats text by line length'''
    formatted_text = ""
    separated_text = split_by_len_line(text, length)
    for line in separated_text:
        if line == separated_text[-1]:
            formatted_text += f'{line}'
        else:
            if len(line) == length - 1:
                formatted_text = f"{line}\n"
            else:
                num_of_space = length - len(line)
                longer_line = make_line_longer(line, num_of_space)
                formatted_text += f"{longer_line}\n"
    return formatted_text


def input_error(handler):
    """Errors handler"""

    def decorate_handler(data=None):
        warning = ""
        if handler.__name__ == "call_handler" and data is not None:
            command = data[0]

            if data[1]:
                args_count = len(data[1])
                if args_count > COMMANDS[command]["args_count"]:
                    warning = "Extra arguments discarded.\n"
                    data = data[1][:COMMANDS[command]["args_count"]]
        try :
            return f"{warning}{handler(data)}"
        except KeyError as k_err:
            if handler.__name__ == "call_handler":
                return "Unknown command."
            else:
                print(k_err)
        except ValueError:
            if handler.__name__ == "call_handler":
                return "Too many arguments."
        except IndexError:
            if handler.__name__ in (
                    "add_handler",
                    "change_handler"
            ):
                if not data:
                    return "Input should be: note_id"
            else :
                if not data:
                    return "Specify a note ID please."

    return decorate_handler
# command handlers


@input_error
def hello_handler(data=None):
    return "How can I help you?"

class Help():
    @input_error
    def help_handler(data=None):
        field_len = len(sorted(COMMANDS.keys(), key=lambda x: len(x), reverse=True)[0])
        commands = [f"{c:<{field_len}} - {COMMANDS[c]['description']}" for c in COMMANDS]
        return f"   Available commands:\n\t" + '\n\t'.join(sorted(commands))


@input_error
def add_note(data=None) -> str:
    title = Title(input(f"Title: "))
    if len(title.value) > 80:
        return "The title must contain no more than 80 symbols"
    content = Content(content_format(input(f"Content: ")))
    notebook.add_note(Note(title, content))
    return "Note successfully added."


@input_error
def note_del(data):
    notebook.del_note(int(data[0]))
    return "Note deleted"


@input_error
def search_id(data):
    return notebook.search_by_id(int(data[0]))


@input_error
def search_note(data):
    show_paginated(notebook.search(data[0], False), 3)
    return 'Done!'


@input_error
def add_tag(data):
    tag = Tag(input(f"Add Tag: "))
    note_id = int(data[0])
    notebook.add_tag(tag, note_id)
    return "Tag added"


@input_error
def del_tag(data):
    notebook.del_tag(Tag(data[0]))
    return "Tag Deleted"


@input_error
def search_tag(data):
    show_paginated(notebook.get_by_tag(Tag(data[0]), False), 3)
    return 'Done!'


@input_error
def remove_note(data):
    note_id = int(data[0])
    title = Title(input(f"New Title: "))
    content = Content(input(f"New Content: "))
    new_note = Note(title, content)
    notebook.overwrite_note(note_id, new_note)
    return "Note overwrite"

@input_error
def clear_tags(data):
    notebook.clear_note_tags(data[0])
    return "Tags Deleted"


@input_error
def untag_note(note_id, tag):
    tag = Tag(input())
    note_id = note_id
    notebook.untag_note(tag, note_id)
    return "Tag deleted on Note"


@input_error
def show_tags(data=None):
    tags_list = content_format(", ".join([tag for tag in notebook.tags]))
    return tags_list

class Response():
    @input_error
    def show_all_handler(data=None):
        if len(notebook) == 0:
            return "I do not have any notes yet."

        if data:
            show_paginated(notebook, int(data[0]))
            return "Done!"

        else:
            return str(notebook)


@input_error
def sort_by_tags(data=None):
    sorted_by_tag = {}
    not_tagged = []
    id_with_tags = []
    for tag in sorted(notebook.tags):
        sorted_by_tag[tag] = notebook.get_by_tag(Tag(tag), False)
        id_with_tags.extend(notebook.tags[tag].notes)

    id_with_tags = set(id_with_tags)

    for note in notebook.values():
        if note.id not in id_with_tags:
            not_tagged.append(note)

    for tag, items in sorted_by_tag.items():
        print(f"TAG: {tag}:")
        print('\n'.join([str(n) for n in items.values()]), end="\n\n")

    print(f"TAG: {UNKNOWN_TAG}:")
    print('\n'.join([str(n) for n in not_tagged]), end="\n\n")

    return "Done!"


@input_error
def exit_handler(data=None):
    if notebook.save_to_file():
        print("Database saved.")

    return GOOD_BYE_MSG


COMMANDS = {
    "hello": {
        "handler": hello_handler,
        "args_count": 0,
        "description": "shows greetings"
    },
    "show tags": {
        "handler": show_tags,
        "args_count": 0,
        "description": "shows all tags"
    },
    "help": {
        "handler": Help.help_handler,
        "args_count": 0,
        "description": "shows this help"
    },
    "add note": {
        "handler": add_note,
        "args_count": 0,
        "description": "adds note to the Notebook"
    },
    "add tag": {
        "handler": add_tag,
        "args_count": 1,
        "description": "adds a tag to the Notebook"
    },
    "del note": {
        "handler": note_del,
        "args_count": 1,
        "description": "Deleted note on Notebook"
    },
    "del tag": {
        "handler": del_tag,
        "args_count": 1,
        "description": "Deleted tag"
    },
    "search tag": {
        "handler": search_tag,
        "args_count": 1,
        "description": "Search tag in Notebook"
    },
    "overwrite": {
        "handler": remove_note,
        "args_count": 1,
        "description": "overwrite note"
    },
    "search id": {
        "handler": search_id,
        "args_count": 1,
        "description": "Print Note "
    },
    "find note": {
        "handler": search_note,
        "args_count": 1,
        "description": "Find note on the Notebook"
    },
    "clear tags": {
        "handler": clear_tags,
        "args_count": 1,
        "description": "Clear tags"
    },
    "show all": {
        "handler": Response.show_all_handler,
        "args_count": 1,
        "description": "prints all Notes on Notebook"
    },
    "sort by tags": {
        "handler": sort_by_tags,
        "args_count": 0,
        "description": "outputs all notes sorted by tags"
    },
    "untag": {
        "handler": untag_note,
        "args_count": 1,
        "description": "Untag note"
    },
    "exit": {
        "handler": exit_handler,
        "args_count": 0,
        "description": "quits the program"
    }
}
commands = ['hello', 'help', 'add note', 'add tag', 'del note',
            'search id', 'find note', 'show all', 'exit']


@input_error
def call_handler(command_data):
    if command_data[1] and len(command_data[1]) > COMMAND_ARGS_MAX_COUNT:
        raise ValueError
    return COMMANDS[command_data[0]]["handler"](command_data[1])


def main():
    notebook.load_from_file()
    command_completer = WordCompleter(COMMANDS)

    while True:
        try:
            command_with_args = prompt("Enter command: ", completer=command_completer).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            exit_handler()
            exit()

        if command_with_args:
            command_parts = command_with_args.split(' ')

            command = None
            data = None
            for i, _ in enumerate(command_parts):
                if (command := ' '.join(command_parts[:i + 1])) in list(COMMANDS.keys()):
                    data = command_parts[i + 1:]
                    break

            handler_result = call_handler((command, data))

            print(handler_result)

            if handler_result == GOOD_BYE_MSG:
                break


if __name__ == "__main__":
    main()


