# ILK - Space Exploration Game (Super Early Alpha)

A space exploration game inspired by Sid Meier's Pirates! but with a focus on space exploration and planet colonization.

## Current Status
⚠️ **SUPER EARLY ALPHA** ⚠️
This game is in very early development. Many features are incomplete or may not work as expected.

## Features
- Space exploration with multiple planets (10 different planet types!)
- Landing and exploration on planets
- First-person controls in both space and on planets
- Basic jumping mechanics
- **Trading System:** 8 different commodities with dynamic pricing
- **Planet Economy:** Each planet type has different supply/demand
- **Ship Upgrades:** Cargo, engines, fuel efficiency, weapons, shields
- **Combat System:** Player health, weapons, and shield upgrades
- **Random Encounters:** Derelict ships, pirates, merchants, asteroid fields
- **Credits & Cargo:** Full economic gameplay loop
- **Town Features:** Trading posts, shipyards, and NPCs
- Save/Load system
- Screenshot capability

## Requirements
- Python 3.x
- Ursina Engine
- Other dependencies listed in requirements.txt

## Installation
1. Clone this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game
```bash
./run_me.py
```

## Controls
- WASD: Movement
- Space: Jump (on planets) / Up (in space)
- Mouse: Look around
- ESC: Pause menu (or close trading/upgrade interface)
- **T**: Open trading interface (when near trading post)
- **U**: Open upgrade interface (when near shipyard)
- **1-8**: Buy commodities (in trading interface)
- **SHIFT+1-8**: Sell commodities (in trading interface)
- **1-3**: Purchase upgrades (in upgrade interface)
- F6: Take screenshot
- F7: Toggle third-person view
- F8: Toggle between space and town modes

## Contributing
This is an early alpha version. Feel free to submit issues and suggestions, but please be aware that the codebase is still in flux.

## License
[License information to be added] 