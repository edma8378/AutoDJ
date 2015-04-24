#Overview of Backend


A daemon on radio 1190's server kicks in every night at 10 pm, generating the next day's playlist from the database.
The script calls PlayMaker.py to do this.
There is a watchdog on the app/music folder checking for updates in music. A folder on the radio station's server is mounted here. 
When music is added to the radio station's folder, it is seen by the watchdog to be in app/music and added to the database. The new music
can now be used in playlist generation. Other folders can be mounted to the watchdog app/music folder. See the Final backend Admin Guide for details.

#Overview of Algorithms

The playlist generation will be used to generate a day’s worth of content from the database,
 meeting requirements for an individual hour. The algorithm selects an advertisement from the advertisement table,
 3-5 sweepers from the table of sweepers, and songs from the music table to fill the time in the hour. 
 The ads and sweepers are selected randomly, the songs however are more complicated.
We select a randoms song from the a subset of the database that hasn’t been played recently to keep the content fresh.
 The subset of the database searched is determined by our proximity protection file, that contains a list of songs played before.
 The list contains a percentage of the total database, currently 60% of the size of the database. 
 The search for new music excludes artists in this file, so replaying an artist in music generation is unlikely.
When generation for the days playlists is complete, the choices are appended to the proximity protection file.
The size of the file is fixed, so the oldest songs are eventually pushed out, and able to be chosen again.

The playlists are generated to be over 60 minutes. This doesn’t seem like an issue, but the FCC 
//Talk about the overfill of songs to fit timing of the hour, Alex 


#Details of Algorithm?



#More WatchDog info



#More Daemon info
