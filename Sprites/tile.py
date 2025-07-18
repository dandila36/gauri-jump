import pygame
import random

import Assets.sounds as sounds

from Sprites.Power_ups.propeller import Propeller
from Sprites.Power_ups.jetpack import Jetpack
from Sprites.Power_ups.spring_shoes import SpringShoes
from Sprites.Power_ups.spring import Spring
from Sprites.Power_ups.trampoline import Trampoline

import texture

class Tile(pygame.sprite.Sprite):

    """
    As all other tiles are variations on this default tile I will comment the default methods 
    shared to all other tiles in the Parent class (here).
    I will only comment functions which are unique to that specific class
    """

    total = 0

    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
    DEFAULT_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(1, 1, 57, 15))  # Extract a 32x32 sprite
    
    MOVING_TILE_IMAGE  = SPRITE_SHEET.subsurface(pygame.Rect(2, 19, 58, 17)) 
    DISAPPEARING_TILE_IMAGE  = SPRITE_SHEET.subsurface(pygame.Rect(1, 55, 57, 15)) 
    SHIFTING_TILE_IMAGE  = SPRITE_SHEET.subsurface(pygame.Rect(1, 184, 57, 15)) 
    
    POWER_UPS = [Jetpack, Trampoline, Spring, Propeller, SpringShoes]

    BROKEN_TILE_IMAGE  = SPRITE_SHEET.subsurface(pygame.Rect(1, 73, 60, 15)) 
    BROKEN_TILE_IMAGE_1  = SPRITE_SHEET.subsurface(pygame.Rect(0, 90, 62, 20)) 
    BROKEN_TILE_IMAGE_2  = SPRITE_SHEET.subsurface(pygame.Rect(0, 116, 62, 27)) 
    BROKEN_TILE_IMAGE_3  = SPRITE_SHEET.subsurface(pygame.Rect(0, 148, 62, 32)) 

    EXPLODING_TILE_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(1, 184, 57, 15)) 
    EXPLODING_TILE_IMAGE_1 = SPRITE_SHEET.subsurface(pygame.Rect(1, 202, 57, 15)) 
    EXPLODING_TILE_IMAGE_2 = SPRITE_SHEET.subsurface(pygame.Rect(1, 220, 57, 15)) 
    EXPLODING_TILE_IMAGE_3 = SPRITE_SHEET.subsurface(pygame.Rect(1, 238, 57, 15)) 
    EXPLODING_TILE_IMAGE_4 = SPRITE_SHEET.subsurface(pygame.Rect(1, 256, 57, 15)) 
    EXPLODING_TILE_IMAGE_5 = SPRITE_SHEET.subsurface(pygame.Rect(1, 274, 58, 18)) 
    EXPLODING_TILE_IMAGE_6 = SPRITE_SHEET.subsurface(pygame.Rect(1, 293, 61, 27)) 
    EXPLODING_TILE_IMAGE_7 = SPRITE_SHEET.subsurface(pygame.Rect(1, 321, 61, 28)) 

    def __init__(self, game, x, y):
        super().__init__()
        Tile.total += 1

        self.game           = game
        self.SCREEN_HEIGHT  = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH   = game.SCREEN_WIDTH
        self.fade_out_alpha = game.fade_out_alpha
        self.CENTER_X       = game.CENTER_X
        self.player         = game.player

        self.x = x
        self.y = y
        self.image = self.DEFAULT_IMAGE 
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.power_up = None

        self.y_pos = self.player.y + (self.rect.y - 390)

        #We do not want to generate a power up for a broken tile or a moving tile, or the main menu tile
        if not isinstance(self, (BrokenTile, MovingTile)) and not self.game.main_menu:
            self.generate_power_up()

        #seperate pygame 
        #if isinstance(self, MoveableTile):
        #    self.game.movable_platforms.add(self)
        #else:
        self.game.platforms.add(self)

    @classmethod
    def update_images(cls):
        """
        This function updates the class images when a different texture pack has been chosen
        """
        cls.SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
        cls.DEFAULT_IMAGE = cls.SPRITE_SHEET.subsurface(pygame.Rect(1, 1, 57, 15))  # Extract a 32x32 sprite
    
        cls.MOVING_TILE_IMAGE  = cls.SPRITE_SHEET.subsurface(pygame.Rect(2, 19, 58, 17)) 
        cls.DISAPPEARING_TILE_IMAGE  = cls.SPRITE_SHEET.subsurface(pygame.Rect(1, 55, 57, 15)) 
        cls.SHIFTING_TILE_IMAGE  = cls.SPRITE_SHEET.subsurface(pygame.Rect(1, 184, 57, 15)) 

        cls.MOVEABLE_TILE_IMAGE  = cls.SPRITE_SHEET.subsurface(pygame.Rect(150, 305, 80, 35)) 

        cls.BROKEN_TILE_IMAGE  = cls.SPRITE_SHEET.subsurface(pygame.Rect(1, 73, 60, 15)) 
        cls.BROKEN_TILE_IMAGE_1  = cls.SPRITE_SHEET.subsurface(pygame.Rect(0, 90, 62, 20)) 
        cls.BROKEN_TILE_IMAGE_2  = cls.SPRITE_SHEET.subsurface(pygame.Rect(0, 116, 62, 27)) 
        cls.BROKEN_TILE_IMAGE_3  = cls.SPRITE_SHEET.subsurface(pygame.Rect(0, 148, 62, 32)) 

        cls.EXPLODING_TILE_IMAGE = cls.SPRITE_SHEET.subsurface(pygame.Rect(1, 184, 57, 15)) 
        cls.EXPLODING_TILE_IMAGE_1 = cls.SPRITE_SHEET.subsurface(pygame.Rect(1, 202, 57, 15)) 
        cls.EXPLODING_TILE_IMAGE_2 = cls.SPRITE_SHEET.subsurface(pygame.Rect(1, 220, 57, 15)) 
        cls.EXPLODING_TILE_IMAGE_3 = cls.SPRITE_SHEET.subsurface(pygame.Rect(1, 238, 57, 15)) 
        cls.EXPLODING_TILE_IMAGE_4 = cls.SPRITE_SHEET.subsurface(pygame.Rect(1, 256, 57, 15)) 
        cls.EXPLODING_TILE_IMAGE_5 = cls.SPRITE_SHEET.subsurface(pygame.Rect(1, 274, 58, 18)) 
        cls.EXPLODING_TILE_IMAGE_6 = cls.SPRITE_SHEET.subsurface(pygame.Rect(1, 293, 61, 27)) 
        cls.EXPLODING_TILE_IMAGE_7 = cls.SPRITE_SHEET.subsurface(pygame.Rect(1, 321, 61, 28)) 
        
    def handle_events(self, event):
        pass

    
    def update_current_image(self):
        """
        This function is specifically here for the default tile in the main menu screen
        When a texture is selected we update just the default tile to be shown
        """
        self.image = self.DEFAULT_IMAGE


    def generate_power_up(self): 
        """
        This function is inherited by every other unique tile type and it simply generate a random power up based on the given probability weights
        """
        power_up = random.choices(population =  self.POWER_UPS+[None], weights=[0.1, 2, 7, 0.8, 1, 80])[0]
        if power_up:
            self.power_up = power_up(self.game, self.rect.centerx, self.rect.centery, self)

    def update(self):
        self.death_check()
        self.player_collision_check()
        self.power_up_check()


    def power_up_check(self):
        """
        If the tile has a power up then we want to update it
        """
        if self.power_up:
            self.power_up.update()

    def player_collision_check(self):
        """
        If the player is falling,
        is not dead, is not using a booster (spring or trampoline) and,
        is not flying (using propeller or rocket) then the collision will take place
        
        The player's jump function is simply called
        """
        if self.rect.colliderect(self.player.rect):
            if (self.player.falling 
                and not self.player.dead
                and not self.player.is_using_booster()
                and not self.player.is_flying()):
                self.player.jump()

    def death_check(self):
        """
        If the tile goes beyond the screen at the bottom then we kill the object whilst decrementing the total tile number
        """
        if self.rect.y > self.SCREEN_HEIGHT:
            Tile.total -= 1
            self.kill()

    def draw(self, screen):
        self.image.set_alpha(self.game.fade_out_alpha)
        screen.blit(self.image, self.rect)
        if self.power_up:
            self.power_up.draw(screen)       

class BrokenTile(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.BROKEN_TILE_IMAGE
        self.start = self.y
        self.velocity = [0, 0]  # Initial velocity
        self.gravity = 0.2
        self.fall = False
        
    def handle_events(self, event):
        pass

    def update(self):
        self.death_check()
        self.player_collision_check()
        self.fall_check()

    
    def fall_check(self):
        """
        As the players velocity increases from the jump() we change the images for an animation of breaking
        """
        if self.fall:
            self.velocity[1] += self.gravity
            self.rect.move_ip(self.velocity[0], self.velocity[1])

            if self.velocity[1] < 2:
                self.image = self.BROKEN_TILE_IMAGE_1
            elif self.velocity[1] < 3:
                self.image = self.BROKEN_TILE_IMAGE_2
            elif self.velocity[1] < 4:
                self.image = self.BROKEN_TILE_IMAGE_3

    def player_collision_check(self):
        if not self.fall:
            collision = pygame.sprite.collide_rect(self.player, self)
            if (collision 
                and self.player.falling 
                and self.player.rect.bottom >= self.rect.top
                and not self.player.dead
                and not self.player.is_using_booster()
                and not self.player.is_flying()):
                sounds.tile_break.play()
                self.fall = True
                
class MovingTile(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.velocity = random.choice([-1, 1])  # -1 for left, 1 for right
        self.speed = random.randint(1, 4)
        self.image = self.MOVING_TILE_IMAGE
        self._generate_boudaries()
        self.paused = False
  
    def handle_events(self, event):
        pass

    def update(self):
        if not self.player.paused:
            self.update_movement()
            self.boundary_check()
            self.death_check()
            self.player_collision_check()
            self.power_up_check()

    def update_movement(self):
        """
        This function simply updates the rect position based on the velocity and speed of the moving tile
        """
        self.rect.x += self.velocity * self.speed
        if self.power_up:
            self.power_up.rect.x += self.velocity * self.speed


    def boundary_check(self):
        """
        When the tile hits the predefined boundaries its velocity will change such that it moves in the opposite direction
        """
        if self.rect.right > self.max_right:
            self.rect.right = self.max_right
            self.velocity *= -1
        
        elif self.rect.left < self.max_left:
            self.rect.left = self.max_left
            self.velocity *= -1

    def _generate_boudaries(self):
        """
        This functions generates a random left and right boundary for the tile
        """
        max_left = random.randint(0, self.CENTER_X)
        max_right = random.randint(self.CENTER_X + 1, 640)
        
        while max_right - max_left < 150:
            max_left = random.randint(0, self.CENTER_X )
            max_right = random.randint(self.CENTER_X + 1 + 1, 640)
        
        self.max_left = max_left
        self.max_right = max_right

    def draw(self, screen):   
        if self.power_up:
            self.power_up.draw(screen)
        
        self.image.set_alpha(self.game.fade_out_alpha) 
        screen.blit(self.image, self.rect)

class DisappearingTile(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.DISAPPEARING_TILE_IMAGE

    def handle_events(self, event):
        pass

    def player_collision_check(self):
        collision = pygame.sprite.collide_rect(self.player, self)
        if (collision 
            and self.player.falling 
            and not self.player.dead
            and not self.player.is_using_booster()
            and not self.player.is_flying()):
            sounds.tile_disappear.play()
            self.player.jump()
            Tile.total -= 1
            self.kill()

class ShiftingTile(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.SHIFTING_TILE_IMAGE
        self.shift = False
        self.move_speed = 5

        self.upper_bound = self.SCREEN_WIDTH - self.rect.width 
        self.lower_bound = self.rect.width

    def handle_events(self, event):
        pass

    def update(self):
        self.death_check()
        self.player_collision_check()
        self.shift_check()
        self.power_up_check()

    def player_collision_check(self):
        collision = pygame.sprite.collide_rect(self.player, self)
        if (collision 
            and self.player.falling
            and self.player.rect.bottom >= self.rect.top
            and not self.player.dead
            and not self.player.is_using_booster()
            and not self.player.is_flying()):
            
            #Generate new random position
            target_x = random.randint(self.lower_bound, self.upper_bound)
            while self.rect.left - 50 < target_x < self.rect.right + 50:
                target_x = random.randint(self.lower_bound, self.upper_bound)

            self.target_x = target_x
            self.player.jump()
            self.shift = True

    def shift_check(self):
        """
        This function gradually shifts the tile to the set random target x location
        """
        if self.shift:
            if self.rect.x < self.target_x:
                self.rect.x += 5

                if self.power_up:
                    self.power_up.rect.x += 5

            elif self.rect.x > self.target_x:
                self.rect.x -= 5
            
                if self.power_up:
                    self.power_up.rect.x -= 5

            if self.target_x - 5 <= self.rect.x <= self.target_x + 5:
                self.shift = False
             
class MoveableTile(Tile):
    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/default.png")
    MOVEABLE_TILE_IMAGE  = SPRITE_SHEET.subsurface(pygame.Rect(150, 305, 80, 35)) 

    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.MOVEABLE_TILE_IMAGE
        self.moving = False
        self.moved = False

        #The power up is slightly off because of the arrows making the rectangle too large
        if self.power_up:
            self.power_up.rect.x = self.rect.x + 20
            self.power_up.rect.y += 6

    def handle_events(self, event):
        """
        This function allows the user to move the tile any position they desire, but only once (self.moved = True)
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.moved:
            if self.rect.collidepoint(event.pos):
                self.moving = True
                self.offset_x = event.pos[0] - self.rect.x
                self.offset_y = event.pos[1] - self.rect.y
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.moving:
            self.moving = False
            self.moved = True

    def update(self):
        self.death_check()
        self.player_collision_check()
        self.check_moving()
        self.power_up_check()

    
    def player_collision_check(self):
        collision = pygame.sprite.collide_rect(self.player, self)
        if (collision 
            and self.player.falling 
            and self.player.rect.bottom >= self.rect.top
            and not self.player.dead
            and not self.player.is_using_booster()
            and not self.player.is_flying()):
            self.player.jump()
           
            if self.moving:
                self.moving = False
                self.moved = True

    def check_moving(self):
        """
        If we are moving this tile then move the rect to the mouse coordinates
        """
        if self.moving:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.x = mouse_x - self.offset_x
            self.rect.y = mouse_y - self.offset_y

            if self.power_up:
                self.power_up.rect.x = mouse_x - self.offset_x + 20
                self.power_up.rect.y = mouse_y - self.offset_y#
            
    def draw(self, screen):

        self.image.set_alpha(self.game.fade_out_alpha)
        screen.blit(self.image, self.rect)
        if self.power_up:
            self.power_up.draw(screen)


class ExplodingTile(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.EXPLODING_TILE_IMAGE
        self.start = self.y
        self.velocity = [0, 0]  # Initial velocity
        self.gravity = 0.2
        self.frame = 0
        self.collision = False
    
    def handle_events(self, event):
        pass

    def update(self):
        self.death_check()
        self.player_collision_check()
        self.explode_check()


    def explode_check(self):
        """
        This function causes the animation of exploding to occur over 35 frames.
        The frame count is initialised upon collision
        """
        if self.collision:
            if self.frame < 5:
                self.image = self.EXPLODING_TILE_IMAGE
            elif self.frame  < 10:
                self.image = self.EXPLODING_TILE_IMAGE_1
            elif self.frame  < 15:
                self.image = self.EXPLODING_TILE_IMAGE_2
            elif self.frame  < 20:
                self.image = self.EXPLODING_TILE_IMAGE_3
            elif self.frame  < 25:
                self.image = self.EXPLODING_TILE_IMAGE_4
            elif self.frame < 30:
                self.image = self.EXPLODING_TILE_IMAGE_5
            elif self.frame < 35:
                self.image = self.EXPLODING_TILE_IMAGE_6
            else:
                self.image = self.EXPLODING_TILE_IMAGE_7
                sounds.explosion.play()
                self.kill()
                #explode

    def player_collision_check(self):
        if not self.collision:
            self.collision = pygame.sprite.collide_rect(self.player, self)
            if (self.collision 
                and self.player.falling 
                and self.player.rect.bottom >= self.rect.top
                and not self.player.dead
                and not self.player.is_using_booster()
                and not self.player.is_flying()):
                self.player.jump()
                sounds.tile_break.play()
        else:
            self.frame += 1
                
                