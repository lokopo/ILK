# ILK - Space Exploration Game (Super Early Alpha)

A space exploration game inspired by Sid Meier's Pirates! but with a focus on space exploration and planet colonization.

## Current Status
⚠️ **SUPER EARLY ALPHA** ⚠️
This game is in very early development. Many features are incomplete or may not work as expected.

## Features
- **Space Exploration:** 10 different planet types with unique economies
- **Faction System:** 6 major factions with complex relationships
- **Reputation System:** Your actions affect standing with each faction
- **Crew Management:** Hire specialists (gunners, pilots, engineers, medics)
- **Time Progression:** Game advances in real-time with daily expenses
- **Mission System:** Take contracts from faction leaders for rewards
- **Trading System:** 8 commodities with dynamic, location-based pricing
- **Ship Upgrades:** Enhance cargo, engines, fuel, weapons, and shields
- **Combat System:** Tactical battles influenced by crew skills and equipment
- **Random Encounters:** Derelict ships, pirates, merchants, asteroid fields
- **Town Features:** Trading posts, shipyards, embassies, crew quarters, mission boards
- **Economic Warfare:** Market fluctuations and faction-based trade advantages
- Landing and exploration on planets with FPS controls
- Save/Load system and screenshot capability

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

### Basic Movement
- **WASD**: Movement in space and on planets
- **Space**: Jump (on planets) / Vertical up (in space)
- **Shift**: Vertical down (in space)
- **Q/E**: Roll ship (in space)
- **Mouse**: Look around and steer ship

### Game Management
- **ESC**: Pause menu / Close any open interface
- **F6**: Take screenshot
- **F7**: Toggle third-person view (in space)
- **F8**: Toggle between space and town modes

### Town Interactions (When Near Buildings)
- **T**: Trading Post - Buy/sell commodities
- **U**: Shipyard - Upgrade your ship
- **R**: Embassy - View faction relations
- **C**: Crew Quarters - Manage your crew
- **M**: Mission Board - Accept faction missions

### Interface Controls
- **1-8**: Buy commodities (trading) / Accept missions (mission board)
- **SHIFT+1-8**: Sell commodities (trading interface)
- **1-5**: Purchase upgrades (shipyard interface)
- **H**: Hire crew member (crew management)
- **F**: Fire crew member (crew management)

### Economic Testing Commands
- **B**: Toggle blockade on current planet (testing)
- **I**: Show detailed economic information for current planet
- **N**: Fast-forward time by one day (testing)

## Contributing
This is an early alpha version. Feel free to submit issues and suggestions, but please be aware that the codebase is still in flux.

## License
[License information to be added] 