# ILK Space Game - Troubleshooting Guide

## 🚨 **QUICK FIXES FOR COMMON ISSUES**

### **Game Won't Start**
1. **Use the automatic launcher**: Run `./run_me.py` instead of direct game launch
2. **Check Python version**: Ensure Python 3.x is installed (`python3 --version`)
3. **Dependencies missing**: The launcher will auto-install required packages
4. **Virtual environment**: The launcher creates and manages this automatically

### **Controls Not Working**
1. **Check game focus**: Click on the game window to ensure it has input focus
2. **Mouse locked**: If mouse is stuck, press **ESC** to unlock
3. **Keyboard layout**: Game uses QWERTY layout (WASD movement)
4. **Wrong mode**: Ensure you're in the correct mode (space vs town) for the controls

### **Can't See Anything/Black Screen**
1. **Graphics drivers**: Update your GPU drivers
2. **OpenGL support**: Ensure your system supports OpenGL 3.0+
3. **Skybox loading**: Wait a few seconds for textures to load
4. **Camera position**: Press **F7** to toggle third-person view in space

---

## 🔧 **INSTALLATION TROUBLESHOOTING**

### **Python Installation Issues**

**Problem**: "Python not found" or "python3 command not found"
```bash
# Linux/Ubuntu
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Windows - Download from python.org
# macOS - Use Homebrew or python.org installer
```

**Problem**: Permission denied when creating virtual environment
```bash
# Linux - Install python3-venv
sudo apt install python3-venv

# Windows - Run as administrator
# macOS - Check user permissions
```

### **Dependency Installation Problems**

**Problem**: "No module named 'ursina'" or similar
**Solution**: 
```bash
# Let run_me.py handle it automatically
./run_me.py

# Or manual installation
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

**Problem**: Ursina installation fails
**Solution**:
```bash
# Try specific version
pip install ursina==5.2.0

# If that fails, try development version
pip install git+https://github.com/pokepetter/ursina.git
```

### **Graphics/OpenGL Issues**

**Problem**: "OpenGL version too old" or graphics errors
**Solutions**:
1. **Update graphics drivers** (most common fix)
2. **Install OpenGL libraries**:
   ```bash
   # Linux
   sudo apt install libgl1-mesa-dev libglu1-mesa-dev
   
   # Additional packages sometimes needed
   sudo apt install python3-opengl
   ```
3. **Use software rendering** (slower but compatible):
   ```bash
   export MESA_GL_VERSION_OVERRIDE=3.3
   export MESA_GLSL_VERSION_OVERRIDE=330
   ```

---

## 🎮 **GAMEPLAY TROUBLESHOOTING**

### **Can't Land on Planets**

**Problem**: Landing prompt doesn't appear
**Solutions**:
1. **Get closer**: Fly directly towards the planet until very close
2. **Check game mode**: Ensure you're in space mode (not town mode)
3. **Planet detection**: Try approaching different planets
4. **Speed**: Slow down when approaching planets

**Problem**: Landing prompt appears but buttons don't work
**Solutions**:
1. **Mouse focus**: Click on the game window first
2. **Use mouse clicks**: Click the "Land" button directly
3. **Keyboard alternative**: Try pressing **F8** to toggle modes

### **Trading Problems**

**Problem**: Can't access trading post
**Solutions**:
1. **Get closer**: Walk right up to the trading post building
2. **Correct key**: Press **T** (not any other key)
3. **Building location**: Look for the large rectangular building
4. **Game mode**: Ensure you're in town mode (landed on planet)

**Problem**: "No market data" or trading interface empty
**Solutions**:
1. **Generate market**: The game auto-generates markets on first visit
2. **Wait**: Give the system a moment to initialize
3. **Try different planet**: Some planets may have limited markets

**Problem**: Can't buy/sell items
**Solutions**:
1. **Check funds**: Ensure you have enough credits
2. **Cargo space**: Check if your cargo hold is full
3. **Availability**: Some items may be out of stock
4. **Correct keys**: Use number keys 1-8 to buy, Shift+1-8 to sell

### **Crew Management Issues**

**Problem**: Can't hire crew
**Solutions**:
1. **Find crew quarters**: Look for the crew quarters building
2. **Get close**: Must be within range of the building
3. **Press C**: Use the crew management key
4. **Check funds**: Hiring costs money upfront
5. **Crew limit**: You may have reached maximum crew size

**Problem**: Crew wages are too expensive
**Solutions**:
1. **Start small**: Hire only essential crew initially
2. **Fire expensive crew**: Use F to fire crew members
3. **Build wealth first**: Focus on trading to increase income
4. **Upgrade gradually**: Add crew as your income grows

### **Mission System Problems**

**Problem**: No missions available
**Solutions**:
1. **Check reputation**: Low reputation limits mission access
2. **Try different planets**: Different planets offer different missions
3. **Wait for generation**: Missions auto-generate over time
4. **Improve faction standing**: Complete easier missions first

**Problem**: Can't complete missions
**Solutions**:
1. **Current system**: Missions auto-complete for demonstration
2. **Check mission board**: Return to mission board to see progress
3. **Faction requirements**: Ensure you meet reputation requirements

### **Combat and Encounters**

**Problem**: Losing all combat encounters
**Solutions**:
1. **Hire gunners**: Crew specialists significantly improve combat
2. **Upgrade weapons**: Visit shipyards to improve combat systems
3. **Avoid early fights**: Build up before engaging in combat
4. **Strategic choices**: Some encounters offer non-combat options

**Problem**: No random encounters
**Solutions**:
1. **Fly in open space**: Encounters happen away from planets
2. **Give it time**: Encounters are random and take time
3. **Keep moving**: Stay active in space exploration

---

## 💾 **SAVE/LOAD ISSUES**

### **Save Game Problems**

**Problem**: Can't save game
**Solutions**:
1. **Use pause menu**: Press ESC and click "Save Game"
2. **Check permissions**: Ensure game can write to directory
3. **Disk space**: Verify adequate free disk space

**Problem**: Save file corrupted
**Solutions**:
1. **Backup saves**: Manually backup `savegame.pkl` file
2. **Start fresh**: Delete save file to start new game
3. **Check file permissions**: Ensure save file isn't read-only

### **Load Game Problems**

**Problem**: Can't load saved game
**Solutions**:
1. **File exists**: Verify `savegame.pkl` exists in game directory
2. **Correct directory**: Ensure you're running from correct folder
3. **Save format**: Don't edit save files manually

---

## 🖥️ **PERFORMANCE ISSUES**

### **Game Running Slowly**

**Solutions**:
1. **Close other programs**: Free up RAM and CPU
2. **Update drivers**: Especially graphics drivers
3. **Lower expectations**: Game is Python-based, not ultra high-performance
4. **Check specs**: Ensure you meet minimum requirements

### **Frame Rate Issues**

**Solutions**:
1. **Dedicated graphics**: Use discrete GPU instead of integrated
2. **Graphics settings**: Future updates may include quality settings
3. **Resolution**: Try running at lower screen resolution
4. **Background apps**: Close unnecessary programs

### **Memory Problems**

**Solutions**:
1. **Restart game**: Clears memory issues
2. **System RAM**: Ensure adequate free memory
3. **Virtual environment**: Helps isolate memory usage

---

## 🔍 **DEBUGGING TIPS**

### **Getting More Information**

**Console Output**:
- Run from terminal/command prompt to see debug messages
- Error messages will appear in console
- Economic information displays via console commands

**Debug Commands**:
- **I key**: Show detailed economic information (in town)
- **B key**: Toggle blockades for testing (in town)
- **N key**: Fast-forward time by one day

### **Log Information**

**Check for messages**:
- Look for print statements in console
- Economic shortages are reported
- Mission completion messages appear
- Trading results are displayed

---

## 🌐 **PLATFORM-SPECIFIC ISSUES**

### **Linux Issues**

**Problem**: Missing development packages
```bash
sudo apt install python3-dev python3-venv
sudo apt install libgl1-mesa-dev libglu1-mesa-dev
sudo apt install python3-tk  # Sometimes needed
```

**Problem**: Audio system conflicts (even though game has no audio)
```bash
# Can sometimes interfere with Ursina
sudo apt install pulseaudio-utils
```

### **Windows Issues**

**Problem**: "Permission denied" errors
**Solutions**:
1. **Run as administrator**: Right-click and "Run as administrator"
2. **Antivirus**: Temporarily disable or add exception
3. **Windows Defender**: Add game folder to exclusions

**Problem**: Python not in PATH
**Solutions**:
1. **Reinstall Python**: Check "Add to PATH" during installation
2. **Manual PATH**: Add Python directory to system PATH
3. **Use full path**: `C:\Python3X\python.exe` instead of `python`

### **macOS Issues**

**Problem**: "Command not found: python3"
**Solutions**:
```bash
# Install via Homebrew
brew install python3

# Or use system Python with explicit path
/usr/bin/python3
```

**Problem**: Permission issues
**Solutions**:
- Use `sudo` when installing system packages
- Consider using Homebrew for package management
- Check security settings for running downloaded software

---

## 🆘 **WHEN ALL ELSE FAILS**

### **Fresh Installation**

1. **Delete everything**: Remove game folder completely
2. **Re-download**: Get fresh copy of all files
3. **Clean Python**: Create new virtual environment
4. **Step-by-step**: Follow installation guide exactly

### **Minimal Test**

```bash
# Test Python installation
python3 --version

# Test basic dependencies
python3 -c "import ursina; print('Ursina OK')"

# Test game compilation
python3 -m py_compile space_game.py
```

### **System Requirements Check**

**Minimum Requirements**:
- Python 3.8 or higher
- OpenGL 3.0+ support
- 4GB RAM
- 100MB disk space
- Mouse and keyboard

**Verify OpenGL**:
```bash
# Linux
glxinfo | grep "OpenGL version"

# Windows - Use GPU-Z or similar
# macOS - Check "About This Mac" > System Report > Graphics
```

---

## 📞 **GETTING HELP**

### **Before Asking for Help**

1. **Read error messages**: They often contain the solution
2. **Check existing documentation**: README, FAQ, this guide
3. **Try basic fixes**: Restart, update, reinstall
4. **Gather information**: OS version, Python version, error messages

### **What Information to Include**

When reporting issues:
- **Operating System**: Windows/Linux/macOS version
- **Python Version**: Output of `python3 --version`
- **Error Messages**: Exact text of any errors
- **Steps to Reproduce**: What you were doing when it failed
- **Game State**: What you were trying to accomplish

### **Known Limitations**

**Current alpha limitations**:
- No audio system
- Single save slot
- Limited graphics settings
- Python performance constraints
- No multiplayer support

**These are design limitations, not bugs.**

---

## ✅ **VERIFICATION CHECKLIST**

**If game works properly, you should be able to**:
- ✅ Launch game using `./run_me.py`
- ✅ See space environment with rotating skybox
- ✅ Move around using WASD and mouse
- ✅ Approach and land on planets
- ✅ Navigate town environments
- ✅ Access trading interface (T key)
- ✅ Buy and sell commodities
- ✅ Access other building interfaces
- ✅ Save and load game (ESC menu)
- ✅ Take screenshots (F6)

**If any of these don't work, refer to the relevant troubleshooting section above.**

---

*This troubleshooting guide covers the most common issues. The ILK Space Game is stable and well-tested, so most problems are installation or environment-related rather than game bugs.*