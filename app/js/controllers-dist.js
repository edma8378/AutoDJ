var myApp=angular.module("myApp",[]);myApp.controller("musicPlayer",function(n,e,o){soundManager.setup({url:"swf/",preferFlash:"false"}),soundManager.onready(function(){t()});var t=function(){e.date=new Date,console.log(e.date),e.filt=n("date")(e.date,"yyyy-MM-dd/Ha"),pl=angular.lowercase(e.filt).toString(),console.log(pl),name="2014-12-19/8am",o.get("playlists/"+pl+".playlist").then(function(o){e.playlists=o.data,e.minute=parseInt(n("date")(new Date,"mm")),console.log(e.minute),e.second=parseInt(n("date")(new Date,"ss")),console.log(e.second),e.curTime=60*e.minute+e.second,console.log(e.curTime),e.songTime=0,e.songNum;for(var t=0;t<=e.playlists.length-1;t++)if(e.songTime=e.songTime+parseInt(e.playlists[t].length),console.log(e.songTime),e.songTime>e.curTime){e.songNum=t+1;break}e.makeMusic(e.songNum)})};e.makeMusic=function(o){e.numSong=o.toString();var t=e.playlists;console.log(t[e.numSong].path),console.log(t.length),path=t[o].path,document.getElementById("songName").innerHTML=t[o].song,document.getElementById("artistAlbum").innerHTML=t[o].artist+"-"+t[o].album,soundManager.createSound({id:e.numSong,url:path,stream:!0,autoLoad:!0,autoPlay:!0,whileplaying:function(){var o=this.duration-this.position;e.timeProg=this.position/this.duration*100;var t=n("date")(new Date(o),"mm:ss");document.getElementById("timeLeft").innerHTML=t,document.getElementById("progBar").style.width=e.timeProg+"%"},onfinish:function(){o++,e.makeMusic(o)}})},e.pauseMusic=function(){console.log(e.numSong),soundManager.togglePause(e.numSong)}});
