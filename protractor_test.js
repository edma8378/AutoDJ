// protractor_spec.js
// Scenario tests for the application

describe('AutoDJ', function() {
	// Put variables you need to access elements here 
	// If more test files are added and global variables are needed, add to
 	// protractor_conf.js in the Global variables section
	//Testing some song functionality with the swing.mp3
        //var song1Path = '/home/kristi/Documents/AutoDj/AutoDJ/app/music/swing.mp3';
	//var song1 = document.getElementById('song1Path');


	beforeEach(function() {
		   // Change this to the address you're using
		   // This much match protractor_conf.js baseURL
		  browser.get('http://localhost');
	});
	
	it('should have the correct title', function() {
  		expect(browser.getTitle()).toEqual('AutoDJ');
	});

	//Soundmanager is working
	it('TEST NOT IMPLEMENTED. should be using soundManager, onready() has occured', function() {
	
	});

	//Soundmanager will play from a paht
 	it('TEST NOT IMPLEMENTED. Should be able to play a url', function(){
		//expect(soundManager.canPlayURL(song1Path)).toEqual(true);
	});
	//Should play an mp3
	it('TEST NOT IMPLEMENTED. Should be able to play a MIME', function(){
		//expect(soundManager.canPlayURL(song1Path)).toEqual(true);
	});
  
	it('TEST NOT IMPLEMENTED. Is AutoDJ, and should have loaded playlist', function(){

	});

	it('TEST NOT IMPLEMENTED. Should be the playlist for the correct hour', function(){

	});

	it('TEST NOT IMPLEMENTED. Should let a user log in', function(){
	});

});
