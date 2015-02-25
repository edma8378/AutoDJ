#!/usr/bin/python
import sys                
import sqlite3
import os
import fnmatch #Unix file name matching
import eyed3 #Works w/ Audio Files
import json 
import datetime
import random

#--Global Variables
PLAYLIST_DIR = "../app/playlists" #path for playlist objects
PROXIMITY_DIR = "../proximity"
DIGITAL_TABLE = "digital" #name of digital table name in database
AD_TABLE = "advertisments" #name of advertisements table name in database
keys = ["path","artist","album","song","genre","length","typeName"]  
LENGTH_INDEX = 5 #index into a song that give the time length of the song
ARTIST_INDEX = 1
TYPE_INDEX = 6
mostRecentArtists = [] # list of the most recent artist put into the playlist
percentage = 0.6
playlistType = [[1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0], #monday
                [0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0], #tuesday
                [0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0], #wednesday
                [0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0], #thursday
                [0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1], #friday
                [1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1], #saturday
                [1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1]] #sunday
                #KEY: 0 = ambient overnight, 1 = blues overnight, 2 = rotation
playlistTypeKeys = ["ambient","blues","rotation"]
proximityTypes = []
#--


#--Definitions

#writes each playlist to a seperate file in the playlists folder
#with the day and hour it will be representing. 
def outputPlaylists(day,listOfPlaylists):
    #Variables
    curHour = 0 #default to 12am (military time)

    #make folder for the day if it doesn't already exist
    if not os.path.isdir(PLAYLIST_DIR+"/"+day):
        if not os.path.isdir(PLAYLIST_DIR):
            os.mkdir(PLAYLIST_DIR) 
        os.mkdir(PLAYLIST_DIR+"/"+day)   

    #go through each hour of a day's worth of playlists
    for hour in listOfPlaylists:
        #touch the new file, should be in playlist folder
        with open(PLAYLIST_DIR+"/"+day+"/"+str(curHour)+".playlist",'w') as outfile:
            pl = [] 
            #for every song in the hour add the key,value to the dictionary which will become the 
            # output jason file
            for song in hour:
                dict1 = dict(zip(keys,song))
                pl.append(dict1)
            json.dump(pl, outfile)
            curHour += 1 
            outfile.close()           
    return;

#generates a set of 24 playlists per day for the next 7 days
def nextWeekPlaylists(day):
    #day = datetime.date.today()
    #day += datetime.timedelta(1)    
    #while day.weekday() != 6:
    #    day += datetime.timedelta(1)
    print "for 7 days from "+str(day)+"\n"
    for i in range(7):
        dayOfPls = []
        for hour in range(24):
            pl = generatePlaylist(hour,day)
            dayOfPls.append(pl)
        outputPlaylists(day.strftime('%Y-%m-%d'),dayOfPls)
        outputProximity(day)
        day += datetime.timedelta(1)
        #print day
    return;

#generates a set of 24 playlists for the given day
def Playlist(day):
    dayOfPls = []
    for hour in range(24):
        pl = generatePlaylist(hour,day)
        dayOfPls.append(pl)
    outputPlaylists(day.strftime('%Y-%m-%d'),dayOfPls)
    outputProximity(day)
    return;


#formating of playist is a jason file.
#Returns a single hour long playlist according to the radio 1190
#standards for when ads and other things need to be there.
#This is where the algoritm will live that checks is the song is allowed
#into the playlist.
def generatePlaylist(hour,day):
    #Variables    
    type = playlistTypeKeys[int(playlistType[int(day.weekday())][hour])]
    timeTotal = 3600 #target length of the playlist in seconds
    marginError = 100 
    maxSongMisses = 20
    addedTime = 0
    songsPerAd = random.randint(2,4)
    songsAdded = 0
    playlist = []
    prevSong = ""
    prevAd = []    
    misses  = 0


    #global proximity
    proximity = proximityTypes[int(playlistType[int(day.weekday())][hour])]
    while(len(mostRecentArtists) > proximity):
            mostRecentArtists.pop()    

    song = randomAD()#PLACEHODLER for top of the hour legal ID
    length = int(song[LENGTH_INDEX])
    addedTime+=length
    playlist.append(list(song))
    while addedTime < (timeTotal - marginError) :
        song = []    
        length = 0    
        if songsAdded < songsPerAd : #a song needs to be added to the playlist
            song = randomSong(type)
            #check if its artist has been played recently
            #print song
            artist = song[ARTIST_INDEX]
            valid = checkArtist(artist)
            length = int(song[LENGTH_INDEX])
            if not valid:
                continue
            else:
                if len(mostRecentArtists) > proximity:
                    mostRecentArtists.pop()
                mostRecentArtists.insert(0,artist)
            if (length + addedTime) > timeTotal:
                misses+=1                
                if misses < maxSongMisses:                
                    continue
                else:
                    break
           
                
            misses = 0
            songsAdded+=1
            prevSong = song[1]
        else:   #it is time to place an ad in the playlist
            song = randomAD()
            length = int(song[LENGTH_INDEX])
            if (length + addedTime) > timeTotal:
                break #selected Ad too long
            if song == prevAd:
                misses+=1                
                if misses < maxSongMisses:                
                    continue
                else:
                    break
            misses = 0
            songsAdded = 0
            prevAd = song
            songsPerAd = random.randint(2,4)
            
        addedTime += int(song[LENGTH_INDEX])
        playlist.append(list(song))
        #print song

    return playlist

def checkArtist(artist):
    if mostRecentArtists.count(artist) > 0:
        return False
    else:
        return True

def outputProximity(day):
    with open(PROXIMITY_DIR+"/"+str(day),'w') as outfile:
        outfile.write("\n".join(mostRecentArtists))
        outfile.close()
    return

def randomAD():
    #returns a random entry from the ads table
    conn = sqlite3.connect(os.getcwd()+"/../db/music.db")
    c = conn.cursor() 
    c.execute('SELECT * FROM '+AD_TABLE+' ORDER BY RANDOM() LIMIT 1')
    ad = c.fetchone()
    conn.close()
    if( not ad):
        print "Table not present. Please run \"./DatabaseTools.py create "+AD_TABLE+"\"\n"
        return None;
    return ad    

def randomSong(type):
    #should be a random song from the digital music table of the db
    #Connect to database, grab the random line and return it
    #type refers to wether it is a rotation song, ambient overnight
    #or blues overnight song
    conn = sqlite3.connect(os.getcwd()+"/../db/music.db")
    c = conn.cursor() 
    c.execute('SELECT * FROM '+DIGITAL_TABLE+' WHERE typeName=? ORDER BY RANDOM() LIMIT 1',(type,))
    song = c.fetchone()
     
    if( not song):
        #grabbing the type might have failed, try again without type
        c.execute('SELECT * FROM '+DIGITAL_TABLE+' ORDER BY RANDOM() LIMIT 1')
        song = c.fetchone()
        conn.close()
        if song:
            return song
        print "Table not present. Please run \"./DatabaseTools.py create "+DIGITAL_TABLE+"\"\n"
        return None;
    conn.close()
    return song

def printUsages():
    print "Valid Arguments: today, tomorrow, week"
    return;

def countArtists(type):
    conn = sqlite3.connect(os.getcwd()+"/../db/music.db")
    c = conn.cursor() 
    total = 0
    for row in c.execute('SELECT DISTINCT artist FROM '+DIGITAL_TABLE+' WHERE typeName=?',(type,)):
        total+=1
    #print "Number of artists:"+str(total)+"\n"
    conn.close()
    return total

#--

#--Main
def main():
    if len(sys.argv) != 2:
        printUsages()
        exit()
    command = sys.argv[1];
    i = 0
    for t in playlistTypeKeys:
        proximityTypes.append(int(countArtists(t) * percentage))
        i+=1

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    tomorrow = today + datetime.timedelta(1)
    filename = ""
    temp = 0
    if command == "today":
        filename = os.getcwd()+"/../proximity/"+str(yesterday)
        temp = countArtists(playlistTypeKeys[playlistType[int(yesterday.weekday())][0]])
        #print temp
    else:
        filename = os.getcwd()+"/../proximity/"+str(today)
        temp = countArtists(playlistTypeKeys[playlistType[int(today.weekday())][0]])

    if (os.path.exists(filename)):
        mostRecentArtists = [line.rstrip('\n') for line in open(filename)]
        while(len(mostRecentArtists) > temp):
            mostRecentArtists.pop()
        

    if command == "tomorrow":
        print "Creating playlist for tomorrow"
        Playlist(tomorrow)
    elif command == "today":
        print "Creating playlist for today"
        Playlist(today)
    elif command == "week":
        print "Creating next week's playlists"
        nextWeekPlaylists(tomorrow) #Make 7 days worth of playlists
    else:
        printUsages()
        exit

if __name__ =="__main__":
    main()
