#!/usr/bin/python
import sys                
import sqlite3
import os
import fnmatch
import eyed3
import re

DB_PATH = "db/music.db"
DIGITAL_TABLE = "digital"
ADS_TABLE = "advertisments"

def printUsages():
    print "Valid arguments: create [all|"+DIGITAL_TABLE+"|"+ADS_TABLE+"], destroy [all|"+DIGITAL_TABLE+"|"+ADS_TABLE+"], update ["+DIGITAL_TABLE+"|"+ADS_TABLE+"] [location], status ["+DIGITAL_TABLE+"|"+ADS_TABLE+"]"

def statusDatabase():
    conn = sqlite3.connect(os.getcwd()+"/db/music.db")
    c = conn.cursor() 
    #TODO catch exception for no table
    print "Artist \t\t Album \t Song \t Length"
    for row in c.execute('SELECT * FROM '+DIGITAL_TABLE):
        artist = str(row[1].encode('utf-8')) if row[1] else "unknown"
        album = str(row[2].encode('utf-8')) if row[2] else "unknown"
        song = str(row[3].encode('utf-8'))if row[3] else "unknown"
        length = str(row[4].encode('utf-8'))
        print artist+"\t\t"+album+"\t"+song+"\t"+length
        #print row[0]
    conn.close()

def updateDigitalTable():
    #grab all mp3 in the specified folder
    path = raw_input("Please enter the absolute path to the top level music folder to add to the db:")
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            matches.append(os.path.join(root, filename))
            #print filename
    
    conn = sqlite3.connect(os.getcwd()+"/db/music.db")
    c = conn.cursor() 
    
    #check if any of them are already in the db   
    insertions = []
    skipped = 0;
    for file in matches:
        audiofile = eyed3.load(file)            
        artist = audiofile.tag.artist if audiofile.tag.artist else "UNKNOWN"
        album = audiofile.tag.album if audiofile.tag.album else "UNKOWN"
        title = audiofile.tag.title if audiofile.tag.title else "UNKOWN"
        length = audiofile.info.time_secs #if this is 0 we may consider not allowing it to the db
        info = [title,artist,album]
        #query = 'SELECT * FROM '+DIGITAL_TABLE+' WHERE title=\''+escaped_cd Detitle+'\' AND artist=\''+escaped_artist+'\' AND album=\''+escaped_album+'\'';
        #print query
        c.execute('SELECT * FROM '+DIGITAL_TABLE+' WHERE title=? AND artist=? AND album=?',info)
        result = c.fetchone()

        if result:
            #given file was in the db so we ignore it            
            #print result
            skipped+=1
        else:
            #this is a new song so we add it to a list of lists that will all be inserted at once
            add = [file.decode('utf8'),artist,album,title,length]
            print add
            insertions.append(add)
        
    c.executemany('INSERT INTO digital VALUES (?,?,?,?,?)', insertions)
    conn.commit()
    conn.close()
    #print query   

def destroyTable(table):
    print "WHY WOULD YOU WANT TO DO THIS!?"
    answer = raw_input("Are you sure?(y/n):")
    if answer != "y":
        exit()    
    conn=sqlite3.connect(os.getcwd()+"/db/music.db")
    c = conn.cursor()
    if ( table == DIGITAL_TABLE || table == "all" ):
        c.execute('Drop TABLE '+DIGITAL_TABLE)
        print "destroyed tables: "+DIGITAL_TABLE

    if ( table == DIGITAL_TABLE || table == "all" ):
        c.execute('Drop TABLE '+ADS_TABLE)
        print "destroyed tables: "+ADS_TABLE
    
    conn.commit()
    conn.close()
    
def createTable(table):
    #path of database should be in a folder named db 
    print "db is located in " + os.getcwd()+"/db/music.db"
    conn=sqlite3.connect(os.getcwd()+"/db/music.db")
    c = conn.cursor()

    if ( table == DIGITAL_TABLE || table == "all" ):
        c.execute('CREATE TABLE '+DIGITAL_TABLE+' (path text, artist text, album text, title text, length text)')
        print "New table created in db: "+DIGITAL_TABLE    

    if ( table == ADS_TABLE || table == "all" ):
        c.execute('CREATE TABLE '+ADS_TABLE+' (path text, title text, length text)')
        print "New table created in db: "+ADS_TABLE

    conn.commit()
    conn.close()
 
def main():
    #This program assumes it is running in the AutoDJ folder that already has the 
    #proper folder stucture. If not then clone the git repository and run it from there.
    if len(sys.argv) <= 3:
        printUsages()
        exit()
    command = sys.argv[1];
    table = sys.argv[2];
    if command == "create":
        #check if there is a music.db file in the proper location
        if (not os.path.exists(os.getcwd()+"/db/music.db")):
            print "Creating new sqlite database..."
        
        ## read arg 2 for which tables to create
        if table == "all":
            createTable("all")
        elif table == DIGITAL_TABLE:
            createTable(DIGITAL_TABLE)
        elif table == ADS_TABLE:
            createTable(ADS_TABLE)
        else:
            printUsages()
            
        exit()                 
        
    elif command == "destroy":
        temp = raw_input("Tables will be destroyed, continue?(y/n)")
        if temp=="y":
                   
            if table == "all":
                destroyTable("all")
            elif table == DIGITAL_TABLE:
                destroyTable(DIGITAL_TABLE)
            elif table == ADS_TABLE:
                destroyTable(ADS_TABLE)
            else:
                printUsages()
            
        elif temp=="n":
            print "Database perserved, exiting."
        else:
            print "Bad Input, exiting"
        exit()
    elif command == "update":
        
        print "Searching file system for new music..."
        updateDatabase()
        exit()
    elif command == "status":
        print "---Current database---"
        statusDatabase()
        exit()

    printUsages()
    exit()

if __name__ =="__main__":
    main()
