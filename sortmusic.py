import os
from os import walk
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3

mypath = "/Users/marius/Music/"

def scanFiles(path):
    for (root, directories, filenames) in walk(mypath):
        for filename in filenames:
            id3 = ID3Read(os.path.join(root, filename))
            print (id3['genre'])
        for directory in directories:
            for filename in filenames:
                id3 = ID3Read(os.path.join(root, filename))
                print (id3['genre'])
                break
                return

def ID3Read(file):
    id3 = {'genre' : 'unknown'}

    if file.find(".mp3") > 0:
        try:
            id3 = EasyID3(file)
        except Exception as e:
            pass

        return id3

def ID3ReadGenre(id3):
    return id3['genre']

scanFiles(mypath);
