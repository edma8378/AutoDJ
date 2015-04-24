#Overview of Backend


A daemon on radio 1190's server kicks in every night at 10 pm, generating the next day's playlist from the database.
The script calls PlayMaker.py to do this.
There is a watchdog on the app/music folder checking for updates in music. Folders on the radio station's server are mounted here. 
When music is added to the radio station's folders, it is seen by the watchdog to be in app/music and added to the database. The new music
can now be used in playlist generation. Other folders can be mounted to the watchdog app/music folder. See the Final backend Admin Guide for details.

#Overview of Algorithms

The playlist generation will be used to generate a day’s worth of content from the database,
 meeting requirements for an individual hour. 
 The algorithm selects a legalID for the top of the hour, and the rest of the hour is composed of randomly selected songs spaced apart by sweepers and ads. There are 3-5 songs picked from the database based on picked artist that have not been picked recently, after this set of songs the there is a sweeper and the second sweeper of the hour is replaced by an advertisment if it exists in the database. 
 The ads and sweepers are selected randomly, the songs however are more complicated.
We select a randoms song from the a subset of the database that hasn’t been played recently to keep the content fresh.
 The subset of the database searched is determined by our proximity protection file, that contains a list of songs played before.
 The proximity is based off a list that contains the database's artists, currently set to 70% of the the total number of unique artists in the database. 
 The search for new music excludes artists in this file, so replaying an artist in music generation is not possible.
The oldest songs are eventually pushed out, and able to be chosen again.
When generation for the days playlists is complete, the most recent choices are appended to the proximity protection file. 

The playlists are generated to be atleast 62 minutes with an allowed error range of up to 1 minute longer because you can't always be accurate to the second when adding random length songs to a playlist. This is so the frontend has some wiggle room when it comes keeping the playlists rotating at the top of the hour, which is important because the legal ID needs to be within 5 minutes of the top of the hour. The longer playlists mean that a frontend can easily remove a song to keep this target. 

#WatchDog info
The Watchdog is there to monitor the AutoDJ/app/music folder and wait for any music files (.mp3) to be created, deleted, or modified. When any of these things occur the sqlite database needs to be updated to reflex the current state of the folder. The piece that is really import is that the database must contain only entries with valid pathes in the folder, so when the frontend goes to grab a song to play it, that path is always valid. The Watchdog runs as two seperate threads one is monitoring the app/music folder and then notifying the the other thread to run the appropriate command to update the database. The second thread runs the DatabaseTools.py file with the correct flags. It is very easy when running the DatabaseTools manually to corrupt or destroy the music.db, which is why this watchdog was created to be able to maintain the database for you.


#More Daemon info
There is a server side daemon that runs every night at 10 pm, and it does two things. 
The first is that it runs the Playmaker.py script that generates the playlists and outputs them in AutoDJ/app/playlists/[date]/. 
The second thing is that it make sure that the Watchdog.py script is running and if it is not it starts it up such that it can run in the background without a user logged into the system. 
An example of what is being run is in the backend folder named noize-machine-cron. 
