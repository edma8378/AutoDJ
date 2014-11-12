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
approved_tables = ["all",DIGITAL_TABLE,ADS_TABLE]

def printUsages():
    print "Valid arguments: create [all|"+DIGITAL_TABLE+"|"+ADS_TABLE+"], destroy [all|"+DIGITAL_TABLE+"|"+ADS_TABLE+"], update ["+DIGITAL_TABLE+"|"+ADS_TABLE+"] [location], status ["+DIGITAL_TABLE+"|"+ADS_TABLE+"]"

def statusDatabase(table):
    conn = sqlite3.connect(os.getcwd()+"/db/music.db")
    c = conn.cursor() 
    data = ['table',table]
    c.execute('SELECT name FROM sqlite_master WHERE type=? AND name=?',data)
    result = c.fetchone()
    if( not result):
        print "Table not present. Please run create "+table
        exit()
    
    print "Artist \t\t Album \t Title \t Length"
    for row in c.execute('SELECT * FROM '+table):
        print ""
        for column in row[1:len(row)]:
           print (str(column.encode('utf-8')) if row[1] else "unknown")+"\t\t",
    conn.close()


def updateTable(table,path):
    #grab all mp3 in the specified folder
    #path = raw_input("Please enter the absolute path to the top level music folder to add to the db:")
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            matches.append(os.path.join(root, filename))
            #print filename
    
    conn = sqlite3.connect(os.getcwd()+"/db/music.db")
    c = conn.cursor() 
    data = ['table',DIGITAL_TABLE]
    c.execute('SELECT name FROM sqlite_master WHERE type=? AND name=?',data)
    result = c.fetchone()
    if( not result):
        print "Table not present. Please run create "+DIGITAL_TABLE
        exit()
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
        c.execute('SELECT * FROM '+table+' WHERE title=? AND artist=? AND album=?',info)
        result = c.fetchone()

        if result:
            #given file was in the db so we ignore it            
            #print result
            skipped+=1
        else:
            #this is a new song so we add it to a list of lists that will all be inserted at once
            add = [file.decode('utf8'),artist,album,title,length]
            #print add
            insertions.append(add)
        
    c.executemany('INSERT INTO '+table+' VALUES (?,?,?,?,?)', insertions)
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
    data = ['table',table]
    c.execute('SELECT name FROM sqlite_master WHERE type=? AND name=?',data)
    result = c.fetchone()
    if(not result and not table == "all"):
        print "Table not in database, ignoring"
        exit()

    if ( table == DIGITAL_TABLE or table == "all" ):
        c.execute('Drop TABLE '+DIGITAL_TABLE)
        print "destroyed tables: "+DIGITAL_TABLE

    if ( table == ADS_TABLE or table == "all" ):
        c.execute('Drop TABLE '+ADS_TABLE)
        print "destroyed tables: "+ADS_TABLE
    
    conn.commit()
    conn.close()
    
def createTable(table):
    #path of database should be in a folder named db 
    print "db is located in " + os.getcwd()+"/db/music.db"
    conn=sqlite3.connect(os.getcwd()+"/db/music.db")
    c = conn.cursor()
    if table != "all":
        data = ['table',table]
        c.execute('SELECT name FROM sqlite_master WHERE type=? AND name=?',data)
        result = c.fetchone()
        if(result):
            print "Table "+table+" already in database"
            exit()
        else:
            c.execute('CREATE TABLE '+table+' (path text, artist text, album text, title text, length text)')
            print "New table created in db: "+table
    else:
        tables = [ table for table in approved_tables if table != "all"]
        for table in tables:
            data = ['table',table]
            c.execute('SELECT name FROM sqlite_master WHERE type=? AND name=?',data)
            result = c.fetchone()
            if(result):
                print "Table "+table+" already in database"
                exit()
            else:
                c.execute('CREATE TABLE '+table+' (path text, artist text, album text, title text, length text)')
                print "New table created in db: "+table

    conn.commit()
    conn.close()
 
def main():
    #This program assumes it is running in the AutoDJ folder that already has the 
    #proper folder stucture. If not then clone the git repository and run it from there.
    if len(sys.argv) < 3:
        print len(sys.argv)
        printUsages()
        exit()
    command = sys.argv[1];
    table = sys.argv[2];
    #check if there is a music.db file in the proper location
    if (not os.path.exists(os.getcwd()+"/db/music.db")):
            print "Creating new sqlite database..."
            open(os.getcwd()+"/db/music.db", 'a').close()
        
    if command == "create":
        ## read arg 2 for which tables to create
        if table in approved_tables:
            createTable(table)
        else:
            printUsages()
            
        exit()                 
        
    elif command == "destroy":
        temp = raw_input("Tables will be destroyed, continue?(y/n)")
        if temp=="y":
                   
            if table in approved_tables:
                destroyTable(table)
            else:
                printUsages()
            
        elif temp=="n":
            print "Database perserved, exiting."
        else:
            print "Bad Input, exiting"
        exit()

    elif command == "update":
        if(len(sys.argv) != 4):
            print "missing location to update from"
            exit()
        location = sys.argv[3]
        if(not os.path.isdir(location)):
            print "[location] must be a folder"
            exit()
        if(table == DIGITAL_TABLE):
            print "Searching "+location+" for new music..."
            updateTable(table,location)
        elif( table == ADS_TABLE ):
            print "Searching "+location+" for new ads"
            updateTable(table,location)
        exit()

    elif command == "status":
        print "---Current database---"
        statusDatabase(table)
        exit()

    elif command == "clean":
        print "Cleaning database"
        print "<This will check that the path entry in the given table still points to a valid file>"
        exit()

    printUsages()
    exit()

if __name__ =="__main__":
    main()
