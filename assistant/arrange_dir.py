from os import listdir, rename, rmdir
from pathlib import Path
import shutil
from sys import argv
from prettytable import PrettyTable


# python3 clean.py '/home/mykhailo/Стільниця/dir_hlam' for test
PATH = '/Users/mykhailo/studies/del/arrange_dir'
list_type_r = set()
list_type_files = dict(zip(['images', 'video', 'archives', 'documents', 'audio', ],
                           [set(), set(), set(), set(), set()]))
dict_arrange = dict(zip(['images', 'video', 'archives', 'documents', 'audio'],
                            [('JPEG', 'PNG', 'JPG', 'SVG'),
                             ('AVI', 'MP4', 'MOV', 'MKV'), ('ZIP', 'GZ', 'TAR'),
                             ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
                             ('MP3', 'OGG', 'WAV', 'AMR')
                             ]))
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k",
               "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts",
               "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i",
               "ji", "g")
all_known_type = ['JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV', 'MKV',
                 'ZIP', 'GZ', 'TAR', 'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX',
                 'PPTX', 'MP3', 'OGG', 'WAV', 'AMR']
all_unknown_type = set()
report = PrettyTable()
report.field_names = ['path_before', 'path_after', 'name_after']


def arrange_dir(dir):
    PATH = dir
    check_name(dir)
    main(dir, PATH)
    print_report()


def main(dir, PATH):
    val = listdir(dir)
    p = Path(dir)
    for i in dict_arrange:
        try:
            (p / i).mkdir()
        except FileExistsError:
            pass
    for file_name in val:
        q = p / file_name
        if q.is_dir():
            main(q, PATH)
        else:
            list_type_r.add(file_name.split('.')[-1])
            for dir_in, type_f in dict_arrange.items():
                if file_name.split('.')[-1].upper() not in all_known_type:
                    all_unknown_type.add(file_name.split('.')[-1])
                if file_name.split('.')[-1].upper() not in type_f:
                    continue
                list_type_files[dir_in].add(str(file_name))
                if file_name.split('.')[-1].upper() in dict_arrange['archives']:
                    unzip(q, p / dir_in / file_name.split('.')[0])
                    break
                else:
                    try:
                        shutil.move(str(dir) + '/' + file_name,
                                    str(PATH) + '/' + dir_in)
                    except:
                        pass
                    add_to_report(dir, str(PATH) + dir_in + '/', file_name)

                    break
    check_name(dir)
    del_empy_dir(dir)

def normalise_path(path_1, path_2):
    path_1 = str(path_1).split('/')
    path_2 = str(path_2).split('/')
    for i, j in enumerate(path_1):
        if j != path_2[i]:
            path_1 = '/'.join(path_1[i - 1:])
            path_2 = '/'.join(path_2[i - 1:])
            break
    return path_1, path_2

def print_report():
    print(report)
    string_return = ''
    string_return += f'\nA list of all known script extensions,' \
                     f' which are found in the target folder: \n{list_type_r}\n'
    string_return += f'\nA list of all extensions unknown to the script:' \
                     f'\n{all_unknown_type}'
    print(string_return)

def add_to_report(path_before, path_after, name_after):
    path_before, path_after = normalise_path(path_before, path_after)
    report.add_row(['..' + path_before, '..' + path_after, name_after])

def unzip(file, dir):
    shutil.unpack_archive(file, dir)
    file.unlink()


def check_name(dir):
    val = listdir(dir)
    for k in val:
        l = Path(dir)
        p = l / k
        if p.is_dir():
            val2 = listdir(p)
            for i in val2:
                j = normalize(i)
                if j != i:
                    rename(p / i, p / j)


def normalize(file_name: str):
    def translate(name):
        trans = {}
        for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
            trans[ord(c)] = l
            trans[ord(c.upper())] = l.upper()
        return name.translate(trans)
    res = ''
    for i in file_name:
        if 96 < ord(i) < 123 or 64 < ord(i) < 91 or i.isdigit() or i == '.':
            res += i
        elif 1039 < ord(i) < 1104:
            res += translate(i)
        else:
            res += '_'
    return res


def del_empy_dir(dir):
    val = listdir(dir)
    p = Path(dir)
    for i in val:
        if (p / i).is_dir():
            try:
                rmdir(p / i)
            except OSError:
                pass


if __name__ == '__main__':
    arrange_dir(PATH)