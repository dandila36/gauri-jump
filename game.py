import pygame
import sys
import asyncio
import random
import Assets.colours as colours
from random import choice, randint
from math import sqrt

from Sprites.tile import Tile, MovingTile, BrokenTile, DisappearingTile, ShiftingTile, MoveableTile, ExplodingTile
from Buttons.pause import PauseButton
from Buttons.resume import ResumeButton
from Buttons.play import PlayButton
from Buttons.options import OptionButton
from Buttons.play_again import PlayAgain
from Buttons.menu import MenuButton

from Sprites.player import Player
from Sprites.menu_player import MenuPlayer
from Sprites.monster import Monster
from Sprites.blackhole import Blackhole
from Sprites.ufo import UFO
from Sprites.character_selector import CharacterSelector

import texture

class Game:

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 900
    CENTER_X = SCREEN_WIDTH // 2
    CENTER_Y = SCREEN_HEIGHT // 2
    GRAVITY = 0.4 
    JUMP_STRENGTH = -15  
    
    # Remove class-level pygame calls - these will be initialized in __init__
    screen = None
    
    # Image placeholders - will be loaded in __init__
    MAIN_MENU_IMAGE = None
    BACKGROUND_IMAGE = None
    OPTIONS_IMAGE = None
    PLAY_GAME_IMAGE = None
    TOP_SHEET = None
    TOP_IMAGE = None
    END_GAME_SPRITE_SHEET = None
    GAME_OVER_TEXT_IMAGE = None
    GAME_OVER_TEXT_IMAGE_x = None
    END_GAME_BOTTOM_IMAGE = None
    END_GAME_BOTTOM_IMAGE_Y = None
    YOUR_SCORE_IMAGE = None
    YOUR_SCORE_IMAGE_width = None
    YOUR_SCORE_IMAGE_height = None
    YOUR_SCORE_IMAGE_x = None
    YOUR_SCORE_IMAGE_y = None
    YOUR_HIGH_SCORE_IMAGE = None
    YOUR_HIGH_SCORE_IMAGE_width = None
    YOUR_HIGH_SCORE_IMAGE_height = None
    YOUR_HIGH_SCORE_IMAGE_x = None
    YOUR_HIGH_SCORE_IMAGE_y = None
    END_GAME_IMAGES = None
    clock = None

    def __init__(self):
        #Game States
        self.running = True
        self.character_select = False  # Character selection comes after play button
        self.main_menu = True         # Start with main menu
        self.options_menu = False
        self.play_game = False
        self.end_game = False
        
        # Character selection variables
        self.selected_character_file = "doodler.png"  # Default character
        self.selected_character_name = "F*** Ass Bob Gauri"

        # Initialize pygame (this might be called twice, but that's okay)
        pygame.init()
        
        # Initialize display and images AFTER pygame is initialized
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        Game.screen = self.screen  # Set class variable for compatibility
        
        # Load all images after pygame is initialized
        try:
            self.MAIN_MENU_IMAGE = pygame.image.load("Assets/Images/Backgrounds/main_menu.png").convert_alpha()
            self.BACKGROUND_IMAGE = self.MAIN_MENU_IMAGE
            Game.MAIN_MENU_IMAGE = self.MAIN_MENU_IMAGE
            Game.BACKGROUND_IMAGE = self.BACKGROUND_IMAGE
            
            self.OPTIONS_IMAGE = pygame.image.load("Assets/Images/Backgrounds/options.png").convert_alpha()
            Game.OPTIONS_IMAGE = self.OPTIONS_IMAGE
            
            self.PLAY_GAME_IMAGE = pygame.image.load(f"Assets/Images/Backgrounds/Backgrounds/{texture.file_name}.png")
            Game.PLAY_GAME_IMAGE = self.PLAY_GAME_IMAGE
            
            # TOP IMAGES
            self.TOP_SHEET = pygame.image.load(f"Assets/Images/Backgrounds/Tops/{texture.file_name}.png")
            self.TOP_IMAGE = self.TOP_SHEET.subsurface(pygame.Rect(0, 0, 640, 92))
            Game.TOP_SHEET = self.TOP_SHEET
            Game.TOP_IMAGE = self.TOP_IMAGE
            
            # END GAME IMAGES
            self.END_GAME_SPRITE_SHEET = pygame.image.load("Assets/Images/start-end-tiles.png")
            Game.END_GAME_SPRITE_SHEET = self.END_GAME_SPRITE_SHEET
            
            self.GAME_OVER_TEXT_IMAGE = self.END_GAME_SPRITE_SHEET.subsurface(pygame.Rect(2, 209, 433, 157))
            self.GAME_OVER_TEXT_IMAGE_x = self.CENTER_X - (self.GAME_OVER_TEXT_IMAGE.get_width() // 2)
            Game.GAME_OVER_TEXT_IMAGE = self.GAME_OVER_TEXT_IMAGE
            Game.GAME_OVER_TEXT_IMAGE_x = self.GAME_OVER_TEXT_IMAGE_x
            
            self.END_GAME_BOTTOM_IMAGE = pygame.image.load(f"Assets/Images/Backgrounds/Bottoms/{texture.file_name}.png")
            self.END_GAME_BOTTOM_IMAGE_Y = self.SCREEN_HEIGHT - self.END_GAME_BOTTOM_IMAGE.get_height()
            Game.END_GAME_BOTTOM_IMAGE = self.END_GAME_BOTTOM_IMAGE
            Game.END_GAME_BOTTOM_IMAGE_Y = self.END_GAME_BOTTOM_IMAGE_Y
            
            self.YOUR_SCORE_IMAGE = self.END_GAME_SPRITE_SHEET.subsurface(pygame.Rect(795, 339, 218, 40))
            self.YOUR_SCORE_IMAGE_width, self.YOUR_SCORE_IMAGE_height = self.YOUR_SCORE_IMAGE.get_size()
            self.YOUR_SCORE_IMAGE_x = (self.SCREEN_WIDTH - self.YOUR_SCORE_IMAGE_width) // 2
            self.YOUR_SCORE_IMAGE_y = (self.SCREEN_HEIGHT - self.YOUR_SCORE_IMAGE_height) // 2
            Game.YOUR_SCORE_IMAGE = self.YOUR_SCORE_IMAGE
            Game.YOUR_SCORE_IMAGE_width = self.YOUR_SCORE_IMAGE_width
            Game.YOUR_SCORE_IMAGE_height = self.YOUR_SCORE_IMAGE_height
            Game.YOUR_SCORE_IMAGE_x = self.YOUR_SCORE_IMAGE_x
            Game.YOUR_SCORE_IMAGE_y = self.YOUR_SCORE_IMAGE_y
            
            self.YOUR_HIGH_SCORE_IMAGE = self.END_GAME_SPRITE_SHEET.subsurface(pygame.Rect(677, 393, 310, 56))
            self.YOUR_HIGH_SCORE_IMAGE_width, self.YOUR_HIGH_SCORE_IMAGE_height = self.YOUR_HIGH_SCORE_IMAGE.get_size()
            self.YOUR_HIGH_SCORE_IMAGE_x = (self.SCREEN_WIDTH - self.YOUR_HIGH_SCORE_IMAGE_width) // 2
            self.YOUR_HIGH_SCORE_IMAGE_y = (self.SCREEN_HEIGHT - self.YOUR_HIGH_SCORE_IMAGE_height) // 2
            Game.YOUR_HIGH_SCORE_IMAGE = self.YOUR_HIGH_SCORE_IMAGE
            Game.YOUR_HIGH_SCORE_IMAGE_width = self.YOUR_HIGH_SCORE_IMAGE_width
            Game.YOUR_HIGH_SCORE_IMAGE_height = self.YOUR_HIGH_SCORE_IMAGE_height
            Game.YOUR_HIGH_SCORE_IMAGE_x = self.YOUR_HIGH_SCORE_IMAGE_x
            Game.YOUR_HIGH_SCORE_IMAGE_y = self.YOUR_HIGH_SCORE_IMAGE_y
            
            self.END_GAME_IMAGES = (self.YOUR_SCORE_IMAGE, self.YOUR_HIGH_SCORE_IMAGE)
            Game.END_GAME_IMAGES = self.END_GAME_IMAGES
            
            print("✅ All images loaded successfully for web")
            
        except Exception as e:
            print(f"❌ Error loading images: {e}")
            # Create fallback colored surfaces if images fail to load
            self.MAIN_MENU_IMAGE = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.MAIN_MENU_IMAGE.fill((100, 150, 200))
            self.BACKGROUND_IMAGE = self.MAIN_MENU_IMAGE
            
        pygame.display.set_caption("Gauri Jump")
        self.clock = pygame.time.Clock()
        Game.clock = self.clock

        #Sprite Groups
        self.platforms = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.blackholes = pygame.sprite.Group()
        self.UFOs = pygame.sprite.Group()
        
        #Sprite groups in joined list form
        self.all_enemies = [self.monsters, self.blackholes, self.UFOs]
        self.platforms

        #List of objects that are used in generation/spawning
        self.tile_objects = [Tile, MovingTile, ShiftingTile, MoveableTile, DisappearingTile, BrokenTile, ExplodingTile]
        self.enemy_objects = [Monster, Blackhole, UFO]

        #Quadrant variables to ensure spawning is done evenly such that the player always has a tile to jump to.
        self.quadrants = ("Q1", "Q2", "Q3", "Q4")
        self.quadrant_idx = 0

        #self explanatory
        self.fade_out_speed = 3
        self.fade_out_alpha = 255

        self.score_font = pygame.font.Font(None, 50)

        self.frame = 0
        
        # Initialize character selector
        self.character_selector = CharacterSelector(self)
        
        # Initialize title font for main menu
        try:
            self.title_font = pygame.font.Font("Assets/Fonts/DoodleJump.ttf", 84)
        except:
            self.title_font = pygame.font.Font(None, 84)
    
        # Initialize main menu objects since we start with main menu now
        self.initialise_main_menu_objects()

    """Initialise/Reinitialise Functions"""
    def initialise_main_menu_objects(self):
        """
        This function generates all the objects associated with the main menu
        """
        self.player = MenuPlayer(self, 110, 750)

        self.platforms.add(Tile(self, 115, 763))
        self.UFOs.add(UFO(self, x=450, y=200))
        
        self.play_button = PlayButton(self)
        self.options_button = OptionButton(self)
        self.main_menu_button = MenuButton(self, x=None, y=200)

    def initialise_game_objects(self):
        """
        This function generates all the objects associated with playing the game itself
        """
        Tile.total = 0
        self.clear_all_sprites()

        self.resume_button = ResumeButton(self)
        self.pause_button = PauseButton(self)
        self.play_again_button = PlayAgain(self)
        self.main_menu_button = MenuButton(self, x_multiplier=1.75, y_multiplier=1.5)

        self.player = Player(self, self.CENTER_X, self.CENTER_Y)
        self.generate_n_tiles(n=25, top=False)
    
    def initialise_game_weights(self):
        """
        This function initialises the game weights for enemy and tile spawning. 
        It must be reset for every game instance.
        """
        self.max_tile_number = 25
        self.tile_weights = [9999999, 5, 5, 1, 5, 5, 5] 

        self.max_enemy_number = 1
        self.enemy_weight = 0.001

    """Generator Functions """
    def generate_random_tile(self):
        """
        This function ensures there are always n_max random tiles on the screen
        if two are destroyed and max_tile_number = 25
        Tile.total = 23
        this function will generate two random tiles depending on the set weights.
        """
        while Tile.total <= self.max_tile_number:
            tile = random.choices(population=self.tile_objects, weights=self.tile_weights)[0]
            self.generate_n_tiles(top=True, tile_type=tile)

    def generate_random_enemy(self):
        """
        This function will attempt to generate an enemy based on the probability weight insofar as 
        the total number of enemies is less than the maximum boundary set (max_enemy_number)"""
        if len(self.all_enemies) < self.max_enemy_number and not self.player.paused:
            enemy = random.choices(population=self.enemy_objects + [None], weights=[self.enemy_weight, self.enemy_weight, self.enemy_weight, 100])[0]
            if enemy is None:
                pass
            elif enemy is Monster:
                self.monsters.add(enemy(self))
            elif enemy is Blackhole:
                self.blackholes.add(enemy(self))   
            elif enemy is UFO:
                self.UFOs.add(enemy(self))
            
    def generate_n_tiles(self, n=1, top=False, tile_type=Tile):
        """
        This rather beefy function ensures that the spawning of n tiles:
        - does not overlap with other sprites
        - does not spawn such that its sides go off screen
        - the player always has a tile to jump on (spawning in quadrants) 

        To ensure the tiles are evenly spaced and that the player has something to jump on
        the tiles are spawned in quadrants of the square screen:
        I ---- I ---- I
        I      I      I
        I  Q1  I  Q2  I
        I      I      I
        I ---- I ---- I
        I      I      I
        I  Q3  I  Q4  I
        I      I      I
        I ---- I ---- I
        By doing this we ensure the tiles are not just interspersed randomly everywhere over the screen but in segments (quadrants)
        """
        def get_quadrant_range(quadrant):
            match quadrant:
                case "Q1":
                    return ((0, 320),   (0, 450))
                case "Q2":
                    return ((320, 640), (0, 450))
                case "Q3":
                    return ((0, 320),   (450, 900))
                case "Q4":
                    return ((320, 640), (450, 900))
        def get_random_quadrant_coordinates():
            current_quadrant = self.quadrants[self.quadrant_idx % 4]
            x_range, y_range = get_quadrant_range(current_quadrant)
            x_lower, x_higher = x_range
            y_lower, y_higher = y_range
            
            x_lower_bound = 0
            x_upper_bound = 0
            y_lower_bound = 0
            y_upper_bound = 0

            match current_quadrant:
                case "Q1":
                    x_lower_bound = 60
                    y_lower_bound = 20
                case "Q2":
                    x_upper_bound = -60
                    y_lower_bound = 20
                case "Q3":
                    x_lower_bound = 60
                    y_upper_bound = -20
          
                case "Q4":
                    x_upper_bound = -60
                    y_upper_bound = -20
            
                
            x = randint(x_lower + x_lower_bound, x_higher + x_upper_bound)
            y = (randint((y_lower  - y_lower_bound -  900), 
                         (y_higher  - y_upper_bound - 900)))
        
            return (x, y)

        for _ in range(n):
            valid = False
            while not valid:
                valid = True
                x, y = get_random_quadrant_coordinates() if top else (randint(65, self.SCREEN_WIDTH-65), randint(-450, self.SCREEN_HEIGHT-25)) 
                new_platform = pygame.Rect(x, y, 60, 20)
                center1 = new_platform.center

                for sprite in (self.platforms.sprites() + self.all_enemies):
                    center2 = sprite.rect.center
                    distance = sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)

                    if new_platform.colliderect(sprite.rect) or distance < 120:
                        valid = False
                        break

            tile_type(self, x, y)
            self.quadrant_idx += 1


    def clear_all_sprites(self):
        self.platforms.empty()
        self.bullets.empty()
        self.monsters.empty()
        self.blackholes.empty()
        self.UFOs.empty()
    
    def draw_main_menu_title(self):
        """Cross out 'Doodle Jump' and put 'Gauri Jump' below"""
        
        # Cross out the original "Doodle Jump" text with thick red lines
        # The original title is roughly at y=100-140, centered around x=320
        original_title_y = 120
        line_thickness = 6
        
        # Draw multiple thick red lines to cross out "Doodle Jump"
        for i in range(line_thickness):
            # Diagonal line from top-left to bottom-right
            pygame.draw.line(self.screen, colours.RED, 
                           (180, original_title_y - 25 + i), 
                           (460, original_title_y + 25 + i), 4)
            # Diagonal line from top-right to bottom-left  
            pygame.draw.line(self.screen, colours.RED,
                           (460, original_title_y - 25 + i),
                           (180, original_title_y + 25 + i), 4)
        
        # Draw "Gauri Jump" below the crossed out text
        title_text = "Gauri Jump"
        title_x = self.CENTER_X
        title_y = 130  # Below the crossed out text
        
        # Draw white outline for better visibility
        outline_positions = [(-2, -2), (-2, 2), (2, -2), (2, 2), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for offset_x, offset_y in outline_positions:
            outline_surface = self.title_font.render(title_text, True, colours.WHITE)
            outline_rect = outline_surface.get_rect(center=(title_x + offset_x, title_y + offset_y))
            self.screen.blit(outline_surface, outline_rect)
        
        # Draw main title text
        title_surface = self.title_font.render(title_text, True, colours.BLACK)
        title_rect = title_surface.get_rect(center=(title_x, title_y))
        self.screen.blit(title_surface, title_rect)
        

    """
    Drawing functions
    """
    def draw_top(self):
        self.screen.blit(self.TOP_IMAGE, (0, 0))

        # Draw score with thick white outline for maximum visibility
        score_str = str(int(self.player.score))
        
        # Position score further from top edge to avoid cutoff
        score_x, score_y = 50, 50
        
        # Draw thick white outline (more positions for thicker outline)
        outline_positions = [
            (-3, -3), (-3, 0), (-3, 3),
            (0, -3), (0, 3),
            (3, -3), (3, 0), (3, 3),
            (-2, -2), (-2, 2), (2, -2), (2, 2),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for offset_x, offset_y in outline_positions:
            outline_text = self.score_font.render(score_str, True, colours.WHITE)
            self.screen.blit(outline_text, (score_x + offset_x, score_y + offset_y))
        
        # Draw main score text
        score_text = self.score_font.render(score_str, True, colours.BLACK)
        self.screen.blit(score_text, (score_x, score_y))

        self.pause_button.draw(self.screen)
        self.resume_button.draw(self.screen)
        
    def draw_end_game_screen(self):
        self.draw_top()

        score = self.score_font.render(str(int(self.player.score)), True, colours.BLACK)
        score_x = (self.SCREEN_WIDTH - score.get_width()) // 2

        high_score = self.score_font.render(str(int(Player.high_score)), True, colours.BLACK)  
        high_score_x = self.CENTER_X - (high_score.get_width() // 2)

        self.screen.blit(score,      (score_x,      (self.CENTER_Y * 0.826)))
        self.screen.blit(high_score, (high_score_x, (self.CENTER_Y * 1.13)))
        
        self.screen.blit(self.YOUR_SCORE_IMAGE,      (self.YOUR_SCORE_IMAGE_x,       self.CENTER_Y * 0.7))
        self.screen.blit(self.YOUR_HIGH_SCORE_IMAGE, (self.YOUR_HIGH_SCORE_IMAGE_x, (self.CENTER_Y * 0.95)))
        self.screen.blit(self.GAME_OVER_TEXT_IMAGE, (self.GAME_OVER_TEXT_IMAGE_x, 140))

        # Sweet message from Abhi - positioned between high score number and buttons
        love_message = "Abhi Still Loves You!"
        love_y = self.CENTER_Y * 1.18  # Between high score number (1.13) and buttons
        
        # Draw white outline for the love message using DoodleJump font
        outline_positions = [(-2, -2), (-2, 2), (2, -2), (2, 2), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for offset_x, offset_y in outline_positions:
            outline_text = self.title_font.render(love_message, True, colours.WHITE)
            outline_x = self.CENTER_X - (outline_text.get_width() // 2)
            self.screen.blit(outline_text, (outline_x + offset_x, love_y + offset_y))
        
        # Draw main love message text in DoodleJump font
        love_text = self.title_font.render(love_message, True, colours.RED)
        love_x = self.CENTER_X - (love_text.get_width() // 2)
        self.screen.blit(love_text, (love_x, love_y))

        self.play_again_button.draw(self.screen)
        self.main_menu_button.draw(self.screen)

    """
    Main game loop functions
    
    For each of the three functions there are 3 games states that comprise the entire game:
    - main_menu
    - play_game
    - end_game
    
    Each function comrpises the games elements for that given state.
    For example:
    The main menu state will contain all objects that are relevant to the main menu.
    Such as the play and options buttons as well as the unmovable player and the ufo in the top right.

    The handle events function will handle all events made by the player for the objects of that given state
    highlighting over the play button is a user event and causes the button image to change (highlight image)

    The update function updates all objects for every frame of the game running.
    For example for each frame the player is affected by gravity and his y coordinate should be updated for every frame 

    The draw functions simply blits to the screen the associated images/shapes for these objects
    For example the play button image, the player image 
    """
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.character_select:
                self.character_selector.handle_events(event)
                
            elif self.main_menu:
                self.play_button.handle_events(event)
                self.options_button.handle_events(event)
                
                if self.options_menu:
                    self.main_menu_button.handle_events(event)

            elif self.play_game:
                self.pause_button.handle_events(event)
                self.resume_button.handle_events(event)
                self.player.handle_events(event)
                
                for platform in self.platforms:
                    platform.handle_events(event)
            
            elif self.end_game:
                self.play_again_button.handle_events(event)
                self.main_menu_button.handle_events(event)
    
    def update(self):

        if self.character_select:
            # Character selection doesn't need updates
            pass
            
        elif self.main_menu:
            self.player.update()
            self.platforms.update()
            self.UFOs.update()
            
            self.play_button.update()
            self.options_button.update()
            if self.options_menu: self.main_menu_button.update()

        elif self.play_game:
 
            self.generate_random_tile()
            self.generate_random_enemy()

            self.bullets.update()
            self.platforms.update()
            self.player.update()
            self.monsters.update()
            self.blackholes.update()
            self.UFOs.update()

        elif self.end_game:
            self.play_again_button.update()
            self.main_menu_button.update()
        
    def draw(self):
        if self.character_select:
            self.character_selector.draw(self.screen)
        else:
            self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

        if self.main_menu:

            if not self.options_menu:        
                self.play_button.draw(self.screen)
          
            self.options_button.draw(self.screen)
            
            self.player.draw(self.screen)
            self.UFOs.draw(self.screen)
            for platform in self.platforms:
                platform.draw(self.screen)

        
            if self.options_menu:
                self.main_menu_button.draw(self.screen)
            
            # Draw "Gauri Jump" title overlay (only when not in options menu)
            if not self.options_menu:
                self.draw_main_menu_title()
            
        if self.play_game:

            self.bullets.draw(self.screen)
            self.player.draw(self.screen)
            
            for platform in self.platforms:
                platform.draw(self.screen)

            for enemy in self.all_enemies:
                enemy.draw(self.screen)

            self.draw_top()
            
        if self.end_game:
            
            """
            Only once all the sprites have faded do we end the 'play_game' state 
            This line of code saves having to redraw every sprite in the 'end_game' condition
            Instead we simply end the play_game state when their alpha is at 0, i.e. are inivisible.
            """
            if self.fade_out_alpha == 0:
                self.play_game = False
                self.draw_end_game_screen()
                pygame.mixer.stop()     
            
            if self.fade_out_alpha != 0:
                self.fade_out_alpha -= self.fade_out_speed

            #If the player falls to the bottom we want to draw the bottom image to demonstrate falling into the abyss
            if not self.player.dead_by_suction:
                self.screen.blit(self.END_GAME_BOTTOM_IMAGE, (0, self.END_GAME_BOTTOM_IMAGE_Y))

        pygame.display.flip()        

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.frame += 1
            self.clock.tick(60)
        pygame.quit()
        sys.exit()
    
    async def run_web(self):
        """Web-compatible run method for pygbag"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.frame += 1
            self.clock.tick(60)
            await asyncio.sleep(0)  # Essential for web compatibility
        pygame.quit()



    """
    These two class methods are specifically used to update images based on the current texture pack selected
    """
    @classmethod
    def update_top_images(cls):
        cls.TOP_SHEET = pygame.image.load(f"Assets/Images/Backgrounds/Tops/{texture.file_name}.png")
        cls.TOP_IMAGE =  cls.TOP_SHEET.subsurface(pygame.Rect(0, 0, 640, 92))

    @classmethod
    def update_bottom_images(cls):
        cls.END_GAME_BOTTOM_IMAGE = pygame.image.load(f"Assets/Images/Backgrounds/Bottoms/{texture.file_name}.png")
        cls.END_GAME_BOTTOM_IMAGE_Y = cls.SCREEN_HEIGHT - cls.END_GAME_BOTTOM_IMAGE.get_height()



    """"
    Properties getter/setters to access all the sprite groups for either platforms or enemies
    This really just saves having to write 
    for group in self.all_x:
        for x in group.sprites():
            ...
    instead we can just write 
    for x in all_x:
        ...
    """
    @property
    def all_enemies(self):
        return [enemy for group in self._all_enemies for enemy in group.sprites()]
    
    @all_enemies.setter
    def all_enemies(self, value):
        self._all_enemies = value


    
    
