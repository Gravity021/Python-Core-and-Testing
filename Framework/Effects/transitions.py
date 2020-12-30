import pygame

class Transition:
    def __init__(self, game, speed):
        self.game = game
        self.transitioning = False
        self.transitioning_in = True
        self.width = 0
        self.speed = speed
        self.done_for = 0
        self.target = None
    
    def update_linear(self):
        self.width += self.speed

    def update_exponential(self):
        pass

class SideSwipe(Transition):
    def __init__(self, game, speed):
        Transition.__init__(self, game, speed)
        self.sides = [pygame.Rect(0, 0, 0, self.game.window_manager.screen.get_height()), pygame.Rect(self.game.window_manager.screen.get_width(), 0, 0, self.game.window_manager.screen.get_height())]
    
    def update_linear(self):
        if self.transitioning:
            for side in self.sides:
                if self.transitioning_in:
                    if side.width < self.game.window_manager.screen.get_width() / 2:
                        if side == self.sides[0]:
                            side.width += self.speed * self.game.dt
                        elif side == self.sides[1]:
                            side.x -= self.speed * self.game.dt
                            side.width += self.speed * self.game.dt
                    elif side.width >= self.game.window_manager.screen.get_width() / 2:
                        if side == self.sides[0]:
                            side.width = self.game.window_manager.screen.get_width() / 2
                        elif side == self.sides[1]:
                            side.width = self.game.window_manager.screen.get_width() / 2
                            side.x = self.game.window_manager.screen.get_width() / 2
                        
                        self.game.game_map.open(f"Data/Maps/{self.target}")
                        spawn = self.game.game_map.calculate_spawn()
                        self.game.entity_manager.player.rect.x = spawn[0]
                        self.game.entity_manager.player.rect.y = spawn[1]
                        if self.game.menu.MENU:
                            self.game.menu.MENU = False

                        self.transitioning_in = False
                
                elif not self.transitioning_in:
                    if side.width > 0:
                        if side == self.sides[0]:
                            side.width -= self.speed * self.game.dt
                        elif side == self.sides[1]:
                            side.x += self.speed * self.game.dt
                            side.width -= self.speed * self.game.dt
                
                    elif side.width < 0:
                        side.width = 0
                        
                        if side == self.sides[1]:
                            side.x = self.game.window_manager.screen.get_width()
                        
                        self.transitioning = False
                        self.transitioning_in = True
    
            for side in self.sides:
                pygame.draw.rect(self.game.window_manager.self.game.window_manager.screen, (255, 255, 255), side)
    
    def update_exponential(self):
        if self.transitioning:
            for side in self.sides:
                if self.transitioning_in:
                    if side.width < self.game.window_manager.screen.get_width() / 2:
                        if side == self.sides[0]:
                            side.width += ((self.game.window_manager.screen.get_width() - side.width) // 30) * self.game.dt
                        elif side == self.sides[1]:
                            side.x -= ((self.game.window_manager.screen.get_width() - side.width) // 30) * self.game.dt
                            side.width += ((self.game.window_manager.screen.get_width() - side.width) // 30) * self.game.dt
                    elif side.width >= self.game.window_manager.screen.get_width() / 2:
                        if side == self.sides[0]:
                            side.width = self.game.window_manager.screen.get_width() / 2
                        elif side == self.sides[1]:
                            side.width = self.game.window_manager.screen.get_width() / 2
                            side.x = self.game.window_manager.screen.get_width() / 2
                        
                        self.game.game_map.open(f"Data/Maps/{self.target}")
                        spawn = self.game.game_map.calculate_spawn()
                        self.game.entity_manager.player.rect.x = spawn[0]
                        self.game.entity_manager.player.rect.y = spawn[1]
                        if self.game.menu.MENU:
                            self.game.menu.MENU = False

                        self.transitioning_in = False
                
                elif not self.transitioning_in:
                    if side.width > 0:
                        if side == self.sides[0]:
                            side.width -= ((self.game.window_manager.screen.get_width() - side.width) // 30) * self.game.dt
                        elif side == self.sides[1]:
                            side.x += ((self.game.window_manager.screen.get_width() - side.width) // 30) * self.game.dt
                            side.width -= ((self.game.window_manager.screen.get_width() - side.width) // 30) * self.game.dt
                
                    elif side.width < 0:
                        side.width = 0
                        
                        if side == self.sides[1]:
                            side.x = self.game.window_manager.screen.get_width()
                        
                        self.transitioning = False
                        self.transitioning_in = True
    
            for side in self.sides:
                pygame.draw.rect(self.game.window_manager.screen, (255, 255, 255), side)