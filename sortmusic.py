import os
from os import walk
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
import shutil
import datetime

#syncPath = u'/Users/marius/Music/'
#musicLocationPath = u'/Users/marius/Music/music.collection/'
syncPath = u'/Volumes/Volume_1/music'
musicLocationPath = u'/Volumes/Volume_1/music/music.collection/'
musicCollectionName = "music.collection"
unknownGenreFiles = 0
missingGenreID3 = 0
verboseLevel = 1

totalFiles = len(os.listdir(syncPath))
processedFiles = 0


def organizeMusicCollection(targetLocation, newLocation):
    if not os.path.exists(newLocation):
        os.makedirs(newLocation)

    walkSyncPath(targetLocation, newLocation)

    return

def walkSyncPath(targetLocation, newLocation, readOnly = False):
    if targetLocation.find(musicCollectionName) > 0:
        return
    processedFiles = 0

    for (root, directories, filenames) in os.walk(targetLocation):
        for filename in filenames:
            filePath = os.path.join(root, filename)
            if not filePath.find(musicCollectionName) > 0:
                processFile(filename, filePath, newLocation, readOnly)
                processedFiles = processedFiles + 1
                if verboseLevel >= 1:
                    percentage = processedFiles / totalFiles
                    print('Progress: ', round(percentage, 2))
    return

def processFile(filename, filePath, newLocation, readOnly = False):
    id3 = ID3Read(filePath)
    if id3:
        genre = id3.get('genre', ['unknown'])
        if genre[0].find('unknown') > 0:
            missingGenreID3+=1

        timestamp = os.path.getctime(filePath)
        year = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y')

        month = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%B')

        pathTree = getGenreTree(genre[0], getMusicGenres()).replace('.', os.path.sep)+os.path.sep+year+os.path.sep+month+os.path.sep

        if pathTree.find('unknown') > 0:
            unknownGenreFiles+=1

        #create dir with year / month
        if not os.path.exists(newLocation+pathTree) and not readOnly:
            os.makedirs(newLocation+pathTree)

        if verboseLevel >= 2:
            print('copy from '+filePath+' >>> '+os.path.join(newLocation, pathTree, filename))

        if verboseLevel >= 1:
            print('processing ... '+filePath)

        try:
            if not readOnly:
                shutil.copyfile(filePath, os.path.join(newLocation, pathTree, filename))
        except Exception as e:
            pass
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

def scanGenres(targetLocation):
    walkSyncPath(targetLocation, musicLocationPath, True)

    return

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
        'blues' : 'blues',
        #pop
        'pop' : 'pop',
        'dance' : 'pop.dance pop',
        'adult contemporary' : 'pop.adult contemporary',
        'arab pop' : 'pop.arab pop',
        'baroque pop' : 'pop.baroque pop',
        'britpop' : 'pop.britpop',
        'bubblegum pop' : 'pop.bubblegum pop',
        'canción' : 'pop.canción',
        'canzone' : 'pop.canzone',
        'chalga' : 'pop.chalga',
        'chanson' : 'pop.chanson',
        'christian pop' : 'pop.christian pop',
        'classical crossover' : 'pop.classical crossover',
        'country pop' : 'pop.country pop',
        'c-pop' : 'pop.c-pop',
        'mandopop' : 'pop.c-pop.mandopop',
        'disco polo' : 'pop.disco polo',
        'electropop' : 'pop.electropop',
        'europop' : 'pop.europop',
        'austropop' : 'pop.europop.austropop',
        'eurobeat' : 'pop.europop.eurobeat',
        'french pop' : 'pop.europop.french pop',
        'italo dance' : 'pop.europop.italo dance',
        'italo disco' : 'pop.europop.italo disco',
        'laïkó' : 'pop.europop.laïkó',
        'latin pop' : 'pop.europop.latin pop',
        'nederpop' : 'pop.europop.nederpop',
        'russian pop' : 'pop.europop.russian pop',
        'fado' : 'pop.fado',
        'folk pop' : 'pop.folk pop',
        'iranian pop' : 'pop.iranian pop',
        'indie pop' : 'pop.indie pop',
        'j-pop' : 'pop.j-pop',
        'jangle pop' : 'pop.jangle pop',
        'k-pop' : 'pop.k-pop',
        'latin ballad' : 'pop.latin ballad',
        'louisiana swamp pop' : 'pop.louisiana swamp pop',
        'mexican pop' : 'pop.mexican pop',
        'new romanticism' : 'pop.new romanticism',
        'operatic pop' : 'pop.operatic pop',
        'pop rap' : 'pop.pop rap',
        'pop rock' : 'pop.pop rock',
        'power pop' : 'pop.pop rock.power pop',
        'soft rock' : 'pop.pop rock.soft rock',
        'pop soul' : 'pop.pop soul',
        'progressive pop' : 'pop.progressive pop',
        'psychedelic pop' : 'pop.psychedelic pop',
        'rebetiko' : 'pop.rebetiko',
        'schlager' : 'pop.schlager',
        'sophisti-pop' : 'pop.sophisti-pop',
        'space age pop' : 'pop.space age pop',
        'sunshine pop' : 'pop.sunshine pop',
        'surf pop' : 'pop.surf pop',
        'synthpop' : 'pop.synthpop',
        'teen pop' : 'pop.teen pop',
        'traditional pop music' : 'pop.traditional pop music',
        'turkish pop' : 'pop.turkish pop',
        'vispop' : 'pop.vispop',
        'wonky pop' : 'pop.wonky pop',
        'worldbeat' : 'pop.worldbeat'
    }
    return genres

def getGenreTree(selectedGenre, genres):
    return genres.get(selectedGenre, 'unknown')

organizeMusicCollection(syncPath, musicLocationPath);
#scanGenres(syncPath)

print('Files missing genre ID3: ', missingGenreID3)
print('Files missing genre collection: ', unknownGenreFiles)
