import pygame

class Sound:
    def __init__(self, clip, channel, volume=1, play_times=0):
        self.clip = clip
        self.channel = channel
        self.volume = volume
        self.loops = play_times

class AudioManager:
    def __init__(self):
        self.sounds = {}
    
    def play(self, name):
        try:
            s = self.sounds[name]
        except Exception:
            s = None
        
        if s != None:
            # s.clip.play(s.loops)
            s.channel.play(s.clip, s.loops)

        elif s == None:
            print(f"WARNING: Sound {name} could not be found")