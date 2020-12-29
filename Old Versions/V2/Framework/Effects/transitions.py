import pygame

class Transition:
    def __init__(self, speed, on_complete):
        self.transitioning = False
        self.transitioning_in = True
        self.width = 0
        self.speed = speed
        self.done_for = 0
        self.target = None
        self.on_complete = on_complete
    
    def update_linear(self, screen):
        self.width += self.speed

    def update_exponential(self):
        pass

class SideSwipe(Transition):
    def __init__(self, speed, screen, on_complete):
        Transition.__init__(self, speed, on_complete)
        self.sides = [pygame.Rect(0, 0, 0, screen.get_height()), pygame.Rect(screen.get_width(), 0, 0, screen.get_height())]
    
    def update_linear(self, screen, on_complete, dt):
        if self.transitioning:
            for side in self.sides:
                if self.transitioning_in:
                    if side.width < screen.get_width() / 2:
                        if side == self.sides[0]:
                            side.width += self.speed * dt
                        elif side == self.sides[1]:
                            side.x -= self.speed * dt
                            side.width += self.speed * dt
                    elif side.width >= screen.get_width() / 2:
                        if side == self.sides[0]:
                            side.width = screen.get_width() / 2
                        elif side == self.sides[1]:
                            side.width = screen.get_width() / 2
                            side.x = screen.get_width() / 2
                        
                        on_complete(self.target)

                        self.transitioning_in = False
                
                elif not self.transitioning_in:
                    if side.width > 0:
                        if side == self.sides[0]:
                            side.width -= self.speed * dt
                        elif side == self.sides[1]:
                            side.x += self.speed * dt
                            side.width -= self.speed * dt
                
                    elif side.width < 0:
                        side.width = 0
                        
                        if side == self.sides[1]:
                            side.x = screen.get_width()
                        
                        self.transitioning = False
                        self.transitioning_in = True
    
            for side in self.sides:
                pygame.draw.rect(screen, (255, 255, 255), side)
    
    def update_exponential(self, screen, dt):
        if self.transitioning:
            for side in self.sides:
                if self.transitioning_in:
                    if side.width < screen.get_width() / 2:
                        if side == self.sides[0]:
                            side.width += ((screen.get_width() - side.width) // 30) * dt
                        elif side == self.sides[1]:
                            side.x -= ((screen.get_width() - side.width) // 30) * dt
                            side.width += ((screen.get_width() - side.width) // 30) * dt
                    elif side.width >= screen.get_width() / 2:
                        if side == self.sides[0]:
                            side.width = screen.get_width() / 2
                        elif side == self.sides[1]:
                            side.width = screen.get_width() / 2
                            side.x = screen.get_width() / 2
                        
                        self.on_complete(self.target)

                        self.transitioning_in = False
                
                elif not self.transitioning_in:
                    if side.width > 0:
                        if side == self.sides[0]:
                            side.width -= ((screen.get_width() - side.width) // 30) * dt
                        elif side == self.sides[1]:
                            side.x += ((screen.get_width() - side.width) // 30) * dt
                            side.width -= ((screen.get_width() - side.width) // 30) * dt
                
                    elif side.width < 0:
                        side.width = 0
                        
                        if side == self.sides[1]:
                            side.x = screen.get_width()
                        
                        self.transitioning = False
                        self.transitioning_in = True
    
            for side in self.sides:
                pygame.draw.rect(screen, (255, 255, 255), side)