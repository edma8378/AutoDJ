var myApp = angular.module('myApp', []);

myApp.controller('PlaylistCtrl', function($scope, $http) {
  $http.get('playlists/playlist.json')
       .then(function(res){
          $scope.playlists = res.data;
        });
});

myApp.controller('musicPlayer', function() {
	soundManager.setup({
		url:'swf/',
		preferFlash: 'false',

		onready: function() {
			soundManager.createSound({
				id: 'swing',
				url:'music/swing.mp3',
				stream: true,
				whileplaying: function() {
      				var timeLeft = this.duration - this.position;
      				document.getElementById("timeLeft").innerHTML = timeLeft;
     			},
			});
			soundManager.play('swing', {volume:50});
		},
	});
});
