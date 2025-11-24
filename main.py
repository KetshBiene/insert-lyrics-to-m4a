import mutagen
import os 
from typing import Generator

# search by extensions
def search_m4a_lrc_files(dirs : Generator[os.scandir]) -> tuple[list[str], list[str]]:
    m4a_files = []
    lrc_files = []
    for i in dirs:
        if i.is_file():
            if i.name[-4:] == '.m4a':
                m4a_files.append(i.path)
            elif i.name[-4:] == '.lrc' or i.name[-4:] == '.txt':
                lrc_files.append(i.path)
    return m4a_files, lrc_files 

# find two files with exact name except extesion
def search_lrc_m4a_pairs(dirs: Generator[os.scandir]) -> list[tuple[str]]:
    m4a_files, lrc_files = search_m4a_lrc_files(dirs)
    # сut extentions for matching
    m4a_files_sliced = {i[:-4]: i for i in m4a_files}
    lrc_files_sliced = {i[:-4]: i for i in lrc_files}
    matches = set(m4a_files_sliced.keys()).intersection(set(lrc_files_sliced.keys()))
    # get pairs of full path files
    pairs = [(m4a_files_sliced[key], lrc_files_sliced[key]) for key in matches]
    return pairs

# scan all nested dirs
def scan_recursively(path: str, depth: int) -> Generator:
    depth -= 1
    with os.scandir(path) as p:
        for i in p:
            if i.is_file():
                yield i
            if i.is_dir() and depth > 0:
                yield from scan_recursively(i.path, depth)

# read lyrics from file
def write_lyrics_to_m4a(media: tuple[str, str]) -> None:
    m4a_path, lrc_path = media
    with open(lrc_path, 'r', encoding='utf-8') as file:
        lyrics = file.read()
        m4a_file = mutagen.File(m4a_path)
        m4a_file.tags["©lyr"] = lyrics      # Special lyrics tag
        m4a_file.save(m4a_path)
    os.remove(lrc_path)

def main():
    if not path:
        print('Empty path to music dir. Script stopped')
        return
    print('Scanning directory...')
    files = search_lrc_m4a_pairs(scan_recursively(path, 5))
    print(f'Found {len(files)} pairs of music and lyrics')
    print('Starting the embendding proccess...')
    for i in files:
        write_lyrics_to_m4a(i)
    print('Success! All included lyrics files were deleted')

path = r'F:\yandex'
if __name__ == '__main__':
    main()
   