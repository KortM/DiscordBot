import os
import discord
from discord.ext import commands
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
import math

class Music:
    basedir = os.path.dirname(__file__) + '/Musics/'
    def __init__(self):
        self.musics = []
        self.count = 0
        self.audio = None
        list = os.listdir(self.basedir)
        for m in list:
            self.musics.append(m)
        print(list)
    def curent(self):
        return self.musics[self.count]
    def next(self):
        self.count += 1
        if self.count >= len(self.musics):
            self.count = 0
        return self.musics[self.count]
    def prev(self):
        self.count -= 1
        if self.count < 0:
            self.count = len(self.musics)-1
        return self.musics[self.count]

    def getMusics(self):
        return self.musics
    def get_next_track(self):
        i = self.count
        i+=1
        return self.musics[i]
    def get_track(self, id):
        return self.musics[id]
    def get_track_duration(self, aud):
        self.audio = MP3(aud)
        min = int(self.audio.info.length / 60)
        second = round(self.audio.info.length % 60)
        if len(str(second)) <2:
            second = '0'+str(second)
        return str(str(min)+":"+str(second))

    def get_count(self):
        return self.count
    def set_count(self, count):
        self.count = count
    def inc_count(self):
        self.count +=1
if __name__=='__main__':
    b = Music()

    print(b.get_track_duration(b.basedir+b.next()))
    print(b.get_track_duration(b.basedir + b.next()))
    print(b.get_track_duration(b.basedir + b.next()))