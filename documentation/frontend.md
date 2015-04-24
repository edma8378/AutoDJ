The front end of the application is written in angularjs with help from jQuery and Soundmanager.
When starting, the web application grabs the time and date. 
The appropriate JSON object file containing the playlist and paths to each song is opened based on this time, 
and then finds which song should be playing and starts the playlist there. If the playlist is too long then the songs
will be cut from the list until the playlist ends directly at the end of the hour.
After the playlist is cut, it needs to be actually played. 

SoundManager2 is a Javascript library that we use to play MP3s through a web page. You will see this in app/js.
The songs continue to play until prompted to stop.

We also use the toaster class for the alerts in app/js/toaster.js. They are injected into controller.js.



# Controller
In the _controllers.js_ file, the methods that control the UI and create an actual playlist with the songs attached that it receives from the generated json file. 

### SoundManager Setup
The simple call to the SoundManager setup creates the manager and tells it to not default to Flash (as Flash causes more errors in a lot of browsers)

### MakePlaylist
In the _MakePlaylist_ function, it grabs the corresponding playlist based off of the time of day and the date. After loading this playlist file, it looks to decide where it should start. If a 0 was passed in, that means it is the beginning of the listening period, so it decides where in the hour it will be. It takes the current time in the hour and relates it to the playlist in order to start on the correct song. Then it calls on _MakeMusic_ in order actually play the song. It also checks to make sure that the current time wouldn't put it over the hour and it cuts the playlist accordingly if it does go over the hour.

If it isn't the beginning of the listening period, and it reaches the next playlist, it starts the hour at the first song and cuts the playlist accordingly due to the playlists being generated at longer than an hour.

### MakeMusic
In the _MakeMusic_ function, the playlist is called with the passed in index. The path to the song is called within the soundManager2 function _createSound_. The _createSound_ method calls the _whileplaying_ method in order to have the song's progress get shown on the progress bar while playing and then when the song finishes, to determine how to handle the next song (whether it is just the next song in the playlist or if the playlist is over and it needs to load the next one). In the _onfinish_ method, it checks whether or not the stop button was hit, and if it was, it stops playing.

### StartStop
The _StartStop_ function manages the button and whether or not it was pressed. If it is in the "stop" state, it plays the rest of the song and then the next song isn't played. If it is in the "start" state, it sends a the current time and day to the _MakePlaylist_ function, which determines which song to start on.

### AddHours
The _AddHours_ function is called when the playlist ends and the next playlist needs to be loaded. It is called in order to grab the next hour, as grabbing the current time wouldn't get the correct hour.

### UpdateHour
The _UpdateHour_ is called in order to change the "Time Left in Hour" part of the page to represent the correct time left. **This is the time left in the actual hour and not the playlist**

### UpdateCurrentlyPlaying
The _UpdateCurrentlyPlaying_ function is called in the _onload_ method of the _createSound_ function and it turns the color of the currently playing song blue in the UI.

### UpdateNotPlaying
The _UpdateNotPlaying_ function is called in the _onfinish_ method of the _createSound_ function and it turns the color of the song that just finished back to green in the UI.
