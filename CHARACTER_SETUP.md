# Gauri Jump - Character Selector & Web Setup

## 🎭 Character Selector

Your game now starts with a character selection screen featuring:

### Characters Available:
1. **"F*** Ass Bob Gauri"** 
   - File: `Assets/doodler.png` ✅ (already placed)
   
2. **"Wifey Gauri"** 
   - File: `Assets/wifey_gauri.png` ❌ (needs your image file)

### How to Add Second Character:
1. Save your "Wifey Gauri" character image as `wifey_gauri.png` 
2. Place it in the `Assets/` folder (replace the placeholder file)
3. The game will automatically detect and load it

### Character Selection Controls:
- **← → Arrow Keys**: Navigate between characters
- **ENTER or SPACE**: Confirm selection
- **Mouse Click**: Click directly on a character to select

## 🌐 Web Deployment (Play in Browser)

### Option 1: Quick Web Test
```bash
# Install pygbag (already done)
pip install pygbag

# Run web version
python -m pygbag main_web.py
```

### Option 2: Deploy to Web
```bash
# Build for web deployment
python -m pygbag main_web.py --build

# Your game will be available at:
# http://localhost:8080
```

### Web Features:
- ✅ Works in any modern web browser
- ✅ Mobile-friendly controls (touch/mouse)
- ✅ Full game functionality
- ✅ Character selector included
- ✅ Score tracking

### Sharing Your Web Game:
1. Upload the generated files to a web server
2. Share the URL with friends
3. Works on desktop and mobile browsers!

## 🎮 Game Flow

1. **Main Menu** → Choose Play, Options, etc.
2. **Character Selection** → Choose your character (after clicking Play)
3. **Gameplay** → Jump and collect score with chosen character
4. **End Game** → View scores, play again

## 🛠️ File Structure

```
Gauri-Jump/
├── Assets/
│   ├── doodler.png          ← Bob Gauri (current character)
│   └── wifey_gauri.png      ← Wifey Gauri (add your image here)
├── Sprites/
│   ├── character_selector.py ← Character selection screen
│   └── player.py            ← Updated player class
├── main.py                  ← Desktop version
├── main_web.py              ← Web version
└── game.py                  ← Updated game logic
```

## 🎯 Quick Start

### Desktop Version:
```bash
python main.py
```

### Web Version:
```bash
python -m pygbag main_web.py
```

## 🎨 Character Requirements

For best results, your character images should:
- **Format**: PNG with transparency
- **Size**: Any size (auto-scaled to 50×60 pixels)
- **Style**: Match the cartoon aesthetic
- **Orientation**: Facing right (left is auto-generated)

## 🌟 Features

- **Character Preview**: See characters before selecting
- **Dynamic Names**: Each character has a display name
- **Fallback System**: Missing characters show placeholders
- **Web Compatible**: Works in browsers with full functionality
- **Mobile Friendly**: Touch controls for web version

Your personalized **Gauri Jump** with character selection is ready! 🎉 