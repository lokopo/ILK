# QUICK REFERENCE CARD - ILK SPACE GAME
## Instant Access to Essential Information

**Purpose:** This card provides instant access to the most important information for newcomers and LLMs working with the ILK Space Game codebase.

---

## 🚀 **INSTANT START**

### **Run the Game**
```bash
# Auto-setup (recommended)
python run_me.py

# Manual setup
pip install -r requirements.txt
python space_game.py
```

### **Key Files**
- **`space_game.py`** - Main game file (10,006 lines)
- **`run_me.py`** - Auto-setup launcher
- **`requirements.txt`** - Python dependencies

---

## 🔍 **FIND ANYTHING QUICKLY**

### **Search Strategies**
```python
# Find classes
"class ShipClass"          # Ship definitions
"class Commodity"          # Trading goods
"class Faction"            # Political entities
"class Planet"             # World objects

# Find functions
"def handle_text_command"  # Command processing
"def show_text_help"       # Help system
"def text_fly_to_planet"   # Navigation

# Find variables
"self.text_player_pos"     # Player position
"self.text_fuel"           # Fuel system
"player_wallet.credits"    # Money system
```

### **Line Number Quick Reference**
```
Lines 1-300:     Headless mode setup
Lines 500-600:   Ship classes and stats
Lines 800-1500:  Economic systems
Lines 6000-7000: Faction systems
Lines 8000-9000: UI systems
Lines 9000-10006: Game loop
```

---

## 🎮 **COMMON TASKS**

### **Add New Ship**
```python
# 1. Add to ShipClass enum
class ShipClass(Enum):
    NEW_SHIP = "New Ship"

# 2. Add to SHIP_STATS
SHIP_STATS = {
    ShipClass.NEW_SHIP: ShipStats(
        health=400, speed=25, cargo=200, combat=110,
        efficiency=0.6, crew=40, maintenance=20,
        range=600, weapons=4, cost=450000
    ),
}
```

### **Add New Commodity**
```python
# Add to commodity definitions
COMMODITIES = {
    "New Good": Commodity(
        name="New Good",
        base_price=85.0,
        commodity_type=CommodityType.TECHNOLOGY
    ),
}
```

### **Add New Command**
```python
# 1. Add to command handler
def handle_text_command(self, command):
    elif command == "newcommand":
        self.handle_new_command()

# 2. Implement handler
def handle_new_command(self):
    print("🆕 New command executed!")

# 3. Add to help
def show_text_help(self):
    print("  newcommand     - Description")
```

---

## 🐛 **DEBUGGING QUICK FIXES**

### **Common Issues**
```python
# Game won't start
python --version  # Check Python 3.7+
pip install -r requirements.txt  # Install dependencies

# Can't find code
Ctrl+F "class ShipClass"  # Search for classes
Ctrl+F "def handle_text"  # Search for functions

# Changes not working
# 1. Save the file
# 2. Restart the game
# 3. Check console for errors
```

### **Error Messages**
```python
# Syntax Error
# Check for missing colons, parentheses, quotes

# Import Error
# Check requirements.txt and install dependencies

# Runtime Error
# Check console output for specific error details
```

---

## 📚 **ESSENTIAL DOCUMENTATION**

### **Must-Read Files (in order)**
1. **`README.md`** - Project overview
2. **`NEW_DEVELOPER_GUIDE.md`** - Step-by-step guide
3. **`NAVIGATION_GUIDE.md`** - How to find things
4. **`CLASS_FUNCTION_INDEX.md`** - What everything does
5. **`CODE_PATTERNS_LIBRARY.md`** - Reusable templates

### **LLM-Specific Files**
- **`LLM_DEVELOPMENT_GUIDE.md`** - AI assistant guide
- **`COMMENTING_GUIDE.md`** - Documentation patterns
- **`SYSTEM_ARCHITECTURE.md`** - How systems work

---

## 🎯 **DEVELOPMENT WORKFLOW**

### **Quick Development Process**
1. **Find the code** - Use search (Ctrl+F)
2. **Read comments** - Everything is documented
3. **Copy patterns** - Use existing code as template
4. **Test changes** - Run the game and verify
5. **Document** - Add comments explaining changes

### **Testing Checklist**
- [ ] Game starts without errors
- [ ] New feature works as expected
- [ ] No existing features broken
- [ ] Error handling works
- [ ] Documentation updated

---

## 🔧 **USEFUL COMMANDS**

### **Game Commands (Text Mode)**
```
help          - Show all commands
status        - Show player status
planets       - List all planets
fly <planet>  - Travel to planet
trade         - Open trading
wallet        - Show credits
fleet         - Show fleet status
character     - Show character info
scan          - Scan for objects
quit          - Exit game
```

### **Development Commands**
```bash
# Run in different modes
python run_me.py              # Normal mode
python run_me.py --headless   # Text mode
python run_me.py --test       # Test mode
python run_me.py --verbose    # Debug mode

# Check Python version
python --version

# Install dependencies
pip install -r requirements.txt
```

---

## 📊 **KEY SYSTEMS**

### **Game Systems**
- **Ship System** - 10 ship classes with stats
- **Economic System** - 8 commodity types with dynamic pricing
- **Faction System** - 6 factions with relationships
- **Planet System** - Multiple planets with economies
- **Trading System** - Buy/sell commodities
- **Combat System** - Ship battles and boarding
- **Mission System** - Dynamic contracts and quests

### **UI Systems**
- **TradingUI** - Commodity trading interface
- **MissionUI** - Mission and contract interface
- **MapUI** - Navigation and exploration
- **FactionUI** - Political relationships
- **CrewUI** - Crew management
- **UpgradeUI** - Ship upgrades and modifications

---

## 🎨 **CODE PATTERNS**

### **Class Template**
```python
class NewClass:
    """
    Brief description of what this class does.
    
    Attributes:
        attribute1 (type): Description
        attribute2 (type): Description
    """
    
    def __init__(self, parameter):
        """Initialize the class."""
        self.attribute1 = parameter
        self.attribute2 = None
    
    def method_name(self):
        """Brief description of method."""
        # Implementation with comments
        pass
```

### **Function Template**
```python
def function_name(self, parameter):
    """
    Brief description of what this function does.
    
    Args:
        parameter (type): Description
        
    Returns:
        type: Description
        
    Example:
        >>> function_name("test")
        "result"
    """
    # Implementation with comments
    return result
```

---

## 🆘 **GETTING HELP**

### **When Stuck**
1. **Read the comments** - Everything is documented
2. **Search the code** - Use Ctrl+F to find things
3. **Check documentation** - Use the guide files
4. **Look at examples** - Copy existing patterns
5. **Test small changes** - Make tiny modifications

### **Common Questions**
- **"Where is X?"** - Search for "class X" or "def X"
- **"How do I add Y?"** - Look at similar Y in the code
- **"Why isn't Z working?"** - Check console for errors
- **"What does this do?"** - Read the comments next to it

---

## 📈 **SUCCESS METRICS**

### **For New Developers**
- ✅ Can run the game
- ✅ Can find specific code
- ✅ Can make simple changes
- ✅ Can add new features
- ✅ Can debug issues

### **For LLMs**
- ✅ Can understand code structure
- ✅ Can follow existing patterns
- ✅ Can implement new features
- ✅ Can debug and fix issues
- ✅ Can maintain code quality

---

## 🎉 **YOU'RE READY!**

### **What You Can Do Now**
- Find any code in the codebase
- Make simple modifications
- Add new features
- Debug common issues
- Contribute to the project

### **Remember**
- **Everything is documented** - Read the comments!
- **Use search** - Ctrl+F is your friend
- **Follow patterns** - Copy existing code
- **Test everything** - Make sure it works
- **Have fun** - This is a game!

---

*This quick reference card provides instant access to the most important information for working with the ILK Space Game codebase. Keep it handy for quick lookups!*