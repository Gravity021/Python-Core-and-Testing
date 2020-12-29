import pygame

class InputManager:
    def __init__(self):
        pass

    def update(self, events):
        for event in events:
            # QUIT ------------------------------------------ #
            if event.type == pygame.QUIT:
                running = False
            
            # VIDEORESIZE ----------------------------------- #
            elif event.type == pygame.VIDEORESIZE:
                transition.sides[0].height = screen.get_height()
                transition.sides[1].height = screen.get_height()

                transition.sides[1].right = screen.get_width()
            
            # KEYDOWN --------------------------------------- #
            elif event.type == pygame.KEYDOWN:
                if not menu.MENU:
                    # Jump ------------------------ #
                    if event.key == entity_manager.player.controls["Jump"]:
                        if entity_manager.player.jumps_available > 0:
                            if entity_manager.player.jumps_available > 1:
                                entity_manager.player.gravity -= 15
                            elif entity_manager.player.jumps_available <= 1:
                                entity_manager.player.gravity -= 7
                            entity_manager.player.jumps_available -= 1

                            audio_manager.play("Jump")
                        
                        print("jump attempted")
                
                    # Left ------------------------ #
                    elif event.key == entity_manager.player.controls["Left"]:
                        entity_manager.player.moving["Left"] = True
                        entity_manager.player.moving["Right"] = False
                        entity_manager.player.animation.flip = False
                        
                    # Right ----------------------- #
                    elif event.key == entity_manager.player.controls["Right"]:
                        entity_manager.player.moving["Left"] = False
                        entity_manager.player.moving["Right"] = True
                        entity_manager.player.animation.flip = True
                    
                    # Open ------------------------ #
                    elif event.key == entity_manager.player.controls["Open"]:
                        for tile in game_map.doors:
                            if entity_manager.player.rect.colliderect(tile[0]):
                                transition.target = tile[1]
                                transition.transitioning = True
                                transition.transitioning_in = True
                    
                    # K_r ------------------------- #
                    elif event.key == pygame.K_r:
                        spawn = game_map.calculate_spawn(ctx)
                        entity_manager.player.rect.x = spawn[0]
                        entity_manager.player.rect.y = spawn[1]

                # K_SPACE ------------------------- #
                elif event.key == pygame.K_SPACE:
                    pass
            
            # KEYUP ----------------------------------------- #
            elif event.type == pygame.KEYUP:
                if not menu.MENU:
                    # Left ------------------------ #
                    if event.key == entity_manager.player.controls["Left"]:
                        entity_manager.player.moving["Left"] = False
                        
                    # Right ----------------------- #
                    elif event.key == entity_manager.player.controls["Right"]:
                        entity_manager.player.moving["Right"] = False