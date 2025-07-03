# Custom Doodler Character Setup

## Quick Setup

1. **Save your character image** as `doodler.png` in the `Assets/` folder (same level as the `colours.py` file)

2. **Run the game** - the new character will be automatically detected and used!

## Features

### 🎮 **Enhanced Movement**
- **Left/Right Flipping**: Character faces the direction of movement
- **Tilt Animation**: Character tilts ±10° when moving left/right for dynamic feel
- **Auto-scaling**: Image automatically scaled to 50x60 pixels (adjustable in code)

### 🎯 **Improved Collision**
- **Tighter collision box**: 70% width, 80% height of sprite for more precise jumping
- **Foot-aligned**: Collision box aligned with character's feet for realistic platform interaction

### 🔧 **Smart Fallback**
- If `doodler.png` is missing, the game automatically falls back to the original texture system
- No crashes or errors - seamless integration

## Customization Options

### Adjust Character Size
In `Sprites/player.py`, line ~47:
```python
self.doodler_size = (50, 60)  # Change these values
```

### Adjust Tilt Angle
In `Sprites/player.py`, movement methods:
```python
tilted_img = pygame.transform.rotate(base_img, 10)  # Change tilt angle
```

### Debug Collision Box
In `Sprites/player.py`, draw method, uncomment this line:
```python
pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)
```

## File Structure
```
Doodle-Jump/
├── Assets/
│   ├── doodler.png          ← Your character image goes here
│   ├── colours.py
│   └── sounds.py
├── Sprites/
│   └── player.py            ← Modified for custom character
└── game.py
```

## Technical Details

### Image Requirements
- **Format**: PNG with transparency recommended
- **Size**: Any size (will be scaled to 50x60 pixels)
- **Orientation**: Should face right (left-facing version created automatically)

### Collision System
- **Visual rect**: Full character image for drawing
- **Collision rect**: Smaller, tighter box for platform detection
- **Position**: Collision box aligned with character's feet/bottom

### Performance
- Images are loaded once at startup and cached
- Transformations (flip, rotate) are applied in real-time
- Minimal performance impact compared to original system

## Troubleshooting

### Character Not Loading?
- Check that `doodler.png` is in the `Assets/` folder
- Verify the image file isn't corrupted
- Look for console messages when starting the game

### Collision Issues?
- Uncomment the debug line to visualize collision box
- Adjust collision box size in the `__init__` method
- Character might be too small/large - adjust `doodler_size`

### Movement Feels Off?
- Adjust tilt angle in `move_left()` and `move_right()` methods
- Modify collision box alignment in `update_rect()` method

## Success! 🎉

When properly set up, you should see:
- `✓ Custom doodler character loaded successfully!` in the console
- Your character moving and tilting smoothly
- Proper collision detection with platforms

Enjoy your custom Gauri Jump character! 