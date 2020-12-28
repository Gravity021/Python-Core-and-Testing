import pygame, json
from Framework import sound

class AudioManager:
    def __init__(self):
        self.channels = {} # {"name": pygame.mixer.Channel}
        self.sounds = {} # {"name": sound.Sound}
        with open("Data/Audio/audio_config.json") as file:
            file_data = json.loads(file.read())
            channel_no = 0
            for name, data in file_data["Channels"].items():
                self.channels[name] = pygame.mixer.Channel(channel_no)
                self.channels[name].set_volume(data["volume"])

            for name, data in file_data["Sounds"].items():
                self.sounds[name] = sound.Sound(pygame.mixer.Sound("Data/Audio" + data["path"]), self.channels[data["channel"]], data["volume"], data["play_times"] - 1)
    
    def play(self, name):
        try:
            s = self.sounds[name]
        except Exception:
            s = None
        
        if s != None:
            s.channel.play(s.clip, s.loops)

        elif s == None:
            print(f"WARNING: Sound {name} could not be found")

class EntityManager():
    pass