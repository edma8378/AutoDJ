#Front end functionality and sanity tests

These are the expected results of running the webpage.
If you are setting up a local server, you will definitely want to use this.

##Run the page 
via localhost or on Radio1190's server.


##1. Go to the page.
     -The page should start off with a black background and the Noize Machine logo. 
     
     -The right side shoud be an orang section displaying the current time and have a Play button.


##2. Check the Javascript conole.

    Note: You may see soundmanager setup stuff with a bad GET of soundmanager2_debug.swf 404 (Not Found
     This is fine. Ignore this.

     -You will see a block of outputs from soundmanager getting ready,
     warnings are okay as long as at the end the log reads:

     - SoundManager 2: Ready.


     -The Start/Stop button should now be enabled. 
     
     -The Play button should now be red instead of gray.


##3. Press Play 
     -playlist for the hour should load and appear as a green list on the left
     
     -the Play button should convert to Stop
     
     -the current song info should appear
     
     - Song should be playing
     
     - Song should be highlighted blue in the playlist.
     
    -The console will tell you if any songs were cut out of the hour for timing.


     If SoundManager is working the console will spit out the song info and information about the current sound.

      sound#: canplay 

      and

      sound#: playing



##4. Press the Stop buttom.
   -a blue toaster should pop up in the right hand corner informing the user that the sound will stop after the current song   finishes. 
   
   -Clicking the toaster will make it disappear.   
   
   -The Play button should be disabled, and it will stay disabled until the song is over.
   
   -The sound will stop when the current song finishes
   

##5. The DjPro link is hit
   -The DJPro page should pop up
   
    -song should still be playing


These are the things that should happen. Functionality tests are complete. Good for you.


