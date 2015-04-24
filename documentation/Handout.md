#The Problem:
Radio 1190 has been using DJ Pro to control their entire workflow for years. DJ set creation, new album insertion, designating top albums for the week, and DJ choice slots are all controlled there. However, DJ Pro isn’t linked to the music database, so there is no way to play a song from this software. The stations uses DJ Pro as a to-do list and planner for DJ’s set lists. It is up to them to go play the music they put in their list.

A major problem with this is the need for a physical person to be there all the time. DJs are expected to manually create long playlists to fill the air over nights, weekends, and school vacations. DJs can’t be late to a shift, take a break, or lose track of time while on duty. Overall, this system is very prone to human error.

The focus of our project was to provide a tool that fills in the radio space when DJ’s aren’t physically present at the station to mitigate these problems. 



#Previous Development:
Radio 1190 had help from a senior projects group last year, who were expected to have completed the backend for the AutoDJ system they wanted, and we were planning to expand on this code and add features to their system. 
The code we were given was incorrectly documented, non-functional, and poorly written. We made the decision to scrap their code and start the project from scratch. Because of these difficulties it was very important to us to deploy our work to the radio station, so this time they would know it worked. We also strived to provide proper documentation for the radio station and for next year’s team.
Generation Algorithms:
	The playlist generation will be used to generate a day’s worth of content from the database based on requirements for each individual hour. The algorithm selects an advertisement from the advertisement table, 3-5 sweepers from the table of sweepers, and songs from the music table to fill the time in the hour. The ads and sweepers are selected randomly; song selection, however, is a bit more complicated. 
We select a random song from the a subset of the database that is determined by our proximity protection file which contains a list of songs played recently. The search for new music excludes artists in this file, so replaying an artist is unlikely. Shows can also be set up to automatically generate playlists around special events, like holidays.


#Taking the Playlist and Making Music:
When starting, the web application grabs the time and date. The appropriate JSON object file containing the playlist and paths to each song is opened based on this time, and then finds which song should be playing and starts the playlist there. If the playlist is too long then the songs will be cut from the list until the playlist ends directly at the end of the hour.
After the playlist is cut, it needs to be actually played. SoundManager2 is a Javascript library that we use to play MP3s through a web page. After the hour is finished, the playlist is changed to the next hour and played from there.
Future Plans:
Currently, Noize Machine and DJ Pro are separate programs. Radio 1190 is aiming to integrate these different pieces of software with the help of another senior projects team next year. We have left mockups to describe the intended flow between manual DJs and the Noize Machine system, though the rest of the DJ pro system should be given a makeover as well. Eventually, the whole website will be redesigned to have a similar look and feel to Noize Machine. 



