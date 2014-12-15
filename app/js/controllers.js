var myApp = angular.module('myApp', []);

myApp.controller('musicPlayer', function($filter, $scope, $http) {
	soundManager.setup({
		url:'swf/',
		preferFlash: 'false',

		// onready: function() {
		// 	soundManager.createSound({
		// 		id: 'swing',
		// 		url:'music/swing.mp3',
		// 		stream: true,
		// 		whileplaying: function() {
  //     				var timeLeft = this.duration - this.position;
  //     				document.getElementById("timeLeft").innerHTML = timeLeft;
  //    			},
		// 	});
		// 	soundManager.play('swing', {volume:50});
		// },
	});
  soundManager.onready(function(){
    makePlaylist();
  });
  var makePlaylist = function() {
    $http.get('../playlists/2014-12-19/9am.playlist')
       .then(function(res){
          $scope.playlists = res.data;
          $scope.makeMusic(0);
        });
     }
  $scope.makeMusic = function(songId) {
    $scope.numSong = songId.toString();
    var json = $scope.playlists;
    console.log(json[$scope.numSong].path);
    console.log(json.length);
    path = "../" + json[songId].path;
    document.getElementById("songName").innerHTML = json[songId].song;
    document.getElementById("artistAlbum").innerHTML = json[songId].artist + "-" + json[songId].album;
  	soundManager.createSound({
				id: $scope.numSong,
				url: path,
				stream: true,
        autoLoad: true,
        autoPlay: true,
				whileplaying: function() {
      				var timeLeft = this.duration - this.position;
      				var timeLeftFormatted = $filter('date')(new Date(timeLeft), 'mm:ss');
      				document.getElementById("timeLeft").innerHTML = timeLeftFormatted;
     			},
        onfinish: function() {
              songId++;
              $scope.makeMusic(songId)
        }
			});
  }
  $scope.pauseMusic = function() {
    console.log($scope.numSong);
    soundManager.togglePause($scope.numSong);
  }

});
// for(var i = 0; i < json.length; i++)
//           {
//             $scope.flag = true
//             $scope.makeMusic(i, "../" + json[i].path);
//             console.log(json[i].artist);
//             soundManager.play(i, {
//               onfinish: function() {
//                 $scope.flag = false;
//             }})
//             while(!($scope.flag));
//             console.log("here");
//           }
