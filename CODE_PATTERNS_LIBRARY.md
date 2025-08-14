# CODE PATTERNS LIBRARY - ILK SPACE GAME
## Common Patterns and Templates for Development

**Purpose:** This library provides reusable code patterns and templates for common development tasks in the ILK Space Game codebase.

---

## 🎯 **PATTERN CATEGORIES**

### **1. Game System Patterns**
### **2. UI Component Patterns**
### **3. Data Structure Patterns**
### **4. Error Handling Patterns**
### **5. Testing Patterns**
### **6. Documentation Patterns**

---

## 🎮 **GAME SYSTEM PATTERNS**

### **Pattern 1: Adding New Game Objects**

#### **Template: New Ship Class**
```python
# =============================================================================
# NEW SHIP CLASS IMPLEMENTATION
# =============================================================================

# Step 1: Add to ShipClass enum
class ShipClass(Enum):
    # ... existing ships ...
    NEW_SHIP_TYPE = "New Ship Type"  # Add your new ship here

# Step 2: Add to SHIP_STATS dictionary
SHIP_STATS = {
    # ... existing ships ...
    ShipClass.NEW_SHIP_TYPE: ShipStats(
        health=400,        # Ship health points (higher = more durable)
        speed=25,          # Movement speed (higher = faster)
        cargo=200,         # Cargo capacity (higher = more storage)
        combat=110,        # Combat effectiveness (higher = more damage)
        efficiency=0.6,    # Fuel efficiency (0.0-1.0, higher = less fuel use)
        crew=40,           # Crew capacity (higher = more crew needed)
        maintenance=20,    # Maintenance cost per day
        range=600,         # Travel range in units
        weapons=4,         # Number of weapon slots
        cost=450000        # Purchase cost in credits
    ),
}

# Step 3: Add to any relevant UI or display systems
def show_ship_info(self):
    # ... existing code ...
    if ship_class == ShipClass.NEW_SHIP_TYPE:
        print("🆕 New Ship Type - Specialized for [purpose]")
    # ... rest of function ...
```

#### **Template: New Commodity**
```python
# =============================================================================
# NEW COMMODITY IMPLEMENTATION
# =============================================================================

# Step 1: Add to commodity definitions
COMMODITIES = {
    # ... existing commodities ...
    "New Commodity": Commodity(
        name="New Commodity",
        base_price=85.0,  # Base price in credits
        commodity_type=CommodityType.TECHNOLOGY  # Choose appropriate type
    ),
}

# Step 2: Add to trading systems if needed
def calculate_price(self, commodity_name):
    # ... existing code ...
    if commodity_name == "New Commodity":
        # Special pricing logic for new commodity
        return base_price * demand_multiplier
    # ... rest of function ...
```

#### **Template: New Planet**
```python
# =============================================================================
# NEW PLANET IMPLEMENTATION
# =============================================================================

# Step 1: Add planet to planet list
PLANETS = [
    # ... existing planets ...
    Planet(
        name="New Planet",
        position=Vec3(x, y, z),  # 3D coordinates
        planet_type=PlanetType.INDUSTRIAL,  # Choose appropriate type
        population=50000,  # Population size
        economy=EnhancedPlanetEconomy()  # Economic system
    ),
]

# Step 2: Add planet-specific features if needed
def initialize_planet_features(self):
    # ... existing code ...
    if planet.name == "New Planet":
        # Special features for new planet
        planet.add_special_feature("unique_feature")
    # ... rest of function ...
```

### **Pattern 2: Adding New Commands**

#### **Template: New Text Command**
```python
# =============================================================================
# NEW TEXT COMMAND IMPLEMENTATION
# =============================================================================

# Step 1: Add to command handler
def handle_text_command(self, command):
    # ... existing commands ...
    elif command == "newcommand":
        # Handle your new command here
        self.handle_new_command()
    elif command.startswith("newcommand "):
        # Handle command with parameters
        parameter = command[11:].strip()  # Extract parameter
        self.handle_new_command_with_param(parameter)
    # ... rest of function ...

# Step 2: Implement the command handler
def handle_new_command(self):
    """
    Handle the new command functionality.
    
    This method implements the logic for the new command.
    Add comprehensive documentation explaining what it does.
    """
    # Implementation here
    print("🆕 New command executed!")
    # Add your logic here

# Step 3: Add to help system
def show_text_help(self):
    # ... existing help sections ...
    print("🆕 NEW FEATURES:")
    print("  newcommand     - Description of new command")
    print("  newcommand <param> - Description with parameter")
    print("")
```

#### **Template: New Keyboard Shortcut**
```python
# =============================================================================
# NEW KEYBOARD SHORTCUT IMPLEMENTATION
# =============================================================================

# Step 1: Add to input handling
def update(self):
    # ... existing input handling ...
    if held_keys['n']:  # Choose appropriate key
        self.handle_new_shortcut()
    # ... rest of function ...

# Step 2: Implement the shortcut handler
def handle_new_shortcut(self):
    """
    Handle the new keyboard shortcut.
    
    This method is called when the user presses the assigned key.
    Add comprehensive documentation explaining what it does.
    """
    # Implementation here
    print("🆕 Shortcut activated!")
    # Add your logic here
```

### **Pattern 3: Adding New Game Mechanics**

#### **Template: New Game System**
```python
# =============================================================================
# NEW GAME SYSTEM IMPLEMENTATION
# =============================================================================

class NewGameSystem:
    """
    New game system for [specific functionality].
    
    This system handles [describe what it does] and integrates
    with existing game systems to provide [describe benefits].
    
    Attributes:
        enabled (bool): Whether the system is active
        data (dict): System data storage
        config (dict): System configuration
    """
    
    def __init__(self, game_state):
        """
        Initialize the new game system.
        
        Args:
            game_state (GameState): Reference to main game state
        """
        self.game_state = game_state
        self.enabled = True
        self.data = {}
        self.config = {
            'setting1': 100,
            'setting2': 0.5,
            'setting3': True
        }
    
    def update(self):
        """
        Update the system every frame.
        
        This method is called by the main game loop to update
        the system state and process any ongoing operations.
        """
        if not self.enabled:
            return
        
        # Add your update logic here
        self.process_system_logic()
    
    def process_system_logic(self):
        """
        Process the main system logic.
        
        This method contains the core logic for the system.
        Add comprehensive documentation explaining the algorithm.
        """
        # Implementation here
        pass
    
    def save_state(self):
        """
        Save the system state to persistent storage.
        
        Returns:
            dict: System state data for saving
        """
        return {
            'enabled': self.enabled,
            'data': self.data,
            'config': self.config
        }
    
    def load_state(self, state_data):
        """
        Load the system state from persistent storage.
        
        Args:
            state_data (dict): System state data from save
        """
        self.enabled = state_data.get('enabled', True)
        self.data = state_data.get('data', {})
        self.config = state_data.get('config', self.config)
```

---

## 🎨 **UI COMPONENT PATTERNS**

### **Pattern 1: New UI Element**

#### **Template: New UI Panel**
```python
# =============================================================================
# NEW UI PANEL IMPLEMENTATION
# =============================================================================

class NewUIPanel:
    """
    New UI panel for [specific functionality].
    
    This panel provides a user interface for [describe purpose]
    and integrates with the existing UI system.
    
    Attributes:
        visible (bool): Whether the panel is visible
        elements (list): UI elements in the panel
        position (Vec2): Panel position on screen
        size (Vec2): Panel size
    """
    
    def __init__(self, parent=None):
        """
        Initialize the new UI panel.
        
        Args:
            parent (Entity): Parent entity for the panel
        """
        self.visible = False
        self.elements = []
        self.position = Vec2(0, 0)
        self.size = Vec2(300, 200)
        self.parent = parent
        
        # Create UI elements
        self.create_elements()
    
    def create_elements(self):
        """
        Create the UI elements for this panel.
        
        This method creates all the buttons, text, and other
        UI elements that make up the panel.
        """
        # Create title
        self.title = Text(
            text="New Panel Title",
            position=(0, 80),
            parent=self.parent
        )
        self.elements.append(self.title)
        
        # Create buttons
        self.button1 = Button(
            text="Button 1",
            position=(-100, 0),
            parent=self.parent,
            on_click=self.handle_button1_click
        )
        self.elements.append(self.button1)
        
        self.button2 = Button(
            text="Button 2",
            position=(100, 0),
            parent=self.parent,
            on_click=self.handle_button2_click
        )
        self.elements.append(self.button2)
    
    def show(self):
        """
        Show the panel and make it visible.
        """
        self.visible = True
        for element in self.elements:
            element.visible = True
    
    def hide(self):
        """
        Hide the panel and make it invisible.
        """
        self.visible = False
        for element in self.elements:
            element.visible = False
    
    def handle_button1_click(self):
        """
        Handle button 1 click event.
        """
        print("🆕 Button 1 clicked!")
        # Add your button logic here
    
    def handle_button2_click(self):
        """
        Handle button 2 click event.
        """
        print("🆕 Button 2 clicked!")
        # Add your button logic here
```

### **Pattern 2: New Text Command**

#### **Template: New Help Section**
```python
# =============================================================================
# NEW HELP SECTION IMPLEMENTATION
# =============================================================================

def show_text_help(self):
    """
    Show available text commands and their descriptions.
    """
    # ... existing help sections ...
    
    # =============================================================================
    # NEW FEATURES SECTION
    # =============================================================================
    print("🆕 NEW FEATURES:")
    print("  newcommand     - Description of new command")
    print("  newcommand <param> - Description with parameter")
    print("  newshortcut    - Description of new shortcut")
    print("")
    
    # ... rest of help function ...
```

---

## 📊 **DATA STRUCTURE PATTERNS**

### **Pattern 1: New Data Class**

#### **Template: New Game Object Class**
```python
# =============================================================================
# NEW GAME OBJECT CLASS IMPLEMENTATION
# =============================================================================

class NewGameObject:
    """
    New game object for [specific purpose].
    
    This class represents a [describe what it represents] in the game
    and provides methods for [describe functionality].
    
    Attributes:
        name (str): Object name
        position (Vec3): 3D position in world
        enabled (bool): Whether object is active
        data (dict): Object-specific data
    """
    
    def __init__(self, name, position=None):
        """
        Initialize the new game object.
        
        Args:
            name (str): Object name
            position (Vec3): Initial position (optional)
        """
        self.name = name
        self.position = position or Vec3(0, 0, 0)
        self.enabled = True
        self.data = {}
        
        # Initialize object-specific attributes
        self.initialize_attributes()
    
    def initialize_attributes(self):
        """
        Initialize object-specific attributes.
        
        This method sets up any attributes specific to this
        type of game object.
        """
        # Add your initialization logic here
        self.data['created_time'] = time.time()
        self.data['last_updated'] = time.time()
    
    def update(self):
        """
        Update the object every frame.
        
        This method is called by the game loop to update
        the object's state and behavior.
        """
        if not self.enabled:
            return
        
        # Add your update logic here
        self.data['last_updated'] = time.time()
    
    def save_state(self):
        """
        Save the object state for persistence.
        
        Returns:
            dict: Object state data
        """
        return {
            'name': self.name,
            'position': self.position,
            'enabled': self.enabled,
            'data': self.data
        }
    
    def load_state(self, state_data):
        """
        Load the object state from persistence.
        
        Args:
            state_data (dict): Object state data
        """
        self.name = state_data.get('name', self.name)
        self.position = state_data.get('position', self.position)
        self.enabled = state_data.get('enabled', self.enabled)
        self.data = state_data.get('data', self.data)
```

### **Pattern 2: New Configuration System**

#### **Template: New Settings Class**
```python
# =============================================================================
# NEW SETTINGS CLASS IMPLEMENTATION
# =============================================================================

class NewSettings:
    """
    Settings management for [specific system].
    
    This class manages configuration settings for [describe system]
    and provides methods for loading, saving, and accessing settings.
    
    Attributes:
        settings (dict): Current settings values
        defaults (dict): Default settings values
        file_path (str): Settings file path
    """
    
    def __init__(self, file_path="new_settings.json"):
        """
        Initialize the settings system.
        
        Args:
            file_path (str): Path to settings file
        """
        self.file_path = file_path
        self.defaults = {
            'setting1': 100,
            'setting2': 0.5,
            'setting3': True,
            'setting4': "default_value"
        }
        self.settings = self.defaults.copy()
        
        # Load settings from file
        self.load_settings()
    
    def load_settings(self):
        """
        Load settings from file.
        
        This method reads settings from the JSON file and
        falls back to defaults if the file doesn't exist.
        """
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults (new settings get defaults)
                    for key, value in self.defaults.items():
                        if key not in loaded_settings:
                            loaded_settings[key] = value
                    self.settings = loaded_settings
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            # Use defaults if loading fails
            self.settings = self.defaults.copy()
    
    def save_settings(self):
        """
        Save settings to file.
        
        This method writes the current settings to the JSON file.
        """
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
    
    def get_setting(self, key, default=None):
        """
        Get a setting value.
        
        Args:
            key (str): Setting key
            default: Default value if key doesn't exist
            
        Returns:
            Setting value or default
        """
        return self.settings.get(key, default)
    
    def set_setting(self, key, value):
        """
        Set a setting value.
        
        Args:
            key (str): Setting key
            value: Setting value
        """
        self.settings[key] = value
        # Auto-save when settings change
        self.save_settings()
    
    def reset_to_defaults(self):
        """
        Reset all settings to default values.
        """
        self.settings = self.defaults.copy()
        self.save_settings()
```

---

## 🛡️ **ERROR HANDLING PATTERNS**

### **Pattern 1: Comprehensive Error Handling**

#### **Template: Robust Function with Error Handling**
```python
# =============================================================================
# ROBUST FUNCTION WITH ERROR HANDLING
# =============================================================================

def robust_function(self, parameter):
    """
    Robust function with comprehensive error handling.
    
    This function demonstrates proper error handling patterns
    for functions that might fail in various ways.
    
    Args:
        parameter: Input parameter
        
    Returns:
        Result or None if operation failed
        
    Raises:
        ValueError: If parameter is invalid
        RuntimeError: If operation cannot be completed
    """
    # =============================================================================
    # INPUT VALIDATION
    # =============================================================================
    try:
        # Validate input parameter
        if parameter is None:
            raise ValueError("Parameter cannot be None")
        
        if not isinstance(parameter, (str, int, float)):
            raise ValueError(f"Parameter must be string, int, or float, got {type(parameter)}")
        
        # Additional validation as needed
        if isinstance(parameter, str) and len(parameter.strip()) == 0:
            raise ValueError("Parameter cannot be empty string")
            
    except ValueError as e:
        # Log the validation error
        logger.error(f"Input validation failed: {e}")
        # Re-raise for caller to handle
        raise
    
    # =============================================================================
    # MAIN OPERATION
    # =============================================================================
    try:
        # Perform the main operation
        result = self.perform_operation(parameter)
        
        # Validate the result
        if result is None:
            raise RuntimeError("Operation returned None")
        
        # Log successful operation
        logger.info(f"Operation completed successfully: {result}")
        
        return result
        
    except RuntimeError as e:
        # Handle runtime errors (operation-specific)
        logger.error(f"Runtime error during operation: {e}")
        # Return safe default or re-raise
        return None
        
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error during operation: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {str(e)}")
        # Return safe default
        return None
    
    # =============================================================================
    # CLEANUP (if needed)
    # =============================================================================
    finally:
        # Cleanup code that always runs
        self.cleanup_resources()
```

### **Pattern 2: Context Manager Pattern**

#### **Template: Safe Resource Management**
```python
# =============================================================================
# SAFE RESOURCE MANAGEMENT PATTERN
# =============================================================================

class SafeResourceManager:
    """
    Safe resource management with context manager pattern.
    
    This class demonstrates how to safely manage resources
    that need to be acquired and released properly.
    """
    
    def __init__(self, resource_name):
        """
        Initialize the resource manager.
        
        Args:
            resource_name (str): Name of the resource to manage
        """
        self.resource_name = resource_name
        self.resource = None
        self.acquired = False
    
    def __enter__(self):
        """
        Enter the context manager.
        
        Returns:
            self: The resource manager instance
        """
        try:
            # Acquire the resource
            self.resource = self.acquire_resource()
            self.acquired = True
            logger.info(f"Acquired resource: {self.resource_name}")
            return self
            
        except Exception as e:
            logger.error(f"Failed to acquire resource {self.resource_name}: {e}")
            # Ensure cleanup even if acquisition fails
            self.cleanup()
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager.
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        try:
            # Always cleanup, even if exception occurred
            self.cleanup()
            
            # Log any exceptions that occurred
            if exc_type is not None:
                logger.error(f"Exception in resource context: {exc_type.__name__}: {exc_val}")
                
        except Exception as e:
            logger.error(f"Error during resource cleanup: {e}")
    
    def acquire_resource(self):
        """
        Acquire the managed resource.
        
        Returns:
            Resource object
            
        Raises:
            RuntimeError: If resource cannot be acquired
        """
        # Implementation depends on resource type
        # This is a placeholder
        resource = f"acquired_{self.resource_name}"
        if not resource:
            raise RuntimeError(f"Cannot acquire resource: {self.resource_name}")
        return resource
    
    def cleanup(self):
        """
        Clean up the managed resource.
        """
        if self.acquired and self.resource:
            try:
                # Release the resource
                logger.info(f"Releasing resource: {self.resource_name}")
                self.resource = None
                self.acquired = False
                
            except Exception as e:
                logger.error(f"Error releasing resource {self.resource_name}: {e}")

# Usage example:
def use_resource_safely():
    """
    Example of using the safe resource manager.
    """
    try:
        with SafeResourceManager("database_connection") as manager:
            # Use the resource safely
            print(f"Using resource: {manager.resource}")
            # Resource is automatically cleaned up when exiting context
            
    except Exception as e:
        print(f"Error using resource: {e}")
```

---

## 🧪 **TESTING PATTERNS**

### **Pattern 1: Unit Test Template**

#### **Template: Comprehensive Unit Test**
```python
# =============================================================================
# COMPREHENSIVE UNIT TEST TEMPLATE
# =============================================================================

def test_new_feature():
    """
    Test the new feature functionality.
    
    This test verifies that the new feature works correctly
    and integrates properly with existing systems.
    """
    # =============================================================================
    # TEST SETUP
    # =============================================================================
    print("🧪 Testing new feature...")
    
    # Create test environment
    game_state = GameState()
    test_object = NewGameObject("test_object")
    
    # Set up test data
    test_data = {
        'input1': "test_value",
        'input2': 42,
        'input3': True
    }
    
    # =============================================================================
    # TEST CASES
    # =============================================================================
    
    # Test Case 1: Basic functionality
    try:
        result = test_object.basic_function(test_data['input1'])
        assert result is not None, "Basic function should return a result"
        assert isinstance(result, str), "Result should be a string"
        print("✅ Test Case 1: Basic functionality - PASSED")
        
    except Exception as e:
        print(f"❌ Test Case 1: Basic functionality - FAILED: {e}")
        return False
    
    # Test Case 2: Edge cases
    try:
        # Test with None input
        result = test_object.basic_function(None)
        assert result is None, "Function should handle None input gracefully"
        print("✅ Test Case 2: Edge cases - PASSED")
        
    except Exception as e:
        print(f"❌ Test Case 2: Edge cases - FAILED: {e}")
        return False
    
    # Test Case 3: Integration with existing systems
    try:
        # Test integration
        result = test_object.integrate_with_system(game_state)
        assert result is True, "Integration should succeed"
        print("✅ Test Case 3: Integration - PASSED")
        
    except Exception as e:
        print(f"❌ Test Case 3: Integration - FAILED: {e}")
        return False
    
    # =============================================================================
    # TEST CLEANUP
    # =============================================================================
    try:
        # Clean up test resources
        test_object.cleanup()
        print("✅ Test cleanup - PASSED")
        
    except Exception as e:
        print(f"❌ Test cleanup - FAILED: {e}")
        return False
    
    # =============================================================================
    # TEST SUMMARY
    # =============================================================================
    print("🎉 All tests passed! New feature is working correctly.")
    return True

# Run the test
if __name__ == "__main__":
    success = test_new_feature()
    if success:
        print("✅ New feature test suite completed successfully")
    else:
        print("❌ New feature test suite failed")
```

### **Pattern 2: Integration Test Template**

#### **Template: System Integration Test**
```python
# =============================================================================
# SYSTEM INTEGRATION TEST TEMPLATE
# =============================================================================

def test_system_integration():
    """
    Test integration between multiple systems.
    
    This test verifies that different systems work together
    correctly and don't interfere with each other.
    """
    print("🧪 Testing system integration...")
    
    # =============================================================================
    # SYSTEM SETUP
    # =============================================================================
    
    # Initialize all systems
    game_state = GameState()
    economic_system = EconomicSystem(game_state)
    trading_system = TradingSystem(game_state)
    faction_system = FactionSystem(game_state)
    
    # =============================================================================
    # INTEGRATION TESTS
    # =============================================================================
    
    # Test 1: Economic and Trading Integration
    try:
        # Set up test scenario
        player_wallet = PlayerWallet()
        player_wallet.credits = 1000
        
        # Perform trading operation
        trade_result = trading_system.buy_commodity("Food", 10, player_wallet)
        
        # Verify economic impact
        assert trade_result is True, "Trade should succeed"
        assert player_wallet.credits < 1000, "Credits should decrease"
        assert economic_system.get_commodity_price("Food") > 0, "Price should be positive"
        
        print("✅ Economic and Trading Integration - PASSED")
        
    except Exception as e:
        print(f"❌ Economic and Trading Integration - FAILED: {e}")
        return False
    
    # Test 2: Faction and Economic Integration
    try:
        # Test faction influence on economy
        faction = faction_system.get_faction("Terran Federation")
        original_price = economic_system.get_commodity_price("Food")
        
        # Change faction relationship
        faction.reputation = 50  # Friendly
        
        # Verify price change
        new_price = economic_system.get_commodity_price("Food")
        assert new_price != original_price, "Price should change with faction relationship"
        
        print("✅ Faction and Economic Integration - PASSED")
        
    except Exception as e:
        print(f"❌ Faction and Economic Integration - FAILED: {e}")
        return False
    
    # Test 3: End-to-End Workflow
    try:
        # Test complete workflow
        # 1. Player moves to planet
        # 2. Player trades with faction
        # 3. Player reputation changes
        # 4. Economic system updates
        
        # Simulate the workflow
        workflow_result = simulate_complete_workflow(game_state)
        assert workflow_result is True, "Complete workflow should succeed"
        
        print("✅ End-to-End Workflow - PASSED")
        
    except Exception as e:
        print(f"❌ End-to-End Workflow - FAILED: {e}")
        return False
    
    print("🎉 All integration tests passed!")
    return True

def simulate_complete_workflow(game_state):
    """
    Simulate a complete player workflow.
    
    Returns:
        bool: True if workflow succeeds
    """
    try:
        # This would contain the actual workflow simulation
        # For now, return True as placeholder
        return True
    except Exception as e:
        logger.error(f"Workflow simulation failed: {e}")
        return False
```

---

## 📝 **DOCUMENTATION PATTERNS**

### **Pattern 1: Comprehensive Function Documentation**

#### **Template: Well-Documented Function**
```python
# =============================================================================
# COMPREHENSIVE FUNCTION DOCUMENTATION TEMPLATE
# =============================================================================

def comprehensive_function(self, parameter1, parameter2=None, **kwargs):
    """
    Comprehensive function with detailed documentation.
    
    This function demonstrates the proper way to document functions
    in the ILK Space Game codebase. It includes all necessary
    information for developers and LLMs to understand and use
    the function correctly.
    
    The function performs [describe what it does] and integrates
    with [describe which systems] to provide [describe benefits].
    
    Args:
        parameter1 (str): Description of the first parameter.
                         Must be a non-empty string.
                         Example: "player_name"
        
        parameter2 (int, optional): Description of the second parameter.
                                   If not provided, defaults to 100.
                                   Must be between 0 and 1000.
                                   Example: 500
        
        **kwargs: Additional keyword arguments.
                 - 'option1' (bool): Enable option1 (default: False)
                 - 'option2' (float): Option2 value (default: 1.0)
                 - 'option3' (str): Option3 text (default: "")
    
    Returns:
        dict: A dictionary containing the operation results.
              - 'success' (bool): Whether the operation succeeded
              - 'data' (dict): Operation data
              - 'message' (str): Human-readable result message
              - 'timestamp' (float): When the operation completed
    
    Raises:
        ValueError: If parameter1 is empty or parameter2 is out of range
        RuntimeError: If the operation cannot be completed
        KeyError: If required kwargs are missing
    
    Example:
        >>> result = obj.comprehensive_function("player1", 500, option1=True)
        >>> print(result['success'])
        True
        >>> print(result['message'])
        "Operation completed successfully"
    
    Side Effects:
        - Updates internal state
        - Logs operation details
        - May modify external systems
    
    Performance:
        - Time Complexity: O(n) where n is the size of parameter1
        - Space Complexity: O(1) for most operations
        - Memory Usage: Minimal, reuses existing objects
    
    Dependencies:
        - Requires self.game_state to be initialized
        - Requires self.logger to be available
        - May depend on external systems being online
    """
    # =============================================================================
    # INPUT VALIDATION
    # =============================================================================
    # Validate required parameters
    if not parameter1 or not isinstance(parameter1, str):
        raise ValueError("parameter1 must be a non-empty string")
    
    if parameter2 is not None and (parameter2 < 0 or parameter2 > 1000):
        raise ValueError("parameter2 must be between 0 and 1000")
    
    # Extract and validate keyword arguments
    option1 = kwargs.get('option1', False)
    option2 = kwargs.get('option2', 1.0)
    option3 = kwargs.get('option3', "")
    
    if not isinstance(option1, bool):
        raise ValueError("option1 must be a boolean")
    
    if not isinstance(option2, (int, float)) or option2 <= 0:
        raise ValueError("option2 must be a positive number")
    
    # =============================================================================
    # MAIN OPERATION
    # =============================================================================
    try:
        # Log operation start
        self.logger.info(f"Starting comprehensive operation: {parameter1}")
        
        # Perform the main operation
        operation_data = self.perform_main_operation(parameter1, parameter2, option1, option2, option3)
        
        # Process results
        result = {
            'success': True,
            'data': operation_data,
            'message': "Operation completed successfully",
            'timestamp': time.time()
        }
        
        # Log successful completion
        self.logger.info(f"Operation completed successfully: {result}")
        
        return result
        
    except Exception as e:
        # Handle operation failures
        self.logger.error(f"Operation failed: {e}")
        
        result = {
            'success': False,
            'data': {},
            'message': f"Operation failed: {str(e)}",
            'timestamp': time.time()
        }
        
        return result
    
    # =============================================================================
    # CLEANUP (if needed)
    # =============================================================================
    finally:
        # Cleanup code that always runs
        self.cleanup_operation_resources()
```

---

## 🎯 **USING THESE PATTERNS**

### **How to Use This Library**

#### **1. Find the Right Pattern**
- Look for patterns that match your task
- Read the template and understand the structure
- Adapt the pattern to your specific needs

#### **2. Copy and Customize**
- Copy the template code
- Replace placeholder text with your specific implementation
- Adjust parameters and logic as needed

#### **3. Follow the Documentation**
- Read the comments in the template
- Understand what each section does
- Maintain the same documentation style

#### **4. Test Your Implementation**
- Use the testing patterns to verify your code
- Test edge cases and error conditions
- Ensure integration with existing systems

### **Pattern Best Practices**

#### **1. Consistency**
- Follow the same structure as existing code
- Use consistent naming conventions
- Maintain the same documentation style

#### **2. Completeness**
- Include all necessary error handling
- Add comprehensive documentation
- Test all code paths

#### **3. Integration**
- Ensure new code works with existing systems
- Follow established patterns and conventions
- Update relevant documentation

#### **4. Maintainability**
- Write code that's easy to understand and modify
- Add clear comments explaining complex logic
- Structure code for future expansion

---

*This pattern library provides reusable templates for common development tasks in the ILK Space Game codebase. Use these patterns to ensure consistency, completeness, and maintainability in your code.*