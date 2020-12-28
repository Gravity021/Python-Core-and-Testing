import pygame

# from Framework import 

class Transition:
    def __init__(self, speed):
        self.transitioning = False
        self.transitioning_in = True
        self.width = 0
        self.speed = speed
        self.done_for = 0
    
    def update_linear(self, screen):
        self.width += self.speed

    def update_exponential(self):
        pass

class SideSwipe(Transition):
    def __init__(self, speed, screen):
        Transition.__init__(self, speed)
        self.sides = [pygame.Rect(0, 0, 0, screen.get_height()), pygame.Rect(screen.get_width(), 0, 0, screen.get_height())]
    
    def update_linear(self, screen, on_complete):
        if self.transitioning:
            for side in self.sides:
                if self.transitioning_in:
                    if side.width < screen.get_width() / 2:
                        if side == self.sides[0]:
                            side.width += self.speed
                        elif side == self.sides[1]:
                            side.x -= self.speed
                            side.width += self.speed
                    elif side.width > screen.get_width() / 2:
                        if side == self.sides[0]:
                            side.width = screen.get_width() / 2
                        elif side == self.sides[1]:
                            side.width = screen.get_width() / 2
                            side.x = screen.get_width() / 2
                        
                        on_complete()

                        self.transitioning_in = False
                
                elif not self.transitioning_in:
                    if side.width > 0:
                        if side == self.sides[0]:
                            side.width -= self.speed
                        elif side == self.sides[1]:
                            side.x += self.speed
                            side.width -= self.speed
                
                    elif side.width < 0:
                        side.width = 0
                        
                        if side == self.sides[1]:
                            side.x = screen.get_width()
    
            for side in self.sides:
                pygame.draw.rect(screen, (255, 255, 255), side)