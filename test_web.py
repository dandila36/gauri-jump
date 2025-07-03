import asyncio
import pygame

async def main():
    """Simple test to verify pygame web works"""
    try:
        print("🧪 Testing pygame web...")
        
        # Initialize pygame
        pygame.init()
        print("✅ Pygame initialized")
        
        # Create screen
        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Test Game")
        print("✅ Screen created")
        
        # Create a simple colored surface
        screen.fill((0, 128, 255))  # Blue background
        
        # Add some text
        font = pygame.font.Font(None, 74)
        text = font.render("WEB TEST", True, (255, 255, 255))
        screen.blit(text, (200, 200))
        
        pygame.display.flip()
        print("✅ First frame drawn")
        
        # Simple game loop
        clock = pygame.time.Clock()
        running = True
        frame = 0
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Clear screen
            screen.fill((0, 128, 255))
            
            # Draw animated text
            color = (255, 255, 255) if (frame // 30) % 2 == 0 else (255, 255, 0)
            text = font.render(f"FRAME {frame}", True, color)
            screen.blit(text, (150, 200))
            
            # Update display
            pygame.display.flip()
            clock.tick(60)
            frame += 1
            
            # Essential for web compatibility
            await asyncio.sleep(0)
            
            # Exit after 600 frames (10 seconds)
            if frame > 600:
                running = False
        
        print("✅ Test completed successfully")
        pygame.quit()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 