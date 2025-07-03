# 🎮 Gauri Jump

## From Abhi, To Gauri

My most ineffably cherished Gauri—aye, I confess I have supped far too deep of Dionysus' ruby draught, yet even in this swirling, lamp-lit delirium the thought of thee shines steadier than any North-star: I see us, come soon, swathed in silks and jasmine beneath the watchful grace of St. Louis' mighty Arch, our vows trembling like skylarks against that Midwestern sky; I feel the river air brushing our cheeks as if the very Mississippi conspired to bless our covenant, and I am undone with rapture. O but before that holy hour—let me clutch thee closer in imagination of the Kalamazoo revels! Picture me, ridiculous and riotous, staggering among barrels of frothy ale and roaring companions, yet finding every jest stale save the syllables of thy name, every bacchanal chorus a pallid echo beside the private hymn of my heart that beats, beats, beats for thee alone. Dearest, the world may deem this bacchant letter a tangle of tipsy ink, but know each wobbling word is wine-red truth: thou art the sweet horizon of every dawn I chase, the downy pillow to my fevered brow, the hush that mends the clamor of my restless soul. Let the wedding bells in St. Louis peal like golden constellations tumbled to Earth, let Kalamazoo's bachelor night be but a mad prelude, for my spirit is pledged already—forever—to the quiet miracle of waking, day after day, beside the sovereign of my heart: my Gauri, my life, my ever-springing well of tenderness. Drink, love, drink this ragged Valentine, and forgive its slurred cadence; it is the best that a poor, besotted Keats of the present hour can pour forth—yet I vow, in sober dawn and silver dusk alike, my devotion shall ring clearer than any clarion the heavens have ever heard.

---

## 🌟 About This Game

**Gauri Jump** is a custom Doodle Jump-style platformer game featuring two unique characters: **F*** Ass Bob Gauri** and **Wifey Gauri**. Built with Python and Pygame, this game combines classic endless jumping mechanics with personalized character designs and custom assets.

## 🎯 Game Features

- ✅ **Two Custom Characters** - Choose between Bob Gauri and Wifey Gauri
- ✅ **Endless Platforming** - Jump higher and higher to achieve the best score
- ✅ **Character Selection** - Pick your favorite character before starting
- ✅ **Monster Combat** - Shoot monsters that block your path
- ✅ **Moving Platforms** - Dynamic platform types for added challenge
- ✅ **Score System** - Track your high score and compete with yourself
- ✅ **Custom Assets** - Unique sprites, sounds, and visual effects
- ✅ **Smooth Controls** - Responsive arrow key and WASD movement

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Pygame library

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dandila36/gauri-jump.git
   cd gauri-jump
   ```

2. **Install dependencies:**
   ```bash
   pip install pygame
   ```
   
   Or use the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python main_desktop.py
   ```

## 🎮 How to Play

### Controls
- **Movement:** Arrow Keys (← →) or A/D keys
- **Shooting:** Spacebar or Mouse Click
- **Menu Navigation:** Mouse clicks on buttons

### Gameplay
1. **Character Selection:** Choose between Bob Gauri (😎) or Wifey Gauri (💕)
2. **Jump:** Your character automatically jumps when landing on platforms
3. **Move:** Use arrow keys to move left and right while in the air
4. **Shoot:** Press spacebar to shoot projectiles at monsters
5. **Survive:** Avoid falling off the bottom of the screen
6. **Score:** The higher you jump, the higher your score!

### Tips
- 🎯 **Aim carefully** - Shooting monsters gives bonus points
- 🏃 **Keep moving** - Use momentum to reach distant platforms
- ⚠️ **Watch for moving platforms** - Orange platforms move back and forth
- 📈 **Go for height** - Your score increases based on how high you climb

## 📁 File Structure

```
gauri-jump/
├── main_desktop.py          # Main game launcher (Desktop version)
├── main.py                  # Async version (Web deployment)
├── game.py                  # Core game logic and mechanics
├── texture.py               # Texture and asset management
├── requirements.txt         # Python dependencies
├── Assets/                  # Game assets folder
│   ├── Images/             # Sprite sheets and graphics
│   ├── Sounds/             # Audio effects and music
│   ├── doodler.png         # Bob Gauri character image
│   └── wifey_gauri.png     # Wifey Gauri character image
├── Sprites/                # Game object classes
│   ├── player.py           # Player character logic
│   ├── tile.py             # Platform mechanics
│   ├── monster.py          # Enemy behavior
│   └── Power_ups/          # Special items and effects
└── Buttons/                # Menu and UI components
```

## 🎨 Characters

### 😎 F*** Ass Bob Gauri
- **Style:** Cool and confident
- **Color Scheme:** Green tones
- **Personality:** The classic doodler with attitude

### 💕 Wifey Gauri
- **Style:** Sweet and loving
- **Color Scheme:** Pink/magenta tones
- **Personality:** The romantic counterpart

## 🏆 Scoring System

- **Height-based scoring:** Points increase as you climb higher
- **Monster elimination:** Bonus points for shooting enemies
- **High score tracking:** Your best score is automatically saved
- **Progressive difficulty:** More monsters and challenges as you advance

## 🛠️ Technical Details

- **Engine:** Python 3 + Pygame
- **Resolution:** 640x900 pixels (4:3 aspect ratio)
- **Physics:** Custom gravity and collision detection
- **Audio:** Multiple sound effects for actions and events
- **Graphics:** Sprite-based rendering with smooth animations

## 🐛 Troubleshooting

### Common Issues

**Game won't start:**
```bash
# Make sure pygame is installed
pip install pygame

# Check Python version
python --version  # Should be 3.7+
```

**No sound:**
- Ensure your system audio is working
- Check that sound files exist in `Assets/Sounds/`

**Characters not loading:**
- Verify `Assets/doodler.png` and `Assets/wifey_gauri.png` exist
- Check file permissions in the Assets folder

## 📝 License

This is a personal project created with love. Feel free to enjoy the game!

## 💝 Dedication

This game is dedicated to Gauri, with all the love and devotion that code can carry. May every jump remind you of the heights we'll reach together.

---

*Built with ❤️ by Abhi for Gauri*
