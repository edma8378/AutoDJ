var myApp = angular.module('myApp', []);

myApp.controller('musicPlayer', function($filter, $scope, $http) {
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
  soundManager.onready(function(){
    $scope.date = new Date();
    console.log($scope.date);
    $scope.filt = $filter('date')($scope.date, "yyyy-MM-dd/H");
    makePlaylist($scope.filt, 0);
  });
  var makePlaylist = function(date, st) {
      $scope.pl = angular.lowercase(date).toString();
      console.log($scope.pl);
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
                  $scope.songNum = i + 1;
                  break;
                }
              };
              if($scope.songNum > $scope.playlists.length - 1){
                $scope.date.addHours(1);
                $scope.filt = $filter('date')($scope.date, "yyyy-MM-dd/H");
                console.log($scope.filt);
                makePlaylist($scope.filt, 1);
              }
              else{
                $scope.makeMusic($scope.songNum);   
              }
            }
            else{
              $scope.songNum = 0;
              $scope.makeMusic($scope.songNum);
            }
          });
      }
  $scope.makeMusic = function(songId) {
    $scope.numSong = songId.toString();
    var json = $scope.playlists;
    console.log(json[$scope.numSong].path);
    console.log(json.length);
    path = json[songId].path;
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
              $scope.timeProg = (this.position/this.duration) * 100;
              var timeLeftFormatted = $filter('date')(new Date(timeLeft), 'mm:ss');
              document.getElementById("timeLeft").innerHTML = timeLeftFormatted;
              document.getElementById("progBar").style.width = $scope.timeProg +"%";
          },
        onfinish: function() {
          if(songId >= $scope.playlists.length - 1)
          {
            $scope.date.addHours(1);
            $scope.filt = $filter('date')($scope.date, "yyyy-MM-dd/H");
            console.log($scope.filt);
            makePlaylist($scope.filt, 1);
          }
          else{
              console.log($scope.playlists.length);
              songId++;
              $scope.makeMusic(songId)
          }
        }
      });
  }
  $scope.pauseMusic = function() {
    console.log($scope.numSong);
    soundManager.togglePause($scope.numSong);
  }
  Date.prototype.addHours = function (h) {
    this.setHours(this.getHours()+h);
    return this;
    // body...
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
