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
PLAYLIST_DIR = "app/playlists" #path for playlist objects
DIGITAL_TABLE = "digital" #name of digital table name in database
AD_TABLE = "advertisments" #name of advertisements table name in database
##CHECK - should keys be a global variable or declared inline (line 30)?
#keys = ["path","artist","album","song","length"]  
LENGTH_INDEX = 4 #length of song object (keys describes these items)
#--


#--Definitions

#writes each playlist to a seperate file in the playlists folder
#with the day and hour it will be representing. 
def outputPlaylists(day,listOfPlaylists):

    #Variables
    curHour = 0 #default to 12am (military time)
    keys = ["path","artist","album","song","length"] #names of columns in the database

    #make folder for the day if it doesn't already exist
    if not os.path.isdir(PLAYLIST_DIR+"/"+day):
        os.mkdir(PLAYLIST_DIR+"/"+day)   

    #go through each hour of a day's worth of playlists
    for hour in listOfPlaylists:
        #touch the new file, should be in playlist folder
        with open(PLAYLIST_DIR+"/"+day+"/"+str(curHour)+".playlist",'w') as outfile:
            pl = [] 

            #for every song in the hour   
            for song in hour:
                dict1 = dict(zip(keys,song))
                pl.append(dict1)
            json.dump(pl, outfile)
            curHour += 1 
            outfile.close()           

    return;

def nextWeekPlaylists():
    day = datetime.date.today()
    while day.weekday() != 6:
        day += datetime.timedelta(1)
    for i in range(7):
        dayOfPls = []
        for j in range(24):
            pl = generatePlaylist()
            dayOfPls.append(pl)
        outputPlaylists(day.strftime('%Y-%m-%d'),dayOfPls)
        day += datetime.timedelta(1)
        #print day
    return;

def generatePlaylist():
    #formating of playist is TBD.
    #Returns a single hour long playlist according to the radio 1190
    #standards for when ads and other things need.
    #This is where the algoritm will live that checks is the song is allowed
    #into the playlist.
    timeTotal = 3600
    marginError = 100
    maxSongMisses = 20
    addedTime = 0
    songsPerAd = random.randint(2,4)
    songsAdded = 0
    playlist = []
    prevSong = ""
    prevAd = []    
    misses  = 0

    song = randomAD()#PLACEHODLER for top of the hour legal ID
    length = int(song[LENGTH_INDEX])
    addedTime+=length
    playlist.append(list(song))
    while addedTime < (timeTotal - marginError) :
        song = []    
        length = 0    
        if songsAdded < songsPerAd : 
            song = randomSong()
            #print song
            length = int(song[LENGTH_INDEX])
            if song[1] == prevSong or (length + addedTime) > timeTotal:
                misses+=1                
                if misses < maxSongMisses:                
                    continue
                else:
                    break
            misses = 0
            songsAdded+=1
            prevSong = song[1]
        else:
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


    #print addedTime
    #print playlist
    return playlist

def randomAD():
    #returns a random entry from the ads table
    conn = sqlite3.connect(os.getcwd()+"/db/music.db")
    c = conn.cursor() 
    c.execute('SELECT * FROM '+AD_TABLE+' ORDER BY RANDOM() LIMIT 1')
    ad = c.fetchone()
    if( not ad):
        print "Table not present. Please run create "+table
        return None;
    return ad    

def randomSong():
    #should be a random song from the digital music table of the db
    #Connect to database, grab the random line and return it
    conn = sqlite3.connect(os.getcwd()+"/db/music.db")
    c = conn.cursor() 
    c.execute('SELECT * FROM '+DIGITAL_TABLE+' ORDER BY RANDOM() LIMIT 1')
    song = c.fetchone()
    if( not song):
        print "Table not present. Please run create "+table
        return None;

    return song

#--

#--Main
def main():
    nextWeekPlaylists() #Make 7 days worth of playlists, Sunday - Saturday

if __name__ =="__main__":
    main()
