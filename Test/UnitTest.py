#!/usr/bin/python
import sys
import os
#Path to Main AutoDJ folder
sys.path.append(os.getcwd()+"/../")
#print sys.path
from backend.PlayMaker import *
import datetime
import backend.DatabaseTools 
import unittest
import random
import json

playlist_dir = "../app/playlists/test/"

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.playlistList = [[[i+j+k for i in range(5)]for j in range(10)]for k in range(24)]
        self.day = datetime.date.today().strftime('%Y-%m-%d')

    def file_create(self):
        outputPlaylists(self.day,self.playlistList)
        self.assertTrue(os.path.isdir(playlist_dir+self.day))
        path, dirs, files = os.walk(playlist_dir+self.day).next()
        self.assertEqual(len(dirs),0)
        self.assertEqual(len(files),24)

    def file_correct(self):
        self.assertTrue(os.path.isdir(playlist_dir+self.day))
        path, dirs, files = os.walk(playlist_dir+self.day).next()       
        sampleOutput = files[random.randint(0,len(files)-1)]
        with open(playlist_dir+self.day+"/"+sampleOutput) as json_file:
            json_data = json.load(json_file)
            self.assertNotEqual(len(json_data),0)

	
    def random_song_test(self):
        type = "rotation"
        rand1 = randomSong(type)
        rand2 = randomSong(type)
        rand3 = randomSong(type)
        self.assertNotEqual(rand1, None)
        self.assertNotEqual(rand2, None)
        self.assertNotEqual(rand3, None)
        self.assertNotEqual(rand3 == rand2 == rand1, True)
        self.assertEqual(rand1[6] == type, True)

    def random_ad_test(self):
        type = ""
        rand1 = randomAD(type)
        rand2 = randomAD(type)
        self.assertNotEqual(rand1, None)
        self.assertNotEqual(rand2, None)
        #self.assertNotEqual(rand2 == rand1, True)

    def gen_playlist(self):
        day = datetime.date.today()
        playlist = generatePlaylist(15,day)
        self.assertNotEqual(playlist, None)
        for i in range(len(playlist)):
            if i != 0:
                self.assertNotEqual(playlist[i], playlist[i-1])

    def test_steps(self):
        self.file_create()
        self.file_correct()
        self.random_song_test()
        self.random_ad_test()
        self.gen_playlist()
    
if __name__ =="__main__":
    unittest.main()
