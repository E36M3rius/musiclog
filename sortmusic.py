import os
from os import walk
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
import shutil
import datetime

syncPath = "/Users/marius/Music/"
musicLocationPath = "/Users/marius/Music/music.collection/"
musicCollectionName = "music.collection"

def organizeMusicCollection(targetLocation, newLocation):
    if not os.path.exists(newLocation):
        os.makedirs(newLocation)

    # make this function recursive
    for (root, directories, filenames) in walk(targetLocation):
        for filename in filenames:
            filePath = os.path.join(root, filename)
            processFile(filename, filePath, newLocation)

        for directory in directories:
            for filename in filenames:
                if directory != musicCollectionName:
                    filePath = os.path.join(root, directory, filename)
                    processFile(filename, filePath, newLocation)
        return

def processFile(filename, filePath, newLocation):
    id3 = ID3Read(filePath)
    if id3:
        genre = id3.get('genre', ['unknown'])
        timestamp = os.path.getctime(filePath)
        year = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y')

        month = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%B')

        pathTree = getGenreTree(genre[0], getMusicGenres()).replace('.', os.path.sep)+os.path.sep+year+os.path.sep+month+os.path.sep

        #create dir with year / month
        if not os.path.exists(newLocation+pathTree):
            os.makedirs(newLocation+pathTree)

        #print('copy from '+filePath+' >>> '+os.path.join(newLocation, pathTree, filename))
        print('processing ... '+filePath)

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

def getMusicGenres():
    genres = {
        #edm
        'edm' : 'electronic.edm',
        #house
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
        'witch house' : 'electronic.house.witch house',
        #ambient
        'ambient' : 'electronic.ambient',
        'ambient dub' : 'electronic.ambient.ambient dub',
        'dark ambient' : 'electronic.ambient.dark ambient',
        'drone music' : 'electronic.ambient.drone music',
        'space music' : 'electronic.ambient.space music',
        'illbient' : 'electronic.ambient.illbient',
        'psybient' : 'electronic.ambient.psybient',
        'isolationism' : 'electronic.ambient.isolationism',
        'lowercase' : 'electronic.ambient.lowercase',
        #asian underground
        'asian underground' : 'electronic.asian underground',
        #break beat
        'breakbeat' : 'electronic.breakbeat',
        'acid breaks' : 'electronic.breakbeat.acid breaks',
        'baltimore club' : 'electronic.breakbeat.baltimore club',
        'big beat' : 'electronic.breakbeat.big beat',
        'broken beat' : 'electronic.breakbeat.broken beat',
        'florida breaks' : 'electronic.breakbeat.florida breaks',
        'nu funk' : 'electronic.breakbeat.florida breaks.nu funk',
        'miami bass' : 'electronic.breakbeat.florida breaks.miami bass',
        'jersey club' : 'electronic.breakbeat.jersey club',
        'nu skool breaks' : 'electronic.breakbeat.nu skull breaks',
        #disco
        'disco' : 'electronic.disco',
        'Afro' : 'electronic.disco.afro',
        'cosmic disco' : 'electronic.disco.cosmic disco',
        'disco polo' : 'electronic.disco.disco polo',
        'euro disco' : 'electronic.disco.euro disco',
        'italo disco' : 'electronic.disco.italo disco',
        'nu disco' : 'electronic.disco.nu disco',
        'space disco' : 'electronic.disco.space disco',
        #trance
        'trance' : 'electronic.trance',
        'acid trance' : 'electronic.trance.acid trance',
        'balearic trance' : 'electronic.trance.balearic trance',
        'dream trance' : 'electronic.trance.dream trance',
        'goa trance' : 'electronic.trance.goa trance',
        'hard trance' : 'electronic.trance.hard trance',
        'nitzhonot' : 'electronic.trance.nitzhonot',
        'psychedelic trance' : 'electronic.trance.psychedelic trance',
        'suomisaundi' : 'electronic.trance.psychedelic trance.suomisaundi',
        'full on' : 'electronic.trance.psychedelic trance.full on',
        'progressive trance' : 'electronic.trance.progressive trance',
        'tech trance' : 'electronic.trance.tech trance',
        'uplifting trance' : 'electronic.trance.uplifting trance',
        'vocal trance' : 'electronic.trance.vocal trance',
        #techno
        'techno' : 'electronic.techno',
        'acid techno' : 'electronic.techno.acid techno',
        'detroit techno' : 'electronic.techno.detroit techno',
        'dub techno' : 'electronic.techno.dub techno',
        'free tekno' : 'electronic.techno.free tekno',
        'minimal techno' : 'electronic.techno.minimal techno',
        'nortec' : 'electronic.techno.nortec',
        'tecno brega' : 'electronic.techno.techno brega',
        'techdombe' : 'electronic.techno.techdombe',
        'blues' : 'blues'
    }
    return genres

def getGenreTree(selectedGenre, genres):
    return genres.get(selectedGenre, 'unknown')

organizeMusicCollection(syncPath, musicLocationPath);
