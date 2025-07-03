import pygame
import os
import texture
from Assets import colours

class CharacterSelector:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.CENTER_X = game.CENTER_X
        self.CENTER_Y = game.CENTER_Y
        
        # Character data
        self.characters = [
            {
                "name": "F*** Ass Bob Gauri",
                "filename": "doodler.png",
                "display_name": "F*** Ass Bob Gauri"
            },
            {
                "name": "Wifey Gauri", 
                "filename": "wifey_gauri.png",
                "display_name": "Wifey Gauri"
            }
        ]
        
        self.selected_character = 0  # Currently selected character index
        self.character_images = []
        self.load_character_images()
        
        # UI elements - Match game's styling
        try:
            self.title_font = pygame.font.Font("Assets/Fonts/DoodleJump.ttf", 72)
            self.name_font = pygame.font.Font("Assets/Fonts/DoodleJump.ttf", 48)
            self.instruction_font = pygame.font.Font("Assets/Fonts/DoodleJump.ttf", 36)
        except:
            # Fallback to default fonts if custom font fails
            self.title_font = pygame.font.Font(None, 72)
            self.name_font = pygame.font.Font(None, 48)
            self.instruction_font = pygame.font.Font(None, 36)
        
        # Load background image to match game style
        try:
            self.background_image = pygame.image.load(f"Assets/Images/Backgrounds/Backgrounds/{texture.file_name}.png")
            self.background_image = pygame.transform.scale(self.background_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        except:
            self.background_image = None
        
        # Selection indicators - Match game colors
        self.selection_box_color = colours.GREEN
        self.text_color = colours.BLACK
        self.text_outline_color = colours.WHITE
        
    def load_character_images(self):
        """Load and scale character images for preview"""
        for character in self.characters:
            path = f"Assets/{character['filename']}"
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    # Scale for preview (larger than game size)
                    preview_img = pygame.transform.scale(img, (120, 144))
                    self.character_images.append(preview_img)
                except:
                    # Create placeholder if image fails to load
                    placeholder = pygame.Surface((120, 144))
                    placeholder.fill(colours.GREY)
                    self.character_images.append(placeholder)
            else:
                # Create placeholder for missing image
                placeholder = pygame.Surface((120, 144))
                placeholder.fill(colours.GREY)
                # Add text to indicate missing
                font = pygame.font.Font(None, 24)
                text = font.render("Missing", True, colours.WHITE)
                text_rect = text.get_rect(center=(60, 72))
                placeholder.blit(text, text_rect)
                self.character_images.append(placeholder)
    
    def draw_text_with_outline(self, text, font, text_color, outline_color, position, screen):
        """Draw text with outline for better visibility like the game style"""
        # Draw outline
        outline_positions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        for offset_x, offset_y in outline_positions:
            outline_surface = font.render(text, True, outline_color)
            outline_rect = outline_surface.get_rect(center=(position[0] + offset_x, position[1] + offset_y))
            screen.blit(outline_surface, outline_rect)
        
        # Draw main text
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_character = (self.selected_character - 1) % len(self.characters)
            elif event.key == pygame.K_RIGHT:
                self.selected_character = (self.selected_character + 1) % len(self.characters)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Confirm selection and start game
                self.confirm_selection()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if clicked on a character
            for i in range(len(self.characters)):
                char_x = self.CENTER_X - 200 + (i * 400) - 60
                char_y = self.CENTER_Y - 72
                char_rect = pygame.Rect(char_x, char_y, 120, 144)
                if char_rect.collidepoint(mouse_x, mouse_y):
                    self.selected_character = i
                    self.confirm_selection()
                    break
    
    def confirm_selection(self):
        """Confirm character selection and start the game"""
        selected_char = self.characters[self.selected_character]
        
        # Update the game's selected character
        self.game.selected_character_file = selected_char['filename']
        self.game.selected_character_name = selected_char['display_name']
        
        # Transition to gameplay (since character selection comes after play button)
        self.game.character_select = False
        self.game.play_game = True
        
        # Initialize game objects with selected character
        self.game.initialise_game_weights()
        self.game.initialise_game_objects()
    
    def draw(self, screen):
        # Draw background - match game style
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(colours.WHITE)
        
        # Draw title with outline
        self.draw_text_with_outline("Choose Your Character", self.title_font, 
                                   self.text_color, self.text_outline_color, 
                                   (self.CENTER_X, 150), screen)
        
        # Draw characters
        for i, (character, img) in enumerate(zip(self.characters, self.character_images)):
            # Calculate position - improved spacing to prevent cutoff
            if len(self.characters) == 2:
                # For 2 characters, space them better
                char_x = self.CENTER_X - 150 + (i * 300) - 60
            else:
                # For more characters, use original spacing
                char_x = self.CENTER_X - 200 + (i * 400) - 60
            char_y = self.CENTER_Y - 72
            
            # Draw selection box if selected
            if i == self.selected_character:
                selection_rect = pygame.Rect(char_x - 10, char_y - 10, 140, 164)
                pygame.draw.rect(screen, self.selection_box_color, selection_rect, 5)
            
            # Draw character image
            screen.blit(img, (char_x, char_y))
            
            # Draw character name with outline - handle long names
            name_center_x = char_x + 60
            # Ensure the name doesn't go off-screen
            name_center_x = max(name_center_x, 150)  # Minimum distance from left edge
            name_center_x = min(name_center_x, self.SCREEN_WIDTH - 150)  # Maximum distance from right edge
            
            # Check if name is too long and needs to be on multiple lines
            name = character['display_name']
            if len(name) > 15:  # If name is very long
                # Try to split at a space near the middle
                words = name.split()
                if len(words) > 1:
                    mid_point = len(words) // 2
                    line1 = ' '.join(words[:mid_point])
                    line2 = ' '.join(words[mid_point:])
                    
                    # Draw two lines
                    self.draw_text_with_outline(line1, self.name_font,
                                               self.text_color, self.text_outline_color,
                                               (name_center_x, char_y + 160), screen)
                    self.draw_text_with_outline(line2, self.name_font,
                                               self.text_color, self.text_outline_color,
                                               (name_center_x, char_y + 185), screen)
                else:
                    # Single word too long - just draw it
                    self.draw_text_with_outline(name, self.name_font,
                                               self.text_color, self.text_outline_color,
                                               (name_center_x, char_y + 170), screen)
            else:
                # Normal length name
                self.draw_text_with_outline(name, self.name_font,
                                           self.text_color, self.text_outline_color,
                                           (name_center_x, char_y + 170), screen)
        
        # Draw instructions with outline
        instructions = [
            "Use ← → arrow keys to select",
            "Press ENTER or SPACE to confirm", 
            "Or click on a character"
        ]
        
        for i, instruction in enumerate(instructions):
            self.draw_text_with_outline(instruction, self.instruction_font,
                                       self.text_color, self.text_outline_color,
                                       (self.CENTER_X, 700 + i * 40), screen) 