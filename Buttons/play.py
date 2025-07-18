import Assets.sounds as sounds
import pygame
import texture

class PlayButton:
    def __init__(self, game):
        self.game       = game
        self.player     = game.player
        self.CENTER_X   = game.CENTER_X
        self.CENTER_Y   = game.CENTER_Y

        self.image = pygame.image.load("Assets/Images/Buttons/play.png")
        self.hover_image = pygame.image.load("Assets/Images/Buttons/play_hover.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 200

        self.hovering = False
        self.clicked = False
        self.hide = False
        
    def handle_events(self, event):
        if not self.hide:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    self.clicked = True

            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
                self.clicked = False
                self.hide = True

                #Game State change - go to character selection first
                self.game.main_menu = False
                self.game.character_select = True

                #Background changed
                self.game.BACKGROUND_IMAGE = pygame.image.load(f"Assets/Images/Backgrounds/Backgrounds/{texture.file_name}.png")
                
                #Remove the main menu UFO    
                self.game.UFOs.sprites()[0].remove()
            
                # Don't initialize game objects yet - wait for character selection
                # self.game.initialise_game_weights()
                # self.game.initialise_game_objects()

                sounds.button.play()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hovering = True
        else:
            self.hovering = False

    def draw(self, screen):
        if not self.hide:
            if self.hovering:
                screen.blit(self.hover_image, (self.rect.x, self.rect.y))
            else:
                screen.blit(self.image, (self.rect.x, self.rect.y))
