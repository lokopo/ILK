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
            "luxury": {"luxury": 0.8, "food": 1.1, "technology": 1.2, "minerals": 1.2},
            "desert": {"food": 1.5, "technology": 1.2, "minerals": 0.9, "luxury": 1.3},
            "ice": {"food": 1.4, "technology": 1.1, "minerals": 1.0, "luxury": 1.2},
            "volcanic": {"minerals": 0.7, "technology": 1.3, "food": 1.6, "luxury": 1.1},
            "gas_giant": {"fuel": 0.5, "technology": 1.4, "food": 1.8, "luxury": 1.0},
            "oceanic": {"food": 0.9, "technology": 1.1, "minerals": 1.2, "luxury": 0.9}
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
        
        # Health and combat display
        self.health_text = Text(
            parent=camera.ui,
            text='Health: 100/100',
            position=(-0.45, 0.3),
            scale=0.8,
            color=color.red
        )
        
        # Crew and time display
        self.crew_text = Text(
            parent=camera.ui,
            text='Crew: 2/10 (Morale: 75%)',
            position=(-0.45, 0.25),
            scale=0.8,
            color=color.green
        )
        
        self.time_text = Text(
            parent=camera.ui,
            text='Day 1',
            position=(-0.45, 0.2),
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
            
            # Update credits and cargo display
            self.credits_text.text = f'Credits: {player_wallet.credits}'
            used_capacity = player_cargo.get_used_capacity()
            self.cargo_text.text = f'Cargo: {used_capacity}/{player_cargo.max_capacity}'
            
            # Update health display
            self.health_text.text = f'Health: {combat_system.player_health}/{combat_system.max_health}'
            
            # Update crew display
            crew_count = len(crew_system.crew_members)
            self.crew_text.text = f'Crew: {crew_count}/{crew_system.max_crew} (Morale: {crew_system.morale}%)'
            
            # Update time display
            self.time_text.text = f'Day {time_system.game_day}'

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
            
            # Add faction embassy (purple building)
            embassy = Entity(
                model='cube',
                color=color.violet,
                texture='white_cube',
                position=(0, 3, -10),  # Behind podium
                scale=(6, 6, 6),
                collider='box'
            )
            
            embassy_sign = Text(
                parent=embassy,
                text='FACTION EMBASSY\n[R] for Relations',
                position=(0, 0, 3.1),
                scale=100,
                color=color.white,
                billboard=True
            )
            
            # Add crew quarters (green building)
            crew_quarters = Entity(
                model='cube',
                color=color.lime,
                texture='white_cube',
                position=(0, 3, 10),  # In front of podium
                scale=(6, 6, 6),
                collider='box'
            )
            
            crew_sign = Text(
                parent=crew_quarters,
                text='CREW QUARTERS\n[C] for Crew Management',
                position=(0, 0, 3.1),
                scale=100,
                color=color.white,
                billboard=True
            )
            
            # Add mission board (yellow building)
            mission_board = Entity(
                model='cube',
                color=color.gold,
                texture='white_cube',
                position=(-10, 3, -10),  # Corner position
                scale=(6, 6, 6),
                collider='box'
            )
            
            mission_sign = Text(
                parent=mission_board,
                text='MISSION BOARD\n[M] for Missions',
                position=(0, 0, 3.1),
                scale=100,
                color=color.white,
                billboard=True
            )
            
            self.town_entities.extend([embassy, embassy_sign, crew_quarters, crew_sign, mission_board, mission_sign])
            
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
            self.space_controller.health_text.enabled = False
            self.space_controller.crew_text.enabled = False
            self.space_controller.time_text.enabled = False
            
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
            self.space_controller.health_text.enabled = True
            self.space_controller.crew_text.enabled = True
            self.space_controller.time_text.enabled = True
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
            "luxury": {"color": color.magenta, "name_prefix": "Haven"},
            "desert": {"color": color.yellow, "name_prefix": "Dune"},
            "ice": {"color": color.cyan, "name_prefix": "Frost"},
            "volcanic": {"color": color.red, "name_prefix": "Ember"},
            "gas_giant": {"color": color.violet, "name_prefix": "Storm"},
            "oceanic": {"color": color.azure, "name_prefix": "Aqua"}
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

# Random Events System
class RandomEventSystem:
    def __init__(self):
        self.last_event_time = 0
        self.event_cooldown = 30  # Minimum 30 seconds between events
        self.event_chance = 0.02  # 2% chance per second when cooldown is over
        
        self.events = [
            {
                'name': 'Derelict Ship',
                'description': 'You discover a derelict ship floating in space.',
                'options': [
                    {'text': 'Investigate (Risk/Reward)', 'action': 'investigate_derelict'},
                    {'text': 'Ignore and continue', 'action': 'ignore'}
                ]
            },
            {
                'name': 'Pirate Encounter',
                'description': 'A pirate ship demands tribute!',
                'options': [
                    {'text': 'Pay 50 credits', 'action': 'pay_pirates'},
                    {'text': 'Fight!', 'action': 'fight_pirates'},
                    {'text': 'Try to escape', 'action': 'escape_pirates'}
                ]
            },
            {
                'name': 'Merchant Convoy',
                'description': 'A friendly merchant offers to trade.',
                'options': [
                    {'text': 'Trade with merchant', 'action': 'trade_merchant'},
                    {'text': 'Continue on your way', 'action': 'ignore'}
                ]
            },
            {
                'name': 'Asteroid Field',
                'description': 'You enter a dangerous asteroid field.',
                'options': [
                    {'text': 'Navigate carefully', 'action': 'navigate_asteroids'},
                    {'text': 'Power through quickly', 'action': 'rush_asteroids'}
                ]
            }
        ]
        
    def check_for_event(self):
        current_time = time.time()
        if current_time - self.last_event_time > self.event_cooldown:
            if random.random() < self.event_chance:
                self.trigger_random_event()
                self.last_event_time = current_time
                
    def trigger_random_event(self):
        event = random.choice(self.events)
        event_ui.show_event(event)
        
    def handle_event_action(self, action):
        if action == 'investigate_derelict':
            if random.random() < 0.6:  # 60% chance of success
                reward = random.randint(50, 200)
                player_wallet.earn(reward)
                print(f"You found {reward} credits in the derelict ship!")
                
                # Small chance to find valuable cargo
                if random.random() < 0.3:
                    rare_cargo = random.choice(['technology', 'luxury_goods', 'weapons'])
                    if player_cargo.can_add(rare_cargo, 1):
                        player_cargo.add_cargo(rare_cargo, 1)
                        print(f"You also found rare {rare_cargo.replace('_', ' ')}!")
            else:
                damage = random.randint(10, 30)
                print(f"The ship was booby-trapped! You lose {damage} credits in repairs.")
                player_wallet.spend(min(damage, player_wallet.credits))
                
        elif action == 'pay_pirates':
            if player_wallet.can_afford(50):
                player_wallet.spend(50)
                print("The pirates take your credits and leave you alone.")
            else:
                print("You don't have enough credits! The pirates attack!")
                self.handle_event_action('fight_pirates')
                
        elif action == 'fight_pirates':
            # Combat success based on crew, weapons, and ship upgrades
            combat_bonus = crew_system.get_total_bonuses()["combat"]
            weapon_bonus = combat_system.weapon_level * 10
            success_chance = 0.5 + (combat_bonus + weapon_bonus) / 100
            
            if random.random() < success_chance:
                reward = random.randint(100, 300)
                player_wallet.earn(reward)
                print(f"You defeated the pirates and salvaged {reward} credits!")
                
                # Gain reputation with law-abiding factions
                faction_system.change_reputation('terran_federation', 5)
                faction_system.change_reputation('mars_republic', 3)
                faction_system.change_reputation('merchant_guild', 5)
                # Lose reputation with pirates
                faction_system.change_reputation('outer_rim_pirates', -10)
            else:
                damage = random.randint(50, 100)
                print(f"The pirates damaged your ship! Repair costs: {damage} credits.")
                player_wallet.spend(min(damage, player_wallet.credits))
                combat_system.take_damage(random.randint(10, 30))
                
        elif action == 'escape_pirates':
            if random.random() < 0.8:  # 80% chance to escape
                print("You successfully escaped the pirates!")
            else:
                print("The pirates caught you anyway!")
                self.handle_event_action('fight_pirates')
                
        elif action == 'trade_merchant':
            # Simple trade - merchant buys all cargo at good prices
            total_earned = 0
            for commodity_name, quantity in list(player_cargo.cargo.items()):
                sell_price = random.randint(30, 80)  # Better than planet prices
                earnings = sell_price * quantity
                total_earned += earnings
                player_cargo.remove_cargo(commodity_name, quantity)
                
            if total_earned > 0:
                player_wallet.earn(total_earned)
                print(f"The merchant bought all your cargo for {total_earned} credits!")
            else:
                print("You have no cargo to trade.")
                
        elif action == 'navigate_asteroids':
            print("You carefully navigate the asteroid field.")
            # Small chance to find rare minerals
            if random.random() < 0.3:
                if player_cargo.can_add('minerals', 5):
                    player_cargo.add_cargo('minerals', 5)
                    print("You collected 5 rare minerals from the asteroids!")
                    
        elif action == 'rush_asteroids':
            if random.random() < 0.5:  # 50% chance of damage
                damage = random.randint(20, 60)
                print(f"Your ship was damaged by asteroids! Repair costs: {damage} credits.")
                player_wallet.spend(min(damage, player_wallet.credits))
            else:
                print("You made it through the asteroid field unscathed!")

# Enhanced Combat System
class CombatSystem:
    def __init__(self):
        self.player_health = 100
        self.max_health = 100
        self.weapon_level = 1
        self.shield_level = 1
        
    def get_damage_output(self):
        base_damage = 20
        weapon_bonus = (self.weapon_level - 1) * 10
        return base_damage + weapon_bonus
        
    def get_defense_rating(self):
        base_defense = 5
        shield_bonus = (self.shield_level - 1) * 5
        return base_defense + shield_bonus
        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.get_defense_rating())
        self.player_health = max(0, self.player_health - actual_damage)
        return actual_damage
        
    def heal(self, amount):
        self.player_health = min(self.max_health, self.player_health + amount)
        
    def upgrade_weapons(self):
        cost = self.weapon_level * 300
        if player_wallet.can_afford(cost):
            player_wallet.spend(cost)
            self.weapon_level += 1
            print(f"Weapons upgraded to level {self.weapon_level}!")
            return True
        return False
        
    def upgrade_shields(self):
        cost = self.shield_level * 250
        if player_wallet.can_afford(cost):
            player_wallet.spend(cost)
            self.shield_level += 1
            print(f"Shields upgraded to level {self.shield_level}!")
            return True
        return False

# Faction System - Core of Pirates! gameplay
class Faction:
    def __init__(self, name, color_scheme, home_planets=None):
        self.name = name
        self.color_scheme = color_scheme
        self.home_planets = home_planets or []
        self.wealth = random.randint(50000, 100000)
        self.military_strength = random.randint(50, 100)
        self.trade_power = random.randint(30, 80)
        
        # Relationships with other factions (-100 to 100)
        self.relationships = {}
        
class FactionSystem:
    def __init__(self):
        self.factions = {
            'terran_federation': Faction("Terran Federation", color.blue),
            'mars_republic': Faction("Mars Republic", color.red), 
            'jupiter_consortium': Faction("Jupiter Consortium", color.orange),
            'outer_rim_pirates': Faction("Outer Rim Pirates", color.dark_gray),
            'merchant_guild': Faction("Merchant Guild", color.green),
            'independent': Faction("Independent Colonies", color.white)
        }
        
        # Player reputation with each faction (-100 to 100)
        self.player_reputation = {
            faction_id: 0 for faction_id in self.factions.keys()
        }
        
        # Set up initial relationships between factions
        self.setup_faction_relationships()
        
    def setup_faction_relationships(self):
        # Set up complex web of faction relationships
        relationships = {
            'terran_federation': {'mars_republic': -30, 'jupiter_consortium': 20, 'outer_rim_pirates': -80, 'merchant_guild': 40, 'independent': 10},
            'mars_republic': {'terran_federation': -30, 'jupiter_consortium': -10, 'outer_rim_pirates': -60, 'merchant_guild': 20, 'independent': 30},
            'jupiter_consortium': {'terran_federation': 20, 'mars_republic': -10, 'outer_rim_pirates': -40, 'merchant_guild': 60, 'independent': 0},
            'outer_rim_pirates': {'terran_federation': -80, 'mars_republic': -60, 'jupiter_consortium': -40, 'merchant_guild': -50, 'independent': 10},
            'merchant_guild': {'terran_federation': 40, 'mars_republic': 20, 'jupiter_consortium': 60, 'outer_rim_pirates': -50, 'independent': 30},
            'independent': {'terran_federation': 10, 'mars_republic': 30, 'jupiter_consortium': 0, 'outer_rim_pirates': 10, 'merchant_guild': 30}
        }
        
        for faction_id, faction in self.factions.items():
            faction.relationships = relationships.get(faction_id, {})
            
    def change_reputation(self, faction_id, change):
        if faction_id in self.player_reputation:
            old_rep = self.player_reputation[faction_id]
            self.player_reputation[faction_id] = max(-100, min(100, old_rep + change))
            
            # Reputation changes affect relationships with allied/enemy factions
            self.apply_reputation_effects(faction_id, change)
            
    def apply_reputation_effects(self, changed_faction, change):
        faction = self.factions[changed_faction]
        for other_faction_id, relationship in faction.relationships.items():
            if relationship > 50:  # Allied factions
                self.player_reputation[other_faction_id] += int(change * 0.3)
            elif relationship < -50:  # Enemy factions
                self.player_reputation[other_faction_id] -= int(change * 0.2)
                
    def get_reputation_status(self, faction_id):
        rep = self.player_reputation[faction_id]
        if rep >= 80: return "Hero"
        elif rep >= 60: return "Champion"
        elif rep >= 40: return "Friend"
        elif rep >= 20: return "Ally"
        elif rep >= -20: return "Neutral"
        elif rep >= -40: return "Disliked"
        elif rep >= -60: return "Enemy"
        elif rep >= -80: return "Hostile"
        else: return "Nemesis"

# Crew Management System
class CrewMember:
    def __init__(self, name=None, skill_type="general"):
        self.name = name or f"{random.choice(['Alex', 'Sam', 'Chris', 'Jordan', 'Taylor', 'Casey', 'Riley', 'Avery', 'Quinn', 'Morgan'])}-{random.randint(100, 999)}"
        self.skill_type = skill_type  # gunner, pilot, engineer, medic, general
        self.skill_level = random.randint(1, 10)
        self.loyalty = random.randint(50, 80)
        self.wage = self.skill_level * 5  # Daily wage
        
    def get_bonus(self):
        """Get the bonus this crew member provides"""
        if self.skill_type == "gunner":
            return {"combat": self.skill_level * 2}
        elif self.skill_type == "pilot":
            return {"speed": self.skill_level * 1.5}
        elif self.skill_type == "engineer":
            return {"efficiency": self.skill_level * 1.2}
        elif self.skill_type == "medic":
            return {"health_regen": self.skill_level * 0.5}
        else:
            return {"general": self.skill_level}

class CrewSystem:
    def __init__(self):
        self.crew_members = []
        self.max_crew = 10  # Starting crew capacity
        self.morale = 75
        self.daily_wages = 0
        
        # Start with a small crew
        self.hire_crew_member(CrewMember("First Mate Jenkins", "pilot"))
        self.hire_crew_member(CrewMember("Engineer Rodriguez", "engineer"))
        
    def hire_crew_member(self, crew_member):
        if len(self.crew_members) < self.max_crew:
            self.crew_members.append(crew_member)
            self.calculate_daily_wages()
            return True
        return False
        
    def fire_crew_member(self, index):
        if 0 <= index < len(self.crew_members):
            self.crew_members.pop(index)
            self.calculate_daily_wages()
            self.morale -= 5  # Firing crew lowers morale
            
    def calculate_daily_wages(self):
        self.daily_wages = sum(member.wage for member in self.crew_members)
        
    def pay_crew(self):
        """Pay daily wages to crew"""
        if player_wallet.can_afford(self.daily_wages):
            player_wallet.spend(self.daily_wages)
            self.morale = min(100, self.morale + 2)  # Paying crew improves morale
            return True
        else:
            self.morale = max(0, self.morale - 10)  # Not paying severely hurts morale
            return False
            
    def get_total_bonuses(self):
        """Calculate total bonuses from all crew members"""
        bonuses = {"combat": 0, "speed": 0, "efficiency": 0, "health_regen": 0, "general": 0}
        for member in self.crew_members:
            member_bonuses = member.get_bonus()
            for bonus_type, value in member_bonuses.items():
                if bonus_type in bonuses:
                    bonuses[bonus_type] += value
        return bonuses
        
    def update_morale(self):
        """Daily morale updates based on various factors"""
        # Base morale decay
        self.morale = max(0, self.morale - 1)
        
        # Morale effects on crew performance
        if self.morale < 30:
            # Low morale can cause crew to leave
            if random.random() < 0.1:  # 10% chance daily
                if self.crew_members:
                    leaving_member = random.choice(self.crew_members)
                    self.crew_members.remove(leaving_member)
                    print(f"{leaving_member.name} left the crew due to low morale!")
                    
    def get_crew_efficiency(self):
        """Get overall crew efficiency multiplier based on morale"""
        if self.morale >= 80:
            return 1.2
        elif self.morale >= 60:
            return 1.0
        elif self.morale >= 40:
            return 0.9
        elif self.morale >= 20:
            return 0.8
        else:
            return 0.7

# Time and Mission System
class TimeSystem:
    def __init__(self):
        self.game_day = 1
        self.last_day_update = time.time()
        self.day_length = 300  # 5 minutes = 1 game day
        
    def update(self):
        current_time = time.time()
        if current_time - self.last_day_update >= self.day_length:
            self.advance_day()
            self.last_day_update = current_time
            
    def advance_day(self):
        self.game_day += 1
        
        # Daily crew maintenance
        crew_system.pay_crew()
        crew_system.update_morale()
        
        # Health regeneration
        if crew_system.crew_members:
            health_regen = crew_system.get_total_bonuses()["health_regen"]
            combat_system.heal(int(health_regen))
            
        # Market fluctuations
        self.update_markets()
        
        print(f"Day {self.game_day} - Crew wages: {crew_system.daily_wages} credits")
        
    def update_markets(self):
        """Update market prices daily"""
        for planet_name, planet_data in market_system.planet_markets.items():
            market = planet_data['market']
            for commodity in market:
                # Small daily price fluctuations
                change = random.uniform(-0.1, 0.1)
                market[commodity] = max(0.3, min(3.0, market[commodity] + change))

class Mission:
    def __init__(self, mission_type, faction_id, description, reward, reputation_change, requirements=None):
        self.mission_type = mission_type
        self.faction_id = faction_id
        self.description = description
        self.reward = reward
        self.reputation_change = reputation_change
        self.requirements = requirements or {}
        self.completed = False
        
class MissionSystem:
    def __init__(self):
        self.available_missions = []
        self.active_missions = []
        self.last_mission_generation = 0
        
    def generate_missions(self):
        """Generate new missions periodically"""
        if time.time() - self.last_mission_generation > 60:  # New missions every minute
            self.create_random_missions()
            self.last_mission_generation = time.time()
            
    def create_random_missions(self):
        mission_types = [
            {
                "type": "delivery",
                "description": "Deliver cargo to {target_planet}",
                "reward": random.randint(200, 500),
                "reputation": 10
            },
            {
                "type": "escort",
                "description": "Escort merchant convoy through dangerous space",
                "reward": random.randint(300, 700),
                "reputation": 15
            },
            {
                "type": "patrol",
                "description": "Patrol sector and eliminate pirate threats",
                "reward": random.randint(400, 800),
                "reputation": 20
            },
            {
                "type": "reconnaissance",
                "description": "Scout enemy positions in contested space",
                "reward": random.randint(250, 600),
                "reputation": 12
            }
        ]
        
        # Clear old missions
        self.available_missions.clear()
        
        # Generate new missions for each faction
        for faction_id in faction_system.factions.keys():
            if faction_id != 'outer_rim_pirates':  # Pirates don't give normal missions
                mission_template = random.choice(mission_types)
                mission = Mission(
                    mission_template["type"],
                    faction_id,
                    mission_template["description"],
                    mission_template["reward"],
                    mission_template["reputation"]
                )
                self.available_missions.append(mission)

# Create systems
random_event_system = RandomEventSystem()
combat_system = CombatSystem()
faction_system = FactionSystem()
crew_system = CrewSystem()
time_system = TimeSystem()
mission_system = MissionSystem()

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
            text='Press 1-5 to purchase upgrades\nESC to close',
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
        upgrade_text += f"   Current Level: {ship_upgrades.fuel_efficiency} -> {ship_upgrades.fuel_efficiency + 1}\n\n"
        
        # Weapons upgrade
        weapon_cost = combat_system.weapon_level * 300
        weapon_affordable = "✓" if player_wallet.can_afford(weapon_cost) else "✗"
        upgrade_text += f"4. Weapons Upgrade - {weapon_cost} credits {weapon_affordable}\n"
        upgrade_text += f"   Current Level: {combat_system.weapon_level} -> {combat_system.weapon_level + 1}\n\n"
        
        # Shields upgrade
        shield_cost = combat_system.shield_level * 250
        shield_affordable = "✓" if player_wallet.can_afford(shield_cost) else "✗"
        upgrade_text += f"5. Shields Upgrade - {shield_cost} credits {shield_affordable}\n"
        upgrade_text += f"   Current Level: {combat_system.shield_level} -> {combat_system.shield_level + 1}\n"
        
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
        elif key == '4':
            if combat_system.upgrade_weapons():
                self.update_display()
            else:
                print("Cannot afford weapons upgrade!")
            return True
        elif key == '5':
            if combat_system.upgrade_shields():
                self.update_display()
            else:
                print("Cannot afford shields upgrade!")
            return True
                
        return False

# Create upgrade UI
upgrade_ui = UpgradeUI()

# Event UI for random encounters
class EventUI:
    def __init__(self):
        self.active = False
        self.current_event = None
        
        # Main event panel
        self.panel = Panel(
            parent=camera.ui,
            model='quad',
            scale=(0.8, 0.6),
            color=color.dark_gray,
            enabled=False
        )
        
        # Title
        self.title = Text(
            parent=self.panel,
            text='SPACE ENCOUNTER',
            position=(0, 0.2),
            scale=1.5,
            color=color.orange
        )
        
        # Event description
        self.description = Text(
            parent=self.panel,
            text='',
            position=(0, 0.05),
            scale=1,
            color=color.white
        )
        
        # Option buttons
        self.option_buttons = []
        
    def show_event(self, event):
        self.active = True
        self.current_event = event
        self.panel.enabled = True
        
        # Update event info
        self.title.text = event['name'].upper()
        self.description.text = event['description']
        
        # Clear existing buttons
        for button in self.option_buttons:
            destroy(button)
        self.option_buttons.clear()
        
        # Create option buttons
        for i, option in enumerate(event['options']):
            button = Button(
                parent=self.panel,
                text=option['text'],
                color=color.azure.tint(-.2),
                highlight_color=color.azure.tint(-.1),
                pressed_color=color.azure.tint(-.3),
                scale=(0.6, 0.08),
                position=(0, -0.05 - (i * 0.12))
            )
            
            # Store the action in the button
            button.action = option['action']
            button.on_click = lambda action=option['action']: self.handle_option(action)
            self.option_buttons.append(button)
        
        # Pause game and show cursor
        mouse.locked = False
        mouse.visible = True
        
    def handle_option(self, action):
        if action != 'ignore':
            random_event_system.handle_event_action(action)
        
        self.hide()
        
    def hide(self):
        self.active = False
        self.current_event = None
        self.panel.enabled = False
        
        # Clear buttons
        for button in self.option_buttons:
            destroy(button)
        self.option_buttons.clear()
        
        # Resume game and hide cursor
        mouse.locked = True
        mouse.visible = False

# Create event UI
event_ui = EventUI()

# Faction Relations UI
class FactionUI:
    def __init__(self):
        self.active = False
        
        # Main faction panel
        self.panel = Panel(
            parent=camera.ui,
            model='quad',
            scale=(0.9, 0.8),
            color=color.black66,
            enabled=False
        )
        
        # Title
        self.title = Text(
            parent=self.panel,
            text='FACTION RELATIONS',
            position=(0, 0.35),
            scale=1.5,
            color=color.yellow
        )
        
        # Faction list
        self.faction_list = Text(
            parent=self.panel,
            text='',
            position=(0, -0.05),
            scale=0.9,
            color=color.white
        )
        
        # Instructions
        self.instructions = Text(
            parent=self.panel,
            text='ESC to close',
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
        faction_text = "FACTION STANDINGS:\n\n"
        
        for faction_id, faction in faction_system.factions.items():
            reputation = faction_system.player_reputation[faction_id]
            status = faction_system.get_reputation_status(faction_id)
            
            # Color code based on reputation
            if reputation >= 40:
                color_indicator = "✓"
            elif reputation >= -20:
                color_indicator = "○"
            else:
                color_indicator = "✗"
                
            faction_text += f"{color_indicator} {faction.name}: {status} ({reputation:+d})\n"
        
        self.faction_list.text = faction_text

# Crew Management UI
class CrewUI:
    def __init__(self):
        self.active = False
        
        # Main crew panel
        self.panel = Panel(
            parent=camera.ui,
            model='quad',
            scale=(0.9, 0.8),
            color=color.black66,
            enabled=False
        )
        
        # Title
        self.title = Text(
            parent=self.panel,
            text='CREW MANAGEMENT',
            position=(0, 0.35),
            scale=1.5,
            color=color.green
        )
        
        # Crew info
        self.crew_info = Text(
            parent=self.panel,
            text='',
            position=(-0.4, 0.2),
            scale=0.8,
            color=color.white
        )
        
        # Available crew
        self.available_crew = Text(
            parent=self.panel,
            text='',
            position=(0.4, 0.2),
            scale=0.8,
            color=color.cyan
        )
        
        # Instructions
        self.instructions = Text(
            parent=self.panel,
            text='H to hire available crew • F to fire crew member • ESC to close',
            position=(0, -0.35),
            scale=0.8,
            color=color.light_gray
        )
        
        # Generate some available crew for hiring
        self.available_for_hire = []
        self.generate_available_crew()
        
    def generate_available_crew(self):
        self.available_for_hire.clear()
        skill_types = ["gunner", "pilot", "engineer", "medic", "general"]
        for _ in range(3):
            skill = random.choice(skill_types)
            crew_member = CrewMember(skill_type=skill)
            self.available_for_hire.append(crew_member)
        
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
        # Current crew info
        crew_text = f"CURRENT CREW ({len(crew_system.crew_members)}/{crew_system.max_crew}):\n"
        crew_text += f"Morale: {crew_system.morale}%\n"
        crew_text += f"Daily Wages: {crew_system.daily_wages} credits\n\n"
        
        for i, member in enumerate(crew_system.crew_members):
            crew_text += f"{i+1}. {member.name}\n"
            crew_text += f"   {member.skill_type.title()} (Skill: {member.skill_level})\n"
            crew_text += f"   Wage: {member.wage} credits/day\n\n"
        
        self.crew_info.text = crew_text
        
        # Available crew
        available_text = "AVAILABLE FOR HIRE:\n\n"
        for i, member in enumerate(self.available_for_hire):
            cost = member.skill_level * 50  # Hiring cost
            available_text += f"{i+1}. {member.name}\n"
            available_text += f"   {member.skill_type.title()} (Skill: {member.skill_level})\n"
            available_text += f"   Hiring Cost: {cost} credits\n"
            available_text += f"   Daily Wage: {member.wage} credits\n\n"
            
        self.available_crew.text = available_text
        
    def handle_input(self, key):
        if not self.active:
            return False
            
        if key == 'h':
            self.hire_crew()
            return True
        elif key == 'f':
            self.fire_crew()
            return True
            
        return False
        
    def hire_crew(self):
        if self.available_for_hire and len(crew_system.crew_members) < crew_system.max_crew:
            new_crew = self.available_for_hire[0]
            hiring_cost = new_crew.skill_level * 50
            
            if player_wallet.can_afford(hiring_cost):
                player_wallet.spend(hiring_cost)
                crew_system.hire_crew_member(new_crew)
                self.available_for_hire.remove(new_crew)
                print(f"Hired {new_crew.name} for {hiring_cost} credits!")
                
                # Generate new crew member to replace hired one
                skill_types = ["gunner", "pilot", "engineer", "medic", "general"]
                skill = random.choice(skill_types)
                replacement = CrewMember(skill_type=skill)
                self.available_for_hire.append(replacement)
                
                self.update_display()
            else:
                print("Not enough credits to hire crew!")
        else:
            print("Cannot hire more crew!")
            
    def fire_crew(self):
        if crew_system.crew_members:
            # Fire the last crew member for simplicity
            fired_member = crew_system.crew_members[-1]
            crew_system.fire_crew_member(len(crew_system.crew_members) - 1)
            print(f"Fired {fired_member.name}")
            self.update_display()
        else:
            print("No crew to fire!")

# Mission Board UI
class MissionUI:
    def __init__(self):
        self.active = False
        
        # Main mission panel
        self.panel = Panel(
            parent=camera.ui,
            model='quad',
            scale=(0.9, 0.8),
            color=color.black66,
            enabled=False
        )
        
        # Title
        self.title = Text(
            parent=self.panel,
            text='MISSION BOARD',
            position=(0, 0.35),
            scale=1.5,
            color=color.orange
        )
        
        # Mission list
        self.mission_list = Text(
            parent=self.panel,
            text='',
            position=(0, -0.05),
            scale=0.8,
            color=color.white
        )
        
        # Instructions
        self.instructions = Text(
            parent=self.panel,
            text='1-5 to accept mission • ESC to close',
            position=(0, -0.35),
            scale=1,
            color=color.light_gray
        )
        
    def show(self):
        self.active = True
        self.panel.enabled = True
        mission_system.generate_missions()
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
        mission_text = "AVAILABLE MISSIONS:\n\n"
        
        for i, mission in enumerate(mission_system.available_missions[:5]):  # Show first 5
            faction_name = faction_system.factions[mission.faction_id].name
            reputation_req = faction_system.get_reputation_status(mission.faction_id)
            
            mission_text += f"{i+1}. {mission.description}\n"
            mission_text += f"   Client: {faction_name}\n"
            mission_text += f"   Reward: {mission.reward} credits\n"
            mission_text += f"   Reputation: +{mission.reputation_change}\n\n"
            
        if not mission_system.available_missions:
            mission_text += "No missions available. Check back later."
            
        self.mission_list.text = mission_text
        
    def handle_input(self, key):
        if not self.active:
            return False
            
        if key in '12345':
            mission_index = int(key) - 1
            if mission_index < len(mission_system.available_missions):
                mission = mission_system.available_missions[mission_index]
                self.accept_mission(mission)
                return True
                
        return False
        
    def accept_mission(self, mission):
        # Check if player has good enough reputation
        player_rep = faction_system.player_reputation[mission.faction_id]
        if player_rep < -50:
            print(f"Reputation too low with {faction_system.factions[mission.faction_id].name}!")
            return
            
        mission_system.active_missions.append(mission)
        mission_system.available_missions.remove(mission)
        print(f"Accepted mission: {mission.description}")
        print(f"Mission will auto-complete for now...")
        
        # Auto-complete mission for demonstration
        self.complete_mission(mission)
        
    def complete_mission(self, mission):
        # Award rewards
        player_wallet.earn(mission.reward)
        faction_system.change_reputation(mission.faction_id, mission.reputation_change)
        
        print(f"Mission completed! Earned {mission.reward} credits and reputation.")
        
        # Remove from active missions
        if mission in mission_system.active_missions:
            mission_system.active_missions.remove(mission)
            
        self.update_display()

# Create UI systems
faction_ui = FactionUI()
crew_ui = CrewUI()
mission_ui = MissionUI()

def update():
    global nearby_planet
    
    if not paused and not trading_ui.active and not upgrade_ui.active and not event_ui.active and not faction_ui.active and not crew_ui.active and not mission_ui.active:
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
                
            # Check for random events when not near planets and not in landing prompt
            if not nearby_planet and not landing_prompt.enabled:
                random_event_system.check_for_event()
                
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
                    
    # Update time system
    time_system.update()

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
    if crew_ui.handle_input(key):
        return
    if mission_ui.handle_input(key):
        return
    
    if key == 'escape':
        # Close UIs if open
        if trading_ui.active:
            trading_ui.hide()
            return
        if upgrade_ui.active:
            upgrade_ui.hide()
            return
        if faction_ui.active:
            faction_ui.hide()
            return
        if crew_ui.active:
            crew_ui.hide()
            return
        if mission_ui.active:
            mission_ui.hide()
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
    
    if key == 'r' and scene_manager.current_state == GameState.TOWN and not paused:
        # Open faction relations if near embassy
        if scene_manager.town_controller:
            player_pos = scene_manager.town_controller.position
            embassy_pos = Vec3(0, 3, -10)  # Position of embassy
            distance = (player_pos - embassy_pos).length()
            
            if distance < 10:  # Within range of embassy
                faction_ui.show()
            else:
                print("You need to be closer to the embassy!")
    
    if key == 'c' and scene_manager.current_state == GameState.TOWN and not paused:
        # Open crew management if near crew quarters
        if scene_manager.town_controller:
            player_pos = scene_manager.town_controller.position
            crew_quarters_pos = Vec3(0, 3, 10)  # Position of crew quarters
            distance = (player_pos - crew_quarters_pos).length()
            
            if distance < 10:  # Within range of crew quarters
                crew_ui.show()
            else:
                print("You need to be closer to the crew quarters!")
    
    if key == 'm' and scene_manager.current_state == GameState.TOWN and not paused:
        # Open mission board if near mission board
        if scene_manager.town_controller:
            player_pos = scene_manager.town_controller.position
            mission_board_pos = Vec3(-10, 3, -10)  # Position of mission board
            distance = (player_pos - mission_board_pos).length()
            
            if distance < 10:  # Within range of mission board
                mission_ui.show()
            else:
                print("You need to be closer to the mission board!")
    
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