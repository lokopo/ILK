# ILK - Space Exploration Game

A 3D space exploration game inspired by Sid Meier's Pirates! but set in space with trading, exploration, and resource management.

## ✨ Current Status
**FULLY PLAYABLE** - All core systems working perfectly!

## 🎮 Game Features
- **🌌 Space Exploration**: 15 procedurally generated planets to discover
- **🚀 Planetary Landing**: Land on planets and explore surface environments  
- **💰 Trading System**: Complete economy with buy/sell mechanics
- **📦 Inventory Management**: Manage credits and 5 resource types
- **💾 Save/Load System**: Persistent game state with JSON saves
- **🎯 Two Game Modes**: Space flight (6DOF) and surface exploration (FPS)
- **🔫 Combat**: Projectile weapons in space mode
- **📸 Screenshots**: Built-in screenshot system
- **🖼️ Rotating Skybox**: Beautiful space environment

## 🎯 How to Play

### 🚀 Getting Started
1. **Start in Space Mode**: You begin in your ship floating in space
2. **Approach Planets**: Fly close to any planet to get a landing prompt
3. **Land on Planets**: Click "Land" when prompted to explore the surface
4. **Find Trading Posts**: Look for blue buildings with "TRADING POST" signs
5. **Trade Resources**: Press T near trading posts to buy/sell goods
6. **Manage Inventory**: Press I anytime to check your resources

### 💰 Trading & Economy
- **Starting Resources**: 1000 credits, 50 fuel, 10 ore, 5 crystals, 20 food, 3 medicine
- **Buy Items**: Fuel (10 credits), Food (15 credits)
- **Sell Items**: Ore (25 credits), Crystals (75 credits)
- **Inventory Limit**: 100 total items maximum
- **Trading Posts**: Found on planet surfaces (blue buildings)

### 🌍 Planet Exploration
- **Landing**: Approach planets in space, click "Land" when prompted
- **Surface Mode**: First-person movement with collision detection
- **Buildings**: Each planet has procedurally generated structures
- **Trading Posts**: Blue buildings where you can trade resources
- **Return to Space**: Press F8 to switch back to space mode

## 🎮 Controls

### 🚀 Space Mode (6DOF Flight)
- **WASD** - Move forward/back/left/right
- **Space/Shift** - Move up/down  
- **Q/E** - Roll left/right
- **Mouse** - Pitch and yaw (free look)
- **Left Click** - Fire projectiles
- **F7** - Toggle first/third-person view

### 🚶 Surface Mode (FPS-style)
- **WASD** - Walk around
- **Space** - Jump (double jump available)
- **Mouse** - Look around (mouse locked)
- **T** - Open trading menu (when near trading posts)

### 🎛️ Universal Controls
- **ESC** - Pause menu (Save/Load/Quit)
- **I** - Open inventory
- **F6** - Take screenshot (saved to screenshots/)
- **F8** - Switch between Space and Surface modes

## 💻 Installation & Running

### Prerequisites
- Python 3.7+
- OpenGL-capable graphics
- Desktop environment (not headless)

### Quick Start
```bash
# Option 1: Auto-setup (recommended)
python run_me.py

# Option 2: Manual setup
pip install -r requirements.txt
python space_game.py
```

### Dependencies
- **ursina==5.2.0** (3D game engine)
- **numpy==1.26.3** (mathematical operations) 
- **pillow==10.2.0** (image processing)

## 💾 Save System
- **Auto-timestamping**: Saves include date/time stamps
- **JSON Format**: Human-readable save files in saves/ folder
- **Complete State**: Saves player position, resources, planets
- **Quick Save**: F5 (saves to timestamped file)
- **Quick Load**: F9 (loads most recent save)

## 🎯 Gameplay Tips
1. **Start Trading Early**: Use your starting ore/crystals to buy fuel and food
2. **Explore Different Planets**: Each has unique trading post prices
3. **Manage Fuel**: You need fuel for space travel
4. **Check Inventory**: Press I regularly to track your resources
5. **Save Often**: Use ESC menu or F5 to save your progress

## 📁 Project Structure
```
ILK/
├── space_game.py          # Main game file
├── run_me.py             # Auto-setup launcher  
├── requirements.txt      # Dependencies
├── README.md            # This file
├── assets/textures/     # Game textures
├── saves/              # Save game files (auto-created)
└── screenshots/        # Screenshots (auto-created)
```

## 🐛 Troubleshooting
- **Graphics Issues**: Ensure OpenGL drivers are updated
- **Save/Load Problems**: Check file permissions in game directory
- **Performance Issues**: Try reducing planet count in code
- **Missing Textures**: Check assets/textures/ folder exists

## 🌟 Enjoy Your Space Trading Adventure!

Start small, trade smart, and build your space trading empire across the galaxy! 