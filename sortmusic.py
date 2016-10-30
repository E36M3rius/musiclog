import os
from os import walk
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
import shutil

mypath = "/Users/marius/Music/"
musicLoccationPath = "/Users/marius/Music/musiccollection/"
musicCollectionName = "musiccollection"

def organizeMusicCollection(targetLocation, newLocation):
    if not os.path.exists(newLocation):
        os.makedirs(newLocation)

    for (root, directories, filenames) in walk(targetLocation):
        for filename in filenames:
            filePath = os.path.join(root, filename)
            id3 = ID3Read(filePath)
            if id3:
                genre = id3.get('genre', ['unknown'])
                pathTree = getGenreTree(genre[0], getMusicGenres()).replace('.', os.path.sep)+os.path.sep

                if not os.path.exists(newLocation+pathTree):
                    os.makedirs(newLocation+pathTree)

            #    print('copy from '+filePath+' >>> '+os.path.join(newLocation, pathTree, filename))
                shutil.copyfile(filePath, os.path.join(newLocation, pathTree, filename))

        for directory in directories:

            for filename in filenames:
                print(directory)
                if directory != musicCollectionName:
                    filePath = os.path.join(root, directory, filename)
                    id3 = ID3Read(filePath)
                    if id3:
                        genre = id3.get('genre', ['unknown'])
                        pathTree = getGenreTree(genre[0], getMusicGenres()).replace('.', os.path.sep)+os.path.sep

                        if not os.path.exists(newLocation+pathTree):
                            os.makedirs(newLocation+pathTree)

                            #print('copy from '+filePath+' >>> '+os.path.join(newLocation, pathTree, filename))
                        shutil.copyfile(filePath, os.path.join(newLocation, pathTree, filename))
        return

def ID3Read(file):
    id3 = False
    if file.find(".mp3") > 0:
        try:
            id3 = EasyID3(file)

            if "genre" in id3:
                id3['genre'] = id3['genre'][0].lower()
        except Exception as e:
            pass

    return id3

def ID3ReadGenre(id3):
    return id3['genre']

def getMusicGenres2():
    genres = {
        'electronic' : {
            'edm' : 'edm',
            'ambient' : {
                'ambient dub' : 'ambient dub',
                'dark ambient' : 'dark ambient',
                'drone music' : 'drone music',
                'space music' : 'space music',
                'illbient' : 'illbient',
                'psybient' : 'psybient',
                'isolationism' : 'isolationism',
                'lowercase' : 'lowercase'
            },
            'house' : {
                'acid house' : 'acid house',
                'ambient house' : 'ambient house',
                'balearic beat' : 'balearic beat',
                'chicago house' : 'chicago house',
                'deep house' : {
                    'future house',
                    'tropical house'
                },
                'bouncy house' : 'bouncy house',
                'diva house' : 'diva house',
                'handbag house' : 'handbag house',
                'electro house' : {
                    'big room' : 'big room',
                    'complextro' : 'complextro',
                    'melbourne bounce' : 'melbourne bounce',
                    'fidget house' : 'fidget house',
                    'dutch house' : 'dutch house',
                    'moombahton' : {'moombahcore' : 'moombahcore'},
                    'electro swing' : 'electro swing',
                    'french house' : 'french house',
                    'funky house' : 'funky house',
                    'garage house' : 'garage house',
                    'ghetto house' : {'ghettotech' : 'ghettotech'},
                    'hardbag' : 'hardbag',
                    'hard house' : {'hard nrg' : {'nu nrg'}},
                    'hip house' : 'hip house',
                    'italo house' : 'italo house',
                    'jazz house' : 'jazz house',
                    'kwaito' : 'kwaito',
                    'latin house' : 'latin house',
                    'micro house' : 'micro house',
                    'minimal house' : 'minimal house',
                    'new beat' : 'new beat',
                    'outsider house' : 'outsider house',
                    'progressive house' : 'progressive house',
                    'rara tech' : 'rara tech',
                    'tech house' : 'tech house',
                    'tribal house' : 'tribal house',
                    'trival' : 'trival',
                    'witch house' : 'witch house'
                }
            }
        }
    }
    return genres

def getMusicGenres():
    genres = {
        'edm' : 'electronic.edm',
        'house' : 'electronic.house',
        'acid house' : 'electronic.house.acid house',
        'ambient house' : 'electronic.house.ambient house',
        'balearic beat' : 'electronic.house.balearic beat',
        'chicago house' : 'electronic.house.chicago house',
        'deep house' : 'electronic.house.deep house',
        'future house' : 'electronic.house.deep house.future house',
        'tropical house' : 'electronic.house.deep house.tropical house',
        'bouncy house' : 'electronic.house.bouncy house',
        'diva house' : 'electronic.house.diva house',
        'handbag house' : 'electronic.house.handbag house',
        'electro house' : 'electronic.house.electro house',
        'big room' : 'electronic.house.electro house.big room',
        'complextro' : 'electronic.house.electro house.complextro',
        'melbourne bounce' : 'electronic.house.electro house.melbourne bounce',
        'fidget house' : 'electronic.house.electro house.fidget house',
        'dutch house' : 'electronic.house.electro house.dutch house',
        'moombahton' : 'electronic.house.electro house.moombahton',
        'moombahcore' : 'electronic.house.electro house.moombahton.moombahcore',
        'electro swing' : 'electronic.house.electro swing',
        'french house' : 'electronic.house.french house',
        'funky house' : 'electronic.house.funky house',
        'garage house' : 'electronic.house.garage house',
        'ghetto house' : 'electronic.house.ghetto house',
        'ghettotech' : 'electronic.house.ghetto house.ghettotech',
        'hardbag' : 'electronic.house.hardbag',
        'hard house' : 'electronic.house.hard house',
        'hard nrg' : 'electronic.house.hard house.hard nrg',
        'nu nrg' : 'electronic.house.hard house.hard nrg.nu nrg',
        'hip house' : 'electronic.house.hip house',
        'italo house' : 'electronic.house.italo house',
        'jazz house' : 'electronic.house.jazz house',
        'kwaito' : 'electronic.house.kwaito',
        'latin house' : 'electronic.house.latin house',
        'micro house' : 'electronic.house.micro house',
        'minimal house' : 'electronic.house.minimal house',
        'new beat' : 'electronic.house.new beat',
        'outsider house' : 'electronic.house.outsider house',
        'progressive house' : 'electronic.house.progressive house',
        'rara tech' : 'electronic.house.rara tech',
        'tech house' : 'electronic.house.tech house',
        'tribal house' : 'electronic.house.tribal house',
        'trival' : 'electronic.house.trival',
        'witch house' : 'electronic.house.witch house'
    }
    return genres

def getGenreTree(selectedGenre, genres):
    return genres.get(selectedGenre, 'unknown')

organizeMusicCollection(mypath, musicLoccationPath);
