import pygame, random

class Entity:
    def __init__(self, rect, speed):
        rect = (rect[0] - (rect[2] / 2), rect[1] - (rect[3] / 2), rect[2], rect[3])
        self.rect = pygame.Rect(rect)
        self.speed = speed
        self.velocity = pygame.Vector2(0, 0)
        self.gravity = 0
        self.jumps_available = 2
    
    def move(self, colliders):
        # colisions = {"Top": False, "Right": False, "Bottom": False, "Left": False}
        self.rect.x += self.velocity.x
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity.x > 0: # ------------- right
                    self.rect.right = collider.left
                elif self.velocity.x < 0: # ----------- left
                    self.rect.left = collider.right
        self.rect.y += self.velocity.y
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity.y > 0: # ------------- down
                    self.rect.bottom = collider.top
                    self.jumps_available = 2
                elif self.velocity.y < 0: # ----------- up
                    self.rect.top = collider.bottom
                    self.gravity = 0
        self.velocity.update(0, 0)

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
    
    def update(self):
        self.animation_frame += 1
        if self.animation_frame > len(self.animation_database[self.action]) - 1:
            self.animation_frame = 0
        self.image = self.animation_database[self.action][self.animation_frame]

class Player(Entity):
    def __init__(self, rect, controls, speed):
        Entity.__init__(self, rect, speed)
        self.animation = Animated()
        self.controls = controls