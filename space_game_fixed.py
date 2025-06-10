#!/usr/bin/env python3

import os
import sys

# Add error handling for headless environments
try:
    from ursina import *
    from ursina.prefabs.first_person_controller import FirstPersonController
    GRAPHICS_AVAILABLE = True
except Exception as e:
    print(f"Graphics not available: {e}")
    print("This appears to be a headless environment.")
    print("The game requires OpenGL support to run.")
    GRAPHICS_AVAILABLE = False

if not GRAPHICS_AVAILABLE:
    print("\n=== ILK SPACE GAME ===")
    print("This is a 3D space exploration game that requires graphics support.")
    print("\nTo run this game, you need:")
    print("1. A system with OpenGL support")
    print("2. A desktop environment (not headless/remote)")
    print("3. Python dependencies installed (see requirements.txt)")
    print("\nHow to start the game on a local system:")
    print("1. Clone this repository")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run: python3 space_game.py")
    print("   OR")
    print("4. Run: ./run_me.py (sets up virtual environment automatically)")
    print("\n=== GAME FEATURES ===")
    print("• Space exploration with multiple randomly generated planets")
    print("• Landing system - get close to planets to land on them")
    print("• Two game modes: Space (6DOF movement) and Surface (FPS-style)")
    print("• Save/Load game system")
    print("• Beautiful rotating skybox")
    print("• Physics-based movement and collision detection")
    print("\n=== CONTROLS ===")
    print("Space Mode:")
    print("  WASD - Move forward/back/left/right")
    print("  Space/Shift - Move up/down")
    print("  Q/E - Roll left/right")
    print("  Mouse - Look around")
    print("  F7 - Toggle third-person view")
    print("\nSurface Mode:")
    print("  WASD - Walk")
    print("  Space - Jump (double jump available)")
    print("  Mouse - Look around")
    print("\nGeneral:")
    print("  ESC - Pause menu (Save/Load/Quit)")
    print("  F6 - Take screenshot")
    print("  F8 - Switch between space and surface modes")
    print("  Left Click - Shoot projectiles (space mode)")
    sys.exit(0)

import random
import numpy as np
import math
import json
import pickle
from datetime import datetime

# Initialize Ursina with better error handling
try:
    app = Ursina(borderless=False)  # Make window resizable and movable
except Exception as e:
    print(f"Failed to initialize graphics: {e}")
    print("Make sure you have proper graphics drivers and OpenGL support.")
    sys.exit(1)

# Create a rotating skybox instead of stars
class RotatingSkybox(Entity):
    def __init__(self):
        super().__init__(
            model='sphere',
            texture='assets/textures/skybox_right',  # Base texture path
            scale=1000,  # Large enough to contain the scene
            double_sided=True,
            unlit=True  # Make skybox ignore lighting
        )
        # Calculate rotation speed for 2-hour rotation (360 degrees / 7200 seconds)
        self.rotation_speed = 360 / (2 * 60 * 60)  # Approximately 0.05 degrees per second
        
        # Load all six faces of the skybox with error handling
        self.textures = {}
        texture_files = ['right', 'left', 'top', 'bottom', 'front', 'back']
        
        for face in texture_files:
            try:
                texture_path = f'assets/textures/skybox_{face}.png'
                if os.path.exists(texture_path):
                    self.textures[face] = load_texture(texture_path)
                else:
                    print(f"Warning: Skybox texture not found: {texture_path}")
                    self.textures[face] = load_texture('white_cube')  # Fallback
            except Exception as e:
                print(f"Error loading texture {face}: {e}")
                self.textures[face] = load_texture('white_cube')
        
        # Apply textures to the skybox
        self.texture = self.textures.get('right', load_texture('white_cube'))
        
    def update(self):
        if not paused:
            # Rotate the skybox slowly
            self.rotation_y += self.rotation_speed * time.dt

# Create the rotating skybox
skybox = RotatingSkybox()

# Adjust camera settings for far viewing distance
camera.clip_plane_far = 1000000  # Increase far clip plane to see distant objects
camera.fov = 90

# Create coordinate axis indicator
class AxisIndicator(Entity):
    def __init__(self):
        super().__init__(
            position=Vec3(0, 0, -5)  # Place it 5 units in front of spawn
        )
        self.rotation_speed = 100  # Degrees per second
        
        # Create the three poles
        self.x_pole = Entity(
            parent=self,
            model='cube',
            color=color.red,
            scale=(2, 0.1, 0.1),  # Long in X direction
            position=(1, 0, 0)  # Centered on its length
        )
        self.y_pole = Entity(
            parent=self,
            model='cube',
            color=color.green,
            scale=(0.1, 2, 0.1),  # Long in Y direction
            position=(0, 1, 0)  # Centered on its length
        )
        self.z_pole = Entity(
            parent=self,
            model='cube',
            color=color.blue,
            scale=(0.1, 0.1, 2),  # Long in Z direction
            position=(0, 0, 1)  # Centered on its length
        )

    def update(self):
        if not paused:
            rotation_amount = self.rotation_speed * time.dt
            
            # Get the current orientation vectors
            right = self.right
            up = self.up
            forward = self.forward
            
            # Rotate around local axes
            if held_keys['insert']:
                self.rotate(Vec3(rotation_amount, 0, 0), relative_to=self)
            if held_keys['delete']:
                self.rotate(Vec3(-rotation_amount, 0, 0), relative_to=self)
                
            if held_keys['page up']:
                self.rotate(Vec3(0, rotation_amount, 0), relative_to=self)
            if held_keys['page down']:
                self.rotate(Vec3(0, -rotation_amount, 0), relative_to=self)
                
            if held_keys['home']:
                self.rotate(Vec3(0, 0, rotation_amount), relative_to=self)
            if held_keys['end']:
                self.rotate(Vec3(0, 0, -rotation_amount), relative_to=self)

# Create the axis indicator
axis_indicator = AxisIndicator()

# Custom Space Controller
class SpaceController(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.speed = 5  # Base movement speed
        self.max_speed = 50
        self.mouse_sensitivity = Vec2(2000, 2000)
        self.rotation_speed = 100
        
        # Simple velocity system
        self.velocity = Vec3(0, 0, 0)
        
        # Set up camera exactly like RGB structure
        camera.parent = self
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        mouse.locked = True
        mouse.visible = False
        
        # Create player axis indicator (initially disabled)
        self.axis_indicator = Entity(parent=self)
        self.x_pole = Entity(
            parent=self.axis_indicator,
            model='cube',
            color=color.red,
            scale=(2, 0.1, 0.1),
            position=(1, 0, 0)
        )
        self.y_pole = Entity(
            parent=self.axis_indicator,
            model='cube',
            color=color.green,
            scale=(0.1, 2, 0.1),
            position=(0, 1, 0)
        )
        self.z_pole = Entity(
            parent=self.axis_indicator,
            model='cube',
            color=color.blue,
            scale=(0.1, 0.1, 2),
            position=(0, 0, 1)
        )
        self.axis_indicator.enabled = False
        
        # View mode
        self.third_person = False
        
        # Status text for speed
        self.status_text = Text(
            parent=camera.ui,
            text='Speed: 0%',
            position=(-0.3, 0.45),
            scale=0.8,
            color=color.white
        )

    def update(self):
        if not paused:
            # Handle rotations with mouse velocity and time.dt
            rotation_amount_y = mouse.velocity[0] * self.mouse_sensitivity[0] * time.dt
            rotation_amount_x = mouse.velocity[1] * self.mouse_sensitivity[1] * time.dt
            
            # Apply rotations relative to self
            if abs(mouse.velocity[0]) > 0:
                self.rotate(Vec3(0, rotation_amount_y, 0), relative_to=self)
            if abs(mouse.velocity[1]) > 0:
                self.rotate(Vec3(-rotation_amount_x, 0, 0), relative_to=self)

            # Roll with Q/E
            if held_keys['e']:
                self.rotate(Vec3(0, 0, self.rotation_speed * time.dt), relative_to=self)
            if held_keys['q']:
                self.rotate(Vec3(0, 0, -self.rotation_speed * time.dt), relative_to=self)

            # Direct movement in local space
            move_direction = Vec3(0, 0, 0)
            if held_keys['w']: move_direction.z += 1
            if held_keys['s']: move_direction.z -= 1
            if held_keys['d']: move_direction.x += 1
            if held_keys['a']: move_direction.x -= 1
            if held_keys['space']: move_direction.y += 1
            if held_keys['shift']: move_direction.y -= 1
            
            # Apply movement relative to orientation
            if move_direction.length() > 0:
                move_direction = move_direction.normalized()
                self.velocity = (
                    self.right * move_direction.x +
                    self.up * move_direction.y +
                    self.forward * move_direction.z
                ) * self.speed
            else:
                # Stop when no input
                self.velocity = Vec3(0, 0, 0)
            
            # Apply velocity to position
            self.position += self.velocity * time.dt
            
            # Update status text with speed info
            speed_percentage = int((self.velocity.length() / self.max_speed) * 100)
            self.status_text.text = f'Speed: {speed_percentage}%'

# Player setup with proper 3D movement
player = SpaceController()

# Create a pause menu
pause_panel = Panel(
    parent=camera.ui,
    model='quad',
    scale=(1, 1),
    color=color.black66,
    enabled=False
)

pause_text = Text(
    parent=pause_panel,
    text='PAUSED\nESC to Resume',
    origin=(0, 0),
    scale=2,
    position=(0, 0.3)
)

# Add Save Game button
save_button = Button(
    parent=pause_panel,
    text='Save Game',
    color=color.azure.tint(-.2),
    highlight_color=color.azure.tint(-.1),
    pressed_color=color.azure.tint(-.3),
    scale=(0.3, 0.1),
    position=(0, 0.1),
    enabled=False
)

# Add Load Game button
load_button = Button(
    parent=pause_panel,
    text='Load Game',
    color=color.azure.tint(-.2),
    highlight_color=color.azure.tint(-.1),
    pressed_color=color.azure.tint(-.3),
    scale=(0.3, 0.1),
    position=(0, 0),
    enabled=False
)

# Add Return to Desktop button
quit_button = Button(
    parent=pause_panel,
    text='Return to Desktop',
    color=color.red.tint(-.2),
    highlight_color=color.red.tint(-.1),
    pressed_color=color.red.tint(-.3),
    scale=(0.3, 0.1),
    position=(0, -0.2),
    enabled=False
)

# Scene Management
class GameState:
    SPACE = 'space'
    TOWN = 'town'

class TownController(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.speed = 5
        self.mouse_sensitivity = Vec2(4000, 4000)
        self.gravity = 30  # Increased gravity for snappier jumps
        self.velocity_y = 0
        self.jump_height = 8  # Reduced jump height for better control
        self.can_double_jump = True  # Enable double jump
        self.has_double_jumped = False  # Track if double jump was used
        
        # Add collider for player
        self.collider = BoxCollider(self, center=Vec3(0, 1, 0), size=Vec3(1, 2, 1))
        
        # Set up camera
        camera.parent = self
        camera.position = (0, 2, 0)
        camera.rotation = (0, 0, 0)
        mouse.locked = True
        mouse.visible = False
        
        # Start at ground level
        self.position = Vec3(0, 1.5, 0)
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def update(self):
        if not paused:
            # Simple FPS-style mouse look
            self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[0] * time.dt
            camera.rotation_x = clamp(
                camera.rotation_x - mouse.velocity[1] * self.mouse_sensitivity[1] * time.dt,
                -90, 90
            )
            
            # More precise ground check with smaller ray
            hit_info = raycast(self.position + Vec3(0, 0.1, 0), self.down, distance=1.1, ignore=[self])
            is_grounded = hit_info.hit
            
            # Reset double jump when grounded
            if is_grounded:
                self.has_double_jumped = False
            
            # Handle jumping
            if held_keys['space']:
                if is_grounded:
                    self.velocity_y = self.jump_height
                elif self.can_double_jump and not self.has_double_jumped:
                    self.velocity_y = self.jump_height * 0.8  # Slightly weaker double jump
                    self.has_double_jumped = True
            
            # Apply gravity
            self.velocity_y -= self.gravity * time.dt
            self.velocity_y = max(self.velocity_y, -25)  # Cap falling speed
            
            # Apply vertical movement
            self.y += self.velocity_y * time.dt
            
            # Prevent falling through the ground with more precise collision
            if hit_info.hit and self.y < hit_info.point.y + 1:
                self.y = hit_info.point.y + 1
                self.velocity_y = 0
            
            # Horizontal movement with air control
            move_direction = Vec3(0, 0, 0)
            if held_keys['w']: move_direction.z += 1
            if held_keys['s']: move_direction.z -= 1
            if held_keys['d']: move_direction.x += 1
            if held_keys['a']: move_direction.x -= 1
            
            # Apply movement relative to camera direction
            if move_direction.length() > 0:
                move_direction = Vec3(
                    self.forward * move_direction.z +
                    self.right * move_direction.x
                ).normalized()
                
                # Reduce air control when not grounded
                current_speed = self.speed * (0.7 if not is_grounded else 1.0)
                
                # Store original position for collision check
                original_position = self.position
                
                # Apply movement
                self.position += move_direction * current_speed * time.dt
                
                # Handle horizontal collisions
                for entity in scene_manager.town_entities:
                    if entity.collider and self != entity:
                        if self.intersects(entity).hit:
                            self.position = original_position
                            break

class SceneManager:
    def __init__(self):
        self.current_state = GameState.SPACE
        self.space_entities = []
        self.town_entities = []
        self.town_controller = None
        self.space_controller = None
        
    def initialize_space(self):
        self.space_controller = player
        self.space_entities = [skybox, *planets, axis_indicator]
        
    def initialize_town(self):
        if not self.town_controller:
            # Create main ground
            ground = Entity(
                model='plane',
                scale=(100, 1, 100),
                color=color.green.tint(-.2),
                texture='white_cube',
                texture_scale=(100,100),
                collider='box',
                position=(0, 0, 0)
            )
            
            # Create podium like a building
            podium = Entity(
                model='cube',
                scale=(8, 1, 8),
                color=color.light_gray,
                texture='white_cube',
                position=(0, 0.5, 0),
                collider='box'
            )
            
            # Add some buildings with random colors and proper collision, keeping clear of podium
            for i in range(10):
                # Keep trying until we find a valid position
                while True:
                    x = random.uniform(-40, 40)
                    z = random.uniform(-40, 40)
                    # Check if position is far enough from podium (10 units from center)
                    if math.sqrt(x*x + z*z) > 10:
                        break
                
                height = random.uniform(4, 8)
                building = Entity(
                    model='cube',
                    color=color.random_color(),
                    texture='white_cube',
                    position=(x, height/2, z),
                    scale=(4, height, 4),
                    collider='box'
                )
                self.town_entities.append(building)
            
            # Add ground first, then podium, then buildings
            self.town_entities.extend([ground, podium])
            
            # Create and position the town controller on the podium
            self.town_controller = TownController()
            self.town_controller.position = Vec3(0, 1.5, 0)
    
    def switch_to_town(self):
        if self.current_state == GameState.SPACE:
            # Store and reset space controller state
            self.space_controller.disable()
            self.space_controller.status_text.enabled = False
            
            # Hide space entities
            for entity in self.space_entities:
                entity.disable()
            
            # Initialize and setup town
            self.initialize_town()
            for entity in self.town_entities:
                entity.enable()
            
            # Reset and setup town camera/controller
            self.town_controller.rotation = Vec3(0, 0, 0)
            camera.parent = self.town_controller
            camera.position = (0, 2, 0)
            camera.rotation = (0, 0, 0)
            self.town_controller.enable()
            
            self.current_state = GameState.TOWN
    
    def switch_to_space(self):
        if self.current_state == GameState.TOWN:
            # Store and reset town controller state
            self.town_controller.disable()
            
            # Hide town entities
            for entity in self.town_entities:
                entity.disable()
            
            # Show space entities
            for entity in self.space_entities:
                entity.enable()
            
            # Reset and setup space camera/controller
            self.space_controller.enable()
            self.space_controller.status_text.enabled = True
            camera.parent = self.space_controller
            camera.rotation = (0, 0, 0)
            camera.position = (0, 0, -15) if self.space_controller.third_person else (0, 0, 0)
            
            self.current_state = GameState.SPACE

# Create scene manager
scene_manager = SceneManager()

def save_game():
    try:
        if not os.path.exists('saves'):
            os.makedirs('saves')
        
        game_state = {
            'current_scene': scene_manager.current_state,
            'player_position': (player.position.x, player.position.y, player.position.z),
            'player_rotation': (player.rotation.x, player.rotation.y, player.rotation.z),
            'planets': [(p.position.x, p.position.y, p.position.z, p.scale) for p in planets]
        }
        
        if scene_manager.current_state == GameState.TOWN and scene_manager.town_controller:
            game_state['town_player_position'] = (
                scene_manager.town_controller.position.x,
                scene_manager.town_controller.position.y,
                scene_manager.town_controller.position.z
            )
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'saves/save_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(game_state, f, indent=2)
        print(f'Game saved to {filename}')
    except Exception as e:
        print(f'Error saving game: {e}')

def load_game():
    try:
        if not os.path.exists('saves'):
            print('No saves directory found')
            return
            
        save_files = [f for f in os.listdir('saves') if f.endswith('.json')]
        if not save_files:
            print('No save files found')
            return
            
        # Load the most recent save file
        latest_save = max(save_files)
        with open(f'saves/{latest_save}', 'r') as f:
            game_state = json.load(f)
        
        # Switch to correct scene
        if game_state['current_scene'] == GameState.TOWN:
            scene_manager.switch_to_town()
            if 'town_player_position' in game_state:
                pos = game_state['town_player_position']
                scene_manager.town_controller.position = Vec3(pos[0], pos[1], pos[2])
        else:
            scene_manager.switch_to_space()
            pos = game_state['player_position']
            player.position = Vec3(pos[0], pos[1], pos[2])
        
        # Restore planets
        for p in planets:
            destroy(p)
        planets.clear()
        
        for p_data in game_state['planets']:
            planet = Planet(position=Vec3(p_data[0], p_data[1], p_data[2]))
            planet.scale = p_data[3]
            planets.append(planet)
        
        print(f'Game loaded from {latest_save}')
    except Exception as e:
        print(f'Error loading game: {e}')

def quit_game():
    application.quit()

save_button.on_click = save_game
load_button.on_click = load_game
quit_button.on_click = quit_game

# Planet class
class Planet(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            model='sphere',
            color=color.random_color(),
            position=position,
            scale=random.uniform(20, 50),  # Scaled down from 2000-5000
            texture='white_cube',
            collider='sphere'
        )
        # Remove rotation by setting speed to 0
        self.rotation_speed = Vec3(0, 0, 0)
        # Add landing detection radius
        self.landing_radius = self.scale * 2
        # Add name for the planet
        self.name = f"Planet {random.randint(1, 1000)}"
    
    def update(self):
        pass  # Remove rotation update
        
    def is_player_in_landing_range(self, player_position):
        # Calculate distance to player
        distance = (self.position - player_position).length()
        return distance < self.landing_radius

# Create planets with error handling
planets = []
try:
    for _ in range(15):
        pos = Vec3(
            random.uniform(-500, 500),
            random.uniform(-500, 500),
            random.uniform(-500, 500)
        )
        if pos.length() > 100:
            planet = Planet(position=pos)
            planets.append(planet)
except Exception as e:
    print(f"Error creating planets: {e}")

# Landing prompt UI
landing_prompt = Panel(
    parent=camera.ui,
    model='quad',
    scale=(0.4, 0.2),
    color=color.black66,
    enabled=False
)

landing_text = Text(
    parent=landing_prompt,
    text='',
    origin=(0, 0),
    scale=1.5,
    position=(0, 0.05)
)

land_button = Button(
    parent=landing_prompt,
    text='Land',
    color=color.azure.tint(-.2),
    highlight_color=color.azure.tint(-.1),
    pressed_color=color.azure.tint(-.3),
    scale=(0.2, 0.1),
    position=(0, -0.05),
    enabled=False
)

cancel_button = Button(
    parent=landing_prompt,
    text='Cancel',
    color=color.red.tint(-.2),
    highlight_color=color.red.tint(-.1),
    pressed_color=color.red.tint(-.3),
    scale=(0.2, 0.1),
    position=(0, -0.2),
    enabled=False
)

# Variable to track the planet we're near
nearby_planet = None

def update():
    global nearby_planet
    
    if not paused and scene_manager.current_state == GameState.SPACE:
        # Check if player is near any planet
        nearby_planet = None
        for planet in planets:
            if planet.is_player_in_landing_range(player.position):
                nearby_planet = planet
                break
        
        # Show/hide landing prompt based on proximity
        if nearby_planet and not landing_prompt.enabled:
            landing_prompt.enabled = True
            landing_text.text = f"Approaching {nearby_planet.name}\nDo you want to land?"
            land_button.enabled = True
            cancel_button.enabled = True
            
            # Freeze player and release mouse
            player.enabled = False
            mouse.locked = False
            mouse.visible = True
        elif not nearby_planet and landing_prompt.enabled:
            landing_prompt.enabled = False
            
            # Unfreeze player and capture mouse
            player.enabled = True
            mouse.locked = True
            mouse.visible = False

# Function to handle landing
def land_on_planet():
    global nearby_planet
    if nearby_planet:
        # Switch to town mode
        scene_manager.switch_to_town()
        # Hide landing prompt
        landing_prompt.enabled = False
        # Reset nearby planet
        nearby_planet = None

# Function to cancel landing
def cancel_landing():
    global nearby_planet
    landing_prompt.enabled = False
    nearby_planet = None
    
    # Unfreeze player and capture mouse
    player.enabled = True
    mouse.locked = True
    mouse.visible = False

# Set up button callbacks
land_button.on_click = land_on_planet
cancel_button.on_click = cancel_landing

# Lighting
DirectionalLight(y=2, z=3, rotation=(45, -45, 45))
AmbientLight(color=Vec4(0.1, 0.1, 0.1, 1))  # Darker ambient light

# Initialize scene manager after all entities are created
scene_manager.initialize_space()

# Game state
paused = False

def input(key):
    global paused
    
    if key == 'escape':
        paused = not paused
        pause_panel.enabled = paused
        save_button.enabled = paused
        load_button.enabled = paused
        quit_button.enabled = paused
        
        if scene_manager.current_state == GameState.SPACE:
            player.enabled = not paused
        else:
            if scene_manager.town_controller:
                scene_manager.town_controller.enabled = not paused
            
        mouse.locked = not paused
        if paused:
            mouse.visible = True
        else:
            mouse.visible = False
    
    if key == 'f6':  # Screenshot
        try:
            if not os.path.exists('screenshots'):
                os.makedirs('screenshots')
            timestamp = int(time.time())
            filename = f'screenshots/screenshot_{timestamp}.png'
            base.win.saveScreenshot(Filename(filename))
            print(f'Screenshot saved to {filename}')
        except Exception as e:
            print(f'Error taking screenshot: {e}')
    
    if key == 'f7':  # Toggle view and axis visibility
        if scene_manager.current_state == GameState.SPACE:
            player.third_person = not player.third_person
            player.axis_indicator.enabled = player.third_person
            if player.third_person:
                camera.position = (0, 0, -15)
            else:
                camera.position = (0, 0, 0)
    
    if key == 'f8':  # Toggle between space and town
        try:
            if scene_manager.current_state == GameState.SPACE:
                scene_manager.switch_to_town()
            else:
                scene_manager.switch_to_space()
        except Exception as e:
            print(f'Error switching scenes: {e}')
    
    if key == 'left mouse down' and not paused:
        if scene_manager.current_state == GameState.SPACE:
            try:
                # Shoot a projectile
                bullet = Entity(
                    model='sphere',
                    color=color.yellow,
                    position=player.position,
                    scale=0.2
                )
                bullet.animate_position(
                    player.position + player.forward * 100,
                    duration=2,
                    curve=curve.linear
                )
                destroy(bullet, delay=2)
            except Exception as e:
                print(f'Error shooting projectile: {e}')

# Run the game
if __name__ == "__main__":
    print("Starting ILK Space Game...")
    print("Press ESC for pause menu, F6 for screenshots, F7 for third-person view, F8 to switch modes")
    try:
        app.run()
    except Exception as e:
        print(f"Error running game: {e}")