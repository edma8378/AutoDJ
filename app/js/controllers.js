
angular.module('AutoDJ', [])
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
  $scope.makeMusic = function(songNum) {
    $scope.numSong = songNum.toString();
    var json = $scope.playlists;
    $scope.path = json[songNum].path;
    $scope.songId = json[songNum].song;
    document.getElementById("songName").innerHTML = json[songNum].song;
    document.getElementById("artistAlbum").innerHTML = json[songNum].artist + "-" + json[songNum].album;
    soundManager.createSound({
        id: $scope.songNum + "-" + $scope.pl,
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
  }
  $scope.makePlaylist = function(date, st) {
      $scope.pl = angular.lowercase(date).toString();
      console.log($scope.pl);
      name = "2014-12-19/8am";
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
                $scope.makePlaylist($scope.filt, 1);
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
  soundManager.onready(function (){
    $scope.date = new Date();
    console.log($scope.date);
    $scope.filt = $filter('date')($scope.date, "yyyy-MM-dd/H");
    $scope.makePlaylist($scope.filt, 0);
  });
}]);
