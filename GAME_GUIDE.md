# Space Pirates Game Guide

## Your Game is Fixed! 🎉

Your space exploration game has been completely restored and enhanced with all the sophisticated systems that were previously missing. The game now includes:

## ✅ Fixed & Enhanced Systems

### **Trading System**
- 9 different trade items (Food, Water, Fuel, Medicine, Electronics, Weapons, Luxury Goods, Spice, Energy Crystals)
- Market dynamics with supply/demand and price fluctuations
- 4 rarity levels: Common, Uncommon, Rare, Legendary
- Reputation affects trading prices
- Cargo management with capacity limits

### **Economy System**
- Credit management with transaction history
- Different transaction types (trade, combat, missions, repairs)
- Reputation multipliers affect earnings
- Costs for repairs, fuel, upgrades, and docking

### **Ship System**
- 4 ship types: Starter, Medium, Heavy, Elite
- Ship attributes: Health, Shield, Fuel, Cargo capacity, Speed, Damage
- Upgrade system: Engine, Shield, Cargo, Weapon upgrades
- Ship status tracking and damage system

### **Mission System**
- 4 mission types: Trade, Combat, Exploration, Delivery
- Dynamic mission generation with rewards
- Mission difficulty scaling
- Progress tracking

### **NPC System**
- 5 unique NPCs with different factions and personalities
- 4 factions: Trade Federation, Space Navy, Pirates, Independent Traders
- NPC relationships and reputation tracking

### **Combat System**
- Ship-to-ship combat with multiple states
- Damage calculations and boarding mechanics
- Combat rewards and experience
- Random enemy encounters

### **Faction System**
- 4 major factions with territories and relationships
- Reputation affects available services and prices
- Faction-controlled ports and services

### **Port System**
- 4 major ports: New Terra, Nova Prime, Shadow Port, Freeport
- Different services: Market, Shipyard, Missions, Repairs
- Faction-controlled with reputation requirements
- Docking fees based on reputation

### **Weather System**
- 7 weather types affecting gameplay
- Dynamic weather changes during travel
- Weather affects ship performance and encounters

### **Progression System**
- Experience and leveling system
- 4 skill trees: Combat, Trading, Piloting, Engineering
- Skill points allocation
- Level-based unlocks

## 🎮 How to Play

### **Running the Game**

**In a normal environment with display:**
```bash
python3 space_game.py
```

**In a headless/remote environment:**
```bash
python3 space_game.py --headless
```

### **Available Commands**

| Command | Description |
|---------|-------------|
| `help` | Show all available commands |
| `status` | Show detailed ship and player status |
| `trade` | Access trading interface (buy/sell items) |
| `missions` | View and accept available missions |
| `dock <port>` | Dock at a port (new_terra, nova_prime, shadow_port, freeport) |
| `combat` | Start a random combat encounter |
| `travel <location>` | Travel to a new location |
| `repair` | Repair ship damage (costs credits) |
| `refuel` | Refuel ship (costs credits) |
| `upgrade <system>` | Upgrade ship systems (engine, shield, cargo, weapon) |
| `npcs` | View NPCs in current area |
| `faction` | View faction standings |
| `save` | Save game progress |
| `quit` | Exit game |

### **Getting Started**

1. **Check your status**: Type `status` to see your ship condition, credits, and level
2. **Explore ports**: Use `dock new_terra` to visit the main trading hub
3. **Start trading**: Use `trade` to buy low and sell high
4. **Take missions**: Use `missions` to see available contracts
5. **Combat**: Use `combat` for random encounters to earn credits and XP
6. **Upgrade**: Use `repair`, `refuel`, and `upgrade` to improve your ship

### **Trading Strategy**
- Check market prices with the trade menu
- Buy items where they're cheap, sell where they're expensive
- Higher rarity items (Rare, Legendary) have better profit margins
- Build reputation with factions for better prices

### **Combat Tips**
- Keep your ship repaired and fueled
- Combat gives both credits and experience
- Higher level = better rewards
- Upgrade your weapons for better damage

### **Ports Guide**
- **New Terra**: Main trading hub (Trade Federation)
- **Nova Prime**: Secondary trade port (Trade Federation)  
- **Shadow Port**: Pirate haven, cheaper repairs (Pirates)
- **Freeport**: Independent trading post (Independents)

### **Progression**
- Gain experience through combat, missions, and trading
- Level up to unlock skill points
- Spend skill points on Combat, Trading, Piloting, or Engineering
- Higher skills improve performance in those areas

## 🔧 Technical Details

### **3D Mode Features** (when not headless)
- Full 3D space environment with planets
- Mouse look and WASD movement
- Real-time HUD showing ship status
- Visual weather effects and space atmosphere

### **Text Mode Features** (headless mode)
- Complete command-line interface
- All game systems accessible via text commands
- Perfect for remote server environments
- Save/load functionality

### **Save System**
- Saves to `saves/` directory
- JSON format with timestamps
- Includes all player progress, ship status, and game state

## 🚀 What's New

Your game has been transformed from a basic space exploration demo into a full-featured space trading and combat game inspired by classics like Sid Meier's Pirates! The core gameplay loop now includes:

1. **Trade** goods between ports for profit
2. **Combat** pirates and enemies for rewards  
3. **Complete missions** for factions
4. **Upgrade your ship** and skills
5. **Build reputation** with different factions
6. **Explore** the galaxy with dynamic weather and encounters

The game is now fully playable with dozens of hours of gameplay, complex economic systems, and meaningful progression!

## 🎯 Example Gaming Session

```
[Deep Space] > status
[Shows ship health, credits, level]

[Deep Space] > dock new_terra
[Docks at main trading port]

[New Terra] > trade
[Access trading interface, buy cheap goods]

[New Terra] > missions  
[Accept a delivery mission]

[New Terra] > travel nova_prime
[Travel to destination, random encounter might occur]

[Nova Prime] > trade
[Sell goods for profit, complete delivery mission]

[Nova Prime] > upgrade weapon
[Spend credits on ship improvements]

[Nova Prime] > combat
[Random combat encounter for XP and credits]
```

Your space adventure awaits, Captain! 🚀