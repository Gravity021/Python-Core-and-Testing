import pygame

class InputManager:
    def __init__(self, game):
        self.game = game
    
    def start_frame(self):
        self.events = pygame.event.get()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_presses = pygame.mouse.get_pressed()

    def update(self):
        for event in self.events:
            # QUIT ------------------------------------------ #
            if event.type == pygame.QUIT:
                self.game.running = False
            
            # VIDEORESIZE ----------------------------------- #
            elif event.type == pygame.VIDEORESIZE:
                self.game.transition.sides[0].height = screen.get_height()
                self.game.transition.sides[1].height = screen.get_height()

                self.game.transition.sides[1].right = screen.get_width()
            
            # KEYDOWN --------------------------------------- #
            elif event.type == pygame.KEYDOWN:
                if not self.game.menu.MENU:
                    # Jump ------------------------ #
                    if event.key == self.game.entity_manager.player.controls["Jump"]:
                        if self.game.entity_manager.player.jumps_available > 0:
                            if self.game.entity_manager.player.jumps_available > 1:
                                self.game.entity_manager.player.gravity -= 15
                            elif self.game.entity_manager.player.jumps_available <= 1:
                                self.game.entity_manager.player.gravity -= 7
                            self.game.entity_manager.player.jumps_available -= 1

                            self.game.audio_manager.play("Jump")
                        
                        print("jump attempted")
                
                    # Left ------------------------ #
                    elif event.key == self.game.entity_manager.player.controls["Left"]:
                        self.game.entity_manager.player.moving["Left"] = True
                        self.game.entity_manager.player.moving["Right"] = False
                        self.game.entity_manager.player.animation.flip = False
                        
                    # Right ----------------------- #
                    elif event.key == self.game.entity_manager.player.controls["Right"]:
                        self.game.entity_manager.player.moving["Left"] = False
                        self.game.entity_manager.player.moving["Right"] = True
                        self.game.entity_manager.player.animation.flip = True
                    
                    # Open ------------------------ #
                    elif event.key == self.game.entity_manager.player.controls["Open"]:
                        for tile in self.game.game_map.doors:
                            if self.game.entity_manager.player.rect.colliderect(tile[0]):
                                self.game.transition.target = tile[1]
                                self.game.transition.transitioning = True
                                self.game.transition.transitioning_in = True
                    
                    # K_r ------------------------- #
                    elif event.key == pygame.K_r:
                        spawn = self.game.game_map.calculate_spawn()
                        self.game.entity_manager.player.rect.x = spawn[0]
                        self.game.entity_manager.player.rect.y = spawn[1]

                # # K_SPACE ------------------------- #
                elif event.key == pygame.K_SPACE:
                    pass
            
            # KEYUP ----------------------------------------- #
            elif event.type == pygame.KEYUP:
                if not self.game.menu.MENU:
                    # Left ------------------------ #
                    if event.key == self.game.entity_manager.player.controls["Left"]:
                        self.game.entity_manager.player.moving["Left"] = False
                        
                    # Right ----------------------- #
                    elif event.key == self.game.entity_manager.player.controls["Right"]:
                        self.game.entity_manager.player.moving["Right"] = False