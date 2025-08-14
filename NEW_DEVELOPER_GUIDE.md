# NEW DEVELOPER GUIDE - ILK SPACE GAME
## Complete Onboarding for New Developers

**Target Audience:** Developers with basic coding knowledge who are new to this codebase  
**Goal:** Get you productive and contributing within 30 minutes  
**Prerequisites:** Basic Python knowledge, understanding of object-oriented programming  

---

## 🚀 **QUICK START (5 Minutes)**

### **Step 1: Understand What You're Looking At**
```
ILK Space Game = 3D Space Trading Game (like Sid Meier's Pirates! but in space)
Main File = space_game.py (10,006 lines - everything is in one file)
Game Engine = Ursina (3D Python game engine)
Language = Python 3.7+
```

### **Step 2: Run the Game**
```bash
# Option 1: Auto-setup (recommended)
python run_me.py

# Option 2: Manual setup
pip install -r requirements.txt
python space_game.py
```

### **Step 3: Play the Game (5 minutes)**
- **WASD** - Move in space
- **Mouse** - Look around
- **T** - Trade when near trading posts
- **I** - Open inventory
- **ESC** - Pause menu

---

## 📚 **UNDERSTANDING THE CODEBASE (10 Minutes)**

### **File Structure Overview**
```
space_game.py              # MAIN FILE - Everything is here
├── Headless Mode Setup    # Lines 1-300
├── Ship Classes          # Lines 500-600
├── Economic Systems      # Lines 800-1500
├── Faction Systems       # Lines 6000-7000
├── UI Systems           # Lines 8000-9000
└── Game Loop            # Lines 9000-10006

Other Files:
├── run_me.py            # Auto-setup launcher
├── requirements.txt     # Python dependencies
└── assets/textures/     # Game images
```

### **Key Concepts to Understand**

#### **1. Everything is in One File**
- All game systems are in `space_game.py`
- This makes it easy to find things (use Ctrl+F)
- No complex import chains to understand

#### **2. Clear Class Names**
- `ShipClass` - Different types of ships
- `Commodity` - Trade goods
- `Faction` - Political groups
- `Planet` - Places to visit
- `PlayerWallet` - Player's money

#### **3. Simple Architecture**
```
Game Loop → Update Systems → Draw Screen
    ↓
Player Input → Game Logic → Update State
```

---

## 🔍 **HOW TO FIND THINGS (5 Minutes)**

### **Common Tasks and Where to Look**

#### **"I want to change ship speed"**
1. Search for "speed" in `space_game.py`
2. Look for `ShipStats` class (around line 523)
3. Find the ship class you want to modify
4. Change the speed value

#### **"I want to add a new commodity"**
1. Search for "Commodity" class (around line 815)
2. Look at how existing commodities are defined
3. Add your new commodity following the same pattern

#### **"I want to change trading prices"**
1. Search for "base_price" or "current_price"
2. Look in the `Commodity` class or `MarketSystem` class
3. Modify the price calculation logic

#### **"I want to add a new planet"**
1. Search for "Planet" class (around line 5251)
2. Look at how planets are created
3. Add your new planet following the same pattern

### **Search Tips**
- **Use Ctrl+F** to search within the file
- **Search for class names** to find systems
- **Search for variable names** to find specific features
- **Look at line numbers** in the comments to jump to sections

---

## 🛠️ **COMMON DEVELOPMENT TASKS (10 Minutes)**

### **Task 1: Adding a New Ship Class**

#### **What You Need to Know:**
- Ships are defined in the `ShipClass` enum (around line 510)
- Ship stats are in the `ShipStats` class (around line 523)
- Each ship has: health, speed, cargo, combat power, etc.

#### **Step-by-Step:**
1. Find the `ShipClass` enum (search for "class ShipClass")
2. Add your new ship type: `YOUR_SHIP = "Your Ship"`
3. Find the `SHIP_STATS` dictionary (around line 550)
4. Add stats for your ship: `ShipClass.YOUR_SHIP: ShipStats(...)`

#### **Example:**
```python
# In ShipClass enum
EXPLORER = "Explorer"

# In SHIP_STATS dictionary
ShipClass.EXPLORER: ShipStats(300, 20, 150, 90, 0.7, 200, 30, 500, 3, 350000),
```

### **Task 2: Adding a New Commodity**

#### **What You Need to Know:**
- Commodities are defined in the `Commodity` class (around line 815)
- Each commodity has: name, base price, type
- Commodities affect trading and economy

#### **Step-by-Step:**
1. Find where commodities are created (search for "Commodity(")
2. Add your new commodity following the same pattern
3. Make sure to add it to the commodity list

#### **Example:**
```python
# Add to commodity list
"Plasma": Commodity("Plasma", 120.0, CommodityType.TECHNOLOGY),
```

### **Task 3: Changing Game Balance**

#### **What You Need to Know:**
- Most game values are defined as constants
- Look for numbers that seem like game parameters
- Test your changes by running the game

#### **Common Balance Changes:**
- **Starting money**: Search for "credits" and "1000"
- **Ship prices**: Search for ship costs in `SHIP_STATS`
- **Trading prices**: Search for "base_price" in commodities
- **Movement speed**: Search for "speed" in ship stats

---

## 🐛 **DEBUGGING GUIDE (5 Minutes)**

### **Common Issues and Solutions**

#### **"The game won't start"**
1. Check Python version: `python --version` (needs 3.7+)
2. Install dependencies: `pip install -r requirements.txt`
3. Check for error messages in the console
4. Try running: `python run_me.py --verbose`

#### **"I can't find what I'm looking for"**
1. Use the search function (Ctrl+F)
2. Check the `NAVIGATION_GUIDE.md` file
3. Look at the `CLASS_FUNCTION_INDEX.md` file
4. Search for keywords related to what you want to change

#### **"My changes aren't working"**
1. Make sure you saved the file
2. Restart the game completely
3. Check for syntax errors (Python will show them)
4. Look at the console for error messages

#### **"I don't understand this code"**
1. Read the comments - they explain everything
2. Look at similar code for examples
3. Check the `COMMENTING_GUIDE.md` file
4. Ask questions in the project documentation

### **Debugging Tools**

#### **Console Output**
- The game prints helpful messages to the console
- Look for error messages and warnings
- Use `python run_me.py --verbose` for more details

#### **Log Files**
- Check `space_game.log` for detailed error information
- Logs show what the game is doing and where errors occur

#### **Testing Mode**
- Run `python run_me.py --test` to run automated tests
- Tests will help identify if your changes broke something

---

## 📖 **LEARNING RESOURCES (5 Minutes)**

### **Files to Read (in order)**
1. **`README.md`** - Project overview and features
2. **`NAVIGATION_GUIDE.md`** - How to find things quickly
3. **`CLASS_FUNCTION_INDEX.md`** - What each class and function does
4. **`COMMENTING_GUIDE.md`** - How the code is documented
5. **`SYSTEM_ARCHITECTURE.md`** - How everything fits together

### **Key Concepts to Learn**
- **Game Loop**: How games update 60 times per second
- **3D Coordinates**: X, Y, Z positioning system
- **Object-Oriented Programming**: Classes and inheritance
- **Event-Driven Programming**: How user input works
- **State Management**: How game data is stored and updated

### **Python Concepts Used**
- **Classes and Objects**: Everything is organized in classes
- **Dictionaries**: Used for storing data (like ship stats)
- **Lists**: Used for collections (like planets, commodities)
- **Functions**: Used for actions (like movement, trading)
- **Imports**: How different parts of the code connect

---

## 🎯 **FIRST CONTRIBUTION (10 Minutes)**

### **Suggested First Tasks**

#### **Easy Tasks (Good for beginners)**
1. **Change starting money**: Find where credits are set to 1000 and change it
2. **Add a new commodity**: Follow the pattern of existing commodities
3. **Change ship names**: Modify the names in the `ShipClass` enum
4. **Adjust trading prices**: Change base prices in the commodity definitions

#### **Medium Tasks (Some experience needed)**
1. **Add a new planet**: Create a new planet with different characteristics
2. **Modify ship stats**: Change health, speed, or cargo capacity
3. **Add new UI text**: Modify help messages or game text
4. **Change game balance**: Adjust various game parameters

#### **Advanced Tasks (More complex)**
1. **Add new game mechanics**: Create new systems or features
2. **Modify the UI**: Change how the game looks and feels
3. **Add new game modes**: Create different ways to play
4. **Optimize performance**: Make the game run faster

### **How to Submit Changes**
1. **Test your changes**: Make sure the game still works
2. **Document what you did**: Add comments explaining your changes
3. **Keep it simple**: Start with small, focused changes
4. **Ask for help**: Use the documentation and comments as guides

---

## 🆘 **GETTING HELP (5 Minutes)**

### **When You're Stuck**
1. **Read the comments**: They explain everything in detail
2. **Check the documentation**: Use the guide files listed above
3. **Look at similar code**: Find examples of what you want to do
4. **Test small changes**: Make small modifications and test them
5. **Use the search function**: Find relevant code quickly

### **Common Questions**
- **"Where is the main game loop?"** - Search for "def update" or "game loop"
- **"How do I add a new feature?"** - Look at similar features and copy the pattern
- **"What does this variable do?"** - Read the comments next to the variable
- **"How do I test my changes?"** - Run the game and try the feature you modified

### **Best Practices**
- **Start small**: Make tiny changes and test them
- **Read the comments**: They're there to help you
- **Follow patterns**: Copy existing code structure
- **Test everything**: Make sure your changes work
- **Ask questions**: Use the documentation as your guide

---

## 🎉 **YOU'RE READY!**

### **What You Can Do Now**
- ✅ Understand the codebase structure
- ✅ Find specific features and systems
- ✅ Make simple modifications
- ✅ Debug common issues
- ✅ Contribute to the project

### **Next Steps**
1. **Try the quick start** - Run the game and play for 5 minutes
2. **Pick a simple task** - Start with changing a number or adding text
3. **Read the documentation** - Use the guide files when you need help
4. **Make your first contribution** - Add something small and test it
5. **Learn more** - Explore the codebase and understand how it works

### **Remember**
- **Everything is documented** - Read the comments!
- **Start simple** - Don't try to change everything at once
- **Test your changes** - Make sure the game still works
- **Ask for help** - Use the documentation and search functions
- **Have fun** - This is a game, so enjoy working on it!

---

*This guide is designed to get you productive quickly. The codebase is well-documented and organized, so you can focus on making changes rather than figuring out how things work. Good luck and happy coding!*