#!/usr/bin/env python3

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import numpy as np
import os
import math
import json
import pickle
from datetime import datetime

app = Ursina(borderless=False)  # Make window resizable and movable

# Trading and Economy System
class Commodity:
    def __init__(self, name, base_price, category="general"):
        self.name = name
        self.base_price = base_price
        self.category = category
        
    def get_price(self, planet_type="generic", supply_demand_modifier=1.0):
        """Calculate price based on planet type and market conditions"""
        price_modifiers = {
            "agricultural": {"food": 0.7, "technology": 1.3, "minerals": 1.1, "luxury": 1.2},
            "industrial": {"minerals": 0.8, "technology": 0.9, "food": 1.4, "luxury": 1.1},
            "mining": {"minerals": 0.6, "technology": 1.5, "food": 1.3, "luxury": 1.4},
            "tech": {"technology": 0.8, "luxury": 0.9, "food": 1.2, "minerals": 1.3},
            "luxury": {"luxury": 0.8, "food": 1.1, "technology": 1.2, "minerals": 1.2}
        }
        
        modifier = price_modifiers.get(planet_type, {}).get(self.category, 1.0)
        final_price = self.base_price * modifier * supply_demand_modifier
        return max(1, int(final_price))  # Minimum price of 1 credit

class CargoSystem:
    def __init__(self, max_capacity=100):
        self.max_capacity = max_capacity
        self.cargo = {}  # {commodity_name: quantity}
        
    def get_used_capacity(self):
        return sum(self.cargo.values())
        
    def get_free_capacity(self):
        return self.max_capacity - self.get_used_capacity()
        
    def can_add(self, commodity_name, quantity):
        return self.get_free_capacity() >= quantity
        
    def add_cargo(self, commodity_name, quantity):
        if self.can_add(commodity_name, quantity):
            self.cargo[commodity_name] = self.cargo.get(commodity_name, 0) + quantity
            return True
        return False
        
    def remove_cargo(self, commodity_name, quantity):
        current = self.cargo.get(commodity_name, 0)
        if current >= quantity:
            self.cargo[commodity_name] = current - quantity
            if self.cargo[commodity_name] == 0:
                del self.cargo[commodity_name]
            return True
        return False
        
    def get_cargo_list(self):
        return [(name, qty) for name, qty in self.cargo.items()]

class MarketSystem:
    def __init__(self):
        # Define available commodities
        self.commodities = {
            "food": Commodity("Food", 10, "food"),
            "minerals": Commodity("Minerals", 25, "minerals"),
            "technology": Commodity("Technology", 50, "technology"),
            "luxury_goods": Commodity("Luxury Goods", 75, "luxury"),
            "medicine": Commodity("Medicine", 40, "food"),
            "weapons": Commodity("Weapons", 60, "technology"),
            "fuel": Commodity("Fuel", 15, "minerals"),
            "spices": Commodity("Spices", 35, "luxury")
        }
        
        # Planet market data: {planet_name: {commodity: (supply_level, demand_level)}}
        self.planet_markets = {}
        
    def generate_market_for_planet(self, planet_name, planet_type="generic"):
        """Generate a market with random supply/demand for a planet"""
        market = {}
        for commodity_name in self.commodities.keys():
            # Random supply/demand between 0.5 and 2.0
            supply_demand = random.uniform(0.5, 2.0)
            market[commodity_name] = supply_demand
        
        # Store planet type for price calculations
        self.planet_markets[planet_name] = {
            'market': market,
            'type': planet_type
        }
        
    def get_buy_price(self, planet_name, commodity_name):
        """Price player pays to buy from planet"""
        if planet_name not in self.planet_markets:
            return 0
            
        commodity = self.commodities.get(commodity_name)
        if not commodity:
            return 0
            
        planet_data = self.planet_markets[planet_name]
        supply_demand = planet_data['market'].get(commodity_name, 1.0)
        planet_type = planet_data['type']
        
        return commodity.get_price(planet_type, supply_demand)
        
    def get_sell_price(self, planet_name, commodity_name):
        """Price player gets when selling to planet"""
        buy_price = self.get_buy_price(planet_name, commodity_name)
        return max(1, int(buy_price * 0.8))  # 20% margin for the market

class PlayerWallet:
    def __init__(self, starting_credits=1000):
        self.credits = starting_credits
        
    def can_afford(self, amount):
        return self.credits >= amount
        
    def spend(self, amount):
        if self.can_afford(amount):
            self.credits -= amount
            return True
        return False
        
    def earn(self, amount):
        self.credits += amount

# Ship Upgrade System
class ShipUpgrades:
    def __init__(self):
        self.cargo_capacity = 50  # Starting cargo capacity
        self.engine_level = 1     # Engine upgrade level (affects speed)
        self.fuel_efficiency = 1  # Fuel efficiency level
        
        # Upgrade costs (exponentially increasing)
        self.upgrade_costs = {
            'cargo': 200,    # Cost for next cargo upgrade
            'engine': 500,   # Cost for next engine upgrade  
            'fuel': 300      # Cost for next fuel upgrade
        }
        
    def can_afford_upgrade(self, upgrade_type):
        cost = self.upgrade_costs.get(upgrade_type, 0)
        return player_wallet.can_afford(cost)
        
    def upgrade_cargo(self):
        if self.can_afford_upgrade('cargo'):
            cost = self.upgrade_costs['cargo']
            player_wallet.spend(cost)
            
            # Increase cargo capacity
            old_capacity = self.cargo_capacity
            self.cargo_capacity += 25
            player_cargo.max_capacity = self.cargo_capacity
            
            # Increase cost for next upgrade
            self.upgrade_costs['cargo'] = int(cost * 1.5)
            
            print(f"Cargo upgraded! Capacity: {old_capacity} -> {self.cargo_capacity}")
            return True
        return False
        
    def upgrade_engine(self):
        if self.can_afford_upgrade('engine'):
            cost = self.upgrade_costs['engine']
            player_wallet.spend(cost)
            
            # Increase engine level and player speed
            self.engine_level += 1
            player.speed += 2
            player.max_speed += 10
            
            # Increase cost for next upgrade
            self.upgrade_costs['engine'] = int(cost * 1.8)
            
            print(f"Engine upgraded! Level: {self.engine_level}, Speed increased!")
            return True
        return False
        
    def upgrade_fuel_efficiency(self):
        if self.can_afford_upgrade('fuel'):
            cost = self.upgrade_costs['fuel']
            player_wallet.spend(cost)
            
            # Increase fuel efficiency level
            self.fuel_efficiency += 1
            
            # Increase cost for next upgrade
            self.upgrade_costs['fuel'] = int(cost * 1.4)
            
            print(f"Fuel efficiency upgraded! Level: {self.fuel_efficiency}")
            return True
        return False

# Global systems
market_system = MarketSystem()
player_cargo = CargoSystem(max_capacity=50)  # Start with small cargo hold
player_wallet = PlayerWallet(starting_credits=500)
ship_upgrades = ShipUpgrades()

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
        
        # Load all six faces of the skybox
        self.textures = {
            'right': load_texture('assets/textures/skybox_right.png'),
            'left': load_texture('assets/textures/skybox_left.png'),
            'top': load_texture('assets/textures/skybox_top.png'),
            'bottom': load_texture('assets/textures/skybox_bottom.png'),
            'front': load_texture('assets/textures/skybox_front.png'),
            'back': load_texture('assets/textures/skybox_back.png')
        }
        
        # Apply textures to the skybox
        self.texture = self.textures['right']
        
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
            position=(-0.45, 0.45),
            scale=0.8,
            color=color.white
        )
        
        # Credits and cargo display
        self.credits_text = Text(
            parent=camera.ui,
            text='Credits: 500',
            position=(-0.45, 0.4),
            scale=0.8,
            color=color.yellow
        )
        
        self.cargo_text = Text(
            parent=camera.ui,
            text='Cargo: 0/50',
            position=(-0.45, 0.35),
            scale=0.8,
            color=color.cyan
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
            
            # Update credits and cargo display
            self.credits_text.text = f'Credits: {player_wallet.credits}'
            used_capacity = player_cargo.get_used_capacity()
            self.cargo_text.text = f'Cargo: {used_capacity}/{player_cargo.max_capacity}'

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
        self.current_planet = None  # Track which planet player is on
        
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
            
            # Add trading post (large blue building near the podium)
            trading_post = Entity(
                model='cube',
                color=color.blue,
                texture='white_cube',
                position=(10, 3, 0),  # Next to podium
                scale=(6, 6, 6),
                collider='box'
            )
            
            # Add trading post sign
            trading_sign = Text(
                parent=trading_post,
                text='TRADING POST\n[T] to Trade',
                position=(0, 0, 3.1),
                scale=100,
                color=color.white,
                billboard=True
            )
            
            self.town_entities.extend([trading_post, trading_sign])
            
            # Add shipyard (large orange building on the other side)
            shipyard = Entity(
                model='cube',
                color=color.orange,
                texture='white_cube',
                position=(-10, 3, 0),  # Opposite side from trading post
                scale=(6, 6, 6),
                collider='box'
            )
            
            # Add shipyard sign
            shipyard_sign = Text(
                parent=shipyard,
                text='SHIPYARD\n[U] for Upgrades',
                position=(0, 0, 3.1),
                scale=100,
                color=color.white,
                billboard=True
            )
            
            self.town_entities.extend([shipyard, shipyard_sign])
            
            # Add some NPCs (simple colored cubes for now)
            npc_positions = [(15, 1, 15), (-15, 1, -15), (20, 1, -10), (-10, 1, 20)]
            for i, pos in enumerate(npc_positions):
                npc = Entity(
                    model='cube',
                    color=color.random_color(),
                    position=pos,
                    scale=(1, 2, 1),
                    collider='box'
                )
                
                npc_sign = Text(
                    parent=npc,
                    text=f'Citizen {i+1}',
                    position=(0, 0, 1.1),
                    scale=50,
                    color=color.white,
                    billboard=True
                )
                
                self.town_entities.extend([npc, npc_sign])
            
            # Create and position the town controller on the podium
            self.town_controller = TownController()
            self.town_controller.position = Vec3(0, 1.5, 0)
    
    def switch_to_town(self):
        if self.current_state == GameState.SPACE:
            # Store and reset space controller state
            self.space_controller.disable()
            self.space_controller.status_text.enabled = False
            self.space_controller.credits_text.enabled = False
            self.space_controller.cargo_text.enabled = False
            
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
            self.space_controller.credits_text.enabled = True
            self.space_controller.cargo_text.enabled = True
            camera.parent = self.space_controller
            camera.rotation = (0, 0, 0)
            camera.position = (0, 0, -15) if self.space_controller.third_person else (0, 0, 0)
            
            # Clear current planet when leaving
            self.current_planet = None
            
            self.current_state = GameState.SPACE

# Create scene manager
scene_manager = SceneManager()

def save_game():
    if not os.path.exists('saves'):
        os.makedirs('saves')
    
    game_state = {
        'current_scene': scene_manager.current_state,
        'player_position': (player.position.x, player.position.y, player.position.z),
        'player_rotation': (player.rotation.x, player.rotation.y, player.rotation.z),
        'planets': [(p.position.x, p.position.y, p.position.z, p.scale) for p in planets]
    }
    
    if scene_manager.current_state == GameState.TOWN:
        game_state['town_player_position'] = (
            scene_manager.town_controller.position.x,
            scene_manager.town_controller.position.y,
            scene_manager.town_controller.position.z
        )
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'saves/save_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(game_state, f)
    print(f'Game saved to {filename}')

def load_game():
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
        pos = game_state['town_player_position']
        player.position = Vec3(pos[0], pos[1], pos[2])
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

def quit_game():
    application.quit()

save_button.on_click = save_game
load_button.on_click = load_game
quit_button.on_click = quit_game

# Planet class
class Planet(Entity):
    def __init__(self, position=(0,0,0)):
        # Define planet types and their characteristics
        planet_types = {
            "agricultural": {"color": color.green, "name_prefix": "Agri"},
            "industrial": {"color": color.gray, "name_prefix": "Forge"},
            "mining": {"color": color.brown, "name_prefix": "Mine"},
            "tech": {"color": color.blue, "name_prefix": "Tech"},
            "luxury": {"color": color.magenta, "name_prefix": "Haven"}
        }
        
        # Randomly select planet type
        self.planet_type = random.choice(list(planet_types.keys()))
        planet_data = planet_types[self.planet_type]
        
        super().__init__(
            model='sphere',
            color=planet_data["color"].tint(random.uniform(-0.3, 0.3)),
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
        self.name = f"{planet_data['name_prefix']}-{random.randint(100, 999)}"
        
        # Generate market for this planet
        market_system.generate_market_for_planet(self.name, self.planet_type)
    
    def update(self):
        pass  # Remove rotation update
        
    def is_player_in_landing_range(self, player_position):
        # Calculate distance to player
        distance = (self.position - player_position).length()
        return distance < self.landing_radius

# Create planets
planets = []
for _ in range(15):
    pos = Vec3(
        random.uniform(-500, 500),
        random.uniform(-500, 500),
        random.uniform(-500, 500)
    )
    if pos.length() > 100:
        planet = Planet(position=pos)
        planets.append(planet)

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

# Trading UI
class TradingUI:
    def __init__(self):
        self.active = False
        self.current_planet = None
        
        # Main trading panel
        self.panel = Panel(
            parent=camera.ui,
            model='quad',
            scale=(0.9, 0.9),
            color=color.black66,
            enabled=False
        )
        
        # Title
        self.title = Text(
            parent=self.panel,
            text='TRADING POST',
            position=(0, 0.4),
            scale=2,
            color=color.white
        )
        
        # Current planet info
        self.planet_info = Text(
            parent=self.panel,
            text='',
            position=(-0.4, 0.3),
            scale=1,
            color=color.cyan
        )
        
        # Player's credits and cargo
        self.player_info = Text(
            parent=self.panel,
            text='',
            position=(0.4, 0.3),
            scale=1,
            color=color.yellow
        )
        
        # Commodity list
        self.commodity_list = Text(
            parent=self.panel,
            text='',
            position=(-0.4, -0.1),
            scale=0.8,
            color=color.white
        )
        
        # Instructions
        self.instructions = Text(
            parent=self.panel,
            text='Use 1-8 to buy, SHIFT+1-8 to sell\nESC to close',
            position=(0, -0.4),
            scale=1,
            color=color.light_gray
        )
        
    def show(self, planet_name):
        self.active = True
        self.current_planet = planet_name
        self.panel.enabled = True
        self.update_display()
        
        # Pause game and show cursor
        mouse.locked = False
        mouse.visible = True
        
    def hide(self):
        self.active = False
        self.current_planet = None
        self.panel.enabled = False
        
        # Resume game and hide cursor
        mouse.locked = True
        mouse.visible = False
        
    def update_display(self):
        if not self.current_planet:
            return
            
        # Update planet info
        planet_type = market_system.planet_markets[self.current_planet]['type']
        self.planet_info.text = f'Planet: {self.current_planet}\nType: {planet_type.title()}'
        
        # Update player info
        self.player_info.text = f'Credits: {player_wallet.credits}\nCargo: {player_cargo.get_used_capacity()}/{player_cargo.max_capacity}'
        
        # Update commodity list
        commodity_text = "COMMODITIES:\n\n"
        commodities = list(market_system.commodities.keys())
        for i, commodity_name in enumerate(commodities[:8]):  # Show first 8 commodities
            buy_price = market_system.get_buy_price(self.current_planet, commodity_name)
            sell_price = market_system.get_sell_price(self.current_planet, commodity_name)
            player_has = player_cargo.cargo.get(commodity_name, 0)
            commodity_text += f"{i+1}. {commodity_name.replace('_', ' ').title()}\n"
            commodity_text += f"   Buy: {buy_price}  Sell: {sell_price}  Have: {player_has}\n\n"
        
        self.commodity_list.text = commodity_text
        
    def handle_input(self, key):
        if not self.active or not self.current_planet:
            return False
            
        # Handle number keys for buying
        if key in '12345678':
            commodity_index = int(key) - 1
            commodities = list(market_system.commodities.keys())
            if commodity_index < len(commodities):
                commodity_name = commodities[commodity_index]
                self.buy_commodity(commodity_name)
                return True
                
        # Handle shift+number for selling
        elif key.startswith('shift+') and key[-1] in '12345678':
            commodity_index = int(key[-1]) - 1
            commodities = list(market_system.commodities.keys())
            if commodity_index < len(commodities):
                commodity_name = commodities[commodity_index]
                self.sell_commodity(commodity_name)
                return True
                
        return False
        
    def buy_commodity(self, commodity_name):
        buy_price = market_system.get_buy_price(self.current_planet, commodity_name)
        
        if player_wallet.can_afford(buy_price) and player_cargo.can_add(commodity_name, 1):
            player_wallet.spend(buy_price)
            player_cargo.add_cargo(commodity_name, 1)
            print(f"Bought 1 {commodity_name.replace('_', ' ')} for {buy_price} credits")
            self.update_display()
        elif not player_wallet.can_afford(buy_price):
            print("Not enough credits!")
        else:
            print("Cargo hold full!")
            
    def sell_commodity(self, commodity_name):
        if player_cargo.cargo.get(commodity_name, 0) > 0:
            sell_price = market_system.get_sell_price(self.current_planet, commodity_name)
            player_cargo.remove_cargo(commodity_name, 1)
            player_wallet.earn(sell_price)
            print(f"Sold 1 {commodity_name.replace('_', ' ')} for {sell_price} credits")
            self.update_display()
        else:
            print(f"You don't have any {commodity_name.replace('_', ' ')}!")

# Create trading UI
trading_ui = TradingUI()

# Upgrade UI
class UpgradeUI:
    def __init__(self):
        self.active = False
        
        # Main upgrade panel
        self.panel = Panel(
            parent=camera.ui,
            model='quad',
            scale=(0.8, 0.8),
            color=color.black66,
            enabled=False
        )
        
        # Title
        self.title = Text(
            parent=self.panel,
            text='SHIPYARD - UPGRADES',
            position=(0, 0.35),
            scale=2,
            color=color.orange
        )
        
        # Player info
        self.player_info = Text(
            parent=self.panel,
            text='',
            position=(0, 0.25),
            scale=1,
            color=color.yellow
        )
        
        # Upgrade options
        self.upgrade_list = Text(
            parent=self.panel,
            text='',
            position=(0, -0.05),
            scale=1,
            color=color.white
        )
        
        # Instructions
        self.instructions = Text(
            parent=self.panel,
            text='Press 1-3 to purchase upgrades\nESC to close',
            position=(0, -0.35),
            scale=1,
            color=color.light_gray
        )
        
    def show(self):
        self.active = True
        self.panel.enabled = True
        self.update_display()
        
        # Pause game and show cursor
        mouse.locked = False
        mouse.visible = True
        
    def hide(self):
        self.active = False
        self.panel.enabled = False
        
        # Resume game and hide cursor
        mouse.locked = True
        mouse.visible = False
        
    def update_display(self):
        # Update player info
        self.player_info.text = f'Credits: {player_wallet.credits}'
        
        # Update upgrade options
        upgrade_text = "AVAILABLE UPGRADES:\n\n"
        
        # Cargo upgrade
        cargo_cost = ship_upgrades.upgrade_costs['cargo']
        cargo_affordable = "✓" if ship_upgrades.can_afford_upgrade('cargo') else "✗"
        upgrade_text += f"1. Cargo Hold Upgrade - {cargo_cost} credits {cargo_affordable}\n"
        upgrade_text += f"   Current: {ship_upgrades.cargo_capacity} -> {ship_upgrades.cargo_capacity + 25}\n\n"
        
        # Engine upgrade
        engine_cost = ship_upgrades.upgrade_costs['engine']
        engine_affordable = "✓" if ship_upgrades.can_afford_upgrade('engine') else "✗"
        upgrade_text += f"2. Engine Upgrade - {engine_cost} credits {engine_affordable}\n"
        upgrade_text += f"   Current Level: {ship_upgrades.engine_level} -> {ship_upgrades.engine_level + 1}\n\n"
        
        # Fuel efficiency upgrade
        fuel_cost = ship_upgrades.upgrade_costs['fuel']
        fuel_affordable = "✓" if ship_upgrades.can_afford_upgrade('fuel') else "✗"
        upgrade_text += f"3. Fuel Efficiency - {fuel_cost} credits {fuel_affordable}\n"
        upgrade_text += f"   Current Level: {ship_upgrades.fuel_efficiency} -> {ship_upgrades.fuel_efficiency + 1}\n"
        
        self.upgrade_list.text = upgrade_text
        
    def handle_input(self, key):
        if not self.active:
            return False
            
        if key == '1':
            if ship_upgrades.upgrade_cargo():
                self.update_display()
            else:
                print("Cannot afford cargo upgrade!")
            return True
        elif key == '2':
            if ship_upgrades.upgrade_engine():
                self.update_display()
            else:
                print("Cannot afford engine upgrade!")
            return True
        elif key == '3':
            if ship_upgrades.upgrade_fuel_efficiency():
                self.update_display()
            else:
                print("Cannot afford fuel efficiency upgrade!")
            return True
                
        return False

# Create upgrade UI
upgrade_ui = UpgradeUI()

def update():
    global nearby_planet
    
    if not paused and not trading_ui.active and not upgrade_ui.active:
        if scene_manager.current_state == GameState.SPACE:
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
                
        elif scene_manager.current_state == GameState.TOWN:
            # Check if player is near trading post in town
            if scene_manager.town_controller:
                player_pos = scene_manager.town_controller.position
                trading_post_pos = Vec3(10, 3, 0)  # Position of trading post
                distance = (player_pos - trading_post_pos).length()
                
                # Show trading prompt if close to trading post
                if distance < 10:  # Within 10 units of trading post
                    # Display prompt on screen
                    pass  # We'll handle this with T key press

# Function to handle landing
def land_on_planet():
    global nearby_planet
    if nearby_planet:
        # Set current planet in scene manager
        scene_manager.current_planet = nearby_planet
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
    
    # Handle UI input first
    if trading_ui.handle_input(key):
        return
    if upgrade_ui.handle_input(key):
        return
    
    if key == 'escape':
        # Close UIs if open
        if trading_ui.active:
            trading_ui.hide()
            return
        if upgrade_ui.active:
            upgrade_ui.hide()
            return
            
        paused = not paused
        pause_panel.enabled = paused
        save_button.enabled = paused
        load_button.enabled = paused
        quit_button.enabled = paused
        
        if scene_manager.current_state == GameState.SPACE:
            player.enabled = not paused
        else:
            scene_manager.town_controller.enabled = not paused
            
        mouse.locked = not paused
        if paused:
            mouse.visible = True
        else:
            mouse.visible = False
    
    if key == 'f6':  # Screenshot
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        base.win.saveScreenshot(Filename(f'screenshots/screenshot_{time.time()}.png'))
        print(f'Screenshot saved to screenshots folder')
    
    if key == 'f7':  # Toggle view and axis visibility
        if scene_manager.current_state == GameState.SPACE:
            player.third_person = not player.third_person
            player.axis_indicator.enabled = player.third_person
            if player.third_person:
                camera.position = (0, 0, -15)
            else:
                camera.position = (0, 0, 0)
    
    if key == 'f8':  # Toggle between space and town
        if scene_manager.current_state == GameState.SPACE:
            scene_manager.switch_to_town()
        else:
            scene_manager.switch_to_space()
    
    if key == 't' and scene_manager.current_state == GameState.TOWN and not paused:
        # Open trading if near trading post
        if scene_manager.town_controller:
            player_pos = scene_manager.town_controller.position
            trading_post_pos = Vec3(10, 3, 0)
            distance = (player_pos - trading_post_pos).length()
            
            if distance < 10:  # Within range of trading post
                # Use the current planet the player landed on
                if scene_manager.current_planet:
                    trading_ui.show(scene_manager.current_planet.name)
                else:
                    # Fallback for testing
                    planet_name = "Local Trading Post"
                    if planet_name not in market_system.planet_markets:
                        market_system.generate_market_for_planet(planet_name, "generic")
                                         trading_ui.show(planet_name)
            else:
                print("You need to be closer to the trading post!")
    
    if key == 'u' and scene_manager.current_state == GameState.TOWN and not paused:
        # Open upgrades if near shipyard
        if scene_manager.town_controller:
            player_pos = scene_manager.town_controller.position
            shipyard_pos = Vec3(-10, 3, 0)  # Position of shipyard
            distance = (player_pos - shipyard_pos).length()
            
            if distance < 10:  # Within range of shipyard
                upgrade_ui.show()
            else:
                print("You need to be closer to the shipyard!")
    
    if key == 'left mouse down' and not paused:
        if scene_manager.current_state == GameState.SPACE:
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

# Run the game
app.run() 