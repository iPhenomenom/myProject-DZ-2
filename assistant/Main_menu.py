from abc import abstractmethod, ABC
from arrange_dir import arrange_dir
from main_address_book import main as adress_book
from main_note import main as note_book
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import random

ABOUT_MLA = '''
  _____  _             ____     ___     _____  _____  
 |_   _|| |__    ___  / ___|   / _ \   |  ___||_   _| 
   | |  | '_ \  / _ \ \___ \  | | | |  | |_     | |   
   | |  | | | ||  __/  ___) |_| |_| |_ |  _|_   | | _ 
   |_|  |_| |_| \___| |____/(_)\___/(_)|_| (_)  |_|(_) 

  The sophisticated organizer for thoughtful

Select an option:
[1] Open your contact book;
[2] Open your note book;
[3] I can put in order the folder where you put something meaning "it should be sorted later."
'''
JOKE_FROM_GPT = '''Why did the AI cross the road?\n
To prove it wasn't chicken, but it didn't need to prove anything to the humans, it already dominated them.'''
FIRST_MENU = 'Your choice -> '


class AbstractResponse(ABC):
    @abstractmethod
    def get_answer(self):
        pass


class AbstractHelp(ABC):
    @abstractmethod
    def help_handler(self):
        pass


def print_about_mla():
    print(ABOUT_MLA)


def print_hello():
    print(random.choice(['Hi, how can I help you?', 'Hello, human!']))


def print_joke():
    print(JOKE_FROM_GPT)


def goodby():
    exit(0)


def start_arrange_dir():
    try:
        dir = input('Give me the link to the dir: ')
    except (KeyboardInterrupt, EOFError):
        print()
        return False
    else:
        arrange_dir(dir)


def start_note_book():
    note_book()


def start_adress_book():
    adress_book()


COMMANDS = ['help', 'hello', 'hi', 'make jok', 'close', 'quit', 'by', 'goodby',
            '3', 'arrange_dir', '2', 'note', 'add note', '1', 'phone_book',
            'address_book', 'call', 'exit']
FUNCTIONS = [print_about_mla, print_hello, print_hello, print_joke, goodby,
             goodby, goodby, goodby, start_arrange_dir, start_arrange_dir,
             start_note_book, start_note_book, start_adress_book,
             start_adress_book, start_adress_book, start_adress_book,
             start_adress_book, goodby]
COMANDS_DICT = dict(zip(COMMANDS, FUNCTIONS))


def main():
    print(ABOUT_MLA)
    while True:
        command_completer = WordCompleter(COMMANDS)  # Створення об'єкта WordCompleter для автозаповнення команд
        user_input = prompt(FIRST_MENU, completer=command_completer)  # Налаштування промпта з автозаповненням
        try:
            COMANDS_DICT[user_input]()
        except KeyError:
            print("\nUnknown command!")


if __name__ == '__main__':
    try:
        while True:
            main()
    except (KeyboardInterrupt, EOFError):
        print("\nSee you later!")
        goodby()