var myApp = angular.module('myApp', []);

myApp.controller('PlaylistCtrl', function($scope, $http) {
  $http.get('playlist.json')
       .then(function(res){
          $scope.playlists = res.data;                
        });
});
