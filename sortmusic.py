import os
from os import walk
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
import shutil
import datetime

if os.name == 'nt':
    sourcePath = u'\\\\DLINK-00445C\\Volume_1\\music\\'
    scanPath = u'\\\\DLINK-00445C\\Volume_1\\music\\music.collection\\unknown\\'
    destinationPath = u'\\\\DLINK-00445C\\Volume_1\\music\\music.collection\\'
elif os.name == 'mac':
    sourcePath = u'/Volumes/Volume_1/music'
    scanPath = u'/Volumes/Volume_1/music'
    destinationPath = u'/Volumes/Volume_1/music/music.collection/'

musicCollectionName = "music.collection"
verboseLevel = 1

SCAN_MODE = 0

def organizeMusicCollection(targetLocation, newLocation):
    if not os.path.exists(newLocation):
        os.makedirs(newLocation)

    walkSyncPath(targetLocation, newLocation)

    return

def walkSyncPath(targetLocation, newLocation, readOnly = False):
    for (root, directories, filenames) in os.walk(targetLocation):
        for filename in filenames:
            filePath = os.path.join(root, filename)
            if not filePath.find(musicCollectionName) > 0 or readOnly == True:
                processFile(filename, filePath, newLocation, readOnly)
    return

def processFile(filename, filePath, newLocation, readOnly = False):
    id3 = ID3Read(filePath)
    if id3:
        genre = id3.get('genre', ['unknown'])

        timestamp = os.path.getctime(filePath)
        year = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y')

        month = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%B')

        genreTree = getGenreTree(genre[0].split('s,')[0], getMusicGenres())
        if genreTree == 'unknown':
            #try one more time
            genreTree = getGenreTree(''.join(reversed(genre[0].split(' '))), getMusicGenres())

        pathTree = genreTree.replace('.', os.path.sep)+os.path.sep+year+os.path.sep+month+os.path.sep

        #create dir with year / month
        if not os.path.exists(newLocation+pathTree) and not readOnly:
            os.makedirs(newLocation+pathTree)

        if verboseLevel >= 2:
            print('copy from '+filePath+' >>> '+os.path.join(newLocation, pathTree, filename))

        if verboseLevel >= 1:
            print('processing ... '+filePath)

        try:
            if not readOnly:
                shutil.move(filePath, os.path.join(newLocation, pathTree, filename))
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
    walkSyncPath(targetLocation, destinationPath, True)

    return

def ID3ReadGenre(id3):
    return id3['genre']

#this needs improvement, make it more intelligent
def getMusicGenres():
    genres = {
        'club' : 'club',
        'electronic' : 'electronic',
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
        #hi-nrg
        'hi-nrg' : 'electronic.hi-nrg',
        'eurobeat' : 'electronic.hi-nrg.eurobeat',
        'eurodance' : 'electronic.hi-nrg.eurodance',
        'bubblegum dance' : 'electronic.hi-nrg.eurodance.bubblegum dance',
        'italo dance' : 'electronic.hi-nrg.eurodance.italo dance',
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
        'retro' : 'electronic.disco',
        'retro , disco' : 'electronic.disco',
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
        'uplifting' : 'electronic.trance.uplifting trance',
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
        #drum and bass
        'drum and bass' : 'electronic.drum & bass',
        'bass' : 'electronic.drum & bass',
        'future bass' : 'electronic.drum & bass.future bass',
        'drum & bass' : 'electronic.drum & bass',
        'darkstep' : 'electronic.drum & bass.darkstep',
        'drill and bass' : 'electronic.drum & bass',
        'drumstep' : 'electronic.drum & bass.drumstep',
        'funkstep' : 'electronic.drum & bass.funkstep',
        'hardstep' : 'electronic.drum & bass.hardstep',
        'jump-up' : 'electronic.drum & bass.jump-up',
        'liquid funk' : 'electronic.drum & bass.liquid funk',
        'neurofunk' : 'electronic.drum & bass.neurofunk',
        'sambass' : 'electronic.drum & bass.sambass',
        'techstep' : 'electronic.drum & bass.techstep',
        #dub
        'dub' : 'electronic.dub',
        #electronic rock
        'electronic rock' : 'electronic.electronic rock',
        'alternative dance' : 'electronic.electronic rock.alternative dance',
        'indietronica' : 'electronic.electronic rock.alternative dance.indietronica',
        'coldwave' : 'electronic.electronic rock.coldwave',
        'dance-punk' : 'electronic.electronic rock.dance-punk',
        'dark wave' : 'electronic.electronic rock.dark wave',
        'electroclash' : 'electronic.electronic rock.electroclash',
        'electronicore' : 'electronic.electronic rock.electronicore',
        'electropunk' : 'electronic.electronic rock.electropunk',
        'ethereal wave' : 'electronic.electronic rock.ethereal wave',
        'krautrock' : 'electronic.electronic rock.krautrock',
        'minimal wave' : 'electronic.electronic rock.minimal wave',
        'new rave' : 'electronic.electronic rock.new rave',
        'nu-gaze' : 'electronic.electronic rock.nu-gaze',
        'space rock' : 'electronic.electronic rock.space rock',
        'synthpop' : 'electronic.electronic rock.synthpop',
        'synthwave' : 'electronic.electronic rock.synthpop.synthwave',
        #electronica
        'electronica' : 'electronic.electronica',
        'berlin school' : 'electronic.electronica.berlin school',
        'dubtronica' : 'electronic.electronica.dubtronica',
        'ethnic electronica' : 'electronic.electronica.ethnic electronica',
        'folktronica' : 'electronic.electronica.folktronica',
        'funktronica' : 'electronic.electronica.funktronica',
        'laptronica' : 'electronic.electronica.laptronica',
        'livetronica' : 'electronic.electronica.livetronica',
        #hardstyle
        'hardstyle' : 'electronic.hardstyle',
        'dubstyle' : 'electronic.hardstyle.dubstyle',
        'jumpstyle' : 'electronic.hardstyle.jumpstyle',
        'lento violento' : 'electronic.hardstyle.lento violento',
        #post disco
        'post-disco' : 'electronic.post-disco',
        'boogie' : 'electronic.post-disco.boogie',
        'electropop' : 'electronic.post-disco.electropop',
        'chillwave' : 'electronic.post-disco.chillwave',
        'dance-pop' : 'electronic.post-disco.dance-pop',
        'dance-rock' : 'electronic.post-disco.dance-rock',
        'indie dance' : 'electronic.post-disco.indie dance',
        #electro music
        'electro music' : 'electronic.electro music',
        #uk garage
        'uk garage' : 'electronic.uk garage',
        '2-step garage' : 'electronic.uk garage.2-step garage',
        'dubstep' : 'electronic.uk garage.2-step garage.dubstep',
        'brostep' : 'electronic.uk garage.2-step garage.dubstep.brostep',
        'chillstep' : 'electronic.uk garage.2-step garage.dubstep.chillstep',
        'reggaestep' : 'electronic.uk garage.2-step garage.dubstep.raggaestep',
        'trapstep' : 'electronic.uk garage.2-step garage.dubstep.trapstep',
        'liquid dubstep' : 'electronic.uk garage.2-step garage.dubstep.liquid dubstep',
        'neurohop' : 'electronic.uk garage.neurohop',
        'breakstep' : 'electronic.uk garage.breakstep',
        'future garage' : 'electronic.uk garage.future garage',
        'grime' : 'electronic.uk garage.grime',
        'grindie' : 'electronic.uk garage.grime.grindie',
        'speed garage' : 'electronic.uk garage.speed garage',
        'bassline/4x4 garage' : 'electronic.uk garage.speed garage.bassline/4x4 garage',
        'uk funky' : 'electronic.uk garage.uk funky',
        'vaporwave' : 'electronic.uk garage.vaporwave',
        'video game music' : 'electronic.uk garage.video game music',
        'chiptune' : 'electronic.uk garage.video game music.chiptune',
        'bitpop' : 'electronic.uk garage.video game music.bitpop',
        'game boy music' : 'electronic.uk garage.video game music.game boy music',
        'skweee' : 'electronic.uk garage.video game music.skweee',
        'nintendocore' : 'electronic.uk garage.nintendocore',
        #pop
        'pop' : 'pop',
        'dance' : 'pop.dance pop',
        'pop, dance' : 'pop.dance pop',
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
        'worldbeat' : 'pop.worldbeat',
        #hip-hop
        'hip-hop' : 'hip-hop',
        'hip hop' : 'hip-hop',
        'hip-hop & rap' : 'hip-hop.rap',
        'reggaeton' : 'hip-hop.reggaeton',
        'reggae' : 'hip-hop.reggaeton',
        'ragga' : 'hip-hop.ragga',
        'alternative hip hop' : 'hip-hop.alternative hip hop',
        'australian hip hop' : 'hip-hop.australian hip hop',
        'bongo flava' : 'hip-hop.bongo flava',
        'british hip hop' : 'hip-hop.british hip hop',
        'chap hop' : 'hip-hop.chap hop',
        'christian hip hop' : 'hip-hop.christian hip hop',
        'conscious hip hop' : 'hip-hop.conscious hip hop',
        'crunk' : 'hip-hop.crunk',
        'crunkcore' : 'hip-hop.crunkcore',
        'drill' : 'hip-hop.drill',
        'east coast hip hop' : 'hip-hop.east coast hip hop',
        'baltimore club' : 'hip-hop.east coast hip hop.baltimore club',
        'brick city club' : 'hip-hop.east coast hip hop.brick city club',
        'hardcore hip hop' : 'hip-hop.east coast hip hop.hardcore hip hop',
        'mafioso rap' : 'hip-hop.east coast hip hop.mafioso rap',
        'new jersey hip hop' : 'hip-hop.east coast hip hop.new jersey hip hop',
        'experimental hip hop' : 'hip-hop.experimental hip hop',
        'ghetto house' : 'hip-hop.ghetto house',
        'ghettotech' : 'hip-hop.ghettotech',
        'golden age hip hop' : 'hip-hop.golden age hip hop',
        'grime' : 'hip-hop.grime',
        'hardcore hip hop' : 'hip-hop.hardcore hip hop',
        'hip house' : 'hip-hop.hip house',
        'hiplife' : 'hip-hop.hiplife',
        'industrial hip hop' : 'hip-hop.industrial hip hop',
        'instrumental hip hop' : 'hip-hop.instrumental hip hop',
        'kwaito' : 'hip-hop.kwaito',
        'lyrical hip hop' : 'hip-hop.lyrical hip hop',
        'low bap' : 'hip-hop.low bap',
        'midwest hip hop' : 'hip-hop.midwest hip hop',
        'chicago hip hop' : 'hip-hop.midwest hip hop.chicago hip hop',
        'ghetto house' : 'hip-hop.midwest hip hop.chicago hip house.ghetto house',
        'detroit hip hop' : 'hip-hop.midwest hip hop.detroit hip hop',
        'ghettotech' : 'hip-hop.midwest hip hop.detroit hip hop.ghettotech',
        'st. louis hip hop' : 'hip-hop.midwest hip hop.st. louis hip hop',
        'twin cities hip hop' : 'hip-hop.midwest hip hop.twin cities hip hop',
        'horrorcore' : 'hip-hop.midwest hip hop.horrorcore',
        'merenrap' : 'hip-hop.merenrap',
        'motswako' : 'hip-hop.motswako',
        'nerdcore' : 'hip-hop.nerdcore',
        'new jack swing' : 'hip-hop.new jack swing',
        'new school hip hop' : 'hip-hop.new school hip hop',
        'old school hip hop' : 'hip-hop.old school hip hop',
        'political hip hop' : 'hip-hop.political hip hop',
        'rap music' : 'hip-hop.rap music',
        'country-rap' : 'hip-hop.rap music.country-rap',
        'cumbia rap' : 'hip-hop.rap music.cumbia rap',
        'freestyle rap' : 'hip-hop.rap music.freestyle rap',
        'gangsta rap' : 'hip-hop.rap music.gangsta rap',
        'igbo rap' : 'hip-hop.rap music.igbo rap',
        'jazz rap' : 'hip-hop.rap music.jazz rap',
        'rap opera' : 'hip-hop.rap music.rap opera',
        'rap rock' : 'hip-hop.rap music.rap rock',
        'rapcore' : 'hip-hop.rap music.rap rock',
        'rap metal' : 'hip-hop.rap music.rap rock',
        'spanish reggae' : 'hip-hop.spanish reggae',
        'southern hip hop' : 'hip-hop.southern hip hop',
        'atlanta hip hop' : 'hip-hop.southern hip hop.atlanta hip hop',
        'snap music' : 'hip-hop.southern hip hop.atlanta hip hop.snap music',
        'bounce music' : 'hip-hop.bounce music',
        'crunk' : 'hip-hop.crunk',
        'houston hip hop' : 'hip-hop.houston hip hop',
        'chopped and screwed' : 'hip-hop.houston hip hop.chopped and screwed',
        'miami bass' : 'hip-hop.houston hip hop.miami bass',
        'songo-salsa' : 'hip-hop.songo-salsa',
        'trap' : 'hip-hop.trap',
        'trip hop (or bristol sound)' : 'hip-hop.trip hop (or bristol sound)',
        'turntablism' : 'hip-hop.turntablism',
        'underground hip hop' : 'hip-hop.underground hip hop',
        'urban pasifika' : 'hip-hop.urban pasifika',
        'west coast hip hop' : 'hip-hop.west coast hip hop',
        'chicano rap' : 'hip-hop.west coast hip hop.chicano rap',
        'g-funk' : 'hip-hop.west coast hip hop.g-funk',
        'hyphy' : 'hip-hop.west coast hip hop.hyphy',
        'jerkin\'' : 'hip-hop.west coast hip hop.jerkin\'',
        #jazz
        'jazz' : 'jazz',
        'acid jazz' : 'jazz.acid jazz',
        'afro-cuban jazz' : 'jazz.afro-cuban jazz',
        'asian american jazz' : 'jazz.asian american jazz',
        'avant-garde jazz' : 'jazz.avant-garde jazz',
        'bebop' : 'jazz.bebop',
        'boogie-woogie' : 'jazz.boogie-woogie',
        'bossa nova' : 'jazz.bossa nova',
        'british dance band' : 'jazz.british dance band',
        'cape jazz' : 'jazz.cape jazz',
        'chamber jazz' : 'jazz.chamber jazz',
        'continental jazz' : 'jazz.continental jazz',
        'cool jazz' : 'jazz.cool jazz',
        'crossover jazz' : 'jazz.crossover jazz',
        'dixieland' : 'jazz.dixieland',
        'ethno jazz' : 'jazz.ethno jazz',
        'european free jazz' : 'jazz.european free jazz',
        'free funk' : 'jazz.free funk',
        'free improvisation' : 'jazz.free improvisation',
        'free jazz' : 'jazz.free jazz',
        'gypsy jazz' : 'jazz.gypsy jazz',
        'hard bop' : 'jazz.hard bop',
        'jazz blues' : 'jazz.jazz blues',
        'jazz-funk' : 'jazz.jazz-funk',
        'jazz fusion' : 'jazz.jazz fusion',
        'jazz rap' : 'jazz.jazz rap',
        'jazz rock' : 'jazz.jazz rock',
        'kansas city blues' : 'jazz.kansas city blues',
        'kansas city jazz' : 'jazz.kansas city jazz',
        'latin jazz' : 'jazz.latin jazz',
        'livetronica' : 'jazz.livetronica',
        'm-base' : 'jazz.m-base',
        'mainstream jazz' : 'jazz.mainstream jazz',
        'modal jazz' : 'jazz.modal jazz',
        'neo-bop jazz' : 'jazz.neo-bop jazz',
        'neo-swing' : 'jazz.neo-swing',
        'novelty ragtime' : 'jazz.novelty ragtime',
        'nu jazz' : 'jazz.nu jazz',
        'orchestral jazz' : 'jazz.orchestral jazz',
        'post-bop' : 'jazz.post-bop',
        'punk jazz' : 'jazz.punk jazz',
        'ragtime' : 'jazz.ragtime',
        'shibuya-kei' : 'jazz.shibuya-kei',
        'ska jazz' : 'jazz.ska jazz',
        'smooth jazz' : 'jazz.smooth jazz',
        'soul jazz' : 'jazz.soul jazz',
        'stride jazz' : 'jazz.stride jazz',
        'straight-ahead jazz' : 'jazz.straight-ahead jazz',
        'swing' : 'jazz.swing',
        'third stream' : 'jazz.third stream',
        'trad jazz' : 'jazz.trad jazz',
        'vocal jazz' : 'jazz.vocal jazz',
        'west coast jazz' : 'jazz.west coast jazz',
        #latin
        'latin' : 'latin',
        'brazilian' : 'latin.brazilian',
        'axé' : 'latin.brazilian.axé',
        'brazilian rock' : 'latin.brazilian.brazilian rock',
        'brega' : 'latin.brazilian.brega',
        'tecnobrega' : 'latin.tecnobregabrazilian.brega.tecnobrega',
        'choro' : 'latin.brazilian.choro',
        'forró' : 'latin.brazilian.forró',
        'frevo' : 'latin.brazilian.frevo',
        'funk carioca' : 'latin.brazilian.funk carioca',
        'lambada' : 'latin.brazilian.lambada',
        'zouk-lambada' : 'latin.brazilian.lambada.zouk-lambada',
        'maracatu' : 'latin.brazilian.maracatu',
        'música popular brasileira' : 'latin.brazilian.música popular brasileira',
        'tropicalia' : 'latin.brazilian.música popular brasileira.tropicalia',
        'música sertaneja' : 'latin.brazilian.música sertaneja',
        'samba' : 'latin.brazilian.samba',
        'pagode' : 'latin.brazilian.samba.pagode',
        'samba rock' : 'latin.brazilian.samba.samba rock',
        'latin christian' : 'latin.latin christian',
        'latin jazz' : 'latin.latin jazz',
        'afro-cuban jazz' : 'latin.latin jazz.afro-cuban jazz',
        'bossa nova' : 'latin.latin jazz.bossa nova',
        'latin pop' : 'latin.latin pop',
        'latin ballad' : 'latin.latin pop.latin ballad',
        'latin rock' : 'latin.latin rock',
        'latin alternative' : 'latin.latin rock.latin alternative',
        'rock en español' : 'latin.latin rock.rock en español',
        'reggaeton' : 'latin.reggaeton',
        'regional mexican' : 'latin.regional mexican',
        'banda' : 'latin.regional mexican.banda',
        'grupera' : 'latin.regional mexican.grupera',
        'mariachi' : 'latin.regional mexican.mariachi',
        'ranchera' : 'latin.regional mexican.mariachi.ranchera',
        'norteño' : 'latin.regional mexican.norteño',
        'tejano' : 'latin.regional mexican.tejano',
        'traditional:' : 'latin.traditional',
        'flamenco' : 'latin.traditional.flamenco',
        'tango' : 'latin.traditional.tango',
        'folk' : 'latin.traditional.folk',
        'bullerengue' : 'latin.traditional.folk.bullerengue',
        'fado' : 'latin.traditional.folk.bullerengue.fado',
        'huayno' : 'latin.traditional.folk.huayno',
        'mexican son' : 'latin.traditional.folk.mexican son',
        'música criolla' : 'latin.traditional.folk.música criolla',
        'nueva canción' : 'latin.traditional.folk.nueva canción',
        'tropical' : 'latin.tropical',
        'bachata' : 'latin.tropical.bachata',
        'bolero' : 'latin.tropical.bolero',
        'criolla' : 'latin.tropical.criolla',
        'cumbia' : 'latin.tropical.cumbia',
        'chicha' : 'latin.tropical.cumbia.chicha',
        'porro' : 'latin.tropical.cumbia.porro',
        'guajira' : 'latin.tropical.guajira',
        'mambo' : 'latin.tropical.mambo',
        'merengue' : 'latin.tropical.merengue',
        'rumba' : 'latin.tropical.rumba',
        'salsa' : 'latin.tropical.salsa',
        'salsa romántica' : 'latin.tropical.salsa.salsa romántica',
        'son' : 'latin.tropical.son',
        'timba' : 'latin.tropical.timba',
        'tropipop' : 'latin.tropical.tropipop',
        'vallenato' : 'latin.tropical.vallenato',
        #r&b
        'r&b' : 'r & b',
        'contemporary r&b' : 'r & b.contemporary r&b',
        'disco' : 'r & b.disco',
        'funk' : 'r & b.funk',
        'deep funk' : 'r & b.funk.deep funk',
        'freestyle music' : 'r & b.freestyle music',
        'go-go' : 'r & b.freestyle music.go-go',
        'hip hop soul' : 'r & b.hip hop soul',
        'p-funk' : 'r & b.hip hop soul.p-funk',
        'post-disco' : 'r & b.hip hop soul.post-disco',
        'boogie' : 'r & b.hip hop soul.boogie',
        'new jack swing' : 'r & b.new jack swing',
        'rhythm and blues' : 'r & b.rhythm and blues',
        'soul' : 'r & b.soul',
        'blue-eyed soul' : 'r & b.soul.blue-eyed soul',
        'hip hop soul' : 'r & b.soul.hip hop soul',
        'northern soul' : 'r & b.soul.northern soul',
        'neo soul' : 'r & b.soul.neo soul',
        'southern ' : 'r & b.soul.southern',
        #rock
        'rock' : 'rock',
        'alternative rock' : 'rock.alternative rock',
        'grunge' : 'rock.alternative rock.grunge',
        'post-grunge' : 'rock.alternative rock.grunge.post-grunge',
        'indie rock' : 'rock.alternative rock.indie rock',
        'dunedin sound' : 'rock.alternative rock.indie rock.dunedin sound',
        'post-punk revival' : 'rock.indie rock.post-punk revival',
        'industrial rock' : 'rock.alternative rock.industrial rock',
        'post-rock' : 'rock.alternative rock.post-rock',
        'post-metal' : 'rock.alternative rock.post-rock.post-metal',
        'sadcore' : 'rock.alternative rock.sadcore',
        'shoegaze' : 'rock.alternative rock.shoegaze',
        'slowcore' : 'rock.alternative rock.slowcore',
        'art rock' : 'rock.art rock',
        'beat music' : 'rock.beat music',
        'chinese rock' : 'rock.chinese rock',
        'christian rock' : 'rock.christian rock',
        'electronicore' : 'rock.electronicore',
        'dark cabaret' : 'rock.dark cabaret',
        'experimental rock' : 'rock.experimental rock',
        'electronic rock' : 'rock.electronic rock',
        'folk rock' : 'rock.folk rock',
        'garage rock' : 'rock.garage rock',
        'glam rock' : 'rock.glam rock',
        'hard rock' : 'rock.hard rock',
        'heavy metal' : 'rock.heavy metal',
        'alternative metal' : 'rock.heavy metal.alternative metal',
        'avant-garde metal' : 'rock.heavy metal.avant-garde metal',
        'black metal' : 'rock.heavy metal.black metal',
        'symphonic black metal' : 'rock.heavy metal.black metal.symphonic black metal',
        'viking metal' : 'rock.heavy metal.black metal.viking metal',
        'war metal' : 'rock.heavy metal.black metal.war metal',
        'christian metal' : 'rock.heavy metal.christian metal',
        'unblack metal' : 'rock.heavy metal.christian metal.unblack metal',
        'death metal' : 'rock.heavy metal.death metal',
        'death \'n\' roll' : 'rock.heavy metal.death metal.death \'n\' roll',
        'melodic death metal' : 'rock.heavy metal.death metal.melodic death metal',
        'technical death metal' : 'rock.heavy metal.death metal.technical death metal',
        'goregrind' : 'rock.heavy metal.death metal.goregrind',
        'doom metal' : 'rock.heavy metal.doom metal',
        'death-doom' : 'rock.heavy metal.doom metal.death-doom',
        'drone metal' : 'rock.heavy metal.drone metal',
        'folk metal' : 'rock.heavy metal.folk metal',
        'celtic metal' : 'rock.heavy metal.folk metal.celtic metal',
        'medieval metal' : 'rock.heavy metal.folk metal.medieval metal',
        'pagan metal' : 'rock.heavy metal.folk metal.pagan metal',
        'funk metal' : 'rock.heavy metal.funk metal',
        'glam metal' : 'rock.heavy metal.glam metal',
        'gothic metal' : 'rock.heavy metal.gothic metal',
        'grindcore' : 'rock.heavy metal.grindcore',
        'industrial metal' : 'rock.heavy metal.industrial metal',
        'latin metal' : 'rock.heavy metal.latin metal',
        'metalcore' : 'rock.heavy metal.metalcore',
        'melodic metalcore' : 'rock.heavy metal.metalcore.melodic metalcore',
        'deathcore' : 'rock.heavy metal.metalcore.deathcore',
        'mathcore' : 'rock.heavy metal.metalcore.mathcore',
        'neoclassical metal' : 'rock.heavy metal.neoclassical metal',
        'nu metal' : 'rock.heavy metal.nu metal',
        'post-metal' : 'rock.heavy metal.post-metal',
        'power metal' : 'rock.heavy metal.power metal',
        'progressive metal' : 'rock.heavy metal.progressive metal',
        'djent' : 'rock.heavy metal.progressive metal.djent',
        'rap metal' : 'rock.heavy metal.rap metal',
        'sludge metal' : 'rock.heavy metal.sludge metal',
        'speed metal' : 'rock.heavy metal.speed metal',
        'symphonic metal' : 'rock.heavy metal.symphonic metal',
        'thrash metal' : 'rock.heavy metal.thrash metal',
        'crossover thrash' : 'rock.heavy metal.thrash metal.crossover thrash',
        'groove metal' : 'rock.heavy metal.thrash metal.groove metal',
        'jazz rock' : 'rock.jazz rock',
        'math rock' : 'rock.math rock',
        'neue deutsche härte' : 'rock.neue deutsche härte',
        'new wave' : 'rock.new wave',
        'world fusion' : 'rock.new wave.world fusion',
        'paisley underground' : 'rock.paisley underground',
        'desert rock' : 'rock.desert rock',
        'pop rock' : 'rock.pop rock',
        'soft rock' : 'rock.pop rock.soft rock',
        'progressive rock' : 'rock.progressive rock',
        'canterbury scene' : 'rock.progressive rock.canterbury scene',
        'krautrock' : 'rock.progressive rock.krautrock',
        'new prog' : 'rock.progressive rock.new prog',
        'rock in opposition' : 'rock.progressive rock.rock in opposition',
        'space rock' : 'rock.progressive rock.space rock',
        'psychedelic rock' : 'rock.psychedelic rock',
        'acid rock' : 'rock.psychedelic rock.acid rock',
        'freakbeat' : 'rock.psychedelic rock.freakbeat',
        'neo-psychedelia' : 'rock.psychedelic rock.neo-psychedelia',
        'raga rock' : 'rock.psychedelic rock.raga rock',
        'punk rock' : 'rock.punk rock',
        'anarcho punk' : 'rock.punk rock.anarcho punk',
        'crust punk' : 'rock.punk rock.anarcho punk.crust punk',
        'd-beat' : 'rock.punk rock.anarcho punk.crust punk.d-beat',
        'art punk' : 'rock.punk rock.art punk',
        'christian punk' : 'rock.punk rock.christian punk',
        'deathrock' : 'rock.punk rock.deathrock',
        'digital hardcore' : 'rock.punk rock.digital hardcore',
        'folk punk' : 'rock.punk rock.folk punk',
        'celtic punk' : 'rock.punk rock.folk punk.celtic punk',
        'cowpunk' : 'rock.punk rock.folk punk.cowpunk',
        'gypsy punk' : 'rock.punk rock.folk punk.gypsy punk',
        'garage punk' : 'rock.punk rock.garage punk',
        'grindcore' : 'rock.punk rock.grindcore',
        'crustgrind' : 'rock.punk rock.grindcore.crustgrind',
        'noisegrind' : 'rock.punk rock.grindcore.noisegrind',
        'hardcore punk' : 'rock.punk rock.hardcore punk',
        'post-hardcore' : 'rock.punk rock.hardcore punk.post-hardcore',
        'emo' : 'rock.punk rock.hardcore punk.post-hardcore.emo',
        'screamo' : 'rock.punk rock.hardcore punk.post-hardcore.emo.screamo',
        'thrashcore' : 'rock.punk rock.hardcore punk.thrashcore',
        'crossover thrash' : 'rock.punk rock.hardcore punk.crossover thrash',
        'powerviolence' : 'rock.punk rock.hardcore punk.powerviolence',
        'street punk' : 'rock.punk rock.hardcore punk.street punk',
        'horror punk' : 'rock.punk rock.horror punk',
        'pop punk' : 'rock.punk rock.pop punk',
        'psychobilly' : 'rock.punk rock.psychobilly',
        'riot grrrl' : 'rock.punk rock.riot grrrl',
        'ska punk' : 'rock.punk rock.ska punk',
        'skate punk' : 'rock.punk rock.skate punk',
        'post-punk' : 'rock.post-punk',
        'gothic rock' : 'rock.post-punk.gothic rock',
        'no wave' : 'rock.post-punk.no wave',
        'noise rock' : 'rock.post-punk.noise rock',
        'rap rock' : 'rock.rap rock',
        'rapcore' : 'rock.rap rock.rapcore',
        'rock and roll' : 'rock.rock and roll',
        'southern rock' : 'rock.southern rock',
        'stoner rock' : 'rock.stoner rock',
        'sufi rock' : 'rock.sufi rock',
        'surf rock' : 'rock.surf rock',
        'visual kei' : 'rock.visual kei',
        'nagoya kei' : 'rock.visual kei.nagoya kei',
        'worldbeat' : 'rock.worldbeat',
        #folk
        'folk' : 'folk',
        'american folk revival' : 'folk.american folk revival',
        'anti-folk' : 'folk.anti-folk',
        'british folk revival' : 'folk.british folk revival',
        'celtic music' : 'folk.celtic music',
        'chalga' : 'folk.chalga',
        'contemporary folk' : 'folk.contemporary folk',
        'filk music' : 'folk.filk music',
        'folktronica' : 'folk.folktronica',
        'freak folk' : 'folk.freak folk',
        'indie folk' : 'folk.indie folk',
        'industrial folk' : 'folk.industrial folk',
        'neofolk' : 'folk.neofolk',
        'progressive folk' : 'folk.progressive folk',
        'protest song' : 'folk.protest song',
        'psychedelic folk' : 'folk.psychedelic folk',
        'singer-songwriter movement' : 'folk.singer-songwriter movement',
        'skiffle' : 'folk.skiffle',
        'sung poetry' : 'folk.sung poetry',
        'cowboy/western music' : 'folk.cowboy/western music',
        #country
        'country' : 'country',
        'alternative country' : 'country.alternative country',
        'cowpunk' : 'country.cowpunk',
        'blues country' : 'country.blues country',
        'hokum' : 'country.hokum',
        'outlaw country' : 'country.outlaw country',
        'progressive country' : 'country.progressive country',
        'zydeco' : 'country.zydeco',
        'country rap' : 'country.country rap',
        'red dirt' : 'country.red dirt',
        'rockabilly' : 'country.rockabilly',
        'hellbilly music' : 'country.hellbilly music',
        'psychobilly/punkabilly' : 'country.psychobilly/punkabilly',
        'country rock' : 'country.country rock',
        'texas country' : 'country.texas country',
        'americana' : 'country.americana',
        'australian country music' : 'country.australian country music',
        'bakersfield sound' : 'country.bakersfield sound',
        'bluegrass' : 'country.bluegrass',
        'progressive bluegrass' : 'country.progressive bluegrass',
        'reactionary bluegrass' : 'country.reactionary bluegrass',
        'cajun' : 'country.cajun',
        'cajun fiddle tunes' : 'country.cajun fiddle tunes',
        'christian country music' : 'country.christian country music',
        'classic country' : 'country.classic country',
        'close harmony' : 'country.close harmony',
        'dansband music' : 'country.dansband music',
        'franco-country' : 'country.franco-country',
        'honky tonk' : 'country.honky tonk',
        'instrumental country' : 'country.instrumental country',
        'nashville sound' : 'country.nashville sound',
        'neotraditional country' : 'country.neotraditional country',
        'country pop' : 'country.country pop',
        'sertanejo' : 'country.sertanejo',
        'traditional country music' : 'country.traditional country music',
        'truck-driving country' : 'country.truck-driving',
        'wester' : 'country.wester',
        #caribbean
        'caribbean' : 'caribbean',
        #chill out
        'chill out' : 'chill out',
        'lounge' : 'chill out.lounge'
    }
    return genres

def getGenreTree(selectedGenre, genres):
    return genres.get(selectedGenre.lower(), 'unknown')

if SCAN_MODE == 1:
    scanGenres(scanPath)
else:
    organizeMusicCollection(sourcePath, destinationPath);
