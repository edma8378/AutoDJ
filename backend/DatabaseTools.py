#!/usr/bin/python
#                     .     _///_,
#                     .      / ` ' '>
#                       )   o'  __/_'>
#                      (   /  _/  )_\'>
#                       ' "__/   /_/\_>
#                           ____/_/_/_/
#                          /,---, _/ /
#                         ""  /_/_/_/
#                            /_(_(_(_                 \
#                           (   \_\_\\_               )\
#                            \'__\_\_\_\__            ).\
#                            //____|___\__)           )_/
#                            |  _  \'___'_(           /'
#                             \_ (-'\'___'_\      __,'_'
#                             __) \  \\___(_   __/.__,'
#                          ,((,-,__\  '", __\_/. __,'
#                                       '"./_._._-'



import sys                
import sqlite3
import os
import fnmatch
import eyed3
import re

DB_PATH = "/../db/music.db"

DIGITAL_TABLE = "digital"
ADS_TABLE = "advertisments"
approved_tables = ["all",DIGITAL_TABLE,ADS_TABLE]
approved_types =["rotation","ambient","blues","ad_rotation","ad_ambient","ad_blues","legalID_rotation","legalID_ambient","legalID_blues","sweeper_rotation","sweeper_ambient","sweeper_blues"]

def printUsages():
    print "Valid arguments: create ["+"|".join(approved_tables)+"]" 
    print "                 destroy ["+"|".join(approved_tables)+"]"
    print "                 update ["+DIGITAL_TABLE+"|"+ADS_TABLE+"] ["+"|".join(approved_types)+"] " 
    print "                 status ["+DIGITAL_TABLE+"|"+ADS_TABLE+"]"
    print "                 clean"

def statusDatabase(table):
    conn = sqlite3.connect(os.getcwd()+DB_PATH)
    c = conn.cursor() 
    data = ['table',table]
    c.execute('SELECT name FROM sqlite_master WHERE type=? AND name=?',data)
    result = c.fetchone()
    if( not result):
        print "Table not present. Please run create "+table
        exit()
    
    print "Path \t Artist \t\t Album \t Title \t Genre \t Length"
    for row in c.execute('SELECT * FROM '+table):
        print ""
        for column in row[0:len(row)]:
           print (str(column.encode('utf-8')) if row[1] else "unknown")+"\t\t",
    print ""
    conn.close()


def updateTable(table,path,type):
    #grab all mp3 in the specified folder
    #path = raw_input("Please enter the absolute path to the top level music folder to add to the db:")
    matches = []
    charBanlist = ["#"] # hashtags are evil
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            filenameNew = filename
            for char in charBanlist:
                if char in filename:
                    print "BAM "+ filename                
                    filenameNew = filename.replace(char, "")
                    os.rename(os.path.join(root, filename),os.path.join(root, filenameNew))
            matches.append(os.path.join(root, filenameNew))
            

    conn = sqlite3.connect(os.getcwd()+DB_PATH)
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
    for path in matches:
        try:
            audiofile = eyed3.load(path)            
        except:
            print "Failed to load song: "+path
            continue;
        if not audiofile.tag or not audiofile.info:
            print "Invalid tag or info"
            continue;        
        artist = audiofile.tag.artist if audiofile.tag.artist else "UNKNOWN"
        album = audiofile.tag.album if audiofile.tag.album else "UNKNOWN"
        title = audiofile.tag.title if audiofile.tag.title else "UNKNOWN"
        genre = audiofile.tag.genre.name if audiofile.tag.genre else "UNKNOWN"
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
            add = [path[path.find("music"):].decode('utf8'),artist,album,title,genre,length,type]
            #print add
            insertions.append(add)
        
    c.executemany('INSERT INTO '+table+' VALUES (?,?,?,?,?,?,?)', insertions)
    conn.commit()
    conn.close()
    #print query   

def cleanTable(table):
    conn = sqlite3.connect(os.getcwd()+"/../db/music.db")
    c = conn.cursor() 
    deletions = []
    for song in c.execute('SELECT * FROM '+table):
        absolutePath = os.getcwd()+"/../app/" + song[0]
        if not os.path.exists(absolutePath):
            print "File missing:"+song[0]
            deletions.append(song)
    for entry in deletions:
        c.execute('DELETE FROM '+table+ ' WHERE path=?',(entry[0],))
	conn.commit()
    conn.close() 
    return;

def destroyTable(table):
    print "WHY WOULD YOU WANT TO DO THIS!?"
    answer = raw_input("Are you sure?(y/n):")
    if answer != "y":
        exit()    
    conn=sqlite3.connect(os.getcwd()+DB_PATH)
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
    print "db is located in " + os.getcwd()+DB_PATH
    conn=sqlite3.connect(os.getcwd()+DB_PATH)
    c = conn.cursor()
    if table != "all":
        data = ['table',table]
        c.execute('SELECT name FROM sqlite_master WHERE type=? AND name=?',data)
        result = c.fetchone()
        if(result):
            print "Table "+table+" already in database"
            exit()
        else:
            c.execute('CREATE TABLE '+table+' (path text, artist text, album text, title text, genre text, length text, typeName text)')
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
                c.execute('CREATE TABLE '+table+' (path text, artist text, album text, title text, genre text, length text, type text)')
                print "New table created in db: "+table

    conn.commit()
    conn.close()
 
def main():
    #This program assumes it is running in the AutoDJ folder that already has the 
    #proper folder stucture. If not then clone the git repository and run it from there.
    if len(sys.argv) < 3:
        printUsages()
        exit(1)

    command = sys.argv[1];
    table = sys.argv[2];
    #check if there is a music.db file in the proper location
    if (not os.path.exists(os.getcwd()+DB_PATH)):
            print "Creating new sqlite database..."
            open(os.getcwd()+DB_PATH, 'a').close()
        
    if command == "create":
        ## read arg 2 for which tables to create
        if table in approved_tables:
            createTable(table)
        else:
            printUsages()
            exit(1)
            
        exit()                 
        
    elif command == "destroy":
        temp = raw_input("Tables will be destroyed, continue?(y/n)")
        if temp=="y":
                   
            if table in approved_tables:
                destroyTable(table)
            else:
                printUsages()
                exit(1)
            
        elif temp=="n":
            print "Database perserved, exiting."
        else:
            print "Bad Input, exiting"
        exit()

    elif command == "update":
        if(len(sys.argv) != 5):
            print "missing location to update from"
            exit()
        location = sys.argv[4]
        type = sys.argv[3]
        if not type in approved_types:
            if not re.match("show_?\d+",type): 
                print type+" is not a valid type"
                printUsages()
                exit(1)
        if(not os.path.isdir(location)):
            print "[location] must be a folder"
            exit(1)
        if(table == DIGITAL_TABLE):
            print "Searching "+location+" for new "+type+" music..."
            updateTable(table,location,type)
        elif( table == ADS_TABLE ):
            print "Searching "+location+" for new ads"
            updateTable(table,location,type)
        exit()

    elif command == "status":
        print "---Current database---"
        statusDatabase(table)
        exit()

    elif command == "clean":
        print "Cleaning database"
        cleanTable(table)
        exit()


if __name__ =="__main__":
    main()
