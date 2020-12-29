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
        self.rect.x += self.velocity.x
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity.x > 0: # ------------- right
                    self.rect.right = collider.left
                    self.velocity.x = 0
                elif self.velocity.x < 0: # ----------- left
                    self.rect.left = collider.right
                    self.velocity.x = 0
        self.rect.y += self.velocity.y
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity.y > 0: # ------------- down
                    self.rect.bottom = collider.top
                    self.jumps_available = 2
                elif self.velocity.y < 0: # ----------- up
                    self.rect.top = collider.bottom
                    self.gravity = 0

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

class Player(Entity):
    def __init__(self, rect, controls, speed, gravity, game_map):
        Entity.__init__(self, rect, speed)
        self.animation = Animated()
        self.controls = controls
        self.moving = {"Left": False, "Right": False}
        self.GRAVITY = gravity
        self.game_map = game_map

    def update(self, dt):
        if self.moving["Left"] and not self.moving["Right"]:
            self.velocity.x -= 0.5 * dt
            self.velocity.x = max(self.velocity.x, -self.speed)
        elif self.moving["Right"] and not self.moving["Left"]:
            self.velocity.x += 0.5 * dt
            self.velocity.x = min(self.velocity.x, self.speed)
        elif not self.moving["Left"] and not self.moving["Right"]:
            if self.velocity.x > 0:
                self.velocity.x -= 0.5 * dt
            elif self.velocity.x < 0:
                self.velocity.x += 0.5 * dt

        self.gravity = min(self.gravity + self.GRAVITY, 5) * dt
        self.velocity.y = self.gravity
        
        self.move(self.game_map.collidable)
        self.animation.update()