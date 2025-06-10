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
import time
from enum import Enum

# Check if we're in a headless environment
import sys
headless_mode = '--headless' in sys.argv or not os.environ.get('DISPLAY')

# Configure Ursina for headless mode if needed
if headless_mode:
    print("Running in headless mode (no display available)")
    app = Ursina(development_mode=False, window_type='none')
else:
    app = Ursina(borderless=False)  # Make window resizable and movable

# ===== GAME SYSTEMS =====

# Trading System
class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    LEGENDARY = 4

class TradeItem:
    def __init__(self, name, base_price, rarity=Rarity.COMMON, description=""):
        self.name = name
        self.base_price = base_price
        self.rarity = rarity
        self.description = description

class TradingSystem:
    def __init__(self, player_reputation=0):
        self.player_reputation = player_reputation
        self.items = {
            'food': TradeItem('Food Rations', 50, Rarity.COMMON, 'Basic nutrition packs'),
            'water': TradeItem('Purified Water', 30, Rarity.COMMON, 'Clean drinking water'),
            'fuel': TradeItem('Fusion Fuel', 100, Rarity.UNCOMMON, 'Starship fuel cells'),
            'medicine': TradeItem('Medical Supplies', 150, Rarity.UNCOMMON, 'Emergency medical kit'),
            'electronics': TradeItem('Electronics', 200, Rarity.RARE, 'Advanced circuitry'),
            'weapons': TradeItem('Weapons', 300, Rarity.RARE, 'Military-grade equipment'),
            'luxury': TradeItem('Luxury Goods', 500, Rarity.LEGENDARY, 'Rare artifacts and gems'),
            'spice': TradeItem('Spice', 800, Rarity.LEGENDARY, 'Exotic spices from distant worlds'),
            'crystals': TradeItem('Energy Crystals', 1000, Rarity.LEGENDARY, 'Pure energy in crystal form')
        }
        self.cargo = {}
        self.cargo_capacity = 100
        self.current_cargo = 0
        self.market_trends = {}
        for item_name in self.items:
            self.market_trends[item_name] = {
                'demand': random.uniform(0.5, 1.5),
                'supply': random.uniform(0.5, 1.5),
                'trend': random.choice(['rising', 'falling', 'stable'])
            }
    
    def get_item_price(self, item_name, port_name="Generic Port", is_selling=False):
        if item_name not in self.items:
            return 0
        item = self.items[item_name]
        base_price = item.base_price
        trend_data = self.market_trends[item_name]
        price = base_price * trend_data['demand'] / trend_data['supply']
        rarity_multipliers = {Rarity.COMMON: 1.0, Rarity.UNCOMMON: 1.5, Rarity.RARE: 2.5, Rarity.LEGENDARY: 4.0}
        price *= rarity_multipliers[item.rarity]
        rep_modifier = 1.0 + (self.player_reputation * 0.01)
        if is_selling:
            price *= rep_modifier
        else:
            price /= rep_modifier
        price *= random.uniform(0.9, 1.1)
        return max(1, int(price))

# Economy System
class TransactionType(Enum):
    TRADE_BUY = "Trade Purchase"
    TRADE_SELL = "Trade Sale"
    MISSION_REWARD = "Mission Reward"
    COMBAT_REWARD = "Combat Reward"
    REPAIR_COST = "Ship Repair"
    FUEL_COST = "Fuel Purchase"
    UPGRADE_COST = "Ship Upgrade"

class EconomySystem:
    def __init__(self, starting_credits=1000):
        self.credits = starting_credits
        self.transaction_history = []
        self.reputation_multiplier = 1.0
    
    def add_credits(self, amount, transaction_type=TransactionType.MISSION_REWARD, description=""):
        if amount > 0:
            amount = int(amount * self.reputation_multiplier)
        self.credits += amount
        self.transaction_history.append({
            'type': transaction_type.value,
            'amount': amount,
            'balance': self.credits,
            'description': description,
            'timestamp': datetime.now()
        })
        return True
    
    def spend_credits(self, amount, transaction_type=TransactionType.REPAIR_COST, description=""):
        if amount <= 0 or self.credits < amount:
            return False, "Insufficient credits"
        self.credits -= amount
        self.transaction_history.append({
            'type': transaction_type.value,
            'amount': -amount,
            'balance': self.credits,
            'description': description,
            'timestamp': datetime.now()
        })
        return True, "Transaction completed"

# Ship System
class ShipSystem:
    def __init__(self):
        self.ship_types = {
            'starter': {'name': 'Cosmic Drifter', 'health': 100, 'shield': 50, 'fuel': 100, 'cargo': 50, 'speed': 5, 'damage': 20},
            'medium': {'name': 'Star Cruiser', 'health': 200, 'shield': 100, 'fuel': 150, 'cargo': 100, 'speed': 7, 'damage': 40},
            'heavy': {'name': 'Battle Fortress', 'health': 400, 'shield': 200, 'fuel': 200, 'cargo': 150, 'speed': 4, 'damage': 80},
            'elite': {'name': 'Void Phantom', 'health': 300, 'shield': 250, 'fuel': 250, 'cargo': 200, 'speed': 10, 'damage': 100}
        }
        self.current_ship = 'starter'
        self.ship_data = self.ship_types[self.current_ship].copy()
        self.max_values = self.ship_data.copy()
        self.upgrades = {'engine': 0, 'shield': 0, 'cargo': 0, 'weapon': 0}
    
    def get_ship_status(self):
        return {
            'name': self.ship_data['name'],
            'health': f"{self.ship_data['health']}/{self.max_values['health']}",
            'shield': f"{self.ship_data['shield']}/{self.max_values['shield']}",
            'fuel': f"{self.ship_data['fuel']}/{self.max_values['fuel']}",
            'cargo': f"{self.ship_data['cargo']}/{self.max_values['cargo']}",
            'speed': self.ship_data['speed'],
            'damage': self.ship_data['damage']
        }

# Mission System
class MissionType(Enum):
    TRADE = "Trade Mission"
    COMBAT = "Combat Mission"
    EXPLORATION = "Exploration Mission"
    DELIVERY = "Delivery Mission"

class Mission:
    def __init__(self, mission_type, title, description, reward, difficulty=1):
        self.type = mission_type
        self.title = title
        self.description = description
        self.reward = reward
        self.difficulty = difficulty
        self.completed = False
        self.progress = 0
        self.max_progress = 100

class MissionSystem:
    def __init__(self):
        self.available_missions = []
        self.active_missions = []
        self.completed_missions = []
        self.generate_initial_missions()
    
    def generate_initial_missions(self):
        missions = [
            Mission(MissionType.TRADE, "Supply Run", "Deliver 10 food rations to Nova Prime", 500),
            Mission(MissionType.COMBAT, "Pirate Hunt", "Eliminate 3 pirate ships in the asteroid belt", 800),
            Mission(MissionType.EXPLORATION, "Deep Space Survey", "Explore 5 uncharted systems", 1000),
            Mission(MissionType.DELIVERY, "Medical Emergency", "Rush medical supplies to Shadow Port", 600)
        ]
        self.available_missions = missions

# NPC System
class NPCFaction(Enum):
    TRADE_FEDERATION = "Trade Federation"
    SPACE_NAVY = "Space Navy"
    PIRATES = "Pirates"
    INDEPENDENTS = "Independent Traders"

class NPC:
    def __init__(self, name, faction, personality="neutral"):
        self.name = name
        self.faction = faction
        self.personality = personality
        self.reputation = 0
        self.credits = random.randint(1000, 10000)
        self.inventory = {}

class NPCSystem:
    def __init__(self):
        self.npcs = []
        self.generate_initial_npcs()
    
    def generate_initial_npcs(self):
        names = ["Captain Rex", "Admiral Nova", "Trader Zephyr", "Pirate Blackstar", "Engineer Cosmos"]
        factions = list(NPCFaction)
        for name in names:
            faction = random.choice(factions)
            self.npcs.append(NPC(name, faction))

# Faction System
class FactionSystem:
    def __init__(self):
        self.factions = {
            'trade_federation': {'name': 'Trade Federation', 'reputation': 0, 'territory': ['New Terra', 'Nova Prime']},
            'space_navy': {'name': 'Space Navy', 'reputation': 0, 'territory': ['Military Base Alpha']},
            'pirates': {'name': 'Pirates', 'reputation': -50, 'territory': ['Shadow Port']},
            'independents': {'name': 'Independent Traders', 'reputation': 25, 'territory': ['Freeport']}
        }
    
    def get_faction_standing(self, faction_name):
        return self.factions.get(faction_name, {}).get('reputation', 0)

# Port System
class Port:
    def __init__(self, name, faction, services, wealth_level=1.0):
        self.name = name
        self.faction = faction
        self.services = services  # ['market', 'shipyard', 'missions', 'repairs']
        self.wealth_level = wealth_level

class PortSystem:
    def __init__(self):
        self.ports = {
            'new_terra': Port('New Terra', 'trade_federation', ['market', 'shipyard', 'missions', 'repairs'], 1.2),
            'nova_prime': Port('Nova Prime', 'trade_federation', ['market', 'missions', 'repairs'], 1.0),
            'shadow_port': Port('Shadow Port', 'pirates', ['market', 'repairs'], 0.6),
            'freeport': Port('Freeport', 'independents', ['market', 'shipyard', 'missions'], 0.8)
        }
        self.current_port = None
    
    def dock_at_port(self, port_name):
        if port_name in self.ports:
            self.current_port = self.ports[port_name]
            return True
        return False

# Combat System
class CombatState(Enum):
    APPROACH = "Approaching"
    ENGAGE = "Engaging"
    RETREAT = "Retreating"
    BOARD = "Boarding"

class CombatSystem:
    def __init__(self):
        self.in_combat = False
        self.enemy_ship = None
        self.combat_state = None
        self.combat_distance = 100
        self.combat_angle = 0
    
    def start_combat(self, enemy_type="pirate"):
        self.in_combat = True
        self.enemy_ship = {
            'name': f"{enemy_type.title()} Ship",
            'health': random.randint(50, 150),
            'shield': random.randint(25, 75),
            'damage': random.randint(15, 35),
            'crew': random.randint(5, 15)
        }
        self.combat_state = CombatState.APPROACH
        self.combat_distance = random.randint(50, 200)
        return f"Combat started with {self.enemy_ship['name']}!"
    
    def end_combat(self, victory=True):
        if victory:
            reward = random.randint(100, 500)
            self.in_combat = False
            self.enemy_ship = None
            return f"Victory! Earned {reward} credits."
        else:
            self.in_combat = False
            self.enemy_ship = None
            return "Retreat successful."

# Weather System
class WeatherType(Enum):
    CLEAR = "Clear Space"
    SOLAR_FLARE = "Solar Flare"
    ASTEROID_FIELD = "Asteroid Field"
    NEBULA = "Nebula"
    ION_STORM = "Ion Storm"
    PIRATE_AMBUSH = "Pirate Ambush"
    NAVY_PATROL = "Navy Patrol"

class WeatherSystem:
    def __init__(self):
        self.current_weather = WeatherType.CLEAR
        self.weather_timer = 0
        self.weather_duration = 30  # seconds
    
    def update_weather(self):
        self.weather_timer += 1
        if self.weather_timer >= self.weather_duration:
            self.weather_timer = 0
            self.current_weather = random.choice(list(WeatherType))
            return f"Weather changed to: {self.current_weather.value}"
        return None

# Progression System
class ProgressionSystem:
    def __init__(self):
        self.level = 1
        self.experience = 0
        self.skill_points = 0
        self.skills = {
            'combat': 0, 'trading': 0, 'piloting': 0, 'engineering': 0
        }
    
    def add_experience(self, amount):
        self.experience += amount
        old_level = self.level
        self.level = 1 + (self.experience // 1000)
        if self.level > old_level:
            self.skill_points += (self.level - old_level)
            return f"Level up! Now level {self.level}. Skill points: {self.skill_points}"
        return None

# ===== MAIN GAME CLASS =====

class SpaceGame:
    def __init__(self):
        # Initialize all systems
        self.trading_system = TradingSystem()
        self.economy_system = EconomySystem()
        self.ship_system = ShipSystem()
        self.mission_system = MissionSystem()
        self.npc_system = NPCSystem()
        self.faction_system = FactionSystem()
        self.port_system = PortSystem()
        self.combat_system = CombatSystem()
        self.weather_system = WeatherSystem()
        self.progression_system = ProgressionSystem()
        
        # Game state
        self.game_state = 'space'  # 'space', 'port', 'combat'
        self.paused = False
        self.current_location = "Deep Space"
        
        # UI elements (only create if not headless)
        if not headless_mode:
            self.setup_ui()
            self.setup_3d_world()
        
        print("=== SPACE PIRATES GAME INITIALIZED ===")
        print("Available commands:")
        print("- 'help': Show all commands")
        print("- 'status': Show ship and player status") 
        print("- 'trade': Access trading interface")
        print("- 'missions': View available missions")
        print("- 'dock <port>': Dock at a port")
        print("- 'combat': Start combat encounter")
        print("- 'save': Save game")
        print("- 'quit': Exit game")
    
    def setup_ui(self):
        # Create main HUD
        self.hud_panel = Panel(
            parent=camera.ui,
            model='quad',
            scale=(0.4, 0.3),
            position=(-0.7, 0.3),
            color=color.black66
        )
        
        self.status_text = Text(
            parent=self.hud_panel,
            text="Ship Status:\nHealth: 100/100\nShield: 50/50\nFuel: 100/100\nCredits: 1000",
            position=(-0.45, 0.25),
            scale=0.8,
            color=color.white
        )
        
        self.location_text = Text(
            parent=camera.ui,
            text="Location: Deep Space",
            position=(-0.85, 0.45),
            scale=1.2,
            color=color.yellow
        )
        
        self.weather_text = Text(
            parent=camera.ui,
            text="Weather: Clear Space",
            position=(-0.85, 0.4),
            scale=1.0,
            color=color.cyan
        )
        
        # Game info panel
        self.info_panel = Panel(
            parent=camera.ui,
            model='quad',
            scale=(0.6, 0.8),
            position=(0, 0),
            color=color.black66,
            enabled=False
        )
        
        self.info_text = Text(
            parent=self.info_panel,
            text="Game Information",
            position=(0, 0.3),
            scale=1.2,
            color=color.white,
            origin=(0,0)
        )
    
    def setup_3d_world(self):
        # Create skybox
        self.skybox = Entity(
            model='sphere',
            texture='white_cube',
            scale=1000,
            double_sided=True,
            unlit=True,
            color=color.dark_gray
        )
        
        # Create player ship
        self.player_ship = Entity(
            model='cube',
            color=color.blue,
            scale=(2, 0.5, 3),
            position=(0, 0, 0)
        )
        
        # Setup camera
        camera.parent = self.player_ship
        camera.position = (0, 2, -5)
        camera.rotation_x = -10
        
        # Create some planets
        self.planets = []
        for i in range(5):
            planet = Entity(
                model='sphere',
                color=color.random_color(),
                scale=random.uniform(20, 50),
                position=(
                    random.uniform(-500, 500),
                    random.uniform(-100, 100),
                    random.uniform(-500, 500)
                )
            )
            planet.name = f"Planet {i+1}"
            self.planets.append(planet)
        
        # Lighting
        DirectionalLight(y=2, z=3, rotation=(45, -45, 45))
        AmbientLight(color=Vec4(0.1, 0.1, 0.1, 1))
        
        mouse.locked = True
    
    def update_ui(self):
        if headless_mode:
            return
            
        # Update status display
        ship_status = self.ship_system.get_ship_status()
        status_text = f"Ship: {ship_status['name']}\n"
        status_text += f"Health: {ship_status['health']}\n"
        status_text += f"Shield: {ship_status['shield']}\n"
        status_text += f"Fuel: {ship_status['fuel']}\n"
        status_text += f"Credits: {self.economy_system.credits}\n"
        status_text += f"Level: {self.progression_system.level}\n"
        status_text += f"XP: {self.progression_system.experience}"
        
        if hasattr(self, 'status_text'):
            self.status_text.text = status_text
            self.location_text.text = f"Location: {self.current_location}"
            self.weather_text.text = f"Weather: {self.weather_system.current_weather.value}"
    
    def handle_command(self, command):
        """Handle text-based game commands"""
        parts = command.lower().split()
        if not parts:
            return
        
        cmd = parts[0]
        
        if cmd == 'help':
            print("\n=== AVAILABLE COMMANDS ===")
            print("status - Show detailed ship and player status")
            print("trade - Access trading system")
            print("missions - View and accept missions")
            print("dock <port> - Dock at specified port (new_terra, nova_prime, shadow_port, freeport)")
            print("combat - Start a random combat encounter")
            print("travel <location> - Travel to a new location")
            print("repair - Repair ship (costs credits)")
            print("refuel - Refuel ship (costs credits)")
            print("upgrade <system> - Upgrade ship systems")
            print("npcs - Interact with NPCs")
            print("faction - View faction standings")
            print("save - Save game progress")
            print("quit - Exit game")
            
        elif cmd == 'status':
            self.show_detailed_status()
            
        elif cmd == 'trade':
            self.handle_trading()
            
        elif cmd == 'missions':
            self.show_missions()
            
        elif cmd == 'dock':
            if len(parts) > 1:
                self.dock_at_port(parts[1])
            else:
                print("Available ports: new_terra, nova_prime, shadow_port, freeport")
                
        elif cmd == 'combat':
            self.start_random_combat()
            
        elif cmd == 'travel':
            if len(parts) > 1:
                self.travel_to_location(' '.join(parts[1:]))
            else:
                print("Specify a location to travel to")
                
        elif cmd == 'repair':
            self.repair_ship()
            
        elif cmd == 'refuel':
            self.refuel_ship()
            
        elif cmd == 'upgrade':
            if len(parts) > 1:
                self.upgrade_ship(parts[1])
            else:
                print("Available upgrades: engine, shield, cargo, weapon")
                
        elif cmd == 'npcs':
            self.show_npcs()
            
        elif cmd == 'faction':
            self.show_faction_standings()
            
        elif cmd == 'save':
            self.save_game()
            
        elif cmd == 'quit':
            self.quit_game()
            
        else:
            print(f"Unknown command: {cmd}. Type 'help' for available commands.")
    
    def show_detailed_status(self):
        print("\n=== SHIP STATUS ===")
        ship_status = self.ship_system.get_ship_status()
        for key, value in ship_status.items():
            print(f"{key.title()}: {value}")
        
        print(f"\n=== PLAYER STATUS ===")
        print(f"Credits: {self.economy_system.credits}")
        print(f"Level: {self.progression_system.level}")
        print(f"Experience: {self.progression_system.experience}")
        print(f"Skill Points: {self.progression_system.skill_points}")
        
        print(f"\n=== LOCATION INFO ===")
        print(f"Current Location: {self.current_location}")
        print(f"Weather: {self.weather_system.current_weather.value}")
        print(f"Game State: {self.game_state}")
    
    def handle_trading(self):
        print("\n=== TRADING SYSTEM ===")
        print("1. View Market Prices")
        print("2. Buy Items") 
        print("3. Sell Items")
        print("4. View Cargo")
        choice = input("Choose option (1-4): ").strip()
        
        if choice == '1':
            self.show_market_prices()
        elif choice == '2':
            self.buy_items()
        elif choice == '3':
            self.sell_items()
        elif choice == '4':
            self.show_cargo()
    
    def show_market_prices(self):
        print("\n=== MARKET PRICES ===")
        for item_name, item in self.trading_system.items.items():
            buy_price = self.trading_system.get_item_price(item_name, self.current_location, False)
            sell_price = self.trading_system.get_item_price(item_name, self.current_location, True)
            trend = self.trading_system.market_trends[item_name]['trend']
            print(f"{item.name}: Buy {buy_price}c | Sell {sell_price}c | Trend: {trend}")
    
    def buy_items(self):
        self.show_market_prices()
        item_name = input("Enter item name to buy: ").strip().lower()
        if item_name in self.trading_system.items:
            try:
                quantity = int(input("Enter quantity: "))
                price = self.trading_system.get_item_price(item_name, self.current_location, False)
                total_cost = price * quantity
                
                if self.economy_system.credits >= total_cost:
                    self.economy_system.spend_credits(total_cost, TransactionType.TRADE_BUY, f"Bought {quantity} {item_name}")
                    if item_name in self.trading_system.cargo:
                        self.trading_system.cargo[item_name] += quantity
                    else:
                        self.trading_system.cargo[item_name] = quantity
                    self.trading_system.current_cargo += quantity
                    print(f"Bought {quantity} {item_name} for {total_cost} credits")
                else:
                    print("Insufficient credits!")
            except ValueError:
                print("Invalid quantity!")
        else:
            print("Item not found!")
    
    def sell_items(self):
        self.show_cargo()
        item_name = input("Enter item name to sell: ").strip().lower()
        if item_name in self.trading_system.cargo:
            try:
                max_quantity = self.trading_system.cargo[item_name]
                quantity = int(input(f"Enter quantity (max {max_quantity}): "))
                if quantity <= max_quantity:
                    price = self.trading_system.get_item_price(item_name, self.current_location, True)
                    total_earned = price * quantity
                    
                    self.economy_system.add_credits(total_earned, TransactionType.TRADE_SELL, f"Sold {quantity} {item_name}")
                    self.trading_system.cargo[item_name] -= quantity
                    if self.trading_system.cargo[item_name] == 0:
                        del self.trading_system.cargo[item_name]
                    self.trading_system.current_cargo -= quantity
                    print(f"Sold {quantity} {item_name} for {total_earned} credits")
                else:
                    print("Not enough items!")
            except ValueError:
                print("Invalid quantity!")
        else:
            print("Item not in cargo!")
    
    def show_cargo(self):
        print(f"\n=== CARGO BAY ({self.trading_system.current_cargo}/{self.trading_system.cargo_capacity}) ===")
        if self.trading_system.cargo:
            for item_name, quantity in self.trading_system.cargo.items():
                item = self.trading_system.items[item_name]
                print(f"{item.name}: {quantity}")
        else:
            print("Cargo bay is empty")
    
    def show_missions(self):
        print("\n=== AVAILABLE MISSIONS ===")
        for i, mission in enumerate(self.mission_system.available_missions):
            print(f"{i+1}. {mission.title}")
            print(f"   Type: {mission.type.value}")
            print(f"   Reward: {mission.reward} credits")
            print(f"   Description: {mission.description}")
            print()
    
    def dock_at_port(self, port_name):
        if self.port_system.dock_at_port(port_name):
            port = self.port_system.current_port
            self.current_location = port.name
            self.game_state = 'port'
            print(f"\n=== DOCKED AT {port.name.upper()} ===")
            print(f"Faction: {port.faction}")
            print(f"Available services: {', '.join(port.services)}")
            
            # Pay docking fees
            fee = self.economy_system.reputation_multiplier * 25
            self.economy_system.spend_credits(fee, TransactionType.REPAIR_COST, f"Docking fees at {port.name}")
            print(f"Docking fee: {fee} credits")
        else:
            print(f"Port '{port_name}' not found!")
    
    def start_random_combat(self):
        enemy_types = ["pirate", "rogue trader", "space bandit"]
        enemy_type = random.choice(enemy_types)
        result = self.combat_system.start_combat(enemy_type)
        self.game_state = 'combat'
        print(f"\n{result}")
        print("Combat initiated! Use 'attack', 'defend', or 'retreat' commands")
        
        # Simulate quick combat
        player_wins = random.choice([True, False])
        if player_wins:
            reward = random.randint(100, 500)
            self.economy_system.add_credits(reward, TransactionType.COMBAT_REWARD, f"Combat victory against {enemy_type}")
            xp_gained = random.randint(50, 150)
            level_up = self.progression_system.add_experience(xp_gained)
            print(f"Victory! Gained {reward} credits and {xp_gained} XP")
            if level_up:
                print(level_up)
        else:
            damage = random.randint(10, 30)
            self.ship_system.ship_data['health'] -= damage
            print(f"Defeat! Ship took {damage} damage")
        
        self.combat_system.end_combat(player_wins)
        self.game_state = 'space'
    
    def travel_to_location(self, location):
        fuel_cost = random.randint(5, 15)
        if self.ship_system.ship_data['fuel'] >= fuel_cost:
            self.ship_system.ship_data['fuel'] -= fuel_cost
            self.current_location = location
            self.game_state = 'space'
            
            # Update weather
            weather_change = self.weather_system.update_weather()
            if weather_change:
                print(weather_change)
            
            print(f"Traveled to {location}. Fuel consumed: {fuel_cost}")
            
            # Random encounters
            if random.random() < 0.3:
                self.random_encounter()
        else:
            print("Insufficient fuel for travel!")
    
    def random_encounter(self):
        encounters = [
            "You discover a derelict ship with valuable salvage!",
            "Space pirates demand tribute!",
            "A merchant offers rare goods at a discount",
            "You find a hidden asteroid mining operation",
            "A distress signal leads to a rescue mission"
        ]
        encounter = random.choice(encounters)
        print(f"\n*** RANDOM ENCOUNTER ***")
        print(encounter)
        
        if "salvage" in encounter:
            credits = random.randint(100, 300)
            self.economy_system.add_credits(credits, TransactionType.MISSION_REWARD, "Salvage discovery")
            print(f"Gained {credits} credits from salvage!")
    
    def repair_ship(self):
        max_health = self.ship_system.max_values['health']
        current_health = self.ship_system.ship_data['health']
        damage = max_health - current_health
        
        if damage == 0:
            print("Ship is already at full health!")
            return
        
        repair_cost = damage * 5
        if self.economy_system.credits >= repair_cost:
            success, msg = self.economy_system.spend_credits(repair_cost, TransactionType.REPAIR_COST, "Ship repairs")
            if success:
                self.ship_system.ship_data['health'] = max_health
                print(f"Ship repaired for {repair_cost} credits!")
        else:
            print("Insufficient credits for repairs!")
    
    def refuel_ship(self):
        max_fuel = self.ship_system.max_values['fuel']
        current_fuel = self.ship_system.ship_data['fuel']
        fuel_needed = max_fuel - current_fuel
        
        if fuel_needed == 0:
            print("Ship is already fully fueled!")
            return
        
        fuel_cost = fuel_needed * 2
        if self.economy_system.credits >= fuel_cost:
            success, msg = self.economy_system.spend_credits(fuel_cost, TransactionType.FUEL_COST, "Refueling")
            if success:
                self.ship_system.ship_data['fuel'] = max_fuel
                print(f"Ship refueled for {fuel_cost} credits!")
        else:
            print("Insufficient credits for fuel!")
    
    def upgrade_ship(self, system):
        upgrade_costs = {'engine': 500, 'shield': 400, 'cargo': 300, 'weapon': 600}
        if system in upgrade_costs:
            cost = upgrade_costs[system]
            if self.economy_system.credits >= cost:
                success, msg = self.economy_system.spend_credits(cost, TransactionType.UPGRADE_COST, f"{system} upgrade")
                if success:
                    self.ship_system.upgrades[system] += 1
                    print(f"{system.title()} upgraded! Level: {self.ship_system.upgrades[system]}")
            else:
                print("Insufficient credits for upgrade!")
        else:
            print("Invalid upgrade system!")
    
    def show_npcs(self):
        print("\n=== NPCS IN AREA ===")
        for npc in self.npc_system.npcs:
            print(f"{npc.name} - {npc.faction.value} - Reputation: {npc.reputation}")
    
    def show_faction_standings(self):
        print("\n=== FACTION STANDINGS ===")
        for faction_id, faction_data in self.faction_system.factions.items():
            print(f"{faction_data['name']}: {faction_data['reputation']}")
    
    def save_game(self):
        save_data = {
            'credits': self.economy_system.credits,
            'ship_data': self.ship_system.ship_data,
            'ship_upgrades': self.ship_system.upgrades,
            'cargo': self.trading_system.cargo,
            'level': self.progression_system.level,
            'experience': self.progression_system.experience,
            'skills': self.progression_system.skills,
            'location': self.current_location,
            'faction_standings': {k: v['reputation'] for k, v in self.faction_system.factions.items()}
        }
        
        if not os.path.exists('saves'):
            os.makedirs('saves')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'saves/space_game_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"Game saved to {filename}")
    
    def quit_game(self):
        print("Thanks for playing Space Pirates!")
        if not headless_mode:
            application.quit()
        else:
            exit(0)
    
    def update(self):
        """Main game update loop"""
        if not headless_mode:
            self.update_ui()
    
    def run_text_interface(self):
        """Run the game in text mode for headless environments"""
        print("\n=== SPACE PIRATES: TEXT MODE ===")
        print("Welcome to the galaxy, Captain!")
        print("Type 'help' for available commands.")
        
        while True:
            try:
                command = input(f"\n[{self.current_location}] > ")
                if command is None:
                    continue
                command = command.strip()
                if command:
                    self.handle_command(command)
                    if command.lower() == 'quit':
                        break
            except (KeyboardInterrupt, EOFError):
                print("\nExiting game...")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

# ===== SETUP GAME WORLD (only in non-headless mode) =====

if not headless_mode:
    # Create a rotating skybox instead of stars
    class RotatingSkybox(Entity):
        def __init__(self):
            super().__init__(
                model='sphere',
                texture='white_cube',
                scale=1000,
                double_sided=True,
                unlit=True,
                color=color.dark_gray
            )
            self.rotation_speed = 360 / (2 * 60 * 60)
            
        def update(self):
            if not game.paused:
                self.rotation_y += self.rotation_speed * time.dt

    # Create the rotating skybox
    skybox = RotatingSkybox()

    # Adjust camera settings for far viewing distance
    camera.clip_plane_far = 1000000
    camera.fov = 90

# ===== INITIALIZE GAME =====

game = SpaceGame()

# Game state
paused = False

def input(key):
    global paused
    
    if key == 'escape':
        paused = not paused
        if not headless_mode:
            mouse.locked = not paused
    
    # Handle text commands in 3D mode
    if key == 'enter' and not headless_mode:
        command = input("Enter command: ")
        game.handle_command(command)

def update():
    if not paused:
        game.update()

# ===== RUN GAME =====

if __name__ == "__main__":
    if headless_mode:
        game.run_text_interface()
    else:
        print("3D mode: Use mouse to look around, WASD to move")
        print("Press Enter to access command interface")
        app.run() 