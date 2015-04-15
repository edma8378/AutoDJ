angular.module('AutoDJ', ['toaster'])

//Filter for taking the length of the song in seconds and formatting it to be mm:ss
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

.controller('musicPlayer', ['$scope', '$filter', '$http', '$window', 'toaster', function ($scope, $filter, $http, $window, toaster) {
  soundManager.setup({
    url:'swf/',
    preferFlash: 'false',

    // onready: function() {
    //  soundManager.createSound({
    //    id: 'swing',
    //    url:'music/swing.mp3',
    //    stream: true,
    //    whileplaying: function() {
  //            var timeLeft = this.duration - this.position;
  //            document.getElementById("timeLeft").innerHTML = timeLeft;
  //          },
    //  });
    //  soundManager.play('swing', {volume:50});
    // },
  });

//Start off with no music.
$scope.playing = 0;
$scope.disableButton = 0;

//stop and start sound
  $scope.startStop = function() {
   if($scope.disableButton == 0){
    console.log("stop button hit");
    $scope.playing = ($scope.playing + 1)%2;
 
    if($scope.playing){	
      $scope.date = new Date();
      console.log($scope.date);
      $scope.filt = $filter('date')($scope.date, "yyyy-MM-dd/H");
      $scope.makePlaylist($scope.filt, 0);
    }
   else{
    toaster.pop('warning1', "Normal", "The current song will finish playing, AutoDJ is now off.");
       $scope.disableButton = 1;
    }
	}
  }

//Stop and switch to DJ pro when song finishes
$scope.stop = function(){
	console.log("Switched to DJPro, current song will finish and then switch will happen.");
	$scope.playing = 0;
	$window.open('https://radio1190.colorado.edu/djpro', '_blank');
	  toaster.pop('warning2', "DJPro", "The current song will finish playing, AutoDJ is now off.");
}

  Date.prototype.addHours = function (h) {
    this.setHours(this.getHours()+h);
    return this;
    // body...
  }

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

  $scope.updateCurrentlyPlaying = function(myIndex) {
    console.log(myIndex + " IS MY INDEX");
    document.getElementById(myIndex).className = "currentlyPlaying";
  }

  $scope.updateNotPlaying = function(myIndex) {
    document.getElementById(myIndex).className = "notYetPlayed";
  }
    $scope.makePlaylist = function(date, st) {
      $scope.pl = angular.lowercase(date).toString();
      $http.get('playlists/' + $scope.pl + '.playlist')
         .then(function(res){
            $scope.playlists = res.data;
            if(!st)
            {
              $scope.minute = parseInt($filter('date')(new Date(), "mm"));
              console.log($scope.minute);
              $scope.second = parseInt($filter('date')(new Date(), "ss"));
              console.log($scope.second);
              $scope.curTime = ($scope.minute * 60) + $scope.second;
              console.log($scope.curTime);
              $scope.songTime = 0;
              $scope.songNum;
              for (var i = 0; i <= $scope.playlists.length - 1; i++) {
                $scope.songTime = $scope.songTime + parseInt($scope.playlists[i].length);
                console.log($scope.songTime);
                if($scope.songTime > $scope.curTime)
                {
                  $scope.songNum = i;
                  break;
                }
              };
              if($scope.songNum > $scope.playlists.length - 1){
                $scope.date.addHours(1);
                $scope.filt = $filter('date')($scope.date, "yyyy-MM-dd/H");
                console.log($scope.filt);
                $scope.makePlaylist($scope.filt, 1);
              }

              else{
              	for(i = $scope.playlists.length - 1; i >= 0; i--){
              	    $scope.leftInHour = 0;
              	    for(j = $scope.songNum; j <= $scope.playlists.length - 1; j++) {
              		    $scope.leftInHour = $scope.leftInHour + parseInt($scope.playlists[j].length);
              	    }
              	    $scope.totes = $scope.leftInHour + $scope.curTime;
              	    console.log($scope.totes/60);
              	    if($scope.totes > 3600){
              	    	if($scope.playlists[i].isSong === 'yes'){
              	    		if(($scope.totes - parseInt($scope.playlists[i].length)) > 3300){
              	    			console.debug("Cutting: " + $scope.playlists[i].song);
              	    			$scope.playlists.splice(i, 1);

              	    		}
              	    		else{
              	    		}
              	    	}
              	    }
              	}
                $scope.makeMusic($scope.songNum);
              }
            }
            else{
              $scope.songNum = 0;
              for(i = $scope.playlists.length - 1; i >= 0; i--){
                  $scope.leftInHour = 0;
                  for(j = $scope.songNum; j <= $scope.playlists.length - 1; j++) {
              	    $scope.leftInHour = $scope.leftInHour + parseInt($scope.playlists[j].length);
                  }
                  $scope.totes = $scope.leftInHour + 0;
                  console.log($scope.totes/60);
                  $scope.minute = parseInt($filter('date')(new Date(), "mm"));
                  console.log($scope.minute);
                  $scope.second = parseInt($filter('date')(new Date(), "ss"));
                  console.log($scope.second);
                  $scope.curTime = ($scope.minute * 60) + $scope.second;
                  $scope.diffTime = 3600 - $scope.curTime;
                  $scope.extraTime = $scope.diffTime + 3600;
                  if($scope.totes > $scope.extraTime){
              	     if($scope.playlists[i].isSong === 'yes'){
              	 	    if(($scope.totes - parseInt($scope.playlists[i].length)) > (3300 + $scope.diffTime)){
              	 	   	console.debug("Cutting: " + $scope.playlists[i].song);
              	    	$scope.playlists.splice(i, 1);
              	        }
              	        else{
              	        }
              	   }
                }
             }
              $scope.makeMusic($scope.songNum);
            }
          });
  }

  $scope.makeMusic = function(songNum) {
    $scope.numSong = songNum.toString();
    var json = $scope.playlists;
    $scope.path = json[songNum].path;
    $scope.songId = json[songNum].song;
    var currentIndex = "currentSong" + json[songNum].index;
    console.log(currentIndex);
    document.getElementById("songName").innerHTML = json[songNum].song;
    document.getElementById("artistAlbum").innerHTML = json[songNum].artist + "-" + json[songNum].album;
    $scope.currentSound = soundManager.createSound({
        url: $scope.path,
        stream: true,
        autoLoad: true,
        autoPlay: true,
        onload: function() {
          $scope.updateCurrentlyPlaying(currentIndex);
        },
        whileplaying: function() {
              var timeLeft = this.duration - this.position;
              $scope.timeProg = (this.position/this.duration) * 100;
              var timeLeftFormatted = $filter('date')(new Date(timeLeft), 'mm:ss');
              document.getElementById("timeLeft").innerHTML = timeLeftFormatted;
              document.getElementById("progBar").style.width = $scope.timeProg +"%";
          },
        onfinish: function() {
	  if($scope.playing){
          if(songNum >= $scope.playlists.length - 1)
          {
            $scope.date.addHours(1);
            $scope.filt = $filter('date')($scope.date, "yyyy-MM-dd/H");
            console.log($scope.filt);
            $scope.makePlaylist($scope.filt, 1);
          }
          else{
              console.log($scope.playlists.length);
              songNum++;
              $scope.makeMusic(songNum)
          }
          $scope.updateNotPlaying(currentIndex);
        }
	else{
		$scope.disableButton = 0;
 		console.log("Should be stopped now");
	}

	}
      });
    $scope.currentSound._a.addEventListener('stalled', function() {
      if (!self.currentSound) return;
      var audio = this;
      audio.load();
      audio.play();
    });
  }

  $( document ).ready(function() {
    $scope.updateHour();
  });
}]);
