var myApp=angular.module("myApp",[]);myApp.controller("musicPlayer",function(e,t,n){soundManager.setup({url:"swf/",preferFlash:"false"}),soundManager.onready(function(){t.date=new Date,console.log(t.date),t.filt=e("date")(t.date,"yyyy-MM-dd/H"),o(t.filt,0)});var o=function(l,s){t.pl=angular.lowercase(l).toString(),console.log(t.pl),n.get("playlists/"+t.pl+".playlist").then(function(n){if(t.playlists=n.data,s)t.songNum=0,t.makeMusic(t.songNum);else{t.minute=parseInt(e("date")(new Date,"mm")),console.log(t.minute),t.second=parseInt(e("date")(new Date,"ss")),console.log(t.second),t.curTime=60*t.minute+t.second,console.log(t.curTime),t.songTime=0,t.songNum;for(var l=0;l<=t.playlists.length-1;l++)if(t.songTime=t.songTime+parseInt(t.playlists[l].length),console.log(t.songTime),t.songTime>t.curTime){t.songNum=l+1;break}t.songNum>t.playlists.length-1?(t.date.addHours(1),t.filt=e("date")(t.date,"yyyy-MM-dd/H"),console.log(t.filt),o(t.filt,1)):t.makeMusic(t.songNum)}})};t.makeMusic=function(n){t.numSong=n.toString();var l=t.playlists;console.log(l[t.numSong].path),console.log(l.length),path=l[n].path,document.getElementById("songName").innerHTML=l[n].song,document.getElementById("artistAlbum").innerHTML=l[n].artist+"-"+l[n].album,soundManager.createSound({id:t.numSong,url:path,stream:!0,autoLoad:!0,autoPlay:!0,whileplaying:function(){var n=this.duration-this.position;t.timeProg=this.position/this.duration*100;var o=e("date")(new Date(n),"mm:ss");document.getElementById("timeLeft").innerHTML=o,document.getElementById("progBar").style.width=t.timeProg+"%"},onfinish:function(){n>=t.playlists.length-1?(t.date.addHours(1),t.filt=e("date")(t.date,"yyyy-MM-dd/H"),console.log(t.filt),o(t.filt,1)):(console.log(t.playlists.length),n++,t.makeMusic(n))}})},t.pauseMusic=function(){console.log(t.numSong),soundManager.togglePause(t.numSong)},t.submitLogin=function(){console.log("Fire")},Date.prototype.addHours=function(e){return this.setHours(this.getHours()+e),this}});var submitExample=angular.module("submitExample",[]);submitExample.controller("ExampleController",function(e){e.list=[],e.text="hello",e.submit=function(){console.log("Clciked")}});
