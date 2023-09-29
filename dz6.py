import sys
from pathlib import Path
import os
import shutil
import re

CATEGORIES = {"Image": ['.JPEG', '.PNG', '.JPG', 'SVG'],
            "Audio": ['.AVI', '.MP4', '.MOV', '.MKV'],
            "Docs": ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', 'PPTX'],
            "Music": ['.MP3', '.FLAC', '.WAV','AMR' ],
            "Archive": ['.ZIP', '.GZ', '.TAR'],
            "Drawing":[".DWG"]
              }


def normalize(file):
    CYRILLIC_SYMBOLS = r"абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ "
    TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

        file = Path(file)
        suffix = file.suffix
        file = file.stem
        file = re.sub("[!/#$%&'()*+,-/:;<=>?@[\]^`{|}~]", "", file)
        file = file.translate(TRANS) + suffix
    return file

def move_file(file:Path, category:str, root_dir:Path) ->None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    file.replace(target_dir.joinpath(normalize(file)))

def get_categories(file:Path)->str:
    extens = file.suffix.upper()
    for cat, exts in CATEGORIES.items():
        if extens in exts:
            return cat
    return "Other"

def sort_folder(path:Path)->None:
    for el in path.glob("**/*"):
        if el.is_file():
            category = get_categories(el)
            move_file(el, category, path)
            unpack(path)
            del_empty_dirs(path)
                
def del_empty_dirs(path):
    for d in os.listdir(path):
        a = os.path.join(path, d)
        if os.path.isdir(a):
            del_empty_dirs(a)
            if not os.listdir(a):
                os.rmdir(a)
                print(a, 'удалена')

def unpack(path:Path)->None:
    for element in path.glob("**/*"):
        if element.suffix.upper() in CATEGORIES["Archive"]:
            parent_dir = element.parent
            new_dir = parent_dir.joinpath(rf"{element.stem}")
            shutil.unpack_archive(element, new_dir)

                

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "There is no path to folder to sort"
    if not path.exists():
        return "Folder does not exist"
    sort_folder(path)

    return "All OK"

if __name__ == "__main__":
    print(main())








