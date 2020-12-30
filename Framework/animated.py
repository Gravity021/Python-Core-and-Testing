import pygame

class Animated:
    def __init__(self):
        self.animation_database = {} # anim_database = {"action 1": [[frame, duration], [frame, duration]] "action 2": ...
        self.animation_frame = 0
        self.action = None
        self.image = None
        self.flip = False

    def load_images(self, action, folder, durations):
        animation_frames = []
        for frame_duration in range(len(durations)):
            for i in range(durations[frame_duration]):
                animation_frames.append(pygame.image.load(f"{folder}/{action}_{frame_duration}.png"))
        self.animation_database[action] = animation_frames
        self.action = action
    
    def update(self):
        if self.action != None:
            self.animation_frame += 1
            if self.animation_frame > len(self.animation_database[self.action]) - 1:
                self.animation_frame = 0
            self.image = self.animation_database[self.action][self.animation_frame]