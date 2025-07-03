"""
GAURI JUMP - CUSTOM CHARACTER SETUP
====================================

To use your custom doodler character:
1. Save your character image as "doodler.png" in the Assets/ folder
2. The image will be automatically scaled to 50x60 pixels (adjust in code if needed)
3. The character will flip left/right and tilt when moving
4. Collision detection uses a tighter box around the character's body

If doodler.png is not found, the game will fall back to the original texture system.
"""

import Assets.sounds as sounds
import pygame
import texture
import os

from pygame.locals import *
from random import choice, randint
from Sprites.Power_ups.jetpack import Jetpack
from Sprites.Power_ups.propeller import Propeller
from Sprites.Power_ups.spring_shoes import SpringShoes
from Sprites.blackhole import Blackhole
from Sprites.ufo import UFO

class Player(pygame.sprite.Sprite):

    high_score = 0

    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
    
        self.CENTER_X       = game.CENTER_X
        self.CENTER_Y       = game.CENTER_Y
        self.SCREEN_HEIGHT  = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH   = game.SCREEN_WIDTH
        self.GRAVITY        = game.GRAVITY
        self.JUMP_STRENGTH  = game.JUMP_STRENGTH
        self.platforms      = game.platforms
        self.enemies        = game.all_enemies

        self.default_x = self.x = x
        self.default_y = self.y = -900
        self.previous_y_difference = int(self.y - self.CENTER_Y)
        self.d = 1

        #####
        # Player Images - New Doodler Character
        # Try to load custom character image, fall back to original system if not found
        character_file = getattr(game, 'selected_character_file', 'doodler.png')
        character_path = f"Assets/{character_file}"
        self.using_custom_doodler = os.path.exists(character_path)
        
        if self.using_custom_doodler:
            try:
                # Use the selected character file from the game
                character_file = getattr(game, 'selected_character_file', 'doodler.png')
                character_path = f"Assets/{character_file}"
                
                # Load the selected character image and create scaled versions
                self.base_doodler_img = pygame.image.load(character_path).convert_alpha()
                self.doodler_size = (50, 60)  # Adjust size as needed
                
                # Create base images (right-facing)
                self.right_image = pygame.transform.scale(self.base_doodler_img, self.doodler_size)
                self.right_jump_image = self.right_image  # Same image for jumping
                self.shoot_image = self.right_image  # Same image for shooting
                self.shoot_jump_image = self.right_image  # Same image for shoot+jump
                
                # Create left-facing images (flipped)
                self.left_image = pygame.transform.flip(self.right_image, True, False)
                self.left_jump_image = self.left_image
                
                print("✓ Custom doodler character loaded successfully!")
                
            except Exception as e:
                print(f"⚠ Error loading custom doodler: {e}")
                print("Falling back to original texture system...")
                self.using_custom_doodler = False
                
        if not self.using_custom_doodler:
            # Fall back to original texture-based system
            self.left_image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/left.png").convert_alpha()
            self.left_jump_image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/left_jump.png").convert_alpha()
            self.right_image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/right.png").convert_alpha()
            self.right_jump_image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/right_jump.png").convert_alpha()
            self.shoot_image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/shoot.png").convert_alpha()
            self.shoot_jump_image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/shoot_jump.png").convert_alpha()
        

        
        # Current image state
        self.prior_image = self.image = self.right_image
        self.current_tilt = 0  # For tilt animation
        self.is_tilted = False
        #####
        
        self.image_scale = 1
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, game.CENTER_Y)
        
        # Adjust collision rect to be tighter around the character's body/feet
        # Reduce width and height slightly for better collision detection
        self.collision_rect = pygame.Rect(0, 0, int(self.rect.width * 0.7), int(self.rect.height * 0.8))
        self.collision_rect.centerx = self.rect.centerx
        self.collision_rect.bottom = self.rect.bottom - 5  # Align with feet
        
        #####
        # Knocked out Images
        self.stars_1 = pygame.image.load("Assets/Images/Animations/Stars/1.png").convert_alpha()
        self.stars_2 = pygame.image.load("Assets/Images/Animations/Stars/2.png").convert_alpha()
        self.stars_3 = pygame.image.load("Assets/Images/Animations/Stars/3.png").convert_alpha()
        self.stars_location = (self.rect.x, self.rect.top-10)
        self.knocked_out_animation = [self.stars_1,  self.stars_2,  self.stars_3]
        #####
        
        self.speed = 5 
        self.movement_speed = 1
        self.end_game_y = 840
        self.prior_y_velocity = 0
        self.velocity_y = 0
        self.score = 0
        self.spring_shoe_jump_count = 0

        #####
        # Player states
        self.using_spring_shoes = False
        self.using_jetpack = False
        self.using_propeller = False
        self.using_trampoline = False
        self.using_spring = False
    
        self.left = False
        self.right = True
        self.suction_object_collided_with = None
        self.suction_object_collision = False
        self.dead_by_suction = False
        self.dead = False

        self.spring_collision = False
        self.trampoline_collision = False
        
   
        self.jumping = False
        self.falling = False
        self.fall_checked = False
        self.paused = False
        self.knocked_out = False
        self.handling_events = True
        self.collision = False
        self.draw_player = True

    """
    I have structured this class in the typical pattern for a pygame object, i.e.
    - Handle_events
    - update
    - draw

    In the second and third case I place below the two functions all associated functions related to it
    """


    def handle_events(self, event):
        if not self.paused and not self.is_flying() and not self.dead:
            if ((event.type == KEYDOWN and event.key in (K_SPACE, K_UP)) or 
                (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)):
                self.shoot() #We only want to shoot once for every key press

    """
    ------------------------------------------
    UPDATE AND ASSOCIATED UPDATE METHODS BELOW
    ------------------------------------------
    """   
    def update(self):
       
        "when the player is sucked into another sprite the player is paused so no other movement but the suck fuction takes place"
        if not self.paused: 
            self.update_movement()
            self.update_position_based_on_gravity()
            self.update_directional_image()
            self.update_score()
            self.update_spawning_properties()
            
            self.fall_check()
            self.y_boundary_check()
            self.x_boundary_check()
            self.spring_shoe_check()

            self.update_rect()
            self.update_other_sprites_based_upon_player_jump_difference()
        
        elif self.suction_object_collision:
            self.suck_player_to_center_of_object()
        
    def update_movement(self):
        """
        This function updates the movement of the player based on what key they input.
        For example if the user pressed <- the player moves left
        the same is true for ->

        When the user presses 
        - SPACE_BAR
        - UP
        - LEFT MOUSE CLICK
        the player shoots

        This function however handles any key that is held continuously whereas the handling_events function only handles a single event 
        """
        if self.handling_events and not self.dead:
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()
            
            if keys[K_LEFT]:
                self.move_left()
            if keys[K_RIGHT]:
                self.move_right()
            if (keys[K_SPACE] or keys[K_UP] or mouse_buttons[0]) and not self.is_flying():
                #We do not want to shoot continusly otherwise the player could just continuously hold it
                self.prior_image = self.image = self.shoot_image 
    def update_position_based_on_gravity(self):
        """
        This function updates the player based upon gravity
        the y velocity that the player travels is influenced by gravity.
        """
        self.velocity_y += self.GRAVITY
        self.y += self.velocity_y

        #Gravity update
        #Once they have reached the peak jump height for the given jump_strength
        if (self.velocity_y > self.GRAVITY) and not self.falling:  
            #When velocity y is positive we're going down the screen (falling)
            
            self.end_game_y = self.y + 450 + self.image.get_height() + 40 #How far the player has to fall from the new peak height
            
            #Game state changes
            self.using_jetpack = False
            self.using_propeller = False
            self.using_trampoline = False
            self.using_spring = False
            
            self.falling = True 
            self.jumping = False
        elif (self.velocity_y < self.GRAVITY): 
            #While velocity_y is negative we're jumping, going up the screen
            self.falling = False
            self.jumping = True

    def update_directional_image(self): 
        """
        Alter images depending on whether the sprite is jumping, else revert to default
        Also handle tilt animation reset when not actively moving (for custom doodler)
        """
        if self.using_custom_doodler:
            # Custom doodler behavior with tilt animation
            keys = pygame.key.get_pressed()
            is_moving = keys[K_LEFT] or keys[K_RIGHT]
            
            # Reset tilt if not moving
            if not is_moving and self.is_tilted:
                self.is_tilted = False
                self.current_tilt = 0
                if self.left:
                    self.prior_image = self.image = self.left_image
                else:
                    self.prior_image = self.image = self.right_image
            
            # Handle jumping state (for custom doodler, jumping doesn't change the image much)
            if self.jumping:
                # Keep current image but ensure it's properly oriented
                if self.left and not self.is_tilted:
                    self.image = self.left_jump_image
                elif not self.left and not self.is_tilted:
                    self.image = self.right_jump_image
                # If tilted, keep the tilted image
            else:
                # When not jumping, revert to appropriate directional image
                if not self.is_tilted:
                    self.image = self.prior_image
        else:
            # Original texture-based behavior
            if self.jumping:
                if self.image == self.left_image:
                    self.image = self.left_jump_image
                elif self.image == self.right_image:
                    self.image = self.right_jump_image
                elif self.image == self.shoot_image:
                    self.image = self.shoot_jump_image
            else:
                self.image = self.prior_image
    def update_score(self):
        """
        Everytime the player goes past the midline point the score increases
        """
        if self.y < -900:
            self.score = max(self.score, abs(self.y) - 900) 
        Player.high_score = max(Player.high_score, self.score)
    def update_spawning_properties(self):
        """
        For every time the player hits a tile (game.frame == 0 as it is reset) the game spawning rates are changed depending on the score (height)
        Gradually increases difficulty but keeps it manageable and fair
        """
        if self.game.frame == 0:
            # Start with enemies appearing every ~30 seconds, then scale up
            base_enemy_weight = 0.02  # Much higher base rate for ~30 second intervals
            score_multiplier = self.score / 5000  # Faster scaling
            self.game.enemy_weight = min(base_enemy_weight + score_multiplier, 1.0)  # Higher cap for more action
            
            # Progressive tile difficulty scaling
            if self.score > 2000:
                # Start introducing more challenging tiles after score 2000  
                self.game.tile_weights[0] = max(500, 9999999 - (self.score * 1))  
            
            if self.score > 5000:
                # More special tiles but keep it reasonable
                self.game.tile_weights = [max(300, 9999999 - (self.score * 2)), 8, 8, 2, 8, 2, 50]
                
            if self.score > 12000:
                # Moderate difficulty increase
                self.game.tile_weights = [max(150, 9999999 - (self.score * 3)), 10, 10, 3, 10, 3, 35]
                
            if self.score > 25000:
                # Second enemy can appear
                self.game.max_enemy_number = 2
                self.game.tile_weights = [max(75, 9999999 - (self.score * 4)), 12, 12, 4, 12, 4, 25]
            
            if self.score > 50000:
                # Higher difficulty but still manageable
                self.game.tile_weights = [max(50, 9999999 - (self.score * 5)), 15, 15, 5, 15, 5, 15]
                
            if self.score > 75000:
                # Maximum difficulty - 3 enemies possible
                self.game.max_enemy_number = 3
                self.game.tile_weights = [max(30, 200), 18, 18, 6, 18, 6, 10] 
            
    def fall_check(self):
        """
        When the play reaches the end_game_y it means that they have fallen of the map
        When this happens we need to move all enemies and platforms such that they give the appeareance of moving whilst
        the player is in the middle of the screen
        """
        if self.y >= self.end_game_y and not self.fall_checked:

            if self.y < 390:
                difference = abs(self.y) - 900 
                self.y = -900
                
                for platform in self.platforms:
                    platform.rect.y += difference
                    if platform.power_up:
                        platform.power_up.rect.y += difference

                for enemy in self.game.all_enemies:
                    enemy.rect.y += difference
           
            sounds.fall.play()     
            self.fall_checked = True

    def y_boundary_check(self):
        """
        When the player has touched the bottom of the screen we transition to the end_game_state
        """
        if self.rect.top >= 900:
            self.rect.y = 900
            self.velocity_y = 0
            self.dead = True
            self.game.end_game = True   
    def x_boundary_check(self):
        """This function simply ensures the player does not disappear when they go outside the bounds.
        If they do they reappear on the opposite side"""
        if self.x > self.SCREEN_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = self.SCREEN_WIDTH
    def spring_shoe_check(self):
        """
        This function ensures that the player only uses the springshoes for 5 jumps
        when it is finished the jump strength is return back to the original
        """
        if self.using_spring_shoes and self.spring_shoe_jump_count % 5 == 0:
            self.JUMP_STRENGTH = self.game.JUMP_STRENGTH
            self.using_spring_shoes = False
    
    def update_rect(self):
        """
        Based on every single change previously the player rectangle is finally updated
        """
        self.rect.center = (self.x, self.y)
        # Update collision rect to follow the main rect
        self.collision_rect.centerx = self.rect.centerx
        self.collision_rect.bottom = self.rect.bottom - 5    
    def update_other_sprites_based_upon_player_jump_difference(self):
        """
        When the player moves over the halfway point the difference the player would go based upon the  
        worked out and each sprite is moved by this difference
        """
        if (self.y < self.CENTER_Y - self.rect.height):
           
            difference = int((self.y - self.CENTER_Y) - self.previous_y_difference)
            self.previous_y_difference = int(self.y - self.CENTER_Y) 
            
            for platform in self.platforms:
                platform.rect.y -= difference
                if platform.power_up:
                    platform.power_up.rect.y -= difference

            for enemy in self.game.all_enemies:
                enemy.rect.y -= difference

            self.rect.y = (self.SCREEN_HEIGHT // 2 - self.rect.height)
            
    def suck_player_to_center_of_object(self):
        """
        This function moves the player's coordinates gradually to the suction object that has absorbed it
        """
        def resize_image(scale):
            return pygame.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height * scale)))

        
        suction_location = (self.suction_object_collided_with.rect.centerx, 
                            self.suction_object_collided_with.rect.centery)
      
        if self.suction_object_collision and (self.rect.x, self.rect.y) != suction_location:
            dx = suction_location[0] - self.rect.centerx
            dy = suction_location[1] - self.rect.centery
            distance = pygame.math.Vector2(dx, dy).length()
        
            if distance >= 5:
                direction = pygame.math.Vector2(dx, dy).normalize()
                movement_speed = 5
                self.rect.move_ip(direction * movement_speed)
         
            if self.image_scale > 0.02:
                self.image_scale -= 0.02
                self.image = resize_image(self.image_scale)
                scaled_rect = self.image.get_rect()
                scaled_rect.center = self.rect.center 
                self.rect = scaled_rect
    """
    ------------------------------------------
    """


    """
    ------------------------------------------
    DRAW AND ASSOCIATED DRAW METHODS
    ------------------------------------------
    """  
    def draw(self, screen):
 
        if self.draw_player:
            screen.blit(self.image, self.rect)
            
            if self.knocked_out:
                screen.blit(self.knocked_out_animation[self.game.frame % 3] , (self.rect.x, self.rect.top - 10))
            
            if self.is_flying() and self.image == self.shoot_jump_image:
                self.image = self.right_image

            self.draw_jetpack(screen)
            self.draw_propeller(screen)
            self.draw_spring_shoes(screen)
            
            # Optional: Draw collision box for debugging (uncomment to see collision area)
            # pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)
    
    def get_collision_rect(self):
        """
        Returns the tighter collision rectangle for more precise collision detection
        """
        return self.collision_rect
    

    """
    The following methods are self explanatory, thus I will not provide and explanation
    """
    def draw_jetpack(self, screen):
        if self.using_jetpack:
            x = self.rect.x

            x = x-5 if self.right else x+35
            excess_y = 13 if texture.file_name == "ooga" else 0
 
            frame = self.game.frame
            if frame < 16:
                image = Jetpack.START_ANIMATION[frame % 3]
            elif frame < 147: 
                image = Jetpack.MAIN_BLAST[frame % 3]
            elif frame < 155:
                image = Jetpack.END_ANIMAITON[frame % 3]
            else:
                image = Jetpack.DEFAULT_ROCKET

            if self.paused:
                image = Jetpack.MAIN_BLAST[2]

            if self.right:
                image = pygame.transform.flip(image, True, False)

            screen.blit(image, (x, self.rect.y + 20 + excess_y))
    def draw_propeller(self, screen):
        if self.using_propeller:

            frame = self.game.frame
            if self.paused:
                image = Propeller.PROPELLERS[2]
            else:
                image = Propeller.PROPELLERS[frame % 4]

            screen.blit(image, (self.rect.centerx - 15,
                                self.rect.top - 3))

    def draw_spring_shoes(self, screen):
        if self.using_spring_shoes:
            if self.image in (self.shoot_image, self.shoot_jump_image):
                image = SpringShoes.SHOOT_COMPRESSED if self.jumping else SpringShoes.SHOOT_IMAGE
                excess_y = 3 if self.jumping else 0
                screen.blit(image, (self.rect.x + 15, self.rect.bottom - 5 + excess_y))

            else:
                excess_x = 5 if self.right else 0
                excess_y = 3 if self.jumping else 0
                image = SpringShoes.COMPRESSED_IMAGE if self.jumping else SpringShoes.DEFAULT_IMAGE
                if self.right:
                    image = pygame.transform.flip(image, True, False)
                screen.blit(image, (self.rect.x + 15 + excess_x , self.rect.bottom - 5 + excess_y))
    """
    ------------------------------------------
    """


    """
    ------------------------------------------
    PLAY ACTION FUNCTIONS
    ------------------------------------------
    """  
    def move_left(self):
        if self.using_custom_doodler:
            # Apply tilt animation for left movement with custom doodler
            base_img = self.left_image
            tilted_img = pygame.transform.rotate(base_img, 10)  # Tilt 10 degrees right when moving left
            self.prior_image = self.image = tilted_img
            self.current_tilt = 10
            self.is_tilted = True
        else:
            # Original behavior for texture-based characters
            self.prior_image = self.image = self.left_image
        
        self.x -= self.speed
        self.left = True
        self.right = False
        
    def move_right(self):
        if self.using_custom_doodler:
            # Apply tilt animation for right movement with custom doodler
            base_img = self.right_image
            tilted_img = pygame.transform.rotate(base_img, -10)  # Tilt 10 degrees left when moving right
            self.prior_image = self.image = tilted_img
            self.current_tilt = -10
            self.is_tilted = True
        else:
            # Original behavior for texture-based characters
            self.prior_image = self.image = self.right_image
        
        self.x += self.speed
        self.right = True
        self.left = False
    def shoot(self):
        if self.using_custom_doodler:
            # For the custom doodler character, shooting doesn't change the appearance much
            # Just ensure we keep the current directional image
            if self.left:
                self.prior_image = self.image = self.left_image
            else:
                self.prior_image = self.image = self.right_image
        else:
            # Original behavior for texture-based characters
            self.prior_image = self.image = self.shoot_image
        
        shoot_sound = choice((sounds.shoot_1, sounds.shoot_2))
        shoot_sound.play()
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.game.bullets.add(bullet)
    def jump(self, play_sound=True):
        if not self.is_flying():
            self.game.frame = 0
            self.excess_y = self.CENTER_X - (self.y - 273)
            self.velocity_y = self.JUMP_STRENGTH
            self.jumping = True

            if play_sound:
                sounds.jump.play()

            if (self.using_spring_shoes 
                and not self.is_using_booster()):

                sounds.spring.play()
                self.spring_shoe_jump_count += 1
    """
    ------------------------------------------
    """

    def is_flying(self):
        """
        This function returns a boolean determining whether the player is currenntly flying
        i.e using a jetpack or a propeller
        """
        return any((self.using_jetpack, self.using_propeller))
    def is_using_booster(self):
        """
        This function returns a boolean determining whether the player is currenntly using a booster
        i.e using a trampoline or a spring
        """
        return any((self.using_trampoline, self.using_spring))
    

    def update_image(self):
        """
        This function updates the default image (right) for the player
        This function is specifically used in the options menu when the user selects different textures
        Note: For the custom doodler character, this doesn't need to change textures
        """
        if self.using_custom_doodler:
            # For the custom doodler character, we don't change based on texture
            # Just ensure we're using the right-facing image
            self.image = self.right_image
        else:
            # For texture-based characters, reload the texture
            self.image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/right.png")


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(f"Assets/Images/Projectiles/{texture.file_name}.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        """
        Once the bullet goes beyond the top of the screen it is killed
        """
        self.rect.y -= 15
        if self.rect.bottom < 0:
            self.kill()
    
