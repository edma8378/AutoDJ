#Front end functionality and sanity tests

Check the user guide, all that should be kosher.

Also if you check the javascript console you should may see soundmanager setup stuff with a bad GET of soundmanager2_debug.swf 404 (Not Found)
This is fine. Ignore this.
You will see a block of outputs from soundmanager getting ready, warnings are okay as long as at the end the log reads:
SoundManager 2: Ready.
Start/Stop button shuold now be enabled.

Press Play and the playlist for the hour should load,
 the Play buton should convert to Stop,
 and the currentsong info should appear.
 Song should be playing.
 Song should be highlighted blue in the playlist.
The console will spit out the song info and should show the 
sound#: canplay 
and
sound#: playing

The toaster pop up will appear when Stop is hit and when the Open DJ Pro link is hit.
The Play button should be disabled when either event occurs, and it will stay disabled until the song is over.


These are the things that should happen. Functionality tests are complete. Good for you.


