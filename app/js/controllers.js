angular.module('AutoDJ', [])

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

.controller('musicPlayer', ['$scope', '$filter', '$http', function ($scope, $filter, $http) {
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
  $scope.pauseMusic = function() {
    console.log($scope.numSong);
    soundManager.togglePause($scope.numSong);
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
  }

  $scope.makeMusic = function(songNum) {
    $scope.numSong = songNum.toString();
    var json = $scope.playlists;
    $scope.path = json[songNum].path;
    $scope.songId = json[songNum].song;
    document.getElementById("songName").innerHTML = json[songNum].song;
    document.getElementById("artistAlbum").innerHTML = json[songNum].artist + "-" + json[songNum].album;
    var currentSound = soundManager.createSound({
        url: $scope.path,
        stream: true,
        autoLoad: true,
        autoPlay: true,
        whileplaying: function() {
              var timeLeft = this.duration - this.position;
              $scope.timeProg = (this.position/this.duration) * 100;
              var timeLeftFormatted = $filter('date')(new Date(timeLeft), 'mm:ss');
              document.getElementById("timeLeft").innerHTML = timeLeftFormatted;
              document.getElementById("progBar").style.width = $scope.timeProg +"%";
              $scope.updateHour(); //update the hour as often as music is playing
          },
        onfinish: function() {
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
        }
      });
    currentSound._a.addEventListener('stalled', function() {
      if (!self.currentSound) return;
      var audio = this;
      audio.load();
      audio.play();
    });
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
              	    console.log("Hello, the time in the hour is" + $scope.curTime);
              	    $scope.leftInHour = 0;
              	    for(j = $scope.songNum; j <= $scope.playlists.length - 1; j++) {
              		    $scope.leftInHour = $scope.leftInHour + parseInt($scope.playlists[j].length);
              	    }
              	    console.log("The time left in the playlist is" + $scope.leftInHour);
              	    $scope.totes = $scope.leftInHour + $scope.curTime;
              	    console.log($scope.totes/60);
              	    if($scope.totes > 3600){
              	    	if($scope.playlists[i].typeName !== 'ad'){
              	    		if(($scope.totes - parseInt($scope.playlists[i].length)) > 3300){
              	    			console.log("Splicing")
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
                  console.log("Hello, the time in the hour is" + $scope.curTime);
                  $scope.leftInHour = 0;
                  for(j = $scope.songNum; j <= $scope.playlists.length - 1; j++) {
              	    $scope.leftInHour = $scope.leftInHour + parseInt($scope.playlists[j].length);
                  }
                  console.log("The time left in the playlist is" + $scope.leftInHour);
                  $scope.totes = $scope.leftInHour + 0;
                  console.log($scope.totes/60);
                  $scope.minute = parseInt($filter('date')(new Date(), "mm"));
                  console.log($scope.minute);
                  $scope.second = parseInt($filter('date')(new Date(), "ss"));
                  console.log($scope.second);
                  $scope.curTime = ($scope.minute * 60) + $scope.second;
                  $scope.diffTime = 3600 - $scope.curTime;
                  $scope.diffTime = $scope.diffTime + 3600;
                  if($scope.totes > $scope.diffTime){
              	     if($scope.playlists[i].typeName !== 'ad'){
              	 	    if(($scope.totes - parseInt($scope.playlists[i].length)) > 3300){
              	    	console.log("Splicing")
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
  soundManager.onready(function (){
    $scope.date = new Date();
    console.log($scope.date);
    $scope.filt = $filter('date')($scope.date, "yyyy-MM-dd/H");
    $scope.makePlaylist($scope.filt, 0);
  });
}]);
