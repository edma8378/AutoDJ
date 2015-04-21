#!/usr/bin/python
#
#                                          _.-.._         _._
#                                     _,/^^,y./  ^^^^"""^^\= \
#                                     \y###XX;/  /     \    ^\^\
#                                       `\Y^   /   .-==||==-.)^^
#                   ,.-=""""=-.__       /^ (  (   -/<0>++<0>(
#                 .^      .: . . :^===(^ \ (  (  /```^^^^^^^)
#                /      .: .,GGGGp,_ .(   \   /    /-(o'~'o))
#              .^      : . gGG"""YGG}. \   )   / /  _/-====-\
#             /       (. .gGP  __ ~~ . .\  \  (    (  _.---._)
#            /        (. (GGb,,)GGp. . . \_-^-.__(_ /______./
#           (          \ . `"!GGP^ . . . . ^=-._--_--^^^^^~)
#           (        /^^^\_. . . . . . . . . . . . . . . . )
#           )       /     /._. . . . . . . . . . . . . ._.=)
#           \      /      |  ^"=.. . . . . . . ._++""\"^    \
#            \    |       |       )^|^^~'---'~^^      \     )
#            )   /        )      /   \                 \    \
#            |`  |        \     /\    \                (    /
#            |   |         (   (  \ . .\               |   (
#            )   |         )   )   ^^^^^^              |   |
#           /. . \         |  '|                       )   (
#           ^^^^^^         )    \                      /. . \
#                          / . . \                     ^^^^^^
#                          ^^^^^^^
#Ascii Art: Allen Mullen

import sys
import time
import threading
import re
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

##NEEDS CONFIG FILE FOR THIS INFO

dig = "digital"
ads = "ads"
MUSIC_FOLDER = "../app/music/"
ROTATION = "rotation/"
AMBIENT = "overnight/ambient/"
BLUES = "overnight/blues/"
rot = "rotation"
amb = "ambient"
blu = "blues"
#shows variable
SHOWS = "shows/"
sho = "_show_"
days = ["1mon","2tue","3wed","4thur","5fri","6sat","7sun",]
#AD variables
AD_ROTATION = "ads/rotation/"
AD_AMBIENT = "ads/ambient/"
AD_BLUES = "ads/blues/"
ad_rot = "ad_rotation"
ad_amb = "ad_ambient"
ad_blu = "ad_blues"
#legalID variables
LID_ROTATION = "legalIDs/rotation/"
LID_AMBIENT = "legalIDs/ambient/"
LID_BLUES = "legalIDs/blues/"
lid_rot = "legalID_rotation"
lid_amb = "legalID_ambient"
lid_blu = "legalID_blues"
#sweeper variables
SWP_ROTATION = "sweepers/rotation/"
SWP_AMBIENT = "sweepers/ambient/"
SWP_BLUES = "sweepers/blues/"
swp_rot = "sweeper_rotation"
swp_amb = "sweeper_ambient"
swp_blu = "sweeper_blues"

counter = 0
addPaths = []
cleanDB = False
signal = False

def ResolverThread():
    global counter
    global cleanDB
    global addPaths
    while not signal:
        rc = 0
        while 1:
            time.sleep(1)
            if signal:
                break
            if counter > 30 and (addPaths or cleanDB):
                break
        #print "executing commands"
        #print addPaths 
        temp = addPaths
        for (table,path,type) in temp:
            rc = subprocess.call(["python","DatabaseTools.py", "update", table, type, path])
            arr = ["python","DatabaseTools", "update", table, type, path]
            #print arr
        
        for item in temp:
            addPaths.remove(item)

        if cleanDB:
            #system call to clean db
            rc = subprocess.check_call(["python","DatabaseTools.py", "clean", dig])
            rc = subprocess.check_call(["python","DatabaseTools.py", "clean", ads])            
            cleanDB = False
            #print "db cleaned"
        counter = 0        

    if addPaths:
        for (path,type) in addPaths:
            rc = subprocess.check_call(["python","DatabaseTools.py", "update", table, type, path])
            arr = ["./DatabaseTools", "update", table, type, path]
            #print arr

        if cleanDB:
            rc = subprocess.check_call(["python","DatabaseTools.py", "clean", dig])
            rc = subprocess.check_call(["python","DatabaseTools.py", "clean", ads])            
            cleanDB = False
            #print "db cleaned"
    return

class MyHandler(PatternMatchingEventHandler):
    patterns=["*.mp3"]
    global counter
    """
    event.event_type
        'modified' | 'created' | 'moved' | 'deleted'
    event.is_directory
        True | False
    event.src_path
        path/to/observed/file
    """
    
    def matchDayWeek(self,event):  
        path = str(event.src_path)
        global days
        for day in days:
            if re.match(MUSIC_FOLDER+SHOWS+day,path):
                time = path[(path.find(day)+len(day)+1):]
                time = time[0:(time.find("/"))]
                addValue = (dig, MUSIC_FOLDER+SHOWS+day , day+sho+time)
                return addValue
        return ("","","")

    def matchPath(self, event):
        path = str(event.src_path)
        addVaue = ("","","")
        if re.match(MUSIC_FOLDER+ROTATION,path):
            addValue = (dig,MUSIC_FOLDER+ROTATION,rot)
        elif re.match(MUSIC_FOLDER+AMBIENT,path):
            addValue = (dig,MUSIC_FOLDER+AMBIENT,amb)
        elif re.match(MUSIC_FOLDER+BLUES,path):
            addValue = (dig,MUSIC_FOLDER+BLUES,blu)
        #ADs
        elif re.match(MUSIC_FOLDER+AD_ROTATION,path): 
            addValue = (ads,MUSIC_FOLDER+AD_ROTATION,ad_rot) 
        elif re.match(MUSIC_FOLDER+AD_AMBIENT,path): 
            addValue = (ads,MUSIC_FOLDER+AD_AMBIENT,ad_amb)   
        elif re.match(MUSIC_FOLDER+AD_BLUES,path): 
            addValue = (ads,MUSIC_FOLDER+AD_BLUES,ad_blu)
        #Sweepers
        elif re.match(MUSIC_FOLDER+SWP_ROTATION,path): 
            addValue = (ads,MUSIC_FOLDER+SWP_ROTATION,swp_rot) 
        elif re.match(MUSIC_FOLDER+SWP_AMBIENT,path): 
            addValue = (ads,MUSIC_FOLDER+SWP_AMBIENT,swp_amb)   
        elif re.match(MUSIC_FOLDER+SWP_BLUES,path): 
            addValue = (ads,MUSIC_FOLDER+SWP_BLUES,swp_blu)
        #legalIDs
        elif re.match(MUSIC_FOLDER+LID_ROTATION,path): 
            addValue = (ads,MUSIC_FOLDER+LID_ROTATION,lid_rot) 
        elif re.match(MUSIC_FOLDER+LID_AMBIENT,path): 
            addValue = (ads,MUSIC_FOLDER+LID_AMBIENT,lid_amb)   
        elif re.match(MUSIC_FOLDER+LID_BLUES,path): 
            addValue = (ads,MUSIC_FOLDER+LID_BLUES,lid_blu)
        #shows
        elif re.match(MUSIC_FOLDER+SHOWS,path):
            addValue = self.matchDayWeek(event)
        return addValue

    def on_modified(self, event):
        addValue = self.matchPath(event)
        if not event.is_directory:
            global counter
            counter = 0
            if addValue not in addPaths:
                addPaths.append(addValue)
                

    def on_created(self, event):
        addValue = self.matchPath(event)
        if not event.is_directory:
            global counter
            counter = 0
            if addValue not in addPaths:
                addPaths.append(addValue)
                

    def on_moved(self, event):
        addValue = self.matchPath(event)
        if not event.is_directory:
            global counter
            global cleanDB
            counter = 0
            if addValue not in addPaths:
                addPaths.append(addValue)
                cleanDB = True
    
    def on_deleted(self,event):
        addValue = self.matchPath(event)
        if not event.is_directory:
            global counter
            global cleanDB
            counter = 0
            cleanDB = True

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else MUSIC_FOLDER,recursive=True)
    observer.start()

    t = threading.Thread(target=ResolverThread)
    # Sticks the thread in a list so that it remains accessible
    t.start()
    #clean DB on startup
    rc = subprocess.check_call(["python","DatabaseTools.py", "clean", dig])
    rc = subprocess.check_call(["python","DatabaseTools.py", "clean", ads])
    try:
        while True:
            time.sleep(1)
            global counter            
            counter+=1
            counter = counter%100
            #print counter
    except KeyboardInterrupt:
        global signal        
        observer.stop()
        signal = True
        #print "\n"
        t.join()
        observer.join()
        exit()
    
