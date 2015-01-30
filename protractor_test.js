// protractor_spec.js
// Scenario tests for the application

describe('AutoDJ', function() {
	// Put variables you need to access elements here 
	// If more test files are added and global variables are needed, add to
 	// protractor_conf.js in the Global variables section


	beforeEach(function() {
		   // Change this to the address you're using
		   // This much match protractor_conf.js baseURL
		  browser.get('http://localhost');
	});
	
	it('should have the correct title', function() {
  		expect(browser.getTitle()).toEqual('AutoDJ');
	});

	it('should be using soundManager, onready() has occured', function() {
	
	});
  
});
