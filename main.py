import asyncio
import pygame
from game import Game

async def main():
    """Replit-compatible main function for web deployment"""
    try:
        print("🎮 Starting Gauri Jump in Replit...")
        print("✅ Initializing game...")
        
        # Create and run the game
        game = Game()
        print("✅ Game object created successfully!")
        
        # Run the web version
        print("🚀 Starting web game loop...")
        await game.run_web()
        print("✅ Game completed successfully!")
        
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        import traceback
        traceback.print_exc()
        
        # Create a simple error display
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Game Error")
        font = pygame.font.Font(None, 36)
        
        # Show error message
        screen.fill((50, 50, 50))
        error_text = font.render("Game failed to load", True, (255, 100, 100))
        help_text = font.render("Check console for details", True, (255, 255, 255))
        
        screen.blit(error_text, (160, 200))
        screen.blit(help_text, (140, 250))
        pygame.display.flip()
        
        # Keep error screen visible
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            await asyncio.sleep(0.016)  # ~60 FPS
            clock.tick(60)

if __name__ == "__main__":
    print("🌐 Gauri Jump - Replit Web Version")
    print("=" * 40)
    asyncio.run(main())

  















 














































