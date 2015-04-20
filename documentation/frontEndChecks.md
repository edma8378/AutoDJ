#Front end functionality and sanity tests

Check the user guide, all that should be kosher.

Also if you check the javascript console you should may see soundmanager setup stuff with a bad GET of soundmanager2_debug.swf 404 (Not Found)

This is fine. Ignore this.

You will see a block of outputs from soundmanager getting ready, warnings are okay as long as at the end the log reads:
SoundManager 2: Ready.

Start/Stop button should now be enabled. 

Good. The Play button should now be red instead of gray.

Press Play and the playlist for the hour should load,

 the Play button should convert to Stop,
 
 and the currentsong info should appear,
 
 Song should be playing,
 
 Song should be highlighted blue in the playlist.
 
 
The console will tell you if any songs were cut out of the hour for timing. If SoundManager is working the console will spit out the song info and information about the current sound.

sound#: canplay 

and

sound#: playing



When Stop is hit or when the Open DJ Pro link is hit a blue toaster should pop up in the right hand corner informing the user that the sound will stop after the current song finishes. Clicking the toaster will make it disappear.


The Play button should be disabled when either event occurs, and it will stay disabled until the song is over.


These are the things that should happen. Functionality tests are complete. Good for you.


