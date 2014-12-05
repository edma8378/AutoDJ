#!/usr/bin/python
from PlayMaker import outputPlaylists
from PlayMaker import randomSong
from datetime import datetime
from DatabaseTools import createTable
import unittest
import os
import random
import json


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.playlistList = [[[i+j+k for i in range(5)]for j in range(10)]for k in range(24)]
        self.day = datetime.now().strftime('%Y-%m-%d')

    def file_create(self):
        outputPlaylists(self.day,self.playlistList)
        self.assertTrue(os.path.isdir("playlists/"+self.day))
        path, dirs, files = os.walk("playlists/"+self.day).next()
        self.assertEqual(len(dirs),0)
        self.assertEqual(len(files),24)

    def file_correct(self):
        self.assertTrue(os.path.isdir("playlists/"+self.day))
        path, dirs, files = os.walk("playlists/"+self.day).next()       
        sampleOutput = files[random.randint(0,len(files)-1)]
        with open("playlists/"+self.day+"/"+sampleOutput) as json_file:
            json_data = json.load(json_file)
            self.assertNotEqual(len(json_data),0)

	
    def random_song_test(self):
        rand1 = randomSong()
        rand2 = randomSong()
        rand3 = randomSong()
	self.assertNotEqual(rand1, None)
	self.assertNotEqual(rand2, None)
	self.assertNotEqual(rand3, None)
	self.assertNotEqual(rand3 == rand2 == rand1, True)

    def random_ad_test(self):
        rand1 = randomAd()
        rand2 = randomAd()
        self.assertNotEqual(rand1, None)
        self.assertNotEqual(rand2, None)
        self.assertNotEqual(rand2 == rand1, True)

    def test_steps(self):
        self.file_create()
        self.file_correct()
	self.random_song_test()


    
if __name__ == '__main__':
    unittest.main()
