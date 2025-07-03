# ILK Space Game - Frequently Asked Questions (FAQ)

## 🚀 **GAME OVERVIEW**

### What is the ILK Space Game?
ILK is a space exploration and trading game inspired by Sid Meier's Pirates! Set in a rich universe with 6 major factions, 10 planet types, and complex economic systems, you'll build your reputation, manage a crew, and carve out your destiny among the stars.

### What's the current development status?
The game is in **FULLY PLAYABLE ALPHA** status. All core systems are implemented and functional, providing dozens of hours of engaging gameplay. While labeled as "alpha," the game offers a complete experience with all major features working correctly.

### How big is the game world?
- **10 different planet types** with unique economies and characteristics
- **6 major factions** with complex political relationships  
- **8 commodities** for trading with dynamic pricing
- **Persistent economy** where your actions have lasting impact
- **Procedurally generated missions** and random encounters

---

## 🎮 **GETTING STARTED**

### What are the system requirements?
- **Python 3.x** (tested on 3.8+)
- **OpenGL-compatible graphics** for 3D rendering
- **4GB+ RAM** recommended
- **Linux/Windows/Mac** (primarily tested on Linux)

### How do I install and run the game?
1. **Easy setup**: Simply run `./run_me.py` - it automatically creates a virtual environment and installs dependencies
2. **Manual setup**: Create virtual environment, install from `requirements.txt`, then run `python space_game.py`
3. **Dependencies**: Ursina Engine, NumPy, and Pillow (automatically installed)

### I'm getting Python/dependency errors. What should I do?
- Use the `run_me.py` script for automatic setup
- Ensure you have Python 3.x installed
- On Linux, you may need: `sudo apt install python3-dev python3-venv`
- For graphics issues, update your GPU drivers

---

## 🎯 **GAMEPLAY BASICS**

### What can I do in this game?
The game offers **multiple career paths**:
- **🛒 Merchant**: Trade commodities between planets for profit
- **⚔️ Warrior**: Take military contracts and fight pirates
- **🔭 Explorer**: Discover planets and investigate space anomalies  
- **🏛️ Diplomat**: Build relationships across all factions
- **🏴‍☠️ Pirate**: Attack merchants and raid trade routes

### How do the controls work?
**Space Flight:**
- **WASD**: Move ship in space
- **Mouse**: Steer and look around
- **Space/Shift**: Vertical movement up/down
- **Q/E**: Roll ship

**On Planets:**
- **WASD**: Walk around town
- **Mouse**: Look around (FPS-style)
- **Space**: Jump

**Interface:**
- **ESC**: Pause menu / Close interfaces
- **F6**: Screenshot
- **F7**: Toggle third-person view (space only)
- **F8**: Toggle between space and town modes

### How do I trade and make money?
1. **Land on planets** and find the **Trading Post** (large building)
2. **Press T** when near the trading post to open trading interface
3. **Buy low, sell high**: Each planet specializes in different goods
4. **Check multiple planets**: Prices vary dramatically by planet type
5. **Watch your cargo space**: Upgrade ship capacity as you progress

### How does the economy work?
The economy is **persistent and realistic**:
- **Finite stockpiles**: Planets have limited quantities of goods
- **Supply & demand**: Prices change based on availability
- **Production cycles**: Planets produce and consume goods daily
- **Your impact matters**: Large trades affect local market prices
- **Economic warfare**: Blockades and faction conflicts affect trade

---

## 👥 **CREW AND SHIP MANAGEMENT**

### How do I manage my crew?
1. **Visit Crew Quarters** in any town
2. **Press C** when near the building
3. **Hire specialists**: Gunners, pilots, engineers, medics improve performance
4. **Pay daily wages**: Crew must be paid or morale suffers
5. **Balance cost vs benefit**: Better crew costs more but provides significant bonuses

### What do different crew types do?
- **Gunners**: Improve combat effectiveness (+damage)
- **Pilots**: Increase ship speed and maneuverability  
- **Engineers**: Better fuel efficiency and faster repairs
- **Medics**: Heal ship damage over time
- **General Crew**: Basic ship operations (cheaper)

### How do I upgrade my ship?
1. **Visit the Shipyard** in any town
2. **Press U** when near the building
3. **Choose upgrades**: Cargo, engines, fuel efficiency, weapons, shields
4. **Costs increase**: Each upgrade level costs more than the last
5. **Plan strategically**: Balance cargo space vs combat capability

---

## 🏛️ **FACTIONS AND POLITICS**

### How many factions are there?
**6 major factions** with complex relationships:
- **Terran Federation**: Traditional human government
- **Mars Republic**: Independent Martian settlers
- **Jupiter Consortium**: Corporate mining operations
- **Outer Rim Pirates**: Lawless frontier raiders
- **Merchant Guild**: Trade and commerce focused
- **Independent Colonies**: Neutral frontier settlements

### How does reputation work?
- **Range**: -100 (Nemesis) to +100 (Hero) with each faction
- **Actions have consequences**: Help one faction, hurt their enemies
- **Affects gameplay**: Better reputation unlocks better missions and prices
- **Check standings**: Visit Embassy buildings and press R

### Can I be friendly with everyone?
**No** - the factions have conflicting interests. Helping the Federation may anger the Pirates, supporting corporate interests may upset Independent Colonies. Choose your allies carefully!

---

## 🎯 **MISSIONS AND PROGRESSION**

### How do I get missions?
1. **Visit Mission Boards** in towns
2. **Press M** when near the board
3. **Choose missions**: Different factions offer different types of work
4. **Reputation required**: Better missions need better faction standing
5. **Auto-completion**: Current missions complete automatically for demonstration

### What types of missions are available?
- **Delivery**: Transport goods between planets
- **Escort**: Protect merchant convoys
- **Patrol**: Eliminate pirates in specific sectors
- **Reconnaissance**: Gather intelligence on faction activities

### How do I progress in the game?
**No fixed ending** - create your own story:
- **Build wealth** through smart trading
- **Gain faction influence** through mission completion
- **Upgrade your ship** to take on bigger challenges
- **Manage crew morale** and ship efficiency
- **Explore space** and discover random encounters

---

## ⚔️ **COMBAT AND ENCOUNTERS**

### How does combat work?
- **Tactical system**: Success based on weapons, crew skills, and ship upgrades
- **Crew bonuses**: Gunners significantly improve combat effectiveness
- **Ship damage**: Take damage that requires repair over time
- **Strategic choices**: Sometimes avoiding fights is smarter than winning

### What random encounters can I find?
**4 types of space events**:
- **Derelict Ships**: Salvage opportunities with risk/reward choices
- **Pirate Encounters**: Combat situations with multiple response options
- **Merchant Convoys**: Trading or protection opportunities  
- **Asteroid Fields**: Navigation hazards with potential mining rewards

### Can I become a pirate?
**Yes!** Choose aggressive options in encounters and faction missions to become a space pirate. Attack merchants, raid trade routes, and build reputation with Outer Rim Pirates while becoming enemies of law-abiding factions.

---

## 💾 **TECHNICAL QUESTIONS**

### How do I save my game?
- **Press ESC** to open pause menu
- **Click "Save Game"** - saves to `savegame.pkl`
- **Auto-saves**: Game state persists between sessions
- **One save slot**: Currently supports one save file

### Can I take screenshots?
**Yes!** Press **F6** to take screenshots. They're saved to a `screenshots/` folder in the game directory.

### The game runs slowly. How can I improve performance?
- **Close other applications** to free up RAM
- **Update graphics drivers** for better OpenGL performance
- **Lower graphics settings** if available in future updates
- **Use dedicated graphics** instead of integrated graphics if possible

### I found a bug. Where do I report it?
The development team has already identified and fixed major bugs (see `BUG_FIXES_REPORT.md`). For new issues:
- **Check existing documentation** for known issues
- **Verify you're running the latest version**
- **Include error messages** and steps to reproduce

---

## 🎨 **GAMEPLAY TIPS & STRATEGIES**

### Best trading routes for beginners?
1. **Agricultural → Industrial**: Buy food cheap, sell to manufacturing planets
2. **Mining → Tech**: Transport minerals to technology-focused worlds
3. **Luxury routes**: High-profit margins but expensive initial investment

### How should I spend my first credits?
1. **Crew first**: Hire a gunner for safety and pilot for speed
2. **Cargo upgrades**: More space = more profit potential
3. **Engine upgrades**: Faster travel = more trading opportunities
4. **Weapons/shields**: Only if you plan to fight frequently

### What's the best faction to ally with?
**Depends on your playstyle**:
- **Merchant Guild**: Best for pure traders
- **Terran Federation**: Stable, lawful missions
- **Outer Rim Pirates**: High-risk, high-reward piracy
- **Independent Colonies**: Balanced approach

### How do I handle daily expenses?
- **Budget carefully**: Crew wages add up quickly
- **Plan trade routes**: Ensure you can afford crew before long journeys
- **Emergency funds**: Keep reserve credits for unexpected costs
- **Crew efficiency**: Happy crew costs less and performs better

---

## 🔮 **ADVANCED GAMEPLAY**

### How does the blockade system work?
- **Press B** in town mode to toggle blockades (testing feature)
- **Economic impact**: Reduces production, increases prices
- **Strategic opportunities**: Profit from shortages or help break blockades

### What are strategic reserves?
Planets keep **10 days of consumption** as strategic reserves - they won't sell below this amount. This prevents exploitation and maintains realistic economics.

### Can I manipulate markets?
**Yes!** Large trades affect local prices:
- **Buy in bulk**: Reduces available supply, increases prices
- **Flood markets**: Sell large quantities to crash prices
- **Economic warfare**: Support or damage faction economies through trading

### How do I fast-forward time?
**Press N** to advance time by one day (testing feature). Useful for:
- **Seeing economic changes** over time
- **Testing market fluctuations**
- **Advancing mission timers**

---

## 🎓 **FOR NEW PLAYERS**

### I'm overwhelmed. Where should I start?
1. **Learn basic flight**: Practice moving around in space
2. **Land on a planet**: Get familiar with town navigation
3. **Try simple trading**: Buy something cheap, sell somewhere else
4. **Hire one crew member**: See how crew management works
5. **Take an easy mission**: Build reputation slowly
6. **Explore gradually**: The game reveals its depth over time

### What's the learning curve like?
- **Easy to start**: Basic flight and trading are intuitive
- **Moderate complexity**: Faction relationships and crew management add depth
- **Rich mastery**: Economic manipulation and political maneuvering for experts

### Is there a tutorial?
**Currently no in-game tutorial**, but:
- **README.md**: Essential controls and concepts
- **This FAQ**: Comprehensive gameplay information
- **Game prompts**: On-screen instructions for most activities
- **Learn by doing**: The game is forgiving and encourages experimentation

---

## 🌟 **WHAT MAKES THIS GAME SPECIAL?**

### How is this different from other space games?
- **Pirates! inspiration**: Captures the political intrigue and economic gameplay of the classic
- **Persistent economy**: Your actions have lasting impact on the game world
- **Multiple viable paths**: No "right" way to play - create your own story
- **Faction complexity**: Rich political relationships affect every aspect of gameplay
- **Crew personality**: Individual crew members with skills and wages

### What's the most unique feature?
**The persistent economy** - planets have finite resources, realistic production cycles, and remember your trading history. Unlike games with infinite goods at fixed prices, ILK creates a living economic simulation that responds to your actions.

---

*This FAQ covers the major aspects of ILK Space Game. The game is deep and rewards exploration - don't be afraid to experiment and create your own space-faring story!*