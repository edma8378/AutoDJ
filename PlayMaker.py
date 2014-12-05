#!/usr/bin/python
import sys                
import sqlite3
import os
import fnmatch
import eyed3
import json

PLAYLIST_DIR = "playlists/"
DIGITAL_TABLE = "digital"
AD_TABLE = "advertisments"

def outputPlaylists(day,listOfPlaylists):
    #writes each playlist to a seperate file in the playlists folder
    #with the day and hour it will be representing. 
    timeOfDay = "am"
    curHour = 0
    #make folder for the day
    if not os.path.isdir(PLAYLIST_DIR+day):
        os.mkdir(PLAYLIST_DIR+day)  
    keys = ["path","song","artist","album","length"]  
    for hour in listOfPlaylists:        
        #touch the new file, should be in playlist folder
        with open(PLAYLIST_DIR+day+"/"+str(curHour)+timeOfDay+".playlist",'w') as outfile:
            pl = []    
            for song in hour:
                dict1 = dict(zip(keys,song))
                pl.append(dict1)
            json.dump(pl, outfile)
            curHour += 1
            if curHour == 12:
                timeOfDay = "pm" 
            outfile.close()           

    return;

def generatePlaylist():
    #formating of playist is TBD.
    #Returns a single hour long playlist according to the radio 1190
    #standards for when ads and other things need.
    #This is where the algoritm will live that checks is the song is allowed
    #into the playlist.    
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

def main():
    print "hello"

if __name__ =="__main__":
    main()
