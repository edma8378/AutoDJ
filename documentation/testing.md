#Intro -please read-
Order of proper testsing and github pushes located in testingCrunkstep.md
Backend testing is using python unittest. Instructions below.

Front end tests were never done. It proved to be much more trouble to figue out how to write than it would be worth. Manually testing was much easier for this project. Dependencies were installed and ready, so protractor tests are ready to be written if you want. Currently the protractor test just checks it is the correct webpage. 

The expected behavior is documented in frontEndCheck.md, please go there to do sanity checks/tests for the webpage.

If a future team or person decides to implement protractor tests see below for Installation instructions and common problems. Thank you.
If in dire need contact kren7615@colorado.edu

## Back end tests
#Setup for local machines:
If you are on a local machine or server, setup databases and server.
1. Create databases in the directory backend, run DatabaseTools.py to set up databases and add at the very minimum add rotation music to the database:



		$ ./DatabaseTools.py create all
		$ ./DatabaseTools.py update digital rotation [folder/to/music]

2. Create Playlists
	in the backend directory, run:

		$ ./PlayMaker.py today
		today can be substitued with tomorrow or next week. The playlists will be generated and placed in app/music so they may be accessed by the webpage.

#To run: 	
	Go to the test directory and run UnitTest.py 
 	$ ./UnitTest.py

###Common Errors
  - python module problems, python doesn't recognize your modules because you didn't put them in your path, did you? Put them in your path.

    $ export PYTHONPATH=$PYTHONPATH:/my/other/path


#Protractor Test Stuff (not in use currently)
###Dependencies:
 - node.js          
 - java jdk
 - webdriver/selenium ~~OR chromedriver~~


###To Run Tests:  
	RUN SERVER:   $ webdriver-manager start
	RUN TESTS:    $ protractor conf.js


###Install Protractor
	$ npm install -g protractor
Guide: http://angular.github.io/protractor/#/tutorial

###Install Test Server (Webdriver/Selenium)

	$ sudo npm-install selenium-webdriver
	$ sudo webdriver-manager update --standalone

###To run the combo:
1. Start server and leave it running
        $ webdriver-manager start  
2. View session in browser to know it's working http://localhost:4444/wd/hub/
  3. This is the default selenium gives you, if it doesn't work check the protractor_conf.js file and look at the selenium address, match that to your filesystem's selenium path address.
3. Run the written tests
        $ protractor conf.js

	This should open another browser directing to your local server's version 
	of the app. It 	should pop up, maybe not even load all the way cause its
	 supafast, and close. The command line will spit out the results, the one
	 assertion should pass in green.
	 
	 NOTE: If your address is not 'localhost' this will not work, go into 
	protractor_conf.js and 	protractor_test.js and change the baseURL and 
	browser.get()  respectively.

>Leave this below here in case Alex or Mitchell can't use the selenium server or something and need to make chromedriver bullshit to work. (They don't use linux, so no selenium server)

###To install chromedriver: 
####Dependencies
 - Have chrome in /usr/bin/google-chrome
 - Guide: https://code.google.com/p/selenium/wiki/ChromeDriver

####Download and install: 
 - https://sites.google.com/a/chromium.org/chromedriver/downloads
 - executable is in the zip file

####To run the tests with chromedriver:
	$ protractor protractor_conf.js


##Architecture
 - http://www.thoughtworks.com/insights/blog/testing-angularjs-apps-protractor
 - Conclusion:  use combo of seleniumdriver and webdriver
 - No longer supporting chromedriver because I can't get the path to recognize it unles it's 	in node_modules in your app directly and it's not worth the agony.

###More:
 - http://angular.github.io/protractor/#/browser-setup
 - https://code.google.com/p/selenium/wiki/DesiredCapabilities
 - in the end you need to be running the server, and have a conf.js and spec.js
