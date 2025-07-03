import asyncio
import pygame
from game import Game

async def main():
    """Web-compatible main function using the game's run_web method"""
    try:
        print("🎮 Starting Gauri Jump web version...")
        
        # Note: pygame.init() is now called in Game.__init__() after proper setup
        # pygame.init() - removed to avoid double initialization
        
        print("✅ Creating Game object...")
        game = Game()
        print("✅ Game object created successfully")
        
        print("🚀 Starting web game loop...")
        await game.run_web()
        print("✅ Game completed")
        
    except Exception as e:
        print(f"❌ Error in web game: {e}")
        import traceback
        traceback.print_exc()
        
        # Create a simple error display
        try:
            pygame.init()
            screen = pygame.display.set_mode((640, 480))
            pygame.display.set_caption("Gauri Jump - Error")
            font = pygame.font.Font(None, 36)
            
            # Show error message
            error_text = font.render("Game failed to start", True, (255, 255, 255))
            error_text2 = font.render("Check console for details", True, (255, 255, 255))
            
            screen.fill((100, 0, 0))  # Red background for error
            screen.blit(error_text, (50, 200))
            screen.blit(error_text2, (50, 250))
            pygame.display.flip()
            
            # Keep error screen visible
            for _ in range(60):  # Show for ~1 second
                await asyncio.sleep(0.016)
                
        except:
            pass  # If even error display fails, just continue

if __name__ == "__main__":
    asyncio.run(main()) 