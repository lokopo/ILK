# Persistent Economy System Testing Plan

## 🎯 **Testing Goals**
Verify that the new persistent economy system provides realistic, non-exploitable trading with:
- ✅ Planets have finite, trackable stockpiles
- ✅ Trade actually depletes/increases planet supplies  
- ✅ Blockades effectively starve planets
- ✅ No infinite resource generation
- ✅ Realistic supply/demand economics

## 🧪 **Test Plan**

### **Test 1: Basic Persistence Verification**
**Goal**: Ensure planet stockpiles persist and are affected by trade

**Steps**:
1. Start game, land on a planet
2. Press `I` to view initial stockpiles
3. Buy 10 units of a commodity (e.g., food)
4. Press `I` again to verify stockpile decreased
5. Leave planet and return
6. Press `I` to verify stockpile is still reduced (persistence test)

**Expected Result**: Stockpiles should decrease with purchases and remain changed after leaving/returning

### **Test 2: Supply Exhaustion**
**Goal**: Verify planets can run out of commodities

**Steps**:
1. Find a planet with low food supply
2. Buy all available food (should show "OUT OF STOCK" eventually)
3. Try to buy more food (should fail)
4. Check price increase as supply dwindles

**Expected Result**: Cannot buy indefinitely; planet should run out

### **Test 3: Blockade Effects**
**Goal**: Verify blockades effectively reduce production and increase prices

**Steps**:
1. Land on agricultural planet with good food production
2. Press `I` to see baseline production/stockpiles
3. Press `B` to start blockade
4. Press `N` several times to advance days
5. Press `I` to see reduced production and increased prices
6. Try to buy food (should be very expensive)

**Expected Result**: Blockades should reduce production, increase prices, cause shortages

### **Test 4: Economic Cascade Effects**
**Goal**: Verify realistic economic interdependence

**Steps**:
1. Find mining planet that produces minerals
2. Blockade it with `B`
3. Check other planets for mineral shortages (using `I`)
4. Verify mineral prices increase galaxy-wide

**Expected Result**: Supply disruption should affect other planets

### **Test 5: Strategic Reserve Protection**
**Goal**: Verify planets keep strategic reserves and don't sell everything

**Steps**:
1. Find planet with moderate food supply
2. Try to buy ALL their food
3. Should hit limit before planet is completely depleted
4. Press `I` to verify planet kept strategic reserves

**Expected Result**: Cannot buy below strategic reserve levels

## 🔧 **Testing Commands**

### **Economic Information**
- `I` - Show detailed economic report for current planet
- `B` - Toggle blockade on current planet  
- `N` - Fast-forward one day (to see economic changes)

### **Planet Analysis**
When you press `I`, you should see:
```
📊 ECONOMIC REPORT: Agri-234
Population: 567,890
Type: Agricultural
Blockaded: NO

📦 STOCKPILES:
  food: 3,450 (17.3 days) +400/day
  minerals: 120 (1.2 days) -100/day
  technology: 45 (1.5 days) -30/day
  
💰 Current market prices:
  food: Buy 8, Sell 6, Available: 3,250
  technology: Buy 67, Sell 50, Available: 15
```

## ✅ **Success Criteria**

### **Persistence Verified If**:
- ✅ Stockpiles decrease when you buy commodities
- ✅ Stockpiles increase when you sell commodities  
- ✅ Changes persist after leaving and returning to planet
- ✅ Planets can run completely out of goods

### **Blockades Effective If**:
- ✅ Production drops significantly during blockade
- ✅ Prices increase dramatically during blockade
- ✅ Stockpiles decrease faster due to waste/panic
- ✅ Eventually planets run out of critical supplies

### **Realistic Economics If**:
- ✅ Agricultural planets have cheap food, expensive tech
- ✅ Mining planets have cheap minerals, expensive food
- ✅ Tech planets have cheap tech, expensive basic goods
- ✅ Prices reflect actual supply/demand, not random

### **Anti-Exploit Features**:
- ✅ Cannot buy unlimited quantities
- ✅ Planets maintain strategic reserves
- ✅ Market manipulation has realistic consequences
- ✅ No infinite money exploits through trading

## 🚨 **Red Flags to Watch For**

### **Economy Breaking Issues**:
- ❌ Stockpiles reset when leaving/returning (not persistent)
- ❌ Can buy infinite quantities from any planet
- ❌ Blockades have no effect on prices/availability
- ❌ Planets never run out of anything
- ❌ Prices are random rather than supply-based

### **Unrealistic Behavior**:
- ❌ Agricultural planets selling food at premium prices
- ❌ Mining planets with no mineral supply
- ❌ Blockaded planets maintaining normal production
- ❌ Strategic reserves can be bought by player

## 🎮 **Test Scenarios**

### **Scenario A: Food Crisis Simulation**
1. Find agricultural planet producing food
2. Blockade it for several days
3. Watch food prices rise across galaxy
4. Break blockade and see if situation recovers

### **Scenario B: Market Manipulation**
1. Find planet low on luxury goods
2. Sell large quantity of luxury goods
3. Watch prices drop due to oversupply
4. Verify persistent effect

### **Scenario C: Supply Chain Disruption**
1. Identify which planets produce critical resources
2. Blockade multiple production centers
3. Watch galaxy-wide shortages develop
4. Test if trade routes matter for price differences

## 📊 **Expected Test Results**

If the persistent economy works correctly:

1. **No Magic Resources**: Planets can't generate infinite supplies
2. **Meaningful Consequences**: Your trading decisions affect the galactic economy
3. **Realistic Warfare**: Blockades can genuinely starve planets into submission
4. **Strategic Depth**: Trade route planning becomes critical
5. **Emergent Stories**: Economic crises create interesting gameplay situations

The game should feel like a living economic simulation where your actions have real, persistent consequences on the galactic economy!