import pygame

from Framework.entity import Entity
from Framework.animated import Animated

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