angular.module('AutoDJ', ['toaster'])

// Filter for taking the length of the song in seconds and formatting it to be mm:ss
.filter('toSeconds', function()
  {
      return function(input)
      {
          var formattedString = "";
          var minutes = Math.floor(input/60);
          var seconds = input % 60;

          formattedString += "" + minutes + ":" + (seconds < 10 ? "0" : "");
          formattedString += "" + seconds;
          return formattedString;
  };
})

// Iniitialize the soundManager. Do not default to flash

.controller('musicPlayer', ['$scope', '$filter', '$http', '$window', 'toaster', function ($scope, $filter, $http, $window, toaster) {
  soundManager.setup({
    url:'swf/',
    preferFlash: 'false',
  });

//Start off with no music.
$scope.playing = 0;
$scope.disableButton = 0;

//stop and start sound
$scope.startStop = function() {
	if($scope.disableButton == 0){
    	$scope.playing = ($scope.playing + 1)%2;
 
 		// If the play button, start the playlist from where the hour is
	    if($scope.playing){	
	    	$scope.date = new Date();
	    	$scope.filt = $filter('date')($scope.date, "yyyy-MM-dd/H");
	    	$scope.makePlaylist($scope.filt, 0);
	    	document.getElementById("stopstart").innerHTML = "Stop";
	    	document.getElementById("stopstart").className = "orange";
	    }

	    // Else, warn the user and set the variable
	    else{
	    	toaster.pop('warning1', "OFF", "The current song will finish playing, Noize Machine is now off.");
	    	$scope.disableButton = 1;
	    	document.getElementById("stopstart").innerHTML = "Play";
	    	document.getElementById("stopstart").className = "gray";      
	    }
	}
}

//Stop and switch to DJ pro when song finishes
$scope.stop = function(){
	$scope.playing = 0;
	$window.open('https://radio1190.colorado.edu/djpro', '_blank');
	  toaster.pop('warning2', "DJPro", "The current song will finish playing, AutoDJ is now off.");
}

// Does what it says, adds an hour to the current hour and returns it
Date.prototype.addHours = function (h) {
    this.setHours(this.getHours()+h);
    return this;
}

// Update the timeLeftInHour to count down
$scope.updateHour = function() {
    var now = new Date();
    var minutes = 60-now.getMinutes();
    var seconds = 60-now.getSeconds();
    if(minutes < 10) { minutes = "0" + minutes}
    if(seconds < 10) { seconds = "0" + seconds}
    var timeLeftHourFormatted = minutes + ":" + seconds;
    document.getElementById("timeLeftInHour").innerHTML = timeLeftHourFormatted;
    var t = setTimeout(function(){$scope.updateHour()},500);
}

// Set currently playing to blue
$scope.updateCurrentlyPlaying = function(myIndex) {
    document.getElementById(myIndex).className = "currentlyPlaying";
}

//Set just finished song to not play
$scope.updateNotPlaying = function(myIndex) {
    document.getElementById(myIndex).className = "notYetPlayed";
}

// Create the playlist and decide where to start within the playlist
$scope.makePlaylist = function(date, st) {
  //Grab the playlist based off the date and hour
  $scope.pl = angular.lowercase(date).toString();
  $http.get('playlists/' + $scope.pl + '.playlist')
     .then(function(res){
        $scope.playlists = res.data;

        // If in the middle of the hour...
        if(!st){
          // Get current time in seconds
          $scope.minute = parseInt($filter('date')(new Date(), "mm"));
          $scope.second = parseInt($filter('date')(new Date(), "ss"));
          $scope.curTime = ($scope.minute * 60) + $scope.second;
          $scope.songTime = 0;
          $scope.songNum;

          // Get where in the playlist that would be by adding the duration of each song
          for (var i = 0; i <= $scope.playlists.length - 1; i++) {
            $scope.songTime = $scope.songTime + parseInt($scope.playlists[i].length);
            // When it is at the correct time, get the songNumber
            if($scope.songTime > $scope.curTime)
            {
              $scope.songNum = i;
              break;
            }
          };

          // If the songNumber is greater than the playlist, load the next one.
          if($scope.songNum > $scope.playlists.length - 1){
            $scope.date.addHours(1);
            $scope.filt = $filter('date')($scope.date, "yyyy-MM-dd/H");
            $scope.makePlaylist($scope.filt, 1);
          }

          // If not, cut the playlist in order to get the playlist to fit perfectly to an hour
          else{
          	for(i = $scope.playlists.length - 1; i >= 0; i--){
          	    $scope.leftInHour = 0;
          	    for(j = $scope.songNum; j <= $scope.playlists.length - 1; j++) {
          		    $scope.leftInHour = $scope.leftInHour + parseInt($scope.playlists[j].length);
          	    }
          	    $scope.totes = $scope.leftInHour + $scope.curTime;
          	    console.debug($scope.totes/60);
          	    if($scope.totes > 3600){
          	    	if($scope.playlists[i].isSong === 'yes'){
          	    		if(($scope.totes - parseInt($scope.playlists[i].length)) > 3300){
          	    			console.debug("Cutting: " + $scope.playlists[i].song);
          	    			$scope.playlists.splice(i, 1);

          	    		}
          	    	}
          	    }
          	}

          	// Play the song
            $scope.makeMusic($scope.songNum);
          }
        }

        // Start the playlist from the beginning
        else{
          $scope.songNum = 0;
          for(i = $scope.playlists.length - 1; i >= 0; i--){
              $scope.leftInHour = 0;
              for(j = $scope.songNum; j <= $scope.playlists.length - 1; j++) {
          	    $scope.leftInHour = $scope.leftInHour + parseInt($scope.playlists[j].length);
              }
              $scope.totes = $scope.leftInHour + 0;
              console.debug($scope.totes/60);
              $scope.minute = parseInt($filter('date')(new Date(), "mm"));
              $scope.second = parseInt($filter('date')(new Date(), "ss"));
              $scope.curTime = ($scope.minute * 60) + $scope.second;
              $scope.diffTime = 3600 - $scope.curTime;
              $scope.extraTime = $scope.diffTime + 3600;
              if($scope.totes > $scope.extraTime){
          	     if($scope.playlists[i].isSong === 'yes'){
          	 	    if(($scope.totes - parseInt($scope.playlists[i].length)) > (3300 + $scope.diffTime)){
          	 	   		console.debug("Cutting: " + $scope.playlists[i].song);
          	    		$scope.playlists.splice(i, 1);
          	        }
          	   }
            }
         }
          $scope.makeMusic($scope.songNum);
        }
    });
}

// Creates music based off of the song number given by the makePlaylist function
$scope.makeMusic = function(songNum) {
	// Set the proper fields in the page to the correct song
    $scope.numSong = songNum.toString();
    var json = $scope.playlists;
    $scope.path = json[songNum].path;
    $scope.songId = json[songNum].song;
    var currentIndex = "currentSong" + json[songNum].index;
    document.getElementById("songName").innerHTML = json[songNum].song;
    document.getElementById("artistAlbum").innerHTML = json[songNum].artist + "-" + json[songNum].album;

    // Create the sound and play it based off of the path
    $scope.currentSound = soundManager.createSound({
        url: $scope.path,
        stream: true,
        autoLoad: true,
        autoPlay: true,

        // Change the color of the current song
        onload: function() {
          $scope.updateCurrentlyPlaying(currentIndex);
        },

        // Update the progress bar and the time left
        whileplaying: function() {
             var timeLeft = this.duration - this.position;
             $scope.timeProg = (this.position/this.duration) * 100;
             var timeLeftFormatted = $filter('date')(new Date(timeLeft), 'mm:ss');
             document.getElementById("timeLeft").innerHTML = timeLeftFormatted;
             document.getElementById("progBar").style.width = $scope.timeProg +"%";
        },

        // Check the state of the button. If play, play the next song, if not, stop.
        onfinish: function() {
	  		if($scope.playing){
          		if(songNum >= $scope.playlists.length - 1){
            		$scope.date.addHours(1);
            		$scope.filt = $filter('date')($scope.date, "yyyy-MM-dd/H");
            		$scope.makePlaylist($scope.filt, 1);
          		}
          		else{
              		songNum++;
              		$scope.makeMusic(songNum)
            	}
            	$scope.updateNotPlaying(currentIndex);
        	}
			else{
				$scope.disableButton = 0;
    			document.getElementById("stopstart").className = "orange";
			}

		}
	});

	// Check to see if it got stalled for some reason
	$scope.currentSound._a.addEventListener('stalled', function() {
	    if (!self.currentSound) return;
	    var audio = this;
	    audio.load();
	    audio.play();
	});

}

// Call update hour
$( document ).ready(function() {
	$scope.updateHour();
});

}]);
