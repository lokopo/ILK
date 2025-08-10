#!/usr/bin/env python3

import os
import sys
import logging
import traceback

# Setup logging based on environment variables
verbose = os.environ.get('GAME_VERBOSE', '0') == '1'
logging.basicConfig(
    level=logging.DEBUG if verbose else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('space_game.log', mode='w')
    ]
)
logger = logging.getLogger(__name__)

# Check if we're in headless mode
HEADLESS_MODE = os.environ.get('GAME_HEADLESS_MODE', '0') == '1'
TEST_MODE = os.environ.get('GAME_TEST_MODE', '0') == '1'

logger.info("=== ILK SPACE GAME STARTING ===")
logger.info(f"Headless mode: {HEADLESS_MODE}")
logger.info(f"Test mode: {TEST_MODE}")
logger.info(f"Verbose logging: {verbose}")

# Import appropriate modules based on mode
if HEADLESS_MODE:
    logger.info("Loading headless game components...")
    try:
        # Import mock Ursina components for headless mode
        import headless_game_test
        
        # Create mock Ursina components
        Entity = headless_game_test.MockEntity
        Vec3 = headless_game_test.MockVec3
        Vec2 = headless_game_test.MockVec3  # Use Vec3 as Vec2 mock
        time = headless_game_test.MockTime()
        camera = headless_game_test.MockCamera()
        color = headless_game_test.MockColor()
        mouse = headless_game_test.MockMouse()
        held_keys = {}
        paused = False
        
        # Mock Ursina functions
        def load_texture(path):
            return f"texture_{path}"
        
        def Text(**kwargs):
            return headless_game_test.MockEntity(**kwargs)
        
        def Button(**kwargs):
            return headless_game_test.MockEntity(**kwargs)
        
        def Panel(**kwargs):
            return headless_game_test.MockEntity(**kwargs)
        
        def clamp(value, min_val, max_val):
            return max(min_val, min(max_val, value))
        
        def raycast(*args, **kwargs):
            return type('RaycastHit', (), {'hit': False})()
        
        def destroy(*args, **kwargs):
            pass
        
        def DirectionalLight(**kwargs):
            return headless_game_test.MockEntity(**kwargs)
        
        def AmbientLight(**kwargs):
            return headless_game_test.MockEntity(**kwargs)
        
        # Mock FirstPersonController
        class FirstPersonController:
            def __init__(self, **kwargs):
                self.position = Vec3(0, 0, 0)
                self.rotation = Vec3(0, 0, 0)
                self.enabled = True
                self.speed = 5
                self.jump_height = 2
                self.jump_up_time = 0.5
                self.fall_after = 0.35
                self.mouse_sensitivity = Vec3(40, 40, 0)
                self.grounded = True
                self.y = 0
                self.gravity = 1
                self.velocity = Vec3(0, 0, 0)
                self.on_ground = True
                self.air_time = 0
                self.traverse_target = None
                self.model = None
                self.parent = None
                self.third_person = False
                self.axis_indicator = headless_game_test.MockEntity()
                
            def update(self):
                pass
                
            @property
            def forward(self):
                return Vec3(0, 0, 1)
                
            @property
            def right(self):
                return Vec3(1, 0, 0)
                
            @property
            def up(self):
                return Vec3(0, 1, 0)
        
        # Mock application for headless mode
        class MockApp:
            def __init__(self, **kwargs):
                pass
            def run(self):
                # Run actual playable game in text mode
                logger.info("Starting text-based space game...")
                try:
                    return self.run_text_game()
                except Exception as e:
                    logger.error(f"Text game failed: {e}")
                    logger.error(traceback.format_exc())
                    return 1
            
            def run_text_game(self):
                """Run the actual game in text mode"""
                print("\n" + "="*60)
                print("🚀 ILK SPACE GAME - TEXT MODE")
                print("="*60)
                print("Welcome to the galaxy, Captain!")
                print("All the features of the 3D game, now in text format!")
                print("Type 'help' for commands, 'quit' to exit")
                print("="*60)
                
                # Initialize player state in text mode
                self.text_player_pos = Vec3(0, 0, 0)
                self.text_current_planet = None
                self.text_fuel = 100.0
                self.text_max_fuel = 100.0
                self.text_in_space = True
                self.running = True
                
                while self.running:
                    try:
                        user_input = input("\nSpaceGame> ")
                        if user_input is None:
                            continue
                        command = user_input.strip().lower()
                        self.handle_text_command(command)
                    except KeyboardInterrupt:
                        print("\n🛑 Game interrupted by user")
                        break
                    except EOFError:
                        print("\n👋 Goodbye!")
                        break
                    except Exception as e:
                        print(f"❌ Error: {e}")
                
                print("Thanks for playing ILK Space Game!")
                return 0
            
            def handle_text_command(self, command):
                """Handle text-mode commands"""
                if command == "quit" or command == "exit":
                    self.running = False
                    
                elif command == "help":
                    self.show_text_help()
                    
                elif command == "status":
                    self.show_text_status()
                    
                elif command == "planets":
                    self.show_text_planets()
                    
                elif command.startswith("fly "):
                    planet_name = command[4:].strip()
                    self.text_fly_to_planet(planet_name)
                    
                elif command == "land":
                    self.text_land()
                    
                elif command == "takeoff":
                    self.text_takeoff()
                    
                elif command == "trade":
                    self.text_trade()
                    
                elif command == "wallet":
                    print(f"💰 Credits: {player_wallet.credits:,}")
                    
                elif command == "fleet":
                    self.show_text_fleet()
                    
                elif command == "character":
                    self.show_text_character()
                    
                elif command == "scan":
                    self.text_scan()
                    
                elif command == "contracts":
                    print("📋 Contract system would be here (k key in 3D mode)")
                    
                elif command == "save":
                    print("💾 Save functionality would call save_game()")
                    
                elif command == "test":
                    print("🧪 Running stability tests...")
                    headless_game_test.GameStabilityTester().run_all_tests()
                    
                else:
                    print(f"❌ Unknown command: '{command}'. Type 'help' for available commands.")
            
            def show_text_help(self):
                """Show available text commands"""
                print("\n📚 TEXT MODE COMMANDS:")
                print("="*40)
                print("🚀 NAVIGATION:")
                print("  status          - Show player status")
                print("  planets         - List all planets")
                print("  fly <planet>    - Travel to a planet")
                print("  land            - Land on nearest planet")
                print("  takeoff         - Take off from planet")
                print("  scan            - Scan for nearby objects")
                print("")
                print("💰 ECONOMY:")
                print("  trade           - Open trading interface")
                print("  wallet          - Show current credits")
                print("")
                print("🚢 FLEET & CHARACTER:")
                print("  fleet           - Show fleet status")
                print("  character       - Show character development")
                print("  contracts       - Show available contracts")
                print("")
                print("🎮 GAME:")
                print("  save            - Save game")
                print("  test            - Run stability tests")
                print("  help            - Show this help")
                print("  quit            - Exit game")
                print("="*40)
            
            def show_text_status(self):
                """Show player status in text"""
                print("\n" + "="*50)
                print("👨‍🚀 CAPTAIN STATUS")
                print("="*50)
                print(f"📍 Position: ({self.text_player_pos.x:.1f}, {self.text_player_pos.y:.1f}, {self.text_player_pos.z:.1f})")
                print(f"💰 Credits: {player_wallet.credits:,}")
                print(f"⛽ Fuel: {self.text_fuel:.1f}/{self.text_max_fuel:.1f}")
                print(f"🌌 Location: {'Space' if self.text_in_space else f'Landed on {self.text_current_planet}'}")
                print("="*50)
            
            def show_text_planets(self):
                """Show available planets"""
                print("\n🌍 GALAXY MAP:")
                print("-"*30)
                for i, planet in enumerate(planets[:10]):  # Show first 10 planets
                    distance = (planet.position - self.text_player_pos).length()
                    print(f"{i+1}. {planet.name} ({planet.planet_type}) - {distance:.1f} units away")
                print("-"*30)
                print("Use 'fly <planet_name>' to travel")
            
            def text_fly_to_planet(self, planet_name):
                """Fly to a planet in text mode"""
                # Find planet by name (partial match)
                target_planet = None
                for planet in planets:
                    if planet_name.lower() in planet.name.lower():
                        target_planet = planet
                        break
                
                if not target_planet:
                    print(f"❌ Planet '{planet_name}' not found")
                    return
                
                distance = (target_planet.position - self.text_player_pos).length()
                fuel_cost = distance * 0.1
                
                if fuel_cost > self.text_fuel:
                    print(f"❌ Not enough fuel! Need {fuel_cost:.1f}, have {self.text_fuel:.1f}")
                    return
                
                print(f"🚀 Flying to {target_planet.name}...")
                print(f"📏 Distance: {distance:.1f} units")
                print(f"⛽ Fuel cost: {fuel_cost:.1f}")
                
                self.text_player_pos = target_planet.position
                self.text_fuel -= fuel_cost
                self.text_in_space = True
                
                print(f"✅ Arrived at {target_planet.name}")
                print(f"🌍 {target_planet.planet_type.title()} planet with {target_planet.population:,} inhabitants")
            
            def text_land(self):
                """Land on nearby planet"""
                closest_planet = None
                closest_distance = float('inf')
                
                for planet in planets:
                    distance = (planet.position - self.text_player_pos).length()
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_planet = planet
                
                if closest_distance > 5.0:
                    print("❌ No planet close enough to land. Fly closer first.")
                    return
                
                self.text_current_planet = closest_planet.name
                self.text_in_space = False
                print(f"🛬 Landed on {closest_planet.name}")
                print(f"🏢 Facilities: Trading Post, Fuel Station available")
            
            def text_takeoff(self):
                """Take off from planet"""
                if self.text_in_space:
                    print("❌ You're already in space!")
                    return
                
                print(f"🚀 Taking off from {self.text_current_planet}")
                self.text_in_space = True
                self.text_current_planet = None
            
            def text_trade(self):
                """Open trading interface in text"""
                if self.text_in_space:
                    print("❌ You must land on a planet to trade")
                    return
                
                print(f"\n🏪 TRADING POST - {self.text_current_planet}")
                print("="*40)
                print("Available commodities:")
                print("1. Food - Buy: 10 credits, Sell: 8 credits")
                print("2. Minerals - Buy: 25 credits, Sell: 20 credits")
                print("3. Technology - Buy: 50 credits, Sell: 40 credits")
                print("4. Luxury Goods - Buy: 75 credits, Sell: 60 credits")
                print("\n💡 Full trading system available in 3D mode!")
                print("💰 Your credits: {:,}".format(player_wallet.credits))
            
            def show_text_fleet(self):
                """Show fleet status"""
                fleet = enhanced_features.fleet_manager.fleet
                if fleet:
                    print(f"\n🚢 FLEET STATUS ({len(fleet)} ships):")
                    for i, ship in enumerate(fleet, 1):
                        print(f"{i}. {ship.name} ({ship.ship_class.value})")
                        print(f"   Condition: {ship.condition*100:.0f}%")
                else:
                    print("🚢 No ships in fleet")
                    print("💡 Capture ships through boarding in 3D mode!")
            
            def show_text_character(self):
                """Show character development"""
                char = enhanced_features.character_development
                print(f"\n👤 CHARACTER DEVELOPMENT:")
                print(f"Age: {int(char.age)} years old")
                print(f"Years Active: {char.years_active:.1f}")
                print("\n📊 SKILLS:")
                for skill, level in char.skills.items():
                    print(f"  {skill.value}: {level:.1f}")
            
            def text_scan(self):
                """Scan for nearby objects"""
                print("📡 SCANNING...")
                
                # Show nearby planets
                nearby_planets = []
                for planet in planets:
                    distance = (planet.position - self.text_player_pos).length()
                    if distance < 100:
                        nearby_planets.append((planet, distance))
                
                if nearby_planets:
                    print("🌍 Nearby planets:")
                    for planet, distance in sorted(nearby_planets, key=lambda x: x[1])[:5]:
                        print(f"  {planet.name} - {distance:.1f} units")
                else:
                    print("❌ No planets detected in range")
                
                # Show treasure hunt opportunities
                treasures = enhanced_features.treasure_hunting.scan_for_treasures(self.text_player_pos)
                if treasures:
                    print("💎 Treasure sites detected!")
                else:
                    print("🔍 No treasure sites in scanning range")
        
        # Set up mock app
        app = MockApp()
        
        # Add missing color attributes to avoid runtime errors
        color.dark_gray = "dark_gray"
        color.gray = "gray"
        
        logger.info("Headless components loaded successfully")
        GRAPHICS_AVAILABLE = False
        
    except Exception as e:
        logger.error(f"Failed to load headless components: {e}")
        logger.error(traceback.format_exc())
        print("\n❌ HEADLESS MODE FAILED TO INITIALIZE")
        print("This suggests the headless components are not properly installed.")
        print("Please ensure all dependencies are installed correctly.")
        sys.exit(1)
else:
    # Try to load graphics components
    try:
        from ursina import *
        from ursina.prefabs.first_person_controller import FirstPersonController
        GRAPHICS_AVAILABLE = True
        logger.info("Graphics components loaded successfully")
        
        # Create Ursina app for GUI mode
        app = Ursina(borderless=False)  # Make window resizable and movable
    except Exception as e:
        logger.error(f"Graphics not available: {e}")
        logger.error(traceback.format_exc())
        print(f"\n❌ GRAPHICS INITIALIZATION FAILED")
        print(f"Error: {e}")
        print("\nThis appears to be a headless environment or graphics are not available.")
        print("\n=== SOLUTIONS ===")
        print("1. Run in headless mode:")
        print("   python run_me.py --headless")
        print("2. Run headless stability tests:")
        print("   python run_me.py --headless --test")
        print("3. If on a local system with graphics:")
        print("   - Install OpenGL drivers")
        print("   - Install pygame: pip install pygame")
        print("   - Install ursina: pip install ursina")
        print("   - Ensure DISPLAY environment variable is set")
        print("\n=== GAME FEATURES ===")
        print("• Space exploration with multiple randomly generated planets")
        print("• Enhanced Pirates! features: Fleet management, character development")
        print("• Landing system - get close to planets to land on them")
        print("• Trading system - buy and sell resources at different planets")
        print("• Two game modes: Space (6DOF movement) and Surface (FPS-style)")
        print("• Inventory and resource management")
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
        print("  T - Open trading menu (when near trading posts)")
        print("\nUniversal:")
        print("  ESC - Pause menu (Save/Load/Quit)")
        print("  I - Open inventory")
        print("  F6 - Take screenshot")
        print("  F8 - Switch between Space and Surface modes")
        sys.exit(1)
        
        GRAPHICS_AVAILABLE = False

import random
import math
import json
import pickle
from datetime import datetime

# Make numpy optional for headless mode demo
try:
    import numpy as np
except ImportError:
    logger.warning("NumPy not available - some features may be limited")
    np = None

# Transport System Imports
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

# App will be created in the appropriate section based on mode

# ===== ENHANCED PIRATES! FEATURES =====

class ShipClass(Enum):
    FIGHTER = "FIGHTER"
    CORVETTE = "CORVETTE" 
    FRIGATE = "FRIGATE"
    DESTROYER = "DESTROYER"
    CRUISER = "CRUISER"
    BATTLESHIP = "BATTLESHIP"
    CARRIER = "CARRIER"
    FREIGHTER = "FREIGHTER"
    TRANSPORT = "TRANSPORT"
    MINING_BARGE = "MINING_BARGE"

@dataclass
class ShipStats:
    max_health: int
    armor: int
    shield_strength: int
    speed: float
    maneuverability: float
    cargo_capacity: int
    crew_capacity: int
    fuel_capacity: int
    weapon_hardpoints: int
    base_cost: int

class CapturedShip:
    def __init__(self, ship_class, name=None, condition=1.0):
        self.ship_class = ship_class
        self.name = name or f"{ship_class.value}-{random.randint(100, 999)}"
        self.condition = condition
        self.stats = self.get_base_stats()
        self.current_health = int(self.stats.max_health * condition)
        self.assigned_crew = []
        self.position = Vec3(0, 0, 0)
        self.role = "patrol"
        self.cargo = {}
        self.fuel = self.stats.fuel_capacity * condition
        
    def get_base_stats(self):
        ship_stats = {
            ShipClass.FIGHTER: ShipStats(100, 5, 50, 150, 0.9, 10, 2, 80, 2, 50000),
            ShipClass.CORVETTE: ShipStats(200, 15, 100, 120, 0.8, 50, 5, 150, 4, 120000),
            ShipClass.FRIGATE: ShipStats(500, 30, 200, 100, 0.6, 100, 15, 300, 6, 300000),
            ShipClass.DESTROYER: ShipStats(800, 50, 300, 80, 0.5, 150, 25, 500, 8, 600000),
            ShipClass.CRUISER: ShipStats(1200, 75, 500, 70, 0.4, 300, 50, 800, 10, 1200000),
            ShipClass.BATTLESHIP: ShipStats(2000, 120, 800, 50, 0.3, 200, 80, 1200, 15, 2500000),
            ShipClass.CARRIER: ShipStats(1500, 60, 400, 60, 0.3, 500, 100, 1000, 5, 2000000),
            ShipClass.FREIGHTER: ShipStats(400, 20, 100, 70, 0.4, 1000, 10, 600, 2, 400000),
            ShipClass.TRANSPORT: ShipStats(300, 15, 80, 80, 0.5, 200, 50, 400, 1, 250000),
            ShipClass.MINING_BARGE: ShipStats(600, 40, 150, 40, 0.2, 800, 20, 800, 3, 800000)
        }
        return ship_stats.get(self.ship_class, ship_stats[ShipClass.CORVETTE])
    
    def get_effective_stats(self):
        base = self.stats
        condition_mod = self.condition
        crew_mod = min(1.2, len(self.assigned_crew) / (base.crew_capacity * 0.5)) if base.crew_capacity > 0 else 1.0
        
        return {
            'health': int(base.max_health * condition_mod),
            'speed': base.speed * condition_mod * crew_mod,
            'cargo': int(base.cargo_capacity * condition_mod),
            'combat_rating': (base.armor + base.shield_strength) * condition_mod * crew_mod
        }

class FleetManager:
    def __init__(self):
        self.flagship = None
        self.fleet = []
        self.max_fleet_size = 8
        self.fleet_reputation = 0
        
    def add_ship(self, ship):
        if len(self.fleet) < self.max_fleet_size:
            self.fleet.append(ship)
            return True
        return False
    
    def get_fleet_combat_strength(self):
        total_strength = 0
        for ship in self.fleet:
            if ship.role in ['combat', 'escort', 'patrol']:
                stats = ship.get_effective_stats()
                total_strength += stats['combat_rating']
        return total_strength
    
    def update_fleet_positions(self, flagship_pos):
        for i, ship in enumerate(self.fleet):
            angle = (i / len(self.fleet)) * 2 * math.pi if len(self.fleet) > 0 else 0
            distance = 20 + (i % 3) * 10
            offset_x = math.cos(angle) * distance
            offset_z = math.sin(angle) * distance
            ship.position = flagship_pos + Vec3(offset_x, 0, offset_z)

class TreasureType(Enum):
    ANCIENT_ARTIFACT = "ANCIENT_ARTIFACT"
    ALIEN_TECHNOLOGY = "ALIEN_TECHNOLOGY"
    SHIP_WRECKAGE = "SHIP_WRECKAGE"
    DATA_CACHE = "DATA_CACHE"
    MINERAL_DEPOSIT = "MINERAL_DEPOSIT"
    LOST_CARGO = "LOST_CARGO"

@dataclass
class TreasureSite:
    position: Vec3
    treasure_type: TreasureType
    difficulty: int
    discovered: bool
    estimated_value: int
    description: str

class TreasureHuntingSystem:
    def __init__(self):
        self.treasure_sites = []
        self.scanning_range = 15.0
        self.generate_treasure_sites()
        
    def generate_treasure_sites(self):
        for _ in range(15):
            site = TreasureSite(
                position=Vec3(random.randint(-400, 400), 0, random.randint(-400, 400)),
                treasure_type=random.choice(list(TreasureType)),
                difficulty=random.randint(1, 5),
                discovered=False,
                estimated_value=random.randint(10000, 200000),
                description="Mysterious signal detected"
            )
            self.treasure_sites.append(site)
            
    def scan_for_treasures(self, player_position):
        found_treasures = []
        for site in self.treasure_sites:
            distance = (site.position - player_position).length()
            if distance <= self.scanning_range and not site.discovered:
                if random.random() < 0.2:  # 20% chance
                    found_treasures.append(site)
                    print(f"📡 Treasure detected! {site.treasure_type.value} at {site.position}")
        return found_treasures
    
    def excavate_treasure(self, site):
        if site.discovered:
            return None
            
        excavation_roll = random.randint(1, 20)
        if excavation_roll >= (10 + site.difficulty):
            site.discovered = True
            treasure_value = int(site.estimated_value * random.uniform(0.8, 1.2))
            print(f"💎 Treasure found! {site.treasure_type.value} worth {treasure_value} credits!")
            return treasure_value
        else:
            print(f"❌ Excavation failed. Try again later.")
            return None

class AssaultType(Enum):
    ORBITAL_BOMBARDMENT = "ORBITAL_BOMBARDMENT"
    SURGICAL_STRIKE = "SURGICAL_STRIKE"
    BLOCKADE = "BLOCKADE"

class OrbitalCombatSystem:
    def __init__(self):
        self.bombardment_active = False
        
    def initiate_orbital_assault(self, planet_name, assault_type, fleet_strength):
        print(f"🚀 Initiating {assault_type.value} on {planet_name}")
        
        # Calculate success based on fleet strength
        base_chance = 0.6
        strength_bonus = min(0.3, fleet_strength / 1000)
        success_chance = base_chance + strength_bonus
        
        if random.random() < success_chance:
            if assault_type == AssaultType.ORBITAL_BOMBARDMENT:
                credits_gained = random.randint(50000, 200000)
                reputation_loss = -25  # Major war crime
                print(f"💥 Bombardment successful! Gained {credits_gained} credits.")
                print(f"⚠️ WARNING: Massive reputation loss (-25) with all factions!")
                return {'success': True, 'credits': credits_gained, 'reputation': reputation_loss}
            elif assault_type == AssaultType.SURGICAL_STRIKE:
                credits_gained = random.randint(20000, 80000)
                reputation_loss = -10
                print(f"🎯 Surgical strike successful! Gained {credits_gained} credits.")
                return {'success': True, 'credits': credits_gained, 'reputation': reputation_loss}
        else:
            print(f"❌ Assault failed! Fleet took casualties.")
            return {'success': False, 'fleet_damage': random.randint(10, 30)}

class PersonalSkill(Enum):
    PILOTING = "PILOTING"
    COMBAT = "COMBAT"
    LEADERSHIP = "LEADERSHIP"
    ENGINEERING = "ENGINEERING"
    TRADING = "TRADING"
    DIPLOMACY = "DIPLOMACY"

class CharacterDevelopment:
    def __init__(self):
        self.age = 25
        self.skills = {skill: random.randint(3, 7) for skill in PersonalSkill}
        self.experience_points = {skill: 0 for skill in PersonalSkill}
        self.legendary_achievements = []
        self.years_active = 0
        
    def gain_experience(self, skill_type, amount):
        if skill_type in self.experience_points:
            # Implement skill cap at 100 to prevent overflow
            if self.skills[skill_type] >= 100.0:
                return  # Already at maximum skill level
                
            self.experience_points[skill_type] += amount
            required_exp = int(self.skills[skill_type] * 100)
            if self.experience_points[skill_type] >= required_exp:
                self.skills[skill_type] = min(100.0, self.skills[skill_type] + 0.5)
                self.experience_points[skill_type] = 0
                
                if self.skills[skill_type] < 100.0:
                    print(f"📈 {skill_type.value} skill improved to {self.skills[skill_type]:.1f}!")
                else:
                    print(f"🎯 {skill_type.value} skill mastered at maximum level (100.0)!")
                
    def advance_time(self, days):
        years_passed = days / 365.0
        old_age = self.age
        self.age += years_passed
        self.years_active += years_passed
        
        if int(old_age) != int(self.age):
            print(f"🎂 Another year passes. You are now {int(self.age)} years old.")

class BoardingAction(Enum):
    BREACH_AND_CLEAR = "BREACH_AND_CLEAR"
    STEALTH_INFILTRATION = "STEALTH_INFILTRATION"
    NEGOTIATED_SURRENDER = "NEGOTIATED_SURRENDER"

class ShipBoardingSystem:
    def __init__(self):
        self.boarding_active = False
        
    def initiate_boarding(self, target_ship_type, boarding_action):
        print(f"🚀 Initiating boarding: {boarding_action.value}")
        
        success_chances = {
            BoardingAction.BREACH_AND_CLEAR: 0.7,
            BoardingAction.STEALTH_INFILTRATION: 0.5,
            BoardingAction.NEGOTIATED_SURRENDER: 0.4
        }
        
        if random.random() < success_chances[boarding_action]:
            cargo_value = random.randint(15000, 80000)
            ship_condition = random.uniform(0.6, 1.0)
            
            print(f"✅ Boarding successful! Captured {cargo_value} credits worth of cargo.")
            print(f"Ship condition: {ship_condition*100:.0f}%")
            
            if ship_condition > 0.7:
                # Offer to add ship to fleet
                ship_class = random.choice(list(ShipClass))
                captured_ship = CapturedShip(ship_class, condition=ship_condition)
                print(f"💡 {ship_class.value} captured! Consider adding to fleet.")
                return {'success': True, 'cargo': cargo_value, 'ship': captured_ship}
            else:
                return {'success': True, 'cargo': cargo_value, 'ship': None}
        else:
            print(f"❌ Boarding failed!")
            return {'success': False}

# ===== ENHANCED FEATURES INTEGRATION =====

class EnhancedPiratesFeatures:
    def __init__(self):
        self.fleet_manager = FleetManager()
        self.treasure_hunting = TreasureHuntingSystem()
        self.orbital_combat = OrbitalCombatSystem()
        self.character_development = CharacterDevelopment()
        self.ship_boarding = ShipBoardingSystem()
        
        print("🚀 Enhanced Pirates! features loaded!")
        print("   Fleet Management, Treasure Hunting, Orbital Combat, Character Development")
    
    def update(self, dt, player_position, current_time):
        # Update character aging (convert seconds to days)
        self.character_development.advance_time(dt / 86400.0)
        
        # Update fleet positions
        if self.fleet_manager.fleet:
            self.fleet_manager.update_fleet_positions(player_position)
            
        # Random treasure scanning
        if random.random() < 0.005:  # 0.5% chance per update
            treasures = self.treasure_hunting.scan_for_treasures(player_position)

# Trading and Economy System
class Commodity:
    def __init__(self, name, base_price, category="general"):
        self.name = name
        self.base_price = base_price
        self.category = category
        
    def get_price(self, planet_type="generic", supply_demand_modifier=1.0):
        """Calculate price based on planet type and market conditions - allows crashes and booms"""
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
        
        # Allow full price volatility - crashes and booms are realistic!
        final_price = self.base_price * modifier * supply_demand_modifier
        
        # Only prevent technical issues (negative/zero prices), not economic ones
        return max(1, int(final_price))

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

class PlanetEconomy:
    def __init__(self, planet_name, planet_type):
        self.planet_name = planet_name
        self.planet_type = planet_type
        self.population = random.randint(100000, 1000000)
        
        # PERSISTENT STOCKPILES - actual commodity amounts on planet
        self.stockpiles = {}
        
        # PRODUCTION/CONSUMPTION per day based on planet type
        self.daily_production = {}
        self.daily_consumption = {}
        
        # BLOCKADE status - affects supply chain
        self.blockaded = False
        self.blockade_days = 0
        
        # TRADING HISTORY - track player impact
        self.trade_volume_today = {}
        
        self.initialize_economy()
        
    def initialize_economy(self):
        """Set realistic starting stockpiles and production based on planet type"""
        
        # Base consumption for all planets (basic needs)
        base_consumption = {
            "food": self.population // 5000,      # 200 food per day for 1M people
            "medicine": self.population // 50000,  # 20 medicine per day
            "fuel": self.population // 10000      # 100 fuel per day
        }
        
        # Planet type specializations
        if self.planet_type == "agricultural":
            # Produces massive food, consumes tech/luxury
            self.daily_production = {"food": base_consumption["food"] * 3, "spices": 50}
            self.daily_consumption = {**base_consumption, "technology": 30, "luxury_goods": 20}
            self.stockpiles = {"food": 5000, "spices": 500, "technology": 50, "luxury_goods": 100}
            
        elif self.planet_type == "industrial":
            # Produces tech/weapons, consumes food/minerals
            self.daily_production = {"technology": 40, "weapons": 20, "medicine": 30}
            self.daily_consumption = {**base_consumption, "minerals": 100, "luxury_goods": 30}
            self.stockpiles = {"technology": 800, "weapons": 300, "medicine": 400, "food": 200}
            
        elif self.planet_type == "mining":
            # Produces minerals/fuel, consumes food/tech
            self.daily_production = {"minerals": 150, "fuel": 100}
            self.daily_consumption = {**base_consumption, "technology": 40, "luxury_goods": 15}
            self.stockpiles = {"minerals": 3000, "fuel": 2000, "food": 150, "technology": 60}
            
        elif self.planet_type == "tech":
            # Produces advanced tech, consumes minerals/luxury
            self.daily_production = {"technology": 60, "medicine": 40, "weapons": 30}
            self.daily_consumption = {**base_consumption, "minerals": 80, "luxury_goods": 50}
            self.stockpiles = {"technology": 1200, "medicine": 600, "weapons": 400, "luxury_goods": 200}
            
        elif self.planet_type == "luxury":
            # Produces luxury goods, consumes everything else
            self.daily_production = {"luxury_goods": 80, "spices": 40}
            self.daily_consumption = {**base_consumption, "technology": 50, "minerals": 60}
            self.stockpiles = {"luxury_goods": 1500, "spices": 800, "food": 300}
            
        else:  # Generic/other planet types
            # Balanced production/consumption
            self.daily_production = {"food": base_consumption["food"] // 2, "minerals": 50}
            self.daily_consumption = base_consumption
            self.stockpiles = {"food": 1000, "minerals": 800, "technology": 200}
            
        # Ensure all commodities exist in stockpiles (even if 0)
        for commodity in ["food", "minerals", "technology", "luxury_goods", "medicine", "weapons", "fuel", "spices"]:
            if commodity not in self.stockpiles:
                self.stockpiles[commodity] = 0
                
    def daily_economic_update(self):
        """Process daily production, consumption, and trade effects - realistic economics"""
        
        # 1. PRODUCTION PHASE - Only what the planet actually produces
        for commodity, amount in self.daily_production.items():
            production = amount
            
            # Blockades reduce production efficiency
            if self.blockaded:
                production = int(production * (0.5 - min(0.4, self.blockade_days * 0.05)))
                
            self.stockpiles[commodity] = self.stockpiles.get(commodity, 0) + production
            
        # 2. CONSUMPTION PHASE - Realistic rationing when supplies are low
        for commodity, amount in self.daily_consumption.items():
            current_stock = self.stockpiles.get(commodity, 0)
            
            # Calculate actual consumption based on availability
            if current_stock >= amount:
                # Normal consumption when supplies are adequate
                actual_consumption = amount
            elif current_stock > 0:
                # Rationing when supplies are limited - use what's available
                actual_consumption = current_stock
                shortage_ratio = actual_consumption / amount if amount > 0 else 0
                
                # Only print shortage messages for severe shortages to avoid spam
                if shortage_ratio < 0.3:  # Less than 30% of needs met
                    print(f"⚠️ {self.planet_name}: Critical {commodity} shortage! ({shortage_ratio:.1%} needs met)")
            else:
                # No supply available
                actual_consumption = 0
                print(f"🚨 {self.planet_name}: Complete {commodity} shortage!")
                
            # Update stockpiles - can go to zero naturally
            self.stockpiles[commodity] = max(0, current_stock - actual_consumption)
                
        # 3. BLOCKADE EFFECTS - Realistic waste and disruption
        if self.blockaded:
            self.blockade_days += 1
            # Blockades cause waste through disrupted logistics
            for commodity in self.stockpiles:
                if self.stockpiles[commodity] > 0:
                    waste = max(1, int(self.stockpiles[commodity] * 0.02))  # 2% daily waste
                    self.stockpiles[commodity] = max(0, self.stockpiles[commodity] - waste)
        else:
            self.blockade_days = 0
            
        # 4. MARKET RESPONSE TO SHORTAGES - Increased trading activity, not free resources
        self.urgent_needs = []
        for commodity, amount in self.daily_consumption.items():
            current_stock = self.stockpiles.get(commodity, 0)
            days_remaining = current_stock / amount if amount > 0 else float('inf')
            
            if days_remaining < 5:  # Less than 5 days supply
                urgency = "CRITICAL" if days_remaining < 1 else "HIGH"
                self.urgent_needs.append({
                    'commodity': commodity,
                    'days_remaining': days_remaining,
                    'urgency': urgency,
                    'max_price_willing': self.get_buy_price(commodity) * (3 if urgency == "CRITICAL" else 2)
                })
        
        # 5. LOGICAL SECURITY RESPONSE - Wealthy planets invest in defense
        self.assess_security_needs()
            
        # 6. RESET DAILY TRADE TRACKING
        self.trade_volume_today = {}
        
    def assess_security_needs(self):
        """LOGICAL: Wealthy planets should invest more in security"""
        # Calculate planetary wealth
        total_stockpile_value = 0
        for commodity, quantity in self.stockpiles.items():
            if quantity > 0:
                base_prices = {"food": 10, "technology": 50, "minerals": 25, "luxury_goods": 75, 
                              "medicine": 40, "weapons": 60, "fuel": 15, "spices": 35}
                base_price = base_prices.get(commodity, 20)
                total_stockpile_value += quantity * base_price
        
        # Calculate trade volume (wealth generation)
        daily_trade_value = sum(self.trade_volume_today.values()) * 50  # Estimate value
        
        # Total wealth assessment
        wealth_level = total_stockpile_value + (daily_trade_value * 30)  # 30 days of trade
        
        # LOGICAL RESPONSE: Rich planets hire protection
        if wealth_level > 500000:  # Very wealthy
            if random.random() < 0.4:  # 40% chance daily
                self.hire_security("HIGH", wealth_level)
        elif wealth_level > 200000:  # Moderately wealthy  
            if random.random() < 0.2:  # 20% chance daily
                self.hire_security("MEDIUM", wealth_level)
        elif wealth_level > 50000:   # Some wealth
            if random.random() < 0.1:  # 10% chance daily
                self.hire_security("LOW", wealth_level)
                
        # ALSO: Respond to recent pirate activity
        if hasattr(self, 'recent_attacks') and self.recent_attacks > 0:
            if random.random() < 0.6:  # 60% chance after attack
                self.hire_security("EMERGENCY", wealth_level)
                self.recent_attacks = max(0, self.recent_attacks - 1)  # Decay over time
                
    def hire_security(self, security_level, wealth):
        """Hire security forces based on wealth"""
        security_costs = {
            "LOW": wealth * 0.02,      # 2% of wealth
            "MEDIUM": wealth * 0.05,   # 5% of wealth  
            "HIGH": wealth * 0.08,     # 8% of wealth
            "EMERGENCY": wealth * 0.12  # 12% of wealth
        }
        
        cost = int(security_costs[security_level])
        
        # Wealthy planets can afford security
        if wealth > cost * 10:  # Only if cost is <10% of wealth
            # Reduce stockpiles to pay for security (convert wealth to protection)
            # This is a logical trade-off
            security_commodities = ["weapons", "technology", "fuel"]
            for commodity in security_commodities:
                if commodity in self.stockpiles and self.stockpiles[commodity] > 10:
                    reduction = min(cost // 100, self.stockpiles[commodity] // 2)
                    self.stockpiles[commodity] -= reduction
                    cost -= reduction * 50  # Rough value conversion
                    if cost <= 0:
                        break
            
            if not hasattr(self, 'security_level'):
                self.security_level = 0
            self.security_level = min(100, self.security_level + (20 if security_level == "HIGH" else 10))
            
            print(f"🛡️ {self.planet_name} hired {security_level} security (Level: {self.security_level})")
            
    def record_pirate_attack(self):
        """Record when planet is attacked by pirates"""
        if not hasattr(self, 'recent_attacks'):
            self.recent_attacks = 0
        self.recent_attacks += 1
        print(f"⚠️ {self.planet_name} records pirate attack! (Recent attacks: {self.recent_attacks})")
        
    def get_available_supply(self, commodity):
        """How much of this commodity can be purchased"""
        stockpile = self.stockpiles.get(commodity, 0)
        
        # Don't sell below strategic reserves (10 days consumption)
        consumption = self.daily_consumption.get(commodity, 0)
        strategic_reserve = consumption * 10
        
        return max(0, stockpile - strategic_reserve)
        
    def get_buy_price(self, commodity):
        """Calculate buy price with realistic market volatility - allows crashes and booms"""
        base_commodity = market_system.commodities.get(commodity)
        if not base_commodity:
            return 0
            
        base_price = base_commodity.base_price
        
        # Supply factor - dramatic price swings for shortages
        available = self.get_available_supply(commodity)
        consumption = self.daily_consumption.get(commodity, 1)
        
        if available <= 0:
            supply_factor = 20.0  # Extreme crisis pricing
        elif available < consumption:  # Less than 1 day supply
            if consumption > 0:
                days_left = available / consumption
                supply_factor = 10.0 + (1.0 - days_left) * 10.0  # 10x to 20x price
            else:
                supply_factor = 15.0
        elif available < consumption * 3:  # Less than 3 days supply
            if consumption > 0:
                days_left = available / consumption
                supply_factor = 3.0 + (3.0 - days_left) * 2.0  # 3x to 9x price
            else:
                supply_factor = 5.0
        elif available < consumption * 10:  # Less than 10 days supply
            if consumption > 0:
                days_left = available / consumption
                supply_factor = 1.5 + (10.0 - days_left) * 0.15  # 1.5x to 2.5x price
            else:
                supply_factor = 2.0
        elif available > consumption * 50:  # More than 50 days supply
            supply_factor = 0.3  # Market crash - oversupply
        else:
            supply_factor = 1.0  # Normal market
            
        # Demand factor (production surplus = market crash)
        production = self.daily_production.get(commodity, 0)
        if production > consumption * 2:
            demand_factor = 0.2  # Massive oversupply crash
        elif production > consumption:
            demand_factor = 0.5  # Oversupply
        elif production < consumption * 0.5:
            demand_factor = 2.0  # High demand
        else:
            demand_factor = 1.0  # Balanced
            
        # Blockade factor - dramatic price increases
        blockade_factor = 1.0 + (self.blockade_days * 0.2) if self.blockaded else 1.0
        
        # Planet type modifier - specialization matters
        planet_modifiers = {
            "agricultural": {"food": 0.4, "technology": 2.0, "minerals": 1.5, "luxury_goods": 1.8},
            "industrial": {"minerals": 0.6, "technology": 0.5, "food": 2.5, "weapons": 0.6},
            "mining": {"minerals": 0.3, "fuel": 0.4, "technology": 2.5, "food": 2.0},
            "tech": {"technology": 0.4, "medicine": 0.5, "minerals": 1.8, "food": 1.8},
            "luxury": {"luxury_goods": 0.5, "spices": 0.4, "food": 1.5, "technology": 1.5}
        }
        
        planet_factor = planet_modifiers.get(self.planet_type, {}).get(
            base_commodity.category, 1.0)
            
        final_price = base_price * supply_factor * demand_factor * blockade_factor * planet_factor
        return max(1, int(final_price))
        
    def get_sell_price(self, commodity):
        """Price planet pays when buying from player - dramatic swings based on need"""
        buy_price = self.get_buy_price(commodity)
        
        # Calculate urgency of need
        available = self.get_available_supply(commodity)
        consumption = self.daily_consumption.get(commodity, 1)
        
        if available <= 0:
            sell_ratio = 0.98  # Desperate - pay almost full market price
        elif available < consumption:  # Less than 1 day supply
            sell_ratio = 0.95  # Critical need
        elif available < consumption * 3:  # Less than 3 days supply
            sell_ratio = 0.90  # High demand
        elif available < consumption * 10:  # Less than 10 days supply
            sell_ratio = 0.85  # Moderate demand
        else:
            # Check if planet actually needs this commodity
            if commodity in self.daily_consumption and self.daily_consumption[commodity] > 0:
                sell_ratio = 0.75  # Normal demand
            else:
                sell_ratio = 0.40  # Low demand - planet doesn't really need this
            
        # Bonus for urgent needs
        if hasattr(self, 'urgent_needs'):
            for need in self.urgent_needs:
                if need['commodity'] == commodity:
                    if need['urgency'] == "CRITICAL":
                        sell_ratio = min(0.99, sell_ratio + 0.10)  # Desperation bonus
                    else:
                        sell_ratio = min(0.95, sell_ratio + 0.05)  # Urgency bonus
                    break
            
        return max(1, int(buy_price * sell_ratio))
        
    def trade_transaction(self, commodity, quantity, is_player_buying):
        """Execute a trade and update stockpiles"""
        if is_player_buying:
            # Player buying from planet
            available = self.get_available_supply(commodity)
            actual_quantity = min(quantity, available)
            self.stockpiles[commodity] -= actual_quantity
        else:
            # Player selling to planet
            self.stockpiles[commodity] += quantity
            actual_quantity = quantity
            
        # Track trade volume for market effects
        self.trade_volume_today[commodity] = self.trade_volume_today.get(commodity, 0) + actual_quantity
        return actual_quantity

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
        
        # Planet economies - persistent economic simulation
        self.planet_economies = {}
        
    def generate_market_for_planet(self, planet_name, planet_type="generic"):
        """Generate a realistic persistent economy for a planet"""
        if planet_name not in self.planet_economies:
            self.planet_economies[planet_name] = PlanetEconomy(planet_name, planet_type)
        
    def get_buy_price(self, planet_name, commodity_name):
        """Price player pays to buy from planet"""
        if planet_name not in self.planet_economies:
            return 0
            
        economy = self.planet_economies[planet_name]
        return economy.get_buy_price(commodity_name)
        
    def get_sell_price(self, planet_name, commodity_name):
        """Price player gets when selling to planet"""
        if planet_name not in self.planet_economies:
            return 0
            
        economy = self.planet_economies[planet_name]
        return economy.get_sell_price(commodity_name)
        
    def get_available_supply(self, planet_name, commodity_name):
        """How much of this commodity can be purchased from planet"""
        if planet_name not in self.planet_economies:
            return 0
            
        economy = self.planet_economies[planet_name]
        return economy.get_available_supply(commodity_name)
        
    def execute_trade(self, planet_name, commodity_name, quantity, is_player_buying):
        """Execute a trade transaction and update planet economy"""
        if planet_name not in self.planet_economies:
            return 0
            
        economy = self.planet_economies[planet_name]
        return economy.trade_transaction(commodity_name, quantity, is_player_buying)
        
    def daily_economic_update(self):
        """Update all planet economies daily"""
        for economy in self.planet_economies.values():
            economy.daily_economic_update()
            
    def set_blockade(self, planet_name, blockaded=True):
        """Set or remove blockade on a planet"""
        if planet_name in self.planet_economies:
            self.planet_economies[planet_name].blockaded = blockaded
            if blockaded:
                print(f"🚫 {planet_name} is now under blockade!")
            else:
                print(f"✅ Blockade on {planet_name} has been lifted!")
                
    def get_planet_info(self, planet_name):
        """Get detailed economic information about a planet"""
        if planet_name not in self.planet_economies:
            return None
            
        economy = self.planet_economies[planet_name]
        return {
            'population': economy.population,
            'type': economy.planet_type,
            'stockpiles': economy.stockpiles.copy(),
            'blockaded': economy.blockaded,
            'blockade_days': economy.blockade_days
        }

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
# ===== REALISTIC SHIP SYSTEMS =====

class ComponentType(Enum):
    ENGINE = "ENGINE"
    FUEL_TANK = "FUEL_TANK"
    LIFE_SUPPORT = "LIFE_SUPPORT"
    HULL = "HULL"
    SHIELDS = "SHIELDS"
    WEAPONS = "WEAPONS"
    CARGO_BAY = "CARGO_BAY"
    SENSORS = "SENSORS"

class ComponentCondition(Enum):
    PERFECT = "PERFECT"
    GOOD = "GOOD"
    DAMAGED = "DAMAGED"
    CRITICAL = "CRITICAL"
    DESTROYED = "DESTROYED"

@dataclass
class ShipComponent:
    component_type: ComponentType
    level: int
    condition: ComponentCondition
    max_integrity: int
    current_integrity: int
    efficiency: float  # 0.0 to 1.0
    
    def get_performance_modifier(self):
        """Get performance modifier based on condition"""
        condition_modifiers = {
            ComponentCondition.PERFECT: 1.0,
            ComponentCondition.GOOD: 0.85,
            ComponentCondition.DAMAGED: 0.6,
            ComponentCondition.CRITICAL: 0.3,
            ComponentCondition.DESTROYED: 0.0
        }
        return condition_modifiers[self.condition] * self.efficiency
    
    def take_damage(self, damage):
        """Apply damage to component"""
        self.current_integrity = max(0, self.current_integrity - damage)
        
        # Update condition based on integrity
        integrity_ratio = self.current_integrity / self.max_integrity
        if integrity_ratio >= 0.9:
            self.condition = ComponentCondition.PERFECT
        elif integrity_ratio >= 0.7:
            self.condition = ComponentCondition.GOOD
        elif integrity_ratio >= 0.4:
            self.condition = ComponentCondition.DAMAGED
        elif integrity_ratio > 0:
            self.condition = ComponentCondition.CRITICAL
        else:
            self.condition = ComponentCondition.DESTROYED
            
    def repair(self, repair_amount):
        """Repair component"""
        self.current_integrity = min(self.max_integrity, self.current_integrity + repair_amount)
        
        # Update condition
        integrity_ratio = self.current_integrity / self.max_integrity
        if integrity_ratio >= 0.9:
            self.condition = ComponentCondition.PERFECT
        elif integrity_ratio >= 0.7:
            self.condition = ComponentCondition.GOOD
        elif integrity_ratio >= 0.4:
            self.condition = ComponentCondition.DAMAGED
        elif integrity_ratio > 0:
            self.condition = ComponentCondition.CRITICAL

class FuelSystem:
    def __init__(self):
        self.max_fuel = 100.0
        self.current_fuel = 100.0
        self.fuel_efficiency = 1.0  # Base efficiency
        self.fuel_consumption_rate = 1.0  # Base consumption per unit distance
        
    def consume_fuel(self, distance, ship_mass=1.0, engine_efficiency=1.0):
        """Consume fuel based on distance, mass, and engine efficiency"""
        base_consumption = distance * self.fuel_consumption_rate * ship_mass
        actual_consumption = base_consumption / (self.fuel_efficiency * engine_efficiency)
        
        self.current_fuel = max(0, self.current_fuel - actual_consumption)
        return actual_consumption
        
    def refuel(self, amount):
        """Add fuel to tank"""
        self.current_fuel = min(self.max_fuel, self.current_fuel + amount)
        
    def get_fuel_percentage(self):
        """Get fuel level as percentage"""
        return (self.current_fuel / self.max_fuel) * 100
        
    def can_travel_distance(self, distance, ship_mass=1.0, engine_efficiency=1.0):
        """Check if ship has enough fuel for distance"""
        required_fuel = distance * self.fuel_consumption_rate * ship_mass / (self.fuel_efficiency * engine_efficiency)
        return self.current_fuel >= required_fuel

class EnhancedCrewMember:
    def __init__(self, name=None, specialization="general"):
        self.name = name or f"{random.choice(['Alex', 'Sam', 'Chris', 'Jordan', 'Taylor', 'Casey', 'Riley', 'Avery', 'Quinn', 'Morgan'])}-{random.randint(100, 999)}"
        self.specialization = specialization
        
        # Multiple skills per crew member
        self.skills = {
            "engineering": random.randint(1, 10),
            "piloting": random.randint(1, 10),
            "combat": random.randint(1, 10),
            "medical": random.randint(1, 10),
            "science": random.randint(1, 10),
            "leadership": random.randint(1, 10)
        }
        
        # Boost primary specialization
        if specialization in self.skills:
            self.skills[specialization] += random.randint(3, 7)
            self.skills[specialization] = min(20, self.skills[specialization])
        
        self.experience = 0
        self.loyalty = random.randint(50, 80)
        self.fatigue = 0  # 0-100
        self.health = 100
        self.wage = self.calculate_wage()
        
    def calculate_wage(self):
        """Calculate wage based on skills"""
        avg_skill = sum(self.skills.values()) / len(self.skills)
        return int(avg_skill * 3) + random.randint(5, 15)
        
    def get_effective_skill(self, skill_type):
        """Get effective skill considering fatigue and health"""
        base_skill = self.skills.get(skill_type, 0)
        fatigue_penalty = (self.fatigue / 100) * 0.3
        health_penalty = (100 - self.health) / 100 * 0.2
        
        return max(0, base_skill * (1 - fatigue_penalty - health_penalty))
        
    def gain_experience(self, skill_type, amount):
        """Gain experience in a skill with cap"""
        self.experience += amount
        if skill_type in self.skills:
            # Chance to improve skill with better cap
            if random.random() < 0.1:  # 10% chance
                old_skill = self.skills[skill_type]
                self.skills[skill_type] = min(50, self.skills[skill_type] + 1)  # Cap at 50 for crew
                
                if self.skills[skill_type] > old_skill:
                    if self.skills[skill_type] < 50:
                        print(f"{self.name} improved their {skill_type} skill to {self.skills[skill_type]}!")
                    else:
                        print(f"{self.name} has mastered {skill_type} at maximum level!")

class RealisticShipSystems:
    def __init__(self):
        # Initialize ship components
        self.components = {
            ComponentType.ENGINE: ShipComponent(ComponentType.ENGINE, 1, ComponentCondition.PERFECT, 100, 100, 1.0),
            ComponentType.FUEL_TANK: ShipComponent(ComponentType.FUEL_TANK, 1, ComponentCondition.PERFECT, 100, 100, 1.0),
            ComponentType.LIFE_SUPPORT: ShipComponent(ComponentType.LIFE_SUPPORT, 1, ComponentCondition.PERFECT, 100, 100, 1.0),
            ComponentType.HULL: ShipComponent(ComponentType.HULL, 1, ComponentCondition.PERFECT, 100, 100, 1.0),
            ComponentType.SHIELDS: ShipComponent(ComponentType.SHIELDS, 1, ComponentCondition.PERFECT, 100, 100, 1.0),
            ComponentType.WEAPONS: ShipComponent(ComponentType.WEAPONS, 1, ComponentCondition.PERFECT, 100, 100, 1.0),
            ComponentType.CARGO_BAY: ShipComponent(ComponentType.CARGO_BAY, 1, ComponentCondition.PERFECT, 100, 100, 1.0),
            ComponentType.SENSORS: ShipComponent(ComponentType.SENSORS, 1, ComponentCondition.PERFECT, 100, 100, 1.0)
        }
        
        # Fuel system
        self.fuel_system = FuelSystem()
        
        # Enhanced crew system
        self.crew = []
        self.max_crew = 10
        
        # Manufacturing and repair
        self.spare_parts = {
            "basic_components": 5,
            "advanced_components": 2,
            "rare_components": 0
        }
        
        # Performance tracking
        self.last_position = None
        self.distance_traveled = 0
        
        # Upgrade costs
        self.upgrade_costs = {
            'cargo': 200,
            'engine': 500,
            'fuel_tank': 400,
            'shields': 600,
            'weapons': 700,
            'life_support': 300
        }
        
    def update(self, current_position):
        """Update ship systems each frame"""
        # Calculate distance traveled
        if self.last_position is not None:
            distance = (current_position - self.last_position).length()
        else:
            distance = 0
            self.distance_traveled += distance
            
            # Consume fuel based on movement
            if distance > 0:
                engine_efficiency = self.components[ComponentType.ENGINE].get_performance_modifier()
                fuel_efficiency = self.components[ComponentType.FUEL_TANK].get_performance_modifier()
                ship_mass = self.calculate_ship_mass()
                
                fuel_consumed = self.fuel_system.consume_fuel(distance * 0.1, ship_mass, engine_efficiency * fuel_efficiency)
                
                # Gain crew experience for pilots
                for crew_member in self.crew:
                    if crew_member.specialization == "piloting":
                        crew_member.gain_experience("piloting", distance * 0.01)
        
        self.last_position = current_position
        
        # Component wear and tear
        self.apply_component_wear()
        
        # Update crew fatigue
        self.update_crew_fatigue()
        
    def calculate_ship_mass(self):
        """Calculate ship mass based on components and cargo"""
        base_mass = 1.0
        
        # Add mass from components
        for component in self.components.values():
            base_mass += component.level * 0.1
            
        # Add cargo mass
        cargo_mass = player_cargo.get_used_capacity() * 0.01
        
        return base_mass + cargo_mass
        
    def apply_component_wear(self):
        """Apply gradual wear to components"""
        for component in self.components.values():
            # Random chance of minor wear
            if random.random() < 0.0001:  # Very small chance per frame
                component.take_damage(1)
                
    def update_crew_fatigue(self):
        """Update crew fatigue over time"""
        for crew_member in self.crew:
            # Increase fatigue slowly
            crew_member.fatigue = min(100, crew_member.fatigue + 0.001)
            
    def get_engine_performance(self):
        """Get current engine performance"""
        engine = self.components[ComponentType.ENGINE]
        fuel_available = self.fuel_system.current_fuel > 0
        
        if not fuel_available:
            return 0.0
            
        return engine.get_performance_modifier()
        
    def get_cargo_capacity(self):
        """Get current cargo capacity"""
        cargo_bay = self.components[ComponentType.CARGO_BAY]
        base_capacity = 50 + (cargo_bay.level - 1) * 25
        
        return int(base_capacity * cargo_bay.get_performance_modifier())
        
    def get_max_speed(self):
        """Get maximum speed based on engine and mass"""
        engine_performance = self.get_engine_performance()
        ship_mass = self.calculate_ship_mass()
        
        base_speed = 50 + (self.components[ComponentType.ENGINE].level - 1) * 10
        
        return base_speed * engine_performance / ship_mass
        
    def repair_component(self, component_type, repair_parts):
        """Repair a component using spare parts"""
        if component_type not in self.components:
            return False
            
        component = self.components[component_type]
        
        # Check if we have parts
        parts_needed = "basic_components"
        if component.level > 3:
            parts_needed = "advanced_components"
        if component.level > 6:
            parts_needed = "rare_components"
            
        if self.spare_parts.get(parts_needed, 0) >= repair_parts:
            self.spare_parts[parts_needed] -= repair_parts
            component.repair(repair_parts * 20)
            
            # Crew gains experience
            for crew_member in self.crew:
                if crew_member.specialization == "engineering":
                    crew_member.gain_experience("engineering", repair_parts)
                    
            print(f"Repaired {component_type.value} using {repair_parts} {parts_needed}")
            return True
            
        return False
        
    def upgrade_component(self, component_type):
        """Upgrade a component"""
        if component_type not in self.upgrade_costs:
            return False
            
        cost = self.upgrade_costs[component_type]
        
        if player_wallet.can_afford(cost):
            player_wallet.spend(cost)
            
            component = self.components[component_type]
            component.level += 1
            component.max_integrity += 20
            component.current_integrity = component.max_integrity
            component.condition = ComponentCondition.PERFECT
            
            # Update costs
            self.upgrade_costs[component_type] = int(cost * 1.5)
            
            # Update player stats based on component
            if component_type == ComponentType.ENGINE:
                player.max_speed = self.get_max_speed()
            elif component_type == ComponentType.CARGO_BAY:
                player_cargo.max_capacity = self.get_cargo_capacity()
                
            print(f"{component_type.value} upgraded to level {component.level}!")
            return True
            
        return False
        
    def hire_crew_member(self, specialization="general"):
        """Hire a new crew member"""
        if len(self.crew) >= self.max_crew:
            return False
            
        new_crew = EnhancedCrewMember(specialization=specialization)
        hiring_cost = new_crew.wage * 10  # 10 days advance payment
        
        if player_wallet.can_afford(hiring_cost):
            player_wallet.spend(hiring_cost)
            self.crew.append(new_crew)
            print(f"Hired {new_crew.name} ({specialization}) for {hiring_cost} credits")
            return True
            
        return False
        
    def get_crew_effectiveness(self, skill_type):
        """Get total crew effectiveness for a skill"""
        total_effectiveness = 0
        
        for crew_member in self.crew:
            effectiveness = crew_member.get_effective_skill(skill_type)
            total_effectiveness += effectiveness
            
        return total_effectiveness
        
    def get_system_status(self):
        """Get comprehensive system status"""
        status = {
            'fuel_percentage': self.fuel_system.get_fuel_percentage(),
            'engine_performance': self.get_engine_performance(),
            'cargo_capacity': self.get_cargo_capacity(),
            'max_speed': self.get_max_speed(),
            'crew_count': len(self.crew),
            'damaged_components': []
        }
        
        for comp_type, component in self.components.items():
            if component.condition in [ComponentCondition.DAMAGED, ComponentCondition.CRITICAL, ComponentCondition.DESTROYED]:
                status['damaged_components'].append({
                    'type': comp_type.value,
                    'condition': component.condition.value,
                    'integrity': component.current_integrity
                })
                
        return status

# ===== ENHANCED MANUFACTURING SYSTEM =====

class ManufacturingProcess:
    def __init__(self, product, inputs, processing_time, skill_required="engineering"):
        self.product = product
        self.inputs = inputs  # Dict of {commodity: quantity}
        self.processing_time = processing_time  # In seconds
        self.skill_required = skill_required
        self.progress = 0
        self.active = False
        
    def can_start(self, available_materials, crew_effectiveness):
        """Check if manufacturing can start"""
        for commodity, required in self.inputs.items():
            if available_materials.get(commodity, 0) < required:
                return False
        return crew_effectiveness > 0
        
    def start_production(self, available_materials):
        """Start the manufacturing process"""
        if self.can_start(available_materials, 1):  # Simplified check
            for commodity, required in self.inputs.items():
                available_materials[commodity] -= required
            self.active = True
            self.progress = 0
            return True
        return False
        
    def update(self, dt, crew_effectiveness):
        """Update manufacturing progress"""
        if self.active:
            progress_rate = crew_effectiveness / 100.0  # Crew skill affects speed
            self.progress += dt * progress_rate
            
            if self.progress >= self.processing_time:
                self.active = False
                return True  # Production complete
        return False

class EnhancedManufacturing:
    def __init__(self):
        # Define manufacturing recipes
        self.recipes = {
            "advanced_components": ManufacturingProcess(
                "advanced_components",
                {"minerals": 10, "technology": 5, "basic_components": 3},
                60.0,  # 1 minute
                "engineering"
            ),
            "weapons": ManufacturingProcess(
                "weapons",
                {"minerals": 15, "advanced_components": 2, "technology": 8},
                120.0,  # 2 minutes
                "engineering"
            ),
            "medicine": ManufacturingProcess(
                "medicine",
                {"spices": 5, "technology": 3, "basic_components": 1},
                90.0,  # 1.5 minutes
                "medical"
            ),
            "luxury_goods": ManufacturingProcess(
                "luxury_goods",
                {"spices": 8, "technology": 2, "minerals": 5},
                150.0,  # 2.5 minutes
                "science"
            ),
            "basic_components": ManufacturingProcess(
                "basic_components",
                {"minerals": 5, "fuel": 2},
                30.0,  # 30 seconds
                "engineering"
            )
        }
        
        self.active_processes = {}  # Planet -> {recipe_name: ManufacturingProcess}
        
    def start_manufacturing(self, planet_name, recipe_name, available_materials, crew_effectiveness):
        """Start manufacturing on a planet"""
        if recipe_name not in self.recipes:
            return False
            
        if planet_name not in self.active_processes:
            self.active_processes[planet_name] = {}
            
        # Create a copy of the recipe for this planet
        recipe = ManufacturingProcess(
            self.recipes[recipe_name].product,
            self.recipes[recipe_name].inputs.copy(),
            self.recipes[recipe_name].processing_time,
            self.recipes[recipe_name].skill_required
        )
        
        if recipe.start_production(available_materials):
            self.active_processes[planet_name][recipe_name] = recipe
            print(f"🏭 {planet_name} started manufacturing {recipe_name}")
            return True
            
        return False
        
    def update_manufacturing(self, planet_name, dt, crew_effectiveness, stockpiles):
        """Update manufacturing processes for a planet"""
        if planet_name not in self.active_processes:
            return
            
        completed_processes = []
        
        for recipe_name, process in self.active_processes[planet_name].items():
            if process.update(dt, crew_effectiveness):
                # Production completed
                stockpiles[process.product] = stockpiles.get(process.product, 0) + 1
                completed_processes.append(recipe_name)
                print(f"✅ {planet_name} completed manufacturing {process.product}")
                
        # Remove completed processes
        for recipe_name in completed_processes:
            del self.active_processes[planet_name][recipe_name]
            
    def get_manufacturing_status(self, planet_name):
        """Get current manufacturing status for a planet"""
        if planet_name not in self.active_processes:
            return {}
            
        status = {}
        for recipe_name, process in self.active_processes[planet_name].items():
            progress_percentage = (process.progress / process.processing_time) * 100
            status[recipe_name] = {
                'progress': progress_percentage,
                'product': process.product,
                'time_remaining': process.processing_time - process.progress
            }
            
        return status

# Create global manufacturing system
enhanced_manufacturing = EnhancedManufacturing()

# ===== PERSISTENT MILITARY & POLITICAL SYSTEMS =====

class MilitaryShipType(Enum):
    PATROL = "PATROL"
    ESCORT = "ESCORT"
    BLOCKADE = "BLOCKADE"
    ASSAULT = "ASSAULT"
    CAPITAL = "CAPITAL"

class WeatherType(Enum):
    SOLAR_STORM = "SOLAR_STORM"
    ASTEROID_FIELD = "ASTEROID_FIELD"
    NEBULA = "NEBULA"
    ION_STORM = "ION_STORM"
    CLEAR = "CLEAR"

@dataclass
class WeatherEvent:
    weather_type: WeatherType
    position: tuple  # (x, y, z)
    radius: float
    intensity: float  # 0.0 to 1.0
    duration: float  # seconds
    start_time: float
    
class MilitaryShip(Entity):
    """Physical military ships that enforce faction control"""
    
    def __init__(self, faction_id, ship_type, position, patrol_radius=100):
        super().__init__(
            model='cube',
            position=position,
            scale=(1.5, 0.8, 3.0),  # Military ship shape
            color=self.get_faction_color(faction_id)
        )
        
        self.faction_id = faction_id
        self.ship_type = ship_type
        self.patrol_radius = patrol_radius
        self.target_position = position
        self.speed = 8.0
        self.weapons_strength = 50
        self.shields = 100
        self.patrol_center = position
        self.last_patrol_change = 0
        self.engagement_range = 50
        self.hostile_factions = []
        
        # Set hostile factions based on relationships
        if faction_id in faction_system.factions:
            for other_faction, relationship in faction_system.factions[faction_id].relationships.items():
                if relationship < -50:  # Hostile relationship
                    self.hostile_factions.append(other_faction)
        
    def get_faction_color(self, faction_id):
        """Get color based on faction"""
        faction_colors = {
            'terran_federation': color.blue,
            'mars_republic': color.red,
            'jupiter_consortium': color.orange,
            'outer_rim_pirates': color.dark_gray,
            'merchant_guild': color.green,
            'independent': color.white
        }
        return faction_colors.get(faction_id, color.gray)
        
    def update(self):
        if not paused:
            current_time = time.time()
            
            # Patrol behavior
            if self.ship_type == MilitaryShipType.PATROL:
                self.patrol_behavior(current_time)
            elif self.ship_type == MilitaryShipType.BLOCKADE:
                self.blockade_behavior()
            elif self.ship_type == MilitaryShipType.ESCORT:
                self.escort_behavior()
                
            # Move toward target
            if hasattr(self, 'target_position'):
                direction = (self.target_position - self.position).normalized()
                self.position += direction * self.speed * time.dt
                
            # Check for hostiles
            self.check_for_hostiles()
            
    def patrol_behavior(self, current_time):
        """Patrol around assigned area"""
        if current_time - self.last_patrol_change > 30:  # Change direction every 30 seconds
            # Pick new patrol point within radius
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(20, self.patrol_radius)
            
            offset_x = distance * math.cos(angle)
            offset_z = distance * math.sin(angle)
            
            self.target_position = self.patrol_center + Vec3(offset_x, 0, offset_z)
            self.last_patrol_change = current_time
            
    def blockade_behavior(self):
        """Stay in position to block access"""
        # Blockade ships stay near their assigned position
        if (self.position - self.patrol_center).length() > 20:
            self.target_position = self.patrol_center
            
    def escort_behavior(self):
        """Follow and protect cargo ships"""
        # Find nearby friendly cargo ships to escort
        for cargo_ship in unified_transport_system.cargo_ships:
            if hasattr(cargo_ship, 'position'):
                distance = (self.position - cargo_ship.position).length()
                if distance < 150:  # Within escort range
                    # Follow cargo ship's current target (waypoint or destination) for tighter convoying
                    follow_pos = getattr(cargo_ship, 'current_target_pos', cargo_ship.position)
                    self.target_position = follow_pos + Vec3(8, 0, 8)
                    break
                    
    def check_for_hostiles(self):
        """Check for hostile ships and player"""
        # Check player faction standing
        if scene_manager.current_state == GameState.SPACE and scene_manager.space_controller:
            player_pos = scene_manager.space_controller.position
            distance = (self.position - player_pos).length()
            
            if distance < self.engagement_range:
                player_rep = faction_system.player_reputation.get(self.faction_id, 0)
                if player_rep < -30:  # Hostile to player
                    self.engage_target(player_pos, "Player")
                    
        # Check for hostile faction ships
        all_ships = (unified_transport_system.cargo_ships + unified_transport_system.raiders + 
                    unified_transport_system.message_ships)
        
        for ship in all_ships:
            if hasattr(ship, 'position') and hasattr(ship, 'faction_id'):
                if ship.faction_id in self.hostile_factions:
                    distance = (self.position - ship.position).length()
                    if distance < self.engagement_range:
                        self.engage_target(ship.position, f"{ship.faction_id} ship")
                        
    def engage_target(self, target_pos, target_name):
        """Engage hostile target"""
        print(f"🚨 {self.faction_id} {self.ship_type.value} engaging {target_name}!")
        
        # Move to intercept
        self.target_position = target_pos
        
        # Apply damage if close enough
        if (self.position - target_pos).length() < 20:
            if target_name == "Player":
                damage = random.randint(10, 25)
                combat_system.take_damage(damage)
                print(f"💥 Military ship hit player for {damage} damage!")
            
class WeatherSystem:
    """Dynamic weather events that affect gameplay"""
    
    def __init__(self):
        self.active_weather = []
        self.last_weather_spawn = 0
        self.weather_spawn_interval = 180  # 3 minutes between weather events
        
    def update(self):
        current_time = time.time()
        
        # Remove expired weather
        self.active_weather = [w for w in self.active_weather 
                             if current_time - w.start_time < w.duration]
        
        # Spawn new weather events
        if current_time - self.last_weather_spawn > self.weather_spawn_interval:
            if random.random() < 0.3:  # 30% chance
                self.spawn_weather_event()
                self.last_weather_spawn = current_time
                
        # Update weather effects
        self.apply_weather_effects()
        
    def spawn_weather_event(self):
        """Spawn a new weather event"""
        weather_types = [WeatherType.SOLAR_STORM, WeatherType.ASTEROID_FIELD, 
                        WeatherType.NEBULA, WeatherType.ION_STORM]
        
        weather_type = random.choice(weather_types)
        
        # Random position in space
        position = (
            random.uniform(-400, 400),
            random.uniform(-100, 100),
            random.uniform(-400, 400)
        )
        
        radius = random.uniform(50, 150)
        intensity = random.uniform(0.3, 1.0)
        duration = random.uniform(300, 900)  # 5-15 minutes
        
        weather_event = WeatherEvent(
            weather_type=weather_type,
            position=position,
            radius=radius,
            intensity=intensity,
            duration=duration,
            start_time=time.time()
        )
        
        self.active_weather.append(weather_event)
        
        print(f"🌩️ {weather_type.value} spawned at {position} (radius: {radius:.0f})")
        
    def apply_weather_effects(self):
        """Apply weather effects to player and ships"""
        if scene_manager.current_state != GameState.SPACE:
            return
            
        player_pos = scene_manager.space_controller.position
        
        for weather in self.active_weather:
            weather_pos = Vec3(*weather.position)
            distance = (player_pos - weather_pos).length()
            
            if distance < weather.radius:
                # Player is in weather event
                effect_strength = (1.0 - distance / weather.radius) * weather.intensity
                self.apply_weather_effect_to_player(weather.weather_type, effect_strength)
                
    def apply_weather_effect_to_player(self, weather_type, strength):
        """Apply specific weather effects to player"""
        if weather_type == WeatherType.SOLAR_STORM:
            # Damage electronics and reduce fuel efficiency
            if random.random() < 0.001 * strength:  # Small chance per frame
                ship_systems.components[ComponentType.SENSORS].take_damage(1)
                print("⚡ Solar storm damaged sensors!")
                
        elif weather_type == WeatherType.ASTEROID_FIELD:
            # Chance of hull damage
            if random.random() < 0.0005 * strength:
                ship_systems.components[ComponentType.HULL].take_damage(5)
                print("☄️ Asteroid impact damaged hull!")
                
        elif weather_type == WeatherType.NEBULA:
            # Reduce sensor range and speed
            ship_systems.components[ComponentType.SENSORS].efficiency = max(0.5, 
                ship_systems.components[ComponentType.SENSORS].efficiency - 0.001 * strength)
                
        elif weather_type == WeatherType.ION_STORM:
            # Disrupt engines and electronics
            if random.random() < 0.0008 * strength:
                ship_systems.components[ComponentType.ENGINE].take_damage(2)
                print("⚡ Ion storm disrupted engines!")

class FactionMilitaryManager:
    """Manages military ships and territorial control for all factions"""
    
    def __init__(self):
        self.military_ships = []
        self.territorial_claims = {}  # faction_id -> list of planet names
        self.active_conflicts = []  # list of (faction1, faction2, conflict_type)
        self.blockade_zones = {}  # planet_name -> list of blockading ships
        
    def initialize_military_presence(self):
        """Create initial military ships for all factions"""
        print("🛡️ Deploying faction military forces...")
        
        for faction_id, faction in faction_system.factions.items():
            if faction_id == 'independent':
                continue  # Independents don't have organized military
                
            # Create patrol ships
            for _ in range(random.randint(2, 5)):
                position = Vec3(
                    random.uniform(-300, 300),
                    random.uniform(-50, 50),
                    random.uniform(-300, 300)
                )
                
                patrol_ship = MilitaryShip(faction_id, MilitaryShipType.PATROL, position)
                self.military_ships.append(patrol_ship)
                
        # Establish territorial claims
        self.establish_territorial_claims()
        
        # Create some initial conflicts
        self.create_initial_conflicts()
        
    def establish_territorial_claims(self):
        """Assign planets to factions based on their influence"""
        for planet in planets:
            # Assign planets to factions based on type and random factors
            if planet.planet_type == "industrial":
                claiming_faction = random.choice(['terran_federation', 'mars_republic'])
            elif planet.planet_type == "tech":
                claiming_faction = random.choice(['terran_federation', 'jupiter_consortium'])
            elif planet.planet_type == "mining":
                claiming_faction = random.choice(['mars_republic', 'jupiter_consortium'])
            else:
                claiming_faction = random.choice(list(faction_system.factions.keys()))
                
            if claiming_faction not in self.territorial_claims:
                self.territorial_claims[claiming_faction] = []
            self.territorial_claims[claiming_faction].append(planet.name)
            
            # Add faction color indicator to planet
            planet.faction_id = claiming_faction
            
    def create_initial_conflicts(self):
        """Create some conflicts between factions"""
        potential_conflicts = [
            ('terran_federation', 'mars_republic'),
            ('jupiter_consortium', 'outer_rim_pirates'),
            ('mars_republic', 'outer_rim_pirates')
        ]
        
        for faction1, faction2 in potential_conflicts:
            if random.random() < 0.4:  # 40% chance of conflict
                self.start_conflict(faction1, faction2)
                
    def start_conflict(self, faction1, faction2):
        """Start a conflict between two factions"""
        self.active_conflicts.append((faction1, faction2, "territorial_dispute"))
        
        print(f"⚔️ Conflict started: {faction1} vs {faction2}")
        
        # Create blockades
        self.create_blockades(faction1, faction2)
        
    def create_blockades(self, attacking_faction, defending_faction):
        """Create physical blockades around enemy planets"""
        if defending_faction in self.territorial_claims:
            for planet_name in self.territorial_claims[defending_faction]:
                if random.random() < 0.3:  # 30% chance to blockade each planet
                    self.establish_blockade(attacking_faction, planet_name)
                    
    def establish_blockade(self, faction_id, planet_name):
        """Establish a physical blockade around a planet"""
        # Find the planet
        target_planet = None
        for planet in planets:
            if planet.name == planet_name:
                target_planet = planet
                break
                
        if not target_planet:
            return
            
        # Create blockade ships around the planet
        blockade_ships = []
        num_ships = random.randint(3, 6)
        
        for i in range(num_ships):
            angle = (2 * 3.14159 * i) / num_ships
            distance = target_planet.landing_radius + 30
            
            position = target_planet.position + Vec3(
                distance * math.cos(angle),
                random.uniform(-10, 10),
                distance * math.sin(angle)
            )
            
            blockade_ship = MilitaryShip(faction_id, MilitaryShipType.BLOCKADE, position)
            blockade_ship.blockaded_planet = target_planet
            blockade_ships.append(blockade_ship)
            self.military_ships.append(blockade_ship)
            
        self.blockade_zones[planet_name] = blockade_ships
        
        print(f"🚫 {faction_id} established blockade around {planet_name} with {num_ships} ships")
        
    def update(self):
        """Update all military operations"""
        # Update all military ships
        for ship in self.military_ships[:]:
            ship.update()
            
        # Check for blockade effectiveness
        self.update_blockades()
        
        # Evolve conflicts
        self.update_conflicts()
        
    def update_blockades(self):
        """Update blockade status and prevent access"""
        for planet_name, blockade_ships in self.blockade_zones.items():
            # Remove destroyed ships
            active_ships = [ship for ship in blockade_ships if ship in self.military_ships]
            
            if len(active_ships) < len(blockade_ships):
                self.blockade_zones[planet_name] = active_ships
                
            # If no ships left, blockade is broken
            if not active_ships:
                print(f"🔓 Blockade around {planet_name} has been broken!")
                del self.blockade_zones[planet_name]
                
    def update_conflicts(self):
        """Update ongoing conflicts"""
        for conflict in self.active_conflicts[:]:
            faction1, faction2, conflict_type = conflict
            
            # Random chance to escalate or resolve
            if random.random() < 0.001:  # Very small chance per frame
                if random.random() < 0.5:
                    self.escalate_conflict(faction1, faction2)
                else:
                    self.resolve_conflict(faction1, faction2)
                    
    def escalate_conflict(self, faction1, faction2):
        """Escalate conflict by deploying more military"""
        print(f"🔥 Conflict escalating: {faction1} vs {faction2}")
        
        # Deploy additional military ships
        for faction_id in [faction1, faction2]:
            position = Vec3(
                random.uniform(-200, 200),
                random.uniform(-50, 50),
                random.uniform(-200, 200)
            )
            
            assault_ship = MilitaryShip(faction_id, MilitaryShipType.ASSAULT, position)
            self.military_ships.append(assault_ship)
            
    def resolve_conflict(self, faction1, faction2):
        """Resolve conflict and remove blockades"""
        print(f"🕊️ Peace treaty signed: {faction1} and {faction2}")
        
        # Remove this conflict
        self.active_conflicts = [(f1, f2, t) for f1, f2, t in self.active_conflicts 
                               if not ((f1 == faction1 and f2 == faction2) or 
                                      (f1 == faction2 and f2 == faction1))]
        
        # Remove blockades between these factions
        to_remove = []
        for planet_name, blockade_ships in self.blockade_zones.items():
            if blockade_ships and blockade_ships[0].faction_id in [faction1, faction2]:
                # Check if blockading the other faction's planet
                for planet in planets:
                    if (planet.name == planet_name and 
                        hasattr(planet, 'faction_id') and 
                        planet.faction_id in [faction1, faction2]):
                        to_remove.append(planet_name)
                        break
                        
        for planet_name in to_remove:
            for ship in self.blockade_zones[planet_name]:
                if ship in self.military_ships:
                    self.military_ships.remove(ship)
                    destroy(ship)
            del self.blockade_zones[planet_name]
            
    def is_planet_blockaded(self, planet_name):
        """Check if a planet is currently blockaded"""
        return planet_name in self.blockade_zones and len(self.blockade_zones[planet_name]) > 0
        
    def can_player_access_planet(self, planet_name):
        """Check if player can access a planet (not blockaded by hostile factions)"""
        if not self.is_planet_blockaded(planet_name):
            return True
            
        # Check if blockading faction is hostile to player
        blockade_ships = self.blockade_zones[planet_name]
        if blockade_ships:
            blockading_faction = blockade_ships[0].faction_id
            player_rep = faction_system.player_reputation.get(blockading_faction, 0)
            return player_rep > -30  # Can access if not too hostile
            
        return True

# ===== ADVANCED MISSION & CONTRACT SYSTEM =====

class MissionType(Enum):
    CARGO_DELIVERY = "CARGO_DELIVERY"
    PASSENGER_TRANSPORT = "PASSENGER_TRANSPORT"
    EXPLORATION = "EXPLORATION"
    MILITARY_ESCORT = "MILITARY_ESCORT"
    MINING_OPERATION = "MINING_OPERATION"
    RESEARCH = "RESEARCH"
    DIPLOMACY = "DIPLOMACY"
    ASSASSINATION = "ASSASSINATION"
    RESCUE = "RESCUE"
    BLOCKADE_RUNNING = "BLOCKADE_RUNNING"

class ContractStatus(Enum):
    AVAILABLE = "AVAILABLE"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"

@dataclass
class Contract:
    contract_id: str
    mission_type: MissionType
    client_faction: str
    title: str
    description: str
    objectives: list
    rewards: dict  # credits, reputation, items
    penalties: dict  # reputation loss, credits lost
    time_limit: float  # seconds
    difficulty: int  # 1-5
    requirements: dict  # crew skills, ship components, reputation
    status: ContractStatus
    start_time: float
    completion_time: float = None
    
class DynamicContractSystem:
    """Generates contracts based on current galaxy state"""
    
    def __init__(self):
        self.available_contracts = []
        self.active_contracts = []
        self.completed_contracts = []
        self.last_generation = 0
        self.generation_interval = 120  # 2 minutes
        
    def update(self):
        current_time = time.time()
        
        # Generate new contracts periodically
        if current_time - self.last_generation > self.generation_interval:
            self.generate_contracts()
            self.last_generation = current_time
            
        # Update active contracts
        self.update_active_contracts()
        
        # Remove expired contracts
        self.remove_expired_contracts()
        
    def generate_contracts(self):
        """Generate contracts based on current galaxy state"""
        # Generate blockade running missions if blockades exist
        for planet_name in military_manager.blockade_zones:
            if random.random() < 0.7:  # 70% chance
                self.generate_blockade_running_contract(planet_name)
                
        # Generate escort missions for valuable cargo
        if unified_transport_system.cargo_ships:
            if random.random() < 0.3:  # 30% chance
                self.generate_escort_contract()
                
        # Generate exploration contracts for unexplored regions
        if random.random() < 0.2:  # 20% chance
            self.generate_exploration_contract()
            
        # Generate diplomatic missions based on faction relations
        if military_manager.active_conflicts:
            if random.random() < 0.4:  # 40% chance
                self.generate_diplomatic_contract()
                
        # Generate supply missions based on planet needs (use request urgency from enhanced economy)
        for planet_name, economy in enhanced_planet_economies.items():
            needs = economy.calculate_needs()
            critical_needs = [commodity for commodity, req in needs.items()
                              if getattr(req, 'urgency', None) in (UrgencyLevel.CRITICAL, UrgencyLevel.URGENT)]
            if critical_needs and random.random() < 0.5:
                self.generate_supply_contract(planet_name, critical_needs)
                
    def generate_blockade_running_contract(self, planet_name):
        """Generate contract to break through blockade"""
        blockade_ships = military_manager.blockade_zones[planet_name]
        blockading_faction = blockade_ships[0].faction_id if blockade_ships else "unknown"
        
        # Find faction that owns the planet
        planet_faction = None
        for planet in planets:
            if planet.name == planet_name and hasattr(planet, 'faction_id'):
                planet_faction = planet.faction_id
                break
                
        if not planet_faction:
            return
            
        contract = Contract(
            contract_id=f"blockade_{planet_name}_{int(time.time())}",
            mission_type=MissionType.BLOCKADE_RUNNING,
            client_faction=planet_faction,
            title=f"Break Blockade of {planet_name}",
            description=f"The {blockading_faction} has blockaded {planet_name}. "
                       f"We need supplies delivered urgently. High risk, high reward.",
            objectives=[
                f"Deliver critical supplies to {planet_name}",
                f"Avoid or defeat {len(blockade_ships)} blockade ships",
                "Return safely"
            ],
            rewards={
                'credits': 50000 + len(blockade_ships) * 10000,
                'reputation': {planet_faction: 25, blockading_faction: -15}
            },
            penalties={
                'reputation': {planet_faction: -10}
            },
            time_limit=3600,  # 1 hour
            difficulty=4,
            requirements={
                'min_reputation': {planet_faction: -20},
                'ship_components': ['SHIELDS', 'WEAPONS']
            },
            status=ContractStatus.AVAILABLE,
            start_time=time.time()
        )
        
        self.available_contracts.append(contract)
        print(f"📋 New blockade running contract: {contract.title}")
        
    def generate_escort_contract(self):
        """Generate contract to escort valuable cargo"""
        cargo_ship = random.choice(unified_transport_system.cargo_ships)
        if not hasattr(cargo_ship, 'cargo_manifest'):
            return
            
        cargo_value = sum(cargo_ship.cargo_manifest.values()) * 1000  # Estimate value
        
        contract = Contract(
            contract_id=f"escort_{cargo_ship.ship_id}_{int(time.time())}",
            mission_type=MissionType.MILITARY_ESCORT,
            client_faction='merchant_guild',
            title=f"Escort Cargo Ship {cargo_ship.ship_id}",
            description=f"Escort valuable cargo ship from {cargo_ship.origin_planet} "
                       f"to {cargo_ship.destination_planet}. Pirates are active in the area.",
            objectives=[
                f"Escort cargo ship {cargo_ship.ship_id}",
                "Defend against pirate attacks",
                "Ensure safe delivery"
            ],
            rewards={
                'credits': int(cargo_value * 0.1),  # 10% of cargo value
                'reputation': {'merchant_guild': 10}
            },
            penalties={
                'reputation': {'merchant_guild': -20}
            },
            time_limit=1800,  # 30 minutes
            difficulty=3,
            requirements={
                'ship_components': ['WEAPONS', 'SHIELDS']
            },
            status=ContractStatus.AVAILABLE,
            start_time=time.time()
        )
        
        self.available_contracts.append(contract)
        print(f"📋 New escort contract: {contract.title}")
        
    def generate_exploration_contract(self):
        """Generate exploration contract for unknown regions"""
        # Pick random coordinates far from planets
        target_pos = Vec3(
            random.uniform(-500, 500),
            random.uniform(-200, 200),
            random.uniform(-500, 500)
        )
        
        # Make sure it's far from existing planets
        min_distance = min((target_pos - planet.position).length() for planet in planets)
        if min_distance < 100:
            return  # Too close to existing planets
            
        contract = Contract(
            contract_id=f"explore_{int(time.time())}",
            mission_type=MissionType.EXPLORATION,
            client_faction='terran_federation',
            title="Deep Space Exploration",
            description=f"Explore coordinates ({target_pos.x:.0f}, {target_pos.y:.0f}, {target_pos.z:.0f}) "
                       f"and report any findings. Unknown dangers may be present.",
            objectives=[
                f"Travel to coordinates ({target_pos.x:.0f}, {target_pos.y:.0f}, {target_pos.z:.0f})",
                "Scan the area for 60 seconds",
                "Return with exploration data"
            ],
            rewards={
                'credits': 25000,
                'reputation': {'terran_federation': 15}
            },
            penalties={
                'reputation': {'terran_federation': -5}
            },
            time_limit=2400,  # 40 minutes
            difficulty=2,
            requirements={
                'ship_components': ['SENSORS', 'FUEL_TANK']
            },
            status=ContractStatus.AVAILABLE,
            start_time=time.time()
        )
        
        self.available_contracts.append(contract)
        print(f"📋 New exploration contract: {contract.title}")
        
    def generate_diplomatic_contract(self):
        """Generate diplomatic mission to resolve conflicts"""
        if not military_manager.active_conflicts:
            return
            
        faction1, faction2, conflict_type = random.choice(military_manager.active_conflicts)
        
        contract = Contract(
            contract_id=f"diplomacy_{faction1}_{faction2}_{int(time.time())}",
            mission_type=MissionType.DIPLOMACY,
            client_faction='independent',
            title=f"Peace Negotiations: {faction1} vs {faction2}",
            description=f"Mediate peace talks between {faction1} and {faction2}. "
                       f"Both sides must agree to ceasefire terms.",
            objectives=[
                f"Meet with {faction1} representatives",
                f"Meet with {faction2} representatives",
                "Negotiate ceasefire agreement",
                "Ensure both sides sign treaty"
            ],
            rewards={
                'credits': 75000,
                'reputation': {faction1: 20, faction2: 20, 'independent': 30}
            },
            penalties={
                'reputation': {faction1: -10, faction2: -10}
            },
            time_limit=7200,  # 2 hours
            difficulty=5,
            requirements={
                'min_reputation': {faction1: 0, faction2: 0},
                'crew_skills': {'leadership': 3}
            },
            status=ContractStatus.AVAILABLE,
            start_time=time.time()
        )
        
        self.available_contracts.append(contract)
        print(f"📋 New diplomatic contract: {contract.title}")
        
    def generate_supply_contract(self, planet_name, critical_commodities):
        """Generate urgent supply delivery contract"""
        commodity = random.choice(critical_commodities)
        quantity = random.randint(50, 200)
        
        # Find a planet that has this commodity
        supplier_planet = None
        for other_planet, economy in enhanced_planet_economies.items():
            if (other_planet != planet_name and 
                economy.stockpiles.get(commodity, 0) > quantity):
                supplier_planet = other_planet
                break
                
        if not supplier_planet:
            return
            
        contract = Contract(
            contract_id=f"supply_{planet_name}_{commodity}_{int(time.time())}",
            mission_type=MissionType.CARGO_DELIVERY,
            client_faction='merchant_guild',
            title=f"Emergency Supply Run: {commodity} to {planet_name}",
            description=f"{planet_name} has a critical shortage of {commodity}. "
                       f"Pick up {quantity} units from {supplier_planet} and deliver urgently.",
            objectives=[
                f"Travel to {supplier_planet}",
                f"Purchase {quantity} units of {commodity}",
                f"Deliver to {planet_name} within time limit"
            ],
            rewards={
                'credits': quantity * 100,  # Good price per unit
                'reputation': {'merchant_guild': 10}
            },
            penalties={
                'reputation': {'merchant_guild': -15}
            },
            time_limit=1800,  # 30 minutes
            difficulty=2,
            requirements={
                'cargo_capacity': quantity
            },
            status=ContractStatus.AVAILABLE,
            start_time=time.time()
        )
        
        self.available_contracts.append(contract)
        print(f"📋 New supply contract: {contract.title}")
        
    def update_active_contracts(self):
        """Update progress on active contracts"""
        current_time = time.time()
        
        for contract in self.active_contracts[:]:
            # Check for time limit expiration
            if current_time - contract.start_time > contract.time_limit:
                self.fail_contract(contract, "Time limit exceeded")
                continue
                
            # Check for objective completion (simplified)
            if contract.mission_type == MissionType.EXPLORATION:
                self.check_exploration_progress(contract)
            elif contract.mission_type == MissionType.BLOCKADE_RUNNING:
                self.check_blockade_running_progress(contract)
                
    def check_exploration_progress(self, contract):
        """Check if player has reached exploration target"""
        # Extract target coordinates from objectives
        if scene_manager.current_state != GameState.SPACE:
            return
            
        # This is simplified - in a real implementation, you'd parse the coordinates
        # and check if player is within range for the required time
        pass
        
    def check_blockade_running_progress(self, contract):
        """Check progress on blockade running mission"""
        # Check if player has successfully delivered to blockaded planet
        pass
        
    def remove_expired_contracts(self):
        """Remove expired available contracts"""
        current_time = time.time()
        self.available_contracts = [
            contract for contract in self.available_contracts
            if current_time - contract.start_time < contract.time_limit
        ]
        
    def accept_contract(self, contract_id):
        """Player accepts a contract"""
        contract = next((c for c in self.available_contracts if c.contract_id == contract_id), None)
        if not contract:
            return False
            
        # Check requirements
        if not self.check_requirements(contract):
            print(f"❌ Requirements not met for {contract.title}")
            return False
            
        # Move to active contracts
        self.available_contracts.remove(contract)
        contract.status = ContractStatus.ACCEPTED
        self.active_contracts.append(contract)
        
        print(f"✅ Accepted contract: {contract.title}")
        return True
        
    def check_requirements(self, contract):
        """Check if player meets contract requirements"""
        # Check reputation requirements
        if 'min_reputation' in contract.requirements:
            for faction_id, min_rep in contract.requirements['min_reputation'].items():
                player_rep = faction_system.player_reputation.get(faction_id, 0)
                if player_rep < min_rep:
                    return False
                    
        # Check ship component requirements
        if 'ship_components' in contract.requirements:
            for component_name in contract.requirements['ship_components']:
                component_type = getattr(ComponentType, component_name, None)
                if component_type and component_type in ship_systems.components:
                    component = ship_systems.components[component_type]
                    if component.condition == ComponentCondition.DESTROYED:
                        return False
                        
        # Check cargo capacity
        if 'cargo_capacity' in contract.requirements:
            if player_cargo.get_free_capacity() < contract.requirements['cargo_capacity']:
                return False
                
        # Check crew skills
        if 'crew_skills' in contract.requirements:
            for skill, min_level in contract.requirements['crew_skills'].items():
                crew_skill = ship_systems.get_crew_effectiveness(skill)
                if crew_skill < min_level:
                    return False
                    
        return True
        
    def complete_contract(self, contract_id):
        """Complete a contract and award rewards"""
        contract = next((c for c in self.active_contracts if c.contract_id == contract_id), None)
        if not contract:
            return False
            
        # Award rewards
        if 'credits' in contract.rewards:
            player_wallet.earn(contract.rewards['credits'])
            print(f"💰 Earned {contract.rewards['credits']} credits")
            
        if 'reputation' in contract.rewards:
            for faction_id, rep_change in contract.rewards['reputation'].items():
                faction_system.change_reputation(faction_id, rep_change)
                print(f"🤝 Reputation with {faction_id}: {rep_change:+d}")
                
        # Move to completed contracts
        self.active_contracts.remove(contract)
        contract.status = ContractStatus.COMPLETED
        contract.completion_time = time.time()
        self.completed_contracts.append(contract)
        
        print(f"🎉 Contract completed: {contract.title}")
        return True
        
    def fail_contract(self, contract, reason="Unknown"):
        """Fail a contract and apply penalties"""
        print(f"❌ Contract failed: {contract.title} ({reason})")
        
        # Apply penalties
        if 'reputation' in contract.penalties:
            for faction_id, rep_loss in contract.penalties['reputation'].items():
                faction_system.change_reputation(faction_id, rep_loss)
                print(f"💔 Reputation with {faction_id}: {rep_loss:+d}")
                
        # Move to completed contracts (as failed)
        if contract in self.active_contracts:
            self.active_contracts.remove(contract)
        elif contract in self.available_contracts:
            self.available_contracts.remove(contract)
            
        contract.status = ContractStatus.FAILED
        self.completed_contracts.append(contract)

# Create global systems
weather_system = WeatherSystem()
military_manager = FactionMilitaryManager()
dynamic_contracts = DynamicContractSystem()

# ===== TRANSPORT SYSTEM ENUMS AND DATA STRUCTURES =====

class MessageType(Enum):
    GOODS_REQUEST = "GOODS_REQUEST"
    PAYMENT = "PAYMENT"
    WAR_DECLARATION = "WAR_DECLARATION"
    PEACE_TREATY = "PEACE_TREATY"
    MILITARY_ORDERS = "MILITARY_ORDERS"
    TRADE_AGREEMENT = "TRADE_AGREEMENT"
    PIRATE_WARNING = "PIRATE_WARNING"
    NEWS_BULLETIN = "NEWS_BULLETIN"
    DIPLOMATIC_LETTER = "DIPLOMATIC_LETTER"
    INTELLIGENCE_REPORT = "INTELLIGENCE_REPORT"

class UrgencyLevel(Enum):
    LOW = "LOW"
    NORMAL = "NORMAL" 
    URGENT = "URGENT"
    CRITICAL = "CRITICAL"

class ContrabandType(Enum):
    STOLEN_GOODS = "STOLEN_GOODS"
    WEAPONS = "WEAPONS" 
    ILLEGAL_TECH = "ILLEGAL_TECH"
    NARCOTICS = "NARCOTICS"
    SLAVES = "SLAVES"

@dataclass
class GoodsRequest:
    commodity: str
    quantity: int
    max_price: float
    urgency: UrgencyLevel
    requesting_planet: str

@dataclass
class CargoIntelligence:
    ship_id: str
    origin_planet: str
    destination_planet: str
    cargo_manifest: dict
    estimated_value: float
    escort_level: str
    route_danger: float
    intel_timestamp: float

@dataclass
class PhysicalLetter:
    """Physical letter that must be delivered by ship"""
    letter_id: str
    message_type: MessageType
    sender_faction: str
    sender_planet: str
    recipient_faction: str
    recipient_planet: str
    subject: str
    content: str
    timestamp: float
    urgency: UrgencyLevel
    requires_response: bool = False
    
@dataclass 
class PlanetaryNews:
    """Information known at a specific planet"""
    news_id: str
    headline: str
    details: str
    source_planet: str
    timestamp: float
    reliability: float  # 0.0 to 1.0 - how accurate the news is
    spread_count: int   # How many times it's been passed along
    
@dataclass
class WordOfMouthInfo:
    """Information that spreads through word-of-mouth"""
    info_id: str
    info_type: str  # "war", "pirate_attack", "trade_opportunity", etc.
    content: str
    origin_planet: str
    current_accuracy: float  # Degrades as it spreads
    age_hours: float
    visited_planets: set

class PhysicalCommunicationSystem:
    """Handles all physical communication - letters, word-of-mouth, news spreading"""
    
    def __init__(self):
        self.active_letters = []  # Letters being delivered by ships
        self.planetary_mailboxes = {}  # Planet -> list of received letters
        self.planetary_news = {}  # Planet -> list of news/rumors known
        self.word_of_mouth_pool = []  # Active rumors spreading
        self.letter_counter = 0
        
    def send_letter(self, sender_planet, recipient_planet, letter_type, subject, content, urgency=UrgencyLevel.NORMAL, sender_faction="", recipient_faction=""):
        """Send a physical letter via message ship"""
        self.letter_counter += 1
        
        letter = PhysicalLetter(
            letter_id=f"LETTER-{self.letter_counter}",
            message_type=letter_type,
            sender_faction=sender_faction,
            sender_planet=getattr(sender_planet, 'name', str(sender_planet)),
            recipient_faction=recipient_faction,
            recipient_planet=getattr(recipient_planet, 'name', str(recipient_planet)),
            subject=subject,
            content=content,
            timestamp=time.time(),
            urgency=urgency,
            requires_response=(letter_type in [MessageType.WAR_DECLARATION, MessageType.PEACE_TREATY, MessageType.DIPLOMATIC_LETTER])
        )
        
        # Create message ship to deliver the letter
        message_ship = MessageShip(sender_planet, recipient_planet, letter_type, letter)
        unified_transport_system.message_ships.append(message_ship)
        
        print(f"📨 {letter_type.value} sent: {sender_planet.name} → {recipient_planet.name}")
        print(f"   Subject: {subject}")
        
        return letter
        
    def declare_war(self, declaring_faction, target_faction, declaration_text):
        """PHYSICAL WAR DECLARATION - must send letters to all faction planets"""
        print(f"⚔️ {declaring_faction} DECLARES WAR on {target_faction}!")
        print(f"📜 War declaration: {declaration_text}")
        
        # Find faction home planets and send physical letters
        faction_planets = self.find_faction_planets(target_faction)
        faction_leader_planet = self.find_faction_capital(declaring_faction)
        
        if not faction_leader_planet:
            print(f"❌ Cannot declare war - {declaring_faction} has no capital planet!")
            return False
            
        letters_sent = 0
        for planet in faction_planets:
            war_letter = self.send_letter(
                sender_planet=faction_leader_planet,
                recipient_planet=planet,
                letter_type=MessageType.WAR_DECLARATION,
                subject=f"DECLARATION OF WAR",
                content=f"By order of {declaring_faction}, we hereby declare WAR upon {target_faction}. {declaration_text}",
                urgency=UrgencyLevel.CRITICAL,
                sender_faction=declaring_faction,
                recipient_faction=target_faction
            )
            letters_sent += 1
            
        # Also notify own faction planets
        own_planets = self.find_faction_planets(declaring_faction)
        for planet in own_planets:
            if planet != faction_leader_planet:
                self.send_letter(
                    sender_planet=faction_leader_planet,
                    recipient_planet=planet,
                    letter_type=MessageType.MILITARY_ORDERS,
                    subject=f"WAR ORDERS",
                    content=f"We are now at WAR with {target_faction}. Prepare defenses and military operations.",
                    urgency=UrgencyLevel.CRITICAL,
                    sender_faction=declaring_faction,
                    recipient_faction=declaring_faction
                )
                
        print(f"📫 {letters_sent} war declaration letters dispatched by ship")
        
        # Create word-of-mouth rumor
        self.create_rumor(
            info_type="war_declaration",
            content=f"{declaring_faction} has declared war on {target_faction}",
            origin_planet=faction_leader_planet.name,
            accuracy=0.9
        )
        
        return True
        
    def find_faction_planets(self, faction_name):
        """Find all planets belonging to a faction"""
        faction_planets = []
        for planet in planets:
            if hasattr(planet, 'faction') and planet.faction == faction_name:
                faction_planets.append(planet)
            elif hasattr(planet, 'enhanced_economy') and planet.enhanced_economy:
                # Check planet type for faction association
                if faction_name.lower() in planet.planet_type.lower():
                    faction_planets.append(planet)
        return faction_planets
        
    def find_faction_capital(self, faction_name):
        """Find the capital/leader planet of a faction"""
        faction_planets = self.find_faction_planets(faction_name)
        if faction_planets:
            # Capital is usually the largest/wealthiest planet
            best_planet = max(faction_planets, key=lambda p: getattr(p.enhanced_economy, 'calculate_total_wealth', lambda: 0)() if hasattr(p, 'enhanced_economy') else 0)
            return best_planet
        return None
        
    def deliver_letter(self, letter, destination_planet):
        """Deliver a letter to a planet's mailbox"""
        planet_name = getattr(destination_planet, 'name', str(destination_planet))
        
        if planet_name not in self.planetary_mailboxes:
            self.planetary_mailboxes[planet_name] = []
            
        self.planetary_mailboxes[planet_name].append(letter)
        
        print(f"📬 Letter delivered to {planet_name}: {letter.subject}")
        
        # Process urgent letters immediately
        if letter.urgency == UrgencyLevel.CRITICAL:
            self.process_urgent_letter(letter, destination_planet)
            
        # Create word-of-mouth from letter content
        if letter.message_type in [MessageType.WAR_DECLARATION, MessageType.PIRATE_WARNING]:
            self.create_rumor(
                info_type=letter.message_type.value.lower(),
                content=letter.content,
                origin_planet=planet_name,
                accuracy=0.95  # Letters are very accurate
            )
            
    def process_urgent_letter(self, letter, planet):
        """Process urgent letters that require immediate action"""
        if letter.message_type == MessageType.WAR_DECLARATION:
            print(f"🚨 {planet.name} receives WAR DECLARATION from {letter.sender_faction}!")
            # Planet now knows about the war
            self.add_planetary_news(
                planet_name=planet.name,
                headline=f"WAR DECLARED: {letter.sender_faction} vs {letter.recipient_faction}",
                details=letter.content,
                source=letter.sender_planet,
                reliability=1.0
            )
            
        elif letter.message_type == MessageType.PIRATE_WARNING:
            print(f"⚠️ {planet.name} receives PIRATE WARNING!")
            if hasattr(planet, 'enhanced_economy'):
                planet.enhanced_economy.record_pirate_attack()
                
    def create_rumor(self, info_type, content, origin_planet, accuracy=0.8):
        """Create a word-of-mouth rumor that will spread"""
        rumor = WordOfMouthInfo(
            info_id=f"RUMOR-{int(time.time())}-{random.randint(1000, 9999)}",
            info_type=info_type,
            content=content,
            origin_planet=origin_planet,
            current_accuracy=accuracy,
            age_hours=0,
            visited_planets={origin_planet}
        )
        
        self.word_of_mouth_pool.append(rumor)
        print(f"💬 Rumor started at {origin_planet}: {content[:50]}...")
        
    def spread_word_of_mouth(self):
        """Spread rumors through trader and traveler word-of-mouth"""
        for rumor in self.word_of_mouth_pool[:]:
            # Age the rumor
            rumor.age_hours += 1/60  # Assuming 1 minute = 1 hour game time
            
            # Accuracy degrades over time and spreading
            accuracy_decay = 0.95 ** rumor.spread_count
            rumor.current_accuracy *= accuracy_decay
            
            # Remove very old or inaccurate rumors
            if rumor.age_hours > 168 or rumor.current_accuracy < 0.3:  # 1 week or <30% accuracy
                self.word_of_mouth_pool.remove(rumor)
                continue
                
            # Spread to nearby planets through cargo ships
            self.spread_rumor_via_ships(rumor)
            
    def spread_rumor_via_ships(self, rumor):
        """Spread rumors through cargo ships and travelers"""
        for ship in unified_transport_system.cargo_ships:
            if hasattr(ship, 'destination') and hasattr(ship.destination, 'name'):
                dest_name = ship.destination.name
                
                # Ships carry news from their origin
                if hasattr(ship, 'origin') and ship.origin.name in rumor.visited_planets:
                    if dest_name not in rumor.visited_planets and random.random() < 0.3:  # 30% chance
                        rumor.visited_planets.add(dest_name)
                        rumor.spread_count += 1
                        
                        # Add news to destination planet
                        self.add_planetary_news(
                            planet_name=dest_name,
                            headline=f"Traveler's Tale: {rumor.info_type.title()}",
                            details=rumor.content,
                            source=f"Trader from {ship.origin.name}",
                            reliability=rumor.current_accuracy
                        )
                        
                        print(f"💬 Rumor spread to {dest_name} via cargo ship")
                        
    def add_planetary_news(self, planet_name, headline, details, source, reliability=0.8):
        """Add news/information to a planet's knowledge"""
        if planet_name not in self.planetary_news:
            self.planetary_news[planet_name] = []
            
        news = PlanetaryNews(
            news_id=f"NEWS-{int(time.time())}-{random.randint(100, 999)}",
            headline=headline,
            details=details,
            source_planet=source,
            timestamp=time.time(),
            reliability=reliability,
            spread_count=0
        )
        
        self.planetary_news[planet_name].append(news)
        
    def get_planet_knowledge(self, planet_name):
        """Get all information (letters + news) known at a planet"""
        letters = self.planetary_mailboxes.get(planet_name, [])
        news = self.planetary_news.get(planet_name, [])
        
        return {
            'letters': letters,
            'news': news,
            'total_items': len(letters) + len(news)
        }
        
    def player_visits_planet(self, planet_name):
        """When player visits a planet, they learn local news and can spread rumors"""
        knowledge = self.get_planet_knowledge(planet_name)
        
        if knowledge['total_items'] > 0:
            print(f"📰 Local news and letters at {planet_name}:")
            
            # Show recent letters (if any)
            for letter in knowledge['letters'][-3:]:  # Last 3 letters
                age_hours = (time.time() - letter.timestamp) / 3600
                print(f"   📨 {letter.subject} (from {letter.sender_planet}, {age_hours:.1f}h ago)")
                
            # Show recent news
            for news in knowledge['news'][-3:]:  # Last 3 news items
                age_hours = (time.time() - news.timestamp) / 3600
                accuracy_str = f"{news.reliability:.0%} reliable" if news.reliability < 0.9 else "confirmed"
                print(f"   📰 {news.headline} ({accuracy_str}, {age_hours:.1f}h ago)")
                
        # Player can now spread this information to other planets they visit
        return knowledge
        
    def update(self):
        """Update the physical communication system"""
        self.spread_word_of_mouth()
        
        # Clean up old letters and news
        current_time = time.time()
        for planet_name in list(self.planetary_mailboxes.keys()):
            # Keep letters for 30 days
            self.planetary_mailboxes[planet_name] = [
                letter for letter in self.planetary_mailboxes[planet_name]
                if current_time - letter.timestamp < 2592000  # 30 days
            ]
            
        for planet_name in list(self.planetary_news.keys()):
            # Keep news for 14 days
            self.planetary_news[planet_name] = [
                news for news in self.planetary_news[planet_name]
                if current_time - news.timestamp < 1209600  # 14 days
            ]

# Global systems
market_system = MarketSystem()
player_cargo = CargoSystem(max_capacity=50)  # Start with small cargo hold
physical_communication = PhysicalCommunicationSystem()
player_wallet = PlayerWallet(starting_credits=500)
ship_systems = RealisticShipSystems()

# Initialize enhanced Pirates! features
enhanced_features = EnhancedPiratesFeatures()

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
        try:
            self.textures = {
                'right': load_texture('assets/textures/skybox_right.png'),
                'left': load_texture('assets/textures/skybox_left.png'),
                'top': load_texture('assets/textures/skybox_top.png'),
                'bottom': load_texture('assets/textures/skybox_bottom.png'),
                'front': load_texture('assets/textures/skybox_front.png'),
                'back': load_texture('assets/textures/skybox_back.png')
            }
        except:
            # Fallback if textures not found
            self.textures = {'right': 'white_cube'}
        
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

# ===== NPC SYSTEM =====
class NPC(Entity):
    def __init__(self, npc_type="trader", position=(0,0,0), **kwargs):
        super().__init__(position=position, **kwargs)
        # Procedural stick-figure: torso, head, limbs
        self._torso = Entity(parent=self, model='cube', color=color.yellow if npc_type == "trader" else color.orange, scale=(0.6, 1.2, 0.4), position=(0, 0.6, 0))
        self._head = Entity(parent=self, model='sphere', color=color.light_gray, scale=0.4, position=(0, 1.4, 0))
        # Arms
        Entity(parent=self, model='cube', color=color.gray, scale=(0.15, 0.8, 0.15), position=(0.35, 0.6, 0))
        Entity(parent=self, model='cube', color=color.gray, scale=(0.15, 0.8, 0.15), position=(-0.35, 0.6, 0))
        # Legs
        Entity(parent=self, model='cube', color=color.gray, scale=(0.18, 0.9, 0.18), position=(0.2, -0.1, 0))
        Entity(parent=self, model='cube', color=color.gray, scale=(0.18, 0.9, 0.18), position=(-0.2, -0.1, 0))
        self.npc_type = npc_type
        self.move_speed = 2
        self.move_timer = 0
        self.move_direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()
        self.dialogue = self.generate_dialogue()
        
        # Eyes on head
        Entity(parent=self._head, model='cube', color=color.black, scale=(0.07, 0.07, 0.07), position=(-0.1, 0.05, 0.18))
        Entity(parent=self._head, model='cube', color=color.black, scale=(0.07, 0.07, 0.07), position=(0.1, 0.05, 0.18))
        
        # Add name tag
        self.name_tag = Text(
            parent=self,
            text=self.get_name(),
            position=(0, 2.5, 0),
            scale=1.5,
            billboard=True,
            color=color.white
        )
    
    def get_name(self):
        trader_names = ["Bob the Trader", "Space Sally", "Cosmic Carl", "Star Merchant", "Galaxy Gil"]
        citizen_names = ["Local Citizen", "Planet Dweller", "Colonist", "Resident", "Settler"]
        
        if self.npc_type == "trader":
            return random.choice(trader_names)
        else:
            return random.choice(citizen_names)
    
    def generate_dialogue(self):
        if self.npc_type == "trader":
            return [
                "Welcome to my trading post!",
                "Best prices in the galaxy!",
                "Looking to buy or sell?",
                "Fresh supplies just arrived!",
                "Safe travels, space trader!"
            ]
        else:
            return [
                "Beautiful day on the planet!",
                "Welcome to our colony!",
                "The weather's been great lately.",
                "Enjoy your stay!",
                "This is a peaceful place."
            ]
    
    def update(self):
        if not paused and scene_manager.current_state == GameState.TOWN:
            # Purposeful wandering with bias toward role-specific building
            self.move_timer += time.dt
            if self.move_timer > random.uniform(2, 5):
                self.move_timer = 0
                self.move_direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()

            target = None
            if self.npc_type == "trader":
                target = getattr(scene_manager, 'trading_post_entity', None)
            elif self.npc_type == "guard":
                target = getattr(scene_manager, 'embassy_entity', None)
            if target is not None:
                to_target = (target.position - self.position)
                if to_target.length() > 2:
                    self.move_direction = (self.move_direction * 0.5 + to_target.normalized() * 0.5).normalized()

            new_position = self.position + self.move_direction * self.move_speed * time.dt
            if abs(new_position.x) < 30 and abs(new_position.z) < 30:
                can_move = True
                for entity in scene_manager.town_entities:
                    if entity.collider and entity is not self:
                        if (new_position - entity.position).length() < 2.5:
                            can_move = False
                            break
                if can_move:
                    self.position = new_position
                else:
                    self.move_direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()

            # Trader simple task loop: idle near trading post to indicate purpose and nudge economy
            if self.npc_type == "trader" and target is not None:
                if (self.position - target.position).length() < 6:
                    # Simulate trading chatter occasionally
                    if random.random() < 0.01:
                        print("🛒 Trader: Busy with customers…")
                    # Slightly increase local market demand signal
                    if random.random() < 0.005 and scene_manager.current_planet:
                        planet_name = scene_manager.current_planet.name
                        if planet_name in market_system.planet_economies:
                            econ = market_system.planet_economies[planet_name]
                            # Small random consumption bump to simulate foot traffic
                            commodity = random.choice(["food", "medicine", "fuel"]) if econ else "food"
                            econ.stockpiles[commodity] = max(0, econ.stockpiles.get(commodity, 0) - 1)

# Space NPCs (other ships)
class SpaceNPC(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            model='cube',
            color=color.random_color(),
            position=position,
            scale=(3, 1, 6),  # Ship-like shape
            texture='white_cube'
        )
        self.velocity = Vec3(
            random.uniform(-5, 5),
            random.uniform(-2, 2), 
            random.uniform(-5, 5)
        )
        self.ship_type = random.choice(["Trader", "Patrol", "Explorer", "Freighter"])
        
        # Add ship name
        self.name_tag = Text(
            parent=self,
            text=f"{self.ship_type} Ship",
            position=(0, 2, 0),
            scale=2,
            billboard=True,
            color=color.white
        )
    
    def update(self):
        if not paused and scene_manager.current_state == GameState.SPACE:
            # Simple movement pattern
            self.position += self.velocity * time.dt
            
            # Keep ships in a reasonable area around player
            distance_to_player = (self.position - player.position).length()
            if distance_to_player > 200:
                # Turn back toward player area
                direction_to_player = (player.position - self.position).normalized()
                self.velocity = direction_to_player * 3 + Vec3(
                    random.uniform(-2, 2),
                    random.uniform(-1, 1),
                    random.uniform(-2, 2)
                )

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
        
        # Transport system status display
        self.transport_text = Text(
            parent=camera.ui,
            text='🚢 Ships: 0',
            position=(-0.45, 0.15),
            scale=0.6,
            color=color.cyan
        )
        
        # Fuel and ship status display
        self.fuel_text = Text(
            parent=camera.ui,
            text='⛽ Fuel: 100%',
            position=(-0.45, 0.1),
            scale=0.6,
            color=color.orange
        )
        
        self.ship_status_text = Text(
            parent=camera.ui,
            text='🔧 All Systems: GOOD',
            position=(-0.45, 0.05),
            scale=0.6,
            color=color.green
        )
        
        # Weather and conflict status display
        self.weather_text = Text(
            parent=camera.ui,
            text='🌤️ Weather: Clear',
            position=(-0.45, 0.0),
            scale=0.6,
            color=color.white
        )
        
        self.conflict_text = Text(
            parent=camera.ui,
            text='⚔️ Conflicts: 0',
            position=(-0.45, -0.05),
            scale=0.6,
            color=color.orange
        )
        
        self.contracts_text = Text(
            parent=camera.ui,
            text='📋 Contracts: 0 available',
            position=(-0.45, -0.1),
            scale=0.6,
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
            if self.max_speed > 0:  # Prevent division by zero
                speed_percentage = int((self.velocity.length() / self.max_speed) * 100)
            else:
                speed_percentage = 0
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
            
            # Update transport status display
            stats = unified_transport_system.get_statistics()
            self.transport_text.text = f"🚢 Ships: {stats['total_ships']} | 🚛 Cargo: {stats['cargo_ships']} | 🏴‍☠️ Raiders: {stats['raiders']} | ⚠️ Threat: {stats['pirate_threat_level']}"
            
            # Update ship systems
            ship_systems.update(self.position)
            
            # Update speed based on ship performance
            engine_performance = ship_systems.get_engine_performance()
            if engine_performance <= 0:
                # No fuel or engine destroyed
                self.speed = 0
                self.max_speed = 0
            else:
                base_speed = 5
                self.speed = base_speed * engine_performance
                self.max_speed = int(ship_systems.get_max_speed())
                
            # Update cargo capacity
            player_cargo.max_capacity = ship_systems.get_cargo_capacity()
            
            # Update fuel display
            fuel_percentage = ship_systems.fuel_system.get_fuel_percentage()
            self.fuel_text.text = f"⛽ Fuel: {fuel_percentage:.1f}%"
            if fuel_percentage < 20:
                self.fuel_text.color = color.red
            elif fuel_percentage < 50:
                self.fuel_text.color = color.yellow
            else:
                self.fuel_text.color = color.orange
                
            # Update ship status display
            system_status = ship_systems.get_system_status()
            if system_status['damaged_components']:
                damaged_count = len(system_status['damaged_components'])
                self.ship_status_text.text = f"🔧 {damaged_count} Systems Damaged"
                self.ship_status_text.color = color.red
            else:
                self.ship_status_text.text = "🔧 All Systems: GOOD"
                self.ship_status_text.color = color.green
                
            # Update weather status
            if weather_system.active_weather:
                nearest_weather = min(weather_system.active_weather, 
                                    key=lambda w: (self.position - Vec3(*w.position)).length())
                distance = (self.position - Vec3(*nearest_weather.position)).length()
                if distance < nearest_weather.radius:
                    self.weather_text.text = f"🌩️ {nearest_weather.weather_type.value}"
                    self.weather_text.color = color.red
                else:
                    self.weather_text.text = f"🌤️ Weather: Clear"
                    self.weather_text.color = color.white
            else:
                self.weather_text.text = f"🌤️ Weather: Clear"
                self.weather_text.color = color.white
                
            # Update conflict status
            active_conflicts = len(military_manager.active_conflicts)
            total_blockades = len(military_manager.blockade_zones)
            self.conflict_text.text = f"⚔️ Conflicts: {active_conflicts} | 🚫 Blockades: {total_blockades}"
            
            # Update contracts status
            available_contracts = len(dynamic_contracts.available_contracts)
            active_contracts = len(dynamic_contracts.active_contracts)
            self.contracts_text.text = f"📋 Contracts: {available_contracts} available | {active_contracts} active"

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
        self.town_npcs = []
        self.town_controller = None
        self.space_controller = None
        self.current_planet = None  # Track which planet player is on

        # Unified on-screen interaction prompt with anti-flicker hysteresis
        self.interact_prompt = Text(
            parent=camera.ui,
            text='',
            position=(0, -0.45),
            scale=1,
            color=color.white,
            enabled=False
        )
        self._prompt_active = False
        self._prompt_target_kind = None
        self._prompt_show_threshold = 10.0  # show when closer than this
        self._prompt_hide_threshold = 12.0  # hide when farther than this
        
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
            
            # Seeded filler buildings based on current planet
            seed_val = 0
            if self.current_planet is not None and hasattr(self.current_planet, 'name'):
                seed_val = sum(ord(ch) for ch in self.current_planet.name)
            rng = random.Random(seed_val)
            for i in range(12):
                tries = 0
                while True and tries < 20:
                    x = rng.uniform(-40, 40)
                    z = rng.uniform(-40, 40)
                    if math.sqrt(x*x + z*z) > 12:
                        break
                    tries += 1
                height = rng.uniform(4, 8)
                tint = rng.uniform(-0.2, 0.3)
                themed_color = color.light_gray.tint(tint)
                building = Entity(
                    model='cube',
                    color=themed_color,
                    texture='white_cube',
                    position=(x, height/2, z),
                    scale=(4, height, 4),
                    collider='box'
                )
                self.town_entities.append(building)
            
            # Add ground first, then podium, then buildings
            self.town_entities.extend([ground, podium])
            
            # Determine faction theme color for this planet
            faction_col = color.white
            if self.current_planet is not None and hasattr(self.current_planet, 'faction_id'):
                fac_id = self.current_planet.faction_id
                if fac_id in faction_system.factions:
                    faction_col = faction_system.factions[fac_id].color

            # Add trading post (large themed building near the podium)
            trading_post = Entity(
                model='cube',
                color=color.azure.tint(-.1) * 0.5 + faction_col * 0.5,
                texture='white_cube',
                position=(10, 3, 0),  # Next to podium
                scale=(6, 6, 6),
                collider='box'
            )
            
            # Add trading post sign
            trading_sign = Text(
                parent=trading_post,
                text='TRADING POST\nPress E to Trade',
                position=(0, 0, 3.1),
                scale=100,
                color=color.white,
                billboard=True
            )
            
            self.town_entities.extend([trading_post, trading_sign])
            self.trading_post_entity = trading_post
            
            # Add shipyard (large themed building on the other side)
            shipyard = Entity(
                model='cube',
                color=color.orange.tint(-.1) * 0.5 + faction_col * 0.5,
                texture='white_cube',
                position=(-10, 3, 0),  # Opposite side from trading post
                scale=(6, 6, 6),
                collider='box'
            )
            
            # Add shipyard sign
            shipyard_sign = Text(
                parent=shipyard,
                text='SHIPYARD\nPress E for Upgrades',
                position=(0, 0, 3.1),
                scale=100,
                color=color.white,
                billboard=True
            )
            
            self.town_entities.extend([shipyard, shipyard_sign])
            self.shipyard_entity = shipyard
            
            # Add faction embassy (themed building)
            embassy = Entity(
                model='cube',
                color=faction_col.tint(-.2),
                texture='white_cube',
                position=(0, 3, -10),  # Behind podium
                scale=(6, 6, 6),
                collider='box'
            )
            
            embassy_sign = Text(
                parent=embassy,
                text='FACTION EMBASSY\nPress E for Relations',
                position=(0, 0, 3.1),
                scale=100,
                color=color.white,
                billboard=True
            )
            
            # Add crew quarters (themed building)
            crew_quarters = Entity(
                model='cube',
                color=color.lime.tint(-.2) * 0.5 + faction_col * 0.5,
                texture='white_cube',
                position=(0, 3, 10),  # In front of podium
                scale=(6, 6, 6),
                collider='box'
            )
            
            crew_sign = Text(
                parent=crew_quarters,
                text='CREW QUARTERS\nPress E for Crew',
                position=(0, 0, 3.1),
                scale=100,
                color=color.white,
                billboard=True
            )
            
            # Add mission board (themed building)
            mission_board = Entity(
                model='cube',
                color=color.gold.tint(-.2) * 0.5 + faction_col * 0.5,
                texture='white_cube',
                position=(-10, 3, -10),  # Corner position
                scale=(6, 6, 6),
                collider='box'
            )
            
            mission_sign = Text(
                parent=mission_board,
                text='MISSION BOARD\nPress E for Missions',
                position=(0, 0, 3.1),
                scale=100,
                color=color.white,
                billboard=True
            )
            
            self.town_entities.extend([embassy, embassy_sign, crew_quarters, crew_sign, mission_board, mission_sign])
            self.embassy_entity = embassy
            self.crew_quarters_entity = crew_quarters
            self.mission_board_entity = mission_board

            # Faction banners on buildings (simple quads)
            for b in [trading_post, shipyard, embassy, crew_quarters, mission_board]:
                Entity(parent=b, model='quad', color=faction_col, scale=(1.2, 1.8), position=(0, 2.5, 3.05))

            # Add some point lights near core buildings for mood
            Entity.add_to_class('PointLight', Entity)  # no-op alias for readability
            Entity(parent=trading_post, light=PointLight, y=4, color=faction_col)
            Entity(parent=shipyard, light=PointLight, y=4, color=color.orange)
            Entity(parent=embassy, light=PointLight, y=4, color=faction_col)
            
            # Add some NPCs with proper NPC class
            self.town_npcs = []
            npc_positions = [(15, 1, 15), (-15, 1, -15), (20, 1, -10), (-10, 1, 20)]
            for i, pos in enumerate(npc_positions):
                npc_type = "trader" if i == 0 else "citizen"
                npc = NPC(npc_type=npc_type, position=pos)
                self.town_npcs.append(npc)
                self.town_entities.append(npc)
            
            # Create and position the town controller on the podium
            self.town_controller = TownController()
            self.town_controller.position = Vec3(0, 1.5, 0)
    
    def switch_to_town(self):
        # Close any open UIs when switching scenes
        if 'ui_manager' in globals():
            ui_manager.hide_all()
        if self.current_state == GameState.SPACE:
            # Store and reset space controller state
            self.space_controller.disable()
            self.space_controller.status_text.enabled = False
            self.space_controller.credits_text.enabled = False
            self.space_controller.cargo_text.enabled = False
            self.space_controller.health_text.enabled = False
            self.space_controller.crew_text.enabled = False
            self.space_controller.time_text.enabled = False
            self.space_controller.transport_text.enabled = False
            self.space_controller.fuel_text.enabled = False
            self.space_controller.ship_status_text.enabled = False
            
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
        # Close any open UIs when switching scenes
        if 'ui_manager' in globals():
            ui_manager.hide_all()
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
            self.space_controller.transport_text.enabled = True
            self.space_controller.fuel_text.enabled = True
            self.space_controller.ship_status_text.enabled = True
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
        # Add landing detection radius (use scalar X component of scale)
        self.landing_radius = float(self.scale.x) * 2
        # Add name for the planet
        self.name = f"{planet_data['name_prefix']}-{random.randint(100, 999)}"
        
        # Initialize enhanced economy
        self.enhanced_economy = None  # Will be initialized later
        
        # Fuel station availability (some planets have fuel)
        self.has_fuel_station = random.random() < 0.7  # 70% of planets have fuel
        self.fuel_price = random.randint(5, 15)  # Credits per fuel unit
        
        # Generate market for this planet (keep for compatibility)
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

# Landing prompt UI (now managed via UIManager)
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

# Landing prompt managed state
landing_prompt_active = False
nearby_planet = None
landing_show_threshold = 35.0
landing_hide_threshold = 40.0

# ===== TRANSPORT SHIP CLASSES =====

class TransportShip(Entity):
    """Base class for all transport ships"""
    
    def __init__(self, origin_planet, destination_planet, ship_type, **kwargs):
        # Get position from planet objects
        if hasattr(origin_planet, 'position'):
            start_pos = origin_planet.position + Vec3(random.uniform(-10, 10), random.uniform(-5, 5), random.uniform(-10, 10))
        else:
            start_pos = Vec3(0, 0, 0)
            
        # Procedural ship geometry (basic kitbash): hull + nacelles + cargo pods
        super().__init__(position=start_pos, **kwargs)
        self.model = None
        hull = Entity(parent=self, model='capsule', scale=(0.6, 0.6, 2.2), color=color.light_gray)
        # Side nacelles
        Entity(parent=self, model='cube', scale=(0.2, 0.2, 0.8), position=(0.6, 0, -0.3), color=color.gray)
        Entity(parent=self, model='cube', scale=(0.2, 0.2, 0.8), position=(-0.6, 0, -0.3), color=color.gray)
        # Cargo pods for cargo ships
        if getattr(self, 'ship_type', '') in ("CARGO", "PAYMENT"):
            Entity(parent=self, model='cube', scale=(0.5, 0.5, 0.5), position=(0.0, -0.5, -0.2), color=color.orange if self.ship_type=="CARGO" else color.yellow)
        
        self.origin = origin_planet
        self.destination = destination_planet
        self.ship_type = ship_type
        self.delivered = False
        self.encounter_triggered = False
        # Visual trail (simple breadcrumbs)
        self._trail_timer = 0.0
        self._trail_nodes = []
        
    def update(self):
        if self.delivered:
            return
            
        # Move along waypoints if available, else direct to destination
        if hasattr(self.destination, 'position'):
            target_pos = None
            if hasattr(self, 'waypoints') and self.waypoints:
                # Peek next waypoint
                target_pos = self.waypoints[0]
                if (self.position - target_pos).length() < 6:
                    # Consume waypoint
                    self.waypoints.pop(0)
                    target_pos = self.waypoints[0] if self.waypoints else self.destination.position
            else:
                target_pos = self.destination.position

            direction = (target_pos - self.position).normalized()
            speed = getattr(self, 'speed', 10.0)
            # Expose target for escorts/AI consumers
            self.current_target_pos = target_pos
            self.position += direction * speed * time.dt

            # Check if arrived at final destination
            if (self.position - self.destination.position).length() < 5:
                self.on_arrival()
                
        # Check for player encounters
        self.check_player_encounter()

        # LOD: reduce child visuals when far from player
        try:
            if scene_manager.current_state == GameState.SPACE and scene_manager.space_controller:
                d_player = (self.position - scene_manager.space_controller.position).length()
                # If very far, disable children for performance
                for child in self.children:
                    child.enabled = d_player < 400
        except Exception:
            pass

        # Drop simple trail nodes at intervals
        self._trail_timer += time.dt
        if self._trail_timer > 0.6:
            self._trail_timer = 0.0
            try:
                node = Entity(model='sphere', scale=0.2, color=color.white66, position=self.position)
                self._trail_nodes.append(node)
                if len(self._trail_nodes) > 25:
                    old = self._trail_nodes.pop(0)
                    destroy(old)
            except Exception:
                pass
                
    def check_player_encounter(self):
        """Check if player is near this ship"""
        if hasattr(scene_manager, 'space_controller') and scene_manager.space_controller:
            # Guard against empty/destroyed nodepaths
            try:
                player_pos = scene_manager.space_controller.position
                _ = self.position  # access to ensure node exists
            except Exception:
                return
            try:
                distance = (self.position - player_pos).length()
            except Exception:
                return
            if distance < 30 and not self.encounter_triggered:
                self.trigger_player_encounter()
                
    def trigger_player_encounter(self):
        """Trigger encounter with player"""
        self.encounter_triggered = True
        encounter_text = f"\n🚢 SHIP ENCOUNTER!\n"
        encounter_text += f"Ship Type: {self.ship_type}\n"
        encounter_text += f"Origin: {getattr(self.origin, 'name', 'Unknown')}\n"
        encounter_text += f"Destination: {getattr(self.destination, 'name', 'Unknown')}\n"
        
        if hasattr(self, 'cargo'):
            encounter_text += f"Cargo: {self.get_cargo_description()}\n"
        if hasattr(self, 'contract_value'):
            encounter_text += f"Value: {self.contract_value} credits\n"
            
        print(encounter_text)
        
    def on_arrival(self):
        """Override in subclasses"""
        self.delivered = True
        # Removal is handled by transport manager after update loop to avoid mid-frame node issues

class MessageShip(TransportShip):
    """Ship carrying physical letters between planets"""
    
    def __init__(self, origin_planet, destination_planet, message_type, payload):
        super().__init__(
            origin_planet, 
            destination_planet, 
            "MESSAGE",
            color=color.cyan,
            scale=(0.5, 0.2, 0.8)
        )
        
        self.message_type = message_type
        self.payload = payload  # Should be a PhysicalLetter object
        self.speed = 15.0  # Faster than cargo ships for urgent messages
        
        # Display letter type
        if isinstance(payload, PhysicalLetter):
            print(f"📨 Letter courier launched: {getattr(origin_planet, 'name', 'Unknown')} → {getattr(destination_planet, 'name', 'Unknown')}")
            print(f"   📜 Carrying: {payload.subject}")
        else:
            print(f"📨 Message ship launched: {getattr(origin_planet, 'name', 'Unknown')} → {getattr(destination_planet, 'name', 'Unknown')}")
        
    def on_arrival(self):
        """Deliver letter to destination planet's mailbox"""
        destination_name = getattr(self.destination, 'name', 'Unknown')
        
        # Handle physical letters through the communication system
        if isinstance(self.payload, PhysicalLetter):
            physical_communication.deliver_letter(self.payload, self.destination)
        else:
            # Fallback for old message types
            if hasattr(self.destination, 'enhanced_economy') and self.destination.enhanced_economy:
                self.destination.enhanced_economy.receive_message(self.message_type, self.payload)
            print(f"📬 Message delivered to {destination_name}")
            
        super().on_arrival()

class CargoShip(TransportShip):
    """Ship carrying cargo between planets"""
    
    def __init__(self, origin_planet, destination_planet, cargo_manifest):
        super().__init__(
            origin_planet,
            destination_planet, 
            "CARGO",
            color=color.orange,
            scale=(1.2, 0.6, 2.0)
        )
        
        self.cargo = cargo_manifest.copy()
        self.speed = 8.0
        self.contract_value = self.calculate_cargo_value()
        self.shields = random.randint(20, 40)
        # Convoy waypoints
        if hasattr(origin_planet, 'position') and hasattr(destination_planet, 'position'):
            self.waypoints = compute_trade_waypoints(origin_planet.position, destination_planet.position, segments=6)
        else:
            self.waypoints = []
        
        print(f"🚛 Cargo ship launched: {getattr(origin_planet, 'name', 'Unknown')} → {getattr(destination_planet, 'name', 'Unknown')}")
        print(f"   Cargo: {self.get_cargo_description()}")
        
    def calculate_cargo_value(self):
        """Calculate total value of cargo"""
        base_prices = {
            "food": 10, "minerals": 25, "technology": 50,
            "luxury_goods": 75, "medicine": 40, "weapons": 60,
            "fuel": 15, "spices": 35
        }
        
        total_value = 0
        for commodity, quantity in self.cargo.items():
            base_price = base_prices.get(commodity, 20)
            total_value += base_price * quantity
            
        return int(total_value)
    
    def get_cargo_description(self):
        """Human readable cargo description"""
        if not self.cargo:
            return "Empty"
        items = []
        for commodity, quantity in self.cargo.items():
            items.append(f"{quantity} {commodity.replace('_', ' ')}")
        return ", ".join(items)
    
    def on_arrival(self):
        """Deliver cargo and spawn payment ship"""
        # Add cargo to destination
        if hasattr(self.destination, 'enhanced_economy') and self.destination.enhanced_economy:
            for commodity, quantity in self.cargo.items():
                current = self.destination.enhanced_economy.stockpiles.get(commodity, 0)
                self.destination.enhanced_economy.stockpiles[commodity] = current + quantity
                
        print(f"✅ Cargo delivered to {getattr(self.destination, 'name', 'Unknown')}: {self.get_cargo_description()}")
        # Notify contract registry for payment leg
        if hasattr(self, 'contract_id'):
            contract_registry.cargo_delivered(self.contract_id)
        
        # Legacy fallback: spawn payment ship based on value if no contract id
        elif hasattr(self, 'contract_value') and self.contract_value > 0:
            payment_ship = PaymentShip(self.destination, self.origin, self.contract_value)
            if 'unified_transport_system' in globals():
                unified_transport_system.payment_ships.append(payment_ship)
        
        super().on_arrival()

class PaymentShip(TransportShip):
    """Ship carrying payment/credits"""
    
    def __init__(self, origin_planet, destination_planet, credits):
        super().__init__(
            origin_planet,
            destination_planet,
            "PAYMENT", 
            color=color.yellow,
            scale=(0.8, 0.4, 1.0)
        )
        
        self.credits = credits
        self.speed = 12.0
        
        print(f"💰 Payment ship launched: {getattr(origin_planet, 'name', 'Unknown')} → {getattr(destination_planet, 'name', 'Unknown')} ({credits} credits)")
        
    def on_arrival(self):
        """Deliver payment"""
        if hasattr(self.destination, 'enhanced_economy') and self.destination.enhanced_economy:
            self.destination.enhanced_economy.credits += self.credits
            
        print(f"💳 Payment delivered to {getattr(self.destination, 'name', 'Unknown')}: {self.credits} credits")
        # Notify contract completion
        if hasattr(self, 'contract_id'):
            contract_registry.payment_delivered(self.contract_id)
        super().on_arrival()

class PirateRaider(TransportShip):
    """Pirate ship that hunts cargo ships based on intelligence"""
    
    def __init__(self, pirate_base, target_intelligence=None):
        super().__init__(
            pirate_base,
            None,  # No fixed destination - hunting mode
            "RAIDER",
            color=color.dark_gray,
            scale=(1.0, 0.5, 1.8)
        )
        
        self.pirate_base = pirate_base
        self.target_intelligence = target_intelligence
        self.hunting_mode = True
        self.speed = 10.0
        self.weapons_rating = random.randint(20, 50)
        self.crew_size = random.randint(4, 12)
        self.cargo_stolen = {}
        self.raid_range = 200
        
        if target_intelligence:
            print(f"🏴‍☠️ Pirate raider launched from {getattr(pirate_base, 'name', 'Unknown Base')}")
            print(f"   Target: {target_intelligence.cargo_manifest} worth {target_intelligence.estimated_value} credits")
        else:
            print(f"🏴‍☠️ Pirate patrol launched from {getattr(pirate_base, 'name', 'Unknown Base')}")
            
    def update(self):
        """Hunt for cargo ships or return to base"""
        if self.delivered:
            return
            
        if self.hunting_mode:
            self.hunt_cargo_ships()
        else:
            # Return to base with stolen goods
            if hasattr(self.pirate_base, 'position'):
                direction = (self.pirate_base.position - self.position).normalized()
                self.position += direction * self.speed * time.dt
                
                if (self.position - self.pirate_base.position).length() < 5:
                    self.return_to_base()
                    
    def hunt_cargo_ships(self):
        """Hunt for cargo ships to raid"""
        # Look for cargo ships in range
        if 'unified_transport_system' in globals():
            for cargo_ship in unified_transport_system.cargo_ships:
                if not hasattr(cargo_ship, 'position'):
                    continue
                    
                distance = (self.position - cargo_ship.position).length()
                
                if distance < self.raid_range and self.should_attack_cargo_ship(cargo_ship):
                    self.attack_cargo_ship(cargo_ship)
                    return
                    
        # If no targets found, patrol randomly
        self.patrol_movement()
        
    def should_attack_cargo_ship(self, cargo_ship):
        """Decide whether to attack this cargo ship"""
        if self.target_intelligence:
            intel = self.target_intelligence
            if hasattr(cargo_ship, 'cargo'):
                for commodity in intel.cargo_manifest:
                    if commodity in cargo_ship.cargo:
                        return True
                        
        if hasattr(cargo_ship, 'contract_value'):
            return cargo_ship.contract_value > 500
            
        return False
    
    def attack_cargo_ship(self, cargo_ship):
        """Attack and rob cargo ship"""
        print(f"🏴‍☠️ PIRATE ATTACK!")
        print(f"Raider attacking cargo ship: {cargo_ship.get_cargo_description()}")
        
        attack_strength = self.weapons_rating + (self.crew_size * 2)
        defense_strength = getattr(cargo_ship, 'shields', 25) + random.randint(10, 30)
        
        success_chance = attack_strength / (attack_strength + defense_strength)
        
        if random.random() < success_chance:
            # Successful raid
            self.cargo_stolen = cargo_ship.cargo.copy()
            stolen_value = cargo_ship.contract_value
            
            print(f"💀 Pirate raid successful! Stolen: {cargo_ship.get_cargo_description()}")
            print(f"   Value: {stolen_value} credits")
            
            # LOGICAL CORRECTION: Notify destination planet of attack
            if hasattr(cargo_ship, 'destination') and hasattr(cargo_ship.destination, 'enhanced_economy'):
                cargo_ship.destination.enhanced_economy.record_pirate_attack()
                
            # LOGICAL CORRECTION: Increase regional pirate threat
            self.increase_regional_threat(cargo_ship)
            
            # Remove the cargo ship and settle contract consequences
            if 'unified_transport_system' in globals() and cargo_ship in unified_transport_system.cargo_ships:
                unified_transport_system.cargo_ships.remove(cargo_ship)
                if hasattr(cargo_ship, 'contract_id'):
                    contract_registry.cargo_lost(cargo_ship.contract_id)
                destroy(cargo_ship)
                
            # Return to base with stolen goods
            self.hunting_mode = False
            
            # Share intelligence with other pirates
            self.share_intelligence(cargo_ship)
            
        else:
            print(f"⚔️ Cargo ship fought off pirate attack!")
            # Even failed attacks increase threat
            if hasattr(cargo_ship, 'destination') and hasattr(cargo_ship.destination, 'enhanced_economy'):
                if random.random() < 0.3:  # 30% chance failed attack is reported
                    cargo_ship.destination.enhanced_economy.record_pirate_attack()
            self.hunting_mode = False
            
    def increase_regional_threat(self, cargo_ship):
        """LOGICAL: Successful pirate attacks increase regional threat"""
        # PHYSICAL COMMUNICATION: Send warning letters to nearby planets
        if hasattr(cargo_ship, 'position') and hasattr(cargo_ship, 'destination'):
            attack_location = cargo_ship.position
            victim_planet = cargo_ship.destination
            
            # Send physical pirate warning letters to nearby planets
            for planet in planets:
                if hasattr(planet, 'enhanced_economy') and planet.enhanced_economy:
                    distance = (planet.position - attack_location).length() if hasattr(planet, 'position') else 1000
                    if distance < 300 and planet != victim_planet:  # Within threat radius, not victim
                        # Send pirate warning letter
                        if random.random() < 0.4:  # 40% chance nearby planets send warnings
                            physical_communication.send_letter(
                                sender_planet=victim_planet,
                                recipient_planet=planet,
                                letter_type=MessageType.PIRATE_WARNING,
                                subject="PIRATE ATTACK WARNING",
                                content=f"Pirates attacked cargo ship near {victim_planet.name}. Exercise extreme caution in this sector.",
                                urgency=UrgencyLevel.URGENT
                            )
                            
            # Create word-of-mouth rumor about the attack
            physical_communication.create_rumor(
                info_type="pirate_attack",
                content=f"Pirates attacked cargo ship bound for {victim_planet.name}",
                origin_planet=victim_planet.name,
                accuracy=0.8
            )
            
    def patrol_movement(self):
        """Random patrol movement when no targets found"""
        random_offset = Vec3(
            random.uniform(-5, 5),
            random.uniform(-5, 5), 
            random.uniform(-5, 5)
        )
        self.position += random_offset * time.dt
        
    def share_intelligence(self, cargo_ship):
        """Share intelligence about cargo routes with other pirate bases"""
        intelligence = CargoIntelligence(
            ship_id=f"CARGO-{time.time()}",
            origin_planet=getattr(cargo_ship.origin, 'name', 'Unknown'),
            destination_planet=getattr(cargo_ship.destination, 'name', 'Unknown'),
            cargo_manifest=cargo_ship.cargo.copy(),
            estimated_value=cargo_ship.contract_value,
            escort_level="NONE",
            route_danger=0.3,
            intel_timestamp=time.time()
        )
        
        # Send intelligence to other pirate bases
        if 'planets' in globals():
            for planet in planets:
                if (hasattr(planet, 'enhanced_economy') and planet.enhanced_economy and 
                    hasattr(planet.enhanced_economy, 'intelligence_cache')):
                    if (self.position - planet.position).length() < 500:
                        planet.enhanced_economy.receive_intelligence(intelligence)
                
    def return_to_base(self):
        """Return stolen goods to pirate base"""
        self.delivered = True
        
        if hasattr(self.pirate_base, 'enhanced_economy') and self.pirate_base.enhanced_economy:
            self.pirate_base.enhanced_economy.receive_stolen_goods(self.cargo_stolen)
            
        print(f"🏴‍☠️ Raider returned to {getattr(self.pirate_base, 'name', 'Unknown Base')}")
        print(f"   Delivered stolen goods: {self.get_stolen_cargo_description()}")
        
        destroy(self)
        
    def get_stolen_cargo_description(self):
        """Get description of stolen cargo"""
        if not self.cargo_stolen:
            return "Nothing"
        items = []
        for commodity, quantity in self.cargo_stolen.items():
            items.append(f"{quantity} {commodity.replace('_', ' ')}")
        return ", ".join(items)

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
        """Run daily economic simulation for all planets"""
        print(f"\n🌍 Day {self.game_day} Economic Report:")
        
        # Run daily updates for all planet economies  
        market_system.daily_economic_update()
        
        # Random events that can affect supply chains
        if random.random() < 0.1:  # 10% chance daily
            self.random_economic_event()
            
    def random_economic_event(self):
        """Generate random economic events"""
        if not market_system.planet_economies:
            return
            
        event_type = random.choice(['shortage', 'surplus', 'blockade_start', 'blockade_end'])
        planet_name = random.choice(list(market_system.planet_economies.keys()))
        
        if event_type == 'shortage':
            commodity = random.choice(['food', 'medicine', 'fuel'])
            economy = market_system.planet_economies[planet_name]
            # Reduce stockpile by 50%
            current = economy.stockpiles.get(commodity, 0)
            economy.stockpiles[commodity] = current // 2
            print(f"⚠️ {planet_name} reports {commodity} shortage due to supply chain disruption!")
            
        elif event_type == 'surplus':
            commodity = random.choice(['minerals', 'luxury_goods', 'technology'])
            economy = market_system.planet_economies[planet_name]
            # Increase stockpile
            bonus = random.randint(100, 500)
            economy.stockpiles[commodity] = economy.stockpiles.get(commodity, 0) + bonus
            print(f"📈 {planet_name} discovers new {commodity} deposits! Market flooded!")
            
        elif event_type == 'blockade_start' and random.random() < 0.3:  # 30% chance
            if not market_system.planet_economies[planet_name].blockaded:
                market_system.set_blockade(planet_name, True)
                
        elif event_type == 'blockade_end':
            if market_system.planet_economies[planet_name].blockaded:
                market_system.set_blockade(planet_name, False)

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

# ===== ENHANCED PLANET ECONOMIES =====

class EnhancedPlanetEconomy:
    """Enhanced planet economy with realistic transport mechanics"""
    
    def __init__(self, planet_name, planet_type, planet_object):
        self.planet_name = planet_name
        self.planet_type = planet_type
        self.planet_object = planet_object
        
        # Enhanced stockpile system
        self.stockpiles = {}
        self.daily_consumption = {}
        self.daily_production = {}
        self.outgoing_requests = {}
        self.expected_deliveries = {}
        self.credits = random.randint(10000, 50000)
        
        # Transport timing
        self.last_procurement_check = 0
        self.procurement_interval = 45  # Check every 45 seconds
        
        # Connect to existing market system
        if planet_name in market_system.planet_economies:
            old_economy = market_system.planet_economies[planet_name]
            self.stockpiles = old_economy.stockpiles.copy()
            self.daily_consumption = old_economy.daily_consumption.copy()
            self.daily_production = old_economy.daily_production.copy()
        else:
            self.initialize_economy()
            
    def initialize_economy(self):
        """Set up production/consumption based on planet type"""
        economy_templates = {
            "agricultural": {
                "production": {"food": 200, "spices": 50},
                "consumption": {"technology": 30, "minerals": 40, "luxury_goods": 20},
                "stockpiles": {"food": 2000, "spices": 500, "technology": 100, "minerals": 200, "luxury_goods": 50}
            },
            "industrial": {
                "production": {"technology": 100, "weapons": 40, "medicine": 30}, 
                "consumption": {"food": 180, "fuel": 60, "minerals": 80},
                "stockpiles": {"technology": 800, "weapons": 300, "medicine": 400, "food": 600, "fuel": 300, "minerals": 400}
            },
            "mining": {
                "production": {"minerals": 300, "fuel": 100},
                "consumption": {"food": 150, "technology": 50, "medicine": 25},
                "stockpiles": {"minerals": 3000, "fuel": 800, "food": 500, "technology": 200, "medicine": 100}
            },
            "tech": {
                "production": {"technology": 120, "medicine": 60, "weapons": 40},
                "consumption": {"food": 120, "minerals": 100, "fuel": 40},
                "stockpiles": {"technology": 1200, "medicine": 600, "weapons": 400, "food": 400, "minerals": 500, "fuel": 200}
            },
            "luxury": {
                "production": {"luxury_goods": 80, "spices": 40},
                "consumption": {"food": 100, "technology": 50, "minerals": 60},
                "stockpiles": {"luxury_goods": 1500, "spices": 800, "food": 300, "technology": 250, "minerals": 300}
            }
        }
        
        template = economy_templates.get(self.planet_type, economy_templates["agricultural"])
        
        self.daily_production = template["production"].copy()
        self.daily_consumption = template["consumption"].copy()
        self.stockpiles = template["stockpiles"].copy()
        
        # Ensure all commodities exist
        for commodity in ["food", "minerals", "technology", "luxury_goods", "medicine", "weapons", "fuel", "spices"]:
            if commodity not in self.stockpiles:
                self.stockpiles[commodity] = 0
                
    def update(self):
        """Update economy and handle transport needs"""
        current_time = time.time()
        
        # Process production and consumption
        for commodity, amount in self.daily_production.items():
            per_second = amount / 300.0  # 1 game day = 5 minutes = 300 seconds
            self.stockpiles[commodity] = self.stockpiles.get(commodity, 0) + (per_second * time.dt)
            
        for commodity, amount in self.daily_consumption.items():
            per_second = amount / 300.0
            current_stock = self.stockpiles.get(commodity, 0)
            consumption = min(per_second * time.dt, current_stock)
            self.stockpiles[commodity] = current_stock - consumption
            
        # Check for procurement needs
        if current_time - self.last_procurement_check > self.procurement_interval:
            self.assess_and_send_requests()
            self.last_procurement_check = current_time
            
        # Update manufacturing processes
        crew_effectiveness = 50  # Default effectiveness if no crew system
        enhanced_manufacturing.update_manufacturing(self.planet_name, time.dt, crew_effectiveness, self.stockpiles)
        
        # Auto-start manufacturing based on available materials
        self.auto_start_manufacturing()
            
    def assess_and_send_requests(self):
        """Assess needs and send procurement messages + LOGICAL ECONOMIC CORRECTIONS"""
        needs = self.calculate_needs()
        
        for commodity, request in needs.items():
            # Don't spam requests
            if commodity not in self.outgoing_requests or time.time() - self.outgoing_requests[commodity] > 120:
                self.send_procurement_message(request)
                self.outgoing_requests[commodity] = time.time()
                
                # LOGICAL CORRECTION: High prices attract more traders
                if request.max_price > 100:  # High-value commodity
                    self.spawn_additional_traders(request)
                    
    def spawn_additional_traders(self, high_value_request):
        """LOGICAL: High prices attract additional independent traders"""
        # Calculate profit potential
        base_prices = {"food": 10, "technology": 50, "minerals": 25, "luxury_goods": 75, 
                      "medicine": 40, "weapons": 60, "fuel": 15, "spices": 35}
        base_price = base_prices.get(high_value_request.commodity, 20)
        
        profit_margin = (high_value_request.max_price - base_price) / base_price if base_price > 0 else 0
        
        # More traders attracted by higher profit margins
        if profit_margin > 2.0:  # 200%+ profit
            trader_spawn_chance = 0.8
        elif profit_margin > 1.0:  # 100%+ profit
            trader_spawn_chance = 0.5
        elif profit_margin > 0.5:  # 50%+ profit
            trader_spawn_chance = 0.3
        else:
            trader_spawn_chance = 0.1
            
        if random.random() < trader_spawn_chance:
            # Spawn independent trader
            suppliers = self.find_suppliers(high_value_request.commodity)
            if suppliers:
                origin_planet = random.choice(suppliers)
                quantity = min(high_value_request.quantity, 10)
                
                # Create profitable cargo run
                cargo_ship = CargoShip(
                    origin_planet=origin_planet,
                    destination_planet=self.planet_object,
                    cargo_manifest={high_value_request.commodity: quantity}
                )
                cargo_ship.profit_motivated = True  # Mark as profit-seeking
                cargo_ship.expected_profit = profit_margin * quantity * base_price
                
                if 'unified_transport_system' in globals():
                    unified_transport_system.cargo_ships.append(cargo_ship)
                    
                print(f"💰 High prices attract trader: {quantity} {high_value_request.commodity} -> {self.planet_name}")
                print(f"   Expected profit: {cargo_ship.expected_profit:.0f} credits ({profit_margin:.1%} margin)")
                
    def calculate_needs(self):
        """Calculate what goods this planet needs"""
        needs = {}
        
        for commodity, consumption in self.daily_consumption.items():
            if consumption <= 0:
                continue
                
            current_stock = self.stockpiles.get(commodity, 0)
            expected = self.expected_deliveries.get(commodity, 0)
            effective_stock = current_stock + expected
            
            days_remaining = effective_stock / consumption if consumption > 0 else float('inf')
            
            if days_remaining < 30:  # Less than 30 days supply
                urgency = self.determine_urgency(days_remaining)
                quantity_needed = int(consumption * 60 - effective_stock)  # Target 60 days supply
                
                if quantity_needed > 0:
                    needs[commodity] = GoodsRequest(
                        commodity=commodity,
                        quantity=quantity_needed,
                        max_price=self.calculate_max_price(commodity, urgency),
                        urgency=urgency,
                        requesting_planet=self.planet_name
                    )
                    
        return needs
    
    def determine_urgency(self, days_remaining):
        """Determine urgency based on remaining supply"""
        if days_remaining < 7:
            return UrgencyLevel.CRITICAL
        elif days_remaining < 15:
            return UrgencyLevel.URGENT
        elif days_remaining < 25:
            return UrgencyLevel.NORMAL
        else:
            return UrgencyLevel.LOW
            
    def calculate_max_price(self, commodity, urgency):
        """Calculate max price willing to pay"""
        base_prices = {
            "food": 10, "minerals": 25, "technology": 50,
            "luxury_goods": 75, "medicine": 40, "weapons": 60,
            "fuel": 15, "spices": 35
        }
        
        base_price = base_prices.get(commodity, 20)
        urgency_multipliers = {
            UrgencyLevel.LOW: 1.0,
            UrgencyLevel.NORMAL: 1.2,
            UrgencyLevel.URGENT: 1.5,
            UrgencyLevel.CRITICAL: 2.0
        }
        
        return base_price * urgency_multipliers[urgency]
    
    def send_procurement_message(self, request):
        """Send procurement message to suppliers"""
        suppliers = self.find_suppliers(request.commodity)
        
        for supplier_planet in suppliers:
            if supplier_planet.name != self.planet_name:
                message_ship = MessageShip(
                    self.planet_object,
                    supplier_planet,
                    MessageType.GOODS_REQUEST,
                    request
                )
                unified_transport_system.message_ships.append(message_ship)
                
    def find_suppliers(self, commodity):
        """Find planets that produce this commodity"""
        suppliers = []
        
        for planet in planets:
            if hasattr(planet, 'enhanced_economy') and planet.enhanced_economy:
                production = planet.enhanced_economy.daily_production.get(commodity, 0)
                consumption = planet.enhanced_economy.daily_consumption.get(commodity, 0)
                if production > consumption:  # Has surplus
                    suppliers.append(planet)
                    
        return suppliers
    
    def receive_message(self, message_type, payload):
        """Process incoming message"""
        if message_type == MessageType.GOODS_REQUEST:
            self.handle_goods_request(payload)
    
    def calculate_min_acceptable_price(self, commodity):
        """Supplier's minimum acceptable price per unit based on base price and local surplus."""
        base_prices = {
            "food": 10, "minerals": 25, "technology": 50,
            "luxury_goods": 75, "medicine": 40, "weapons": 60,
            "fuel": 15, "spices": 35
        }
        base = base_prices.get(commodity, 20)
        production = self.daily_production.get(commodity, 0)
        consumption = self.daily_consumption.get(commodity, 0)
        surplus = production - consumption
        if surplus > 0:
            return base * 0.9
        elif surplus < 0:
            return base * 1.2
        return base
    
    def estimate_shipping_cost_per_unit(self, origin_planet, destination_planet):
        """Rough per-unit shipping cost proportional to distance."""
        try:
            distance = (origin_planet.position - destination_planet.position).length()
        except Exception:
            distance = 100.0
        return max(0.05 * (distance / 100.0), 0.1)
            
    def handle_goods_request(self, request):
        """Evaluate and respond to goods request"""
        commodity = request.commodity
        quantity = request.quantity
        
        # Check if we can supply
        production = self.daily_production.get(commodity, 0)
        consumption = self.daily_consumption.get(commodity, 0)
        current_stock = self.stockpiles.get(commodity, 0)
        
        surplus = production - consumption
        available_stock = max(0, current_stock - (consumption * 30))  # Keep 30 days reserve
        
        can_supply = min(quantity, available_stock)
        
        if can_supply > 0 and surplus > 0:
            # Find requesting planet
            requesting_planet = None
            for planet in planets:
                if planet.name == request.requesting_planet:
                    requesting_planet = planet
                    break
                    
            if requesting_planet and hasattr(requesting_planet, 'enhanced_economy'):
                # Pricing logic: ensure destination offers enough to cover supplier min + shipping + margin
                unit_min = self.calculate_min_acceptable_price(commodity)
                unit_ship = self.estimate_shipping_cost_per_unit(self.planet_object, requesting_planet)
                unit_needed = unit_min + unit_ship + (unit_min * 0.10)
                if request.max_price < unit_needed:
                    return
                total_cost = int(unit_needed * can_supply)
                dest_econ = requesting_planet.enhanced_economy
                if dest_econ.credits < total_cost:
                    return
                # Reserve credits at destination (escrow-like)
                dest_econ.credits -= total_cost
                
                # Create cargo ship with manifest and register contract
                cargo_manifest = {commodity: can_supply}
                cargo_ship = CargoShip(
                    self.planet_object,
                    requesting_planet,
                    cargo_manifest
                )
                cargo_ship.contract_id = contract_registry.register_contract(
                    origin_planet=self.planet_object,
                    dest_planet=requesting_planet,
                    commodity=commodity,
                    quantity=can_supply,
                    unit_price=unit_needed,
                    total_cost=total_cost
                )
                unified_transport_system.cargo_ships.append(cargo_ship)
                # If destination has close allies, spawn escorts for high-value shipments
                if total_cost > 5000 and hasattr(requesting_planet, 'faction_id'):
                    # Find friendly faction (destination's own faction for now)
                    friendly_faction = requesting_planet.faction_id
                    unified_transport_system.spawn_escorts_for_cargo(cargo_ship, friendly_faction, num_escorts=2)
                
                # Remove goods and track expected delivery
                self.stockpiles[commodity] -= can_supply
                current_expected = dest_econ.expected_deliveries.get(commodity, 0)
                dest_econ.expected_deliveries[commodity] = current_expected + can_supply
                
                # Payment ship returns credits to supplier
                payment_ship = PaymentShip(requesting_planet, self.planet_object, total_cost)
                unified_transport_system.payment_ships.append(payment_ship)
                
                print(f"📦 {self.planet_name} shipping {can_supply} {commodity} to {request.requesting_planet} @ {unit_needed:.1f}/unit (total {total_cost} cr)")
                
    def auto_start_manufacturing(self):
        """Automatically start manufacturing based on available materials and planet type"""
        if self.planet_type == "industrial":
            # Industrial planets prioritize advanced manufacturing
            recipes_to_try = ["advanced_components", "weapons", "basic_components"]
        elif self.planet_type == "tech":
            # Tech planets focus on high-tech goods
            recipes_to_try = ["medicine", "advanced_components", "technology"]
        elif self.planet_type == "luxury":
            # Luxury planets make luxury goods
            recipes_to_try = ["luxury_goods", "medicine"]
        else:
            # Other planets focus on basic manufacturing
            recipes_to_try = ["basic_components"]
            
        for recipe_name in recipes_to_try:
            if recipe_name in enhanced_manufacturing.recipes:
                recipe = enhanced_manufacturing.recipes[recipe_name]
                
                # Check if we have materials and aren't already manufacturing this
                current_processes = enhanced_manufacturing.get_manufacturing_status(self.planet_name)
                if recipe_name not in current_processes:
                    # Check if we have enough materials
                    can_manufacture = True
                    for commodity, required in recipe.inputs.items():
                        if self.stockpiles.get(commodity, 0) < required * 2:  # Keep some buffer
                            can_manufacture = False
                            break
                            
                    if can_manufacture:
                        crew_effectiveness = 50  # Default
                        enhanced_manufacturing.start_manufacturing(
                            self.planet_name, recipe_name, self.stockpiles, crew_effectiveness
                        )
                        break  # Only start one process at a time

class PirateBaseEconomy(EnhancedPlanetEconomy):
    """Economy for pirate bases with contraband and raiding needs"""
    
    def __init__(self, base_name, planet_object):
        super().__init__(base_name, "pirate_hideout", planet_object)
        
        # Pirate-specific stockpiles
        self.contraband_stockpiles = {}
        self.intelligence_cache = []
        self.last_raid_launch = 0
        self.raid_interval = 120  # Launch raiders every 2 minutes
        
        self.initialize_pirate_economy()
        
    def initialize_pirate_economy(self):
        """Set up pirate base economy"""
        self.daily_production = {"weapons": 20}
        
        self.daily_consumption = {
            "food": 50, "fuel": 30, "weapons": 10, "medicine": 15
        }
        
        self.stockpiles = {
            "food": 200, "fuel": 150, "weapons": 100, "medicine": 50,
            "minerals": 100, "technology": 50, "luxury_goods": 25, "spices": 30
        }
        
        self.contraband_stockpiles = {
            ContrabandType.STOLEN_GOODS: 0,
            ContrabandType.WEAPONS: 0,
            ContrabandType.ILLEGAL_TECH: 0,
            ContrabandType.NARCOTICS: 0,
            ContrabandType.SLAVES: 0
        }
        
    def update(self):
        """Update pirate base economy and raiding operations"""
        super().update()
        
        current_time = time.time()
        
        # Launch raiders based on intelligence and needs
        if current_time - self.last_raid_launch > self.raid_interval:
            self.consider_launching_raiders()
            self.last_raid_launch = current_time
            
    def consider_launching_raiders(self):
        """Decide whether to launch raiders - LOGICAL: target wealthy areas and profitable routes"""
        # 1. TARGET WEALTHY PLANETS - Pirates follow the money!
        wealthy_targets = self.find_wealthy_targets()
        
        # 2. TARGET HIGH-VALUE CARGO ROUTES
        profitable_routes = self.find_profitable_routes()
        
        # 3. CRITICAL NEEDS (secondary motivation)
        critical_needs = []
        for commodity, consumption in self.daily_consumption.items():
            current_stock = self.stockpiles.get(commodity, 0)
            days_remaining = current_stock / consumption if consumption > 0 else float('inf')
            if days_remaining < 20:
                critical_needs.append(commodity)
        
        # LOGICAL RAID DECISION: Wealth > Profit > Needs
        raid_motivation = 0.0
        
        # Wealthy targets are ALWAYS attractive (main motivation)
        if wealthy_targets:
            raid_motivation += 0.7  # 70% base chance to raid wealth
            
        # Profitable routes attract raids
        if profitable_routes:
            raid_motivation += 0.5  # 50% chance for profitable routes
            
        # Desperate needs drive raids (but secondary)
        if critical_needs:
            raid_motivation += 0.3  # 30% chance for needs
            
        # Success breeds more raids
        if len(self.intelligence_cache) > 3:  # Lots of intel = successful pirates
            raid_motivation += 0.4  # 40% bonus for successful pirates
            
        # Launch raid if motivated
        if random.random() < min(0.95, raid_motivation):  # Cap at 95%
            target_data = wealthy_targets + profitable_routes + critical_needs
            self.launch_raider(target_data)
            
    def find_wealthy_targets(self):
        """Find wealthy planets/cargo worth raiding"""
        wealthy_targets = []
        
        # Check intelligence for high-value cargo
        for intel in self.intelligence_cache:
            if intel.estimated_value > 50000:  # High-value cargo
                wealthy_targets.append(intel.cargo_manifest)
                
        # TODO: Add logic to identify wealthy planets by trade volume/stockpiles
        return wealthy_targets
        
    def find_profitable_routes(self):
        """Identify profitable trade routes to target"""
        profitable_routes = []
        
        # Look for repeated high-value routes in intelligence
        route_values = {}
        for intel in self.intelligence_cache:
            route_key = f"{intel.origin_planet}->{intel.destination_planet}"
            if route_key not in route_values:
                route_values[route_key] = []
            route_values[route_key].append(intel.estimated_value)
            
        # Find consistently profitable routes
        for route, values in route_values.items():
            if len(values) > 1 and sum(values) / len(values) > 30000:  # Avg > 30k
                profitable_routes.append(values[-1])  # Use latest value
                
        return profitable_routes
            
    def launch_raider(self, target_commodities=None):
        """Launch a pirate raider"""
        target_intel = self.select_raid_target(target_commodities)
        
        raider = PirateRaider(
            pirate_base=self.planet_object,
            target_intelligence=target_intel
        )
        
        unified_transport_system.raiders.append(raider)
        
    def select_raid_target(self, needed_commodities=None):
        """Select the best raid target from intelligence cache"""
        if not self.intelligence_cache:
            return None
            
        best_target = None
        best_score = 0
        
        for intel in self.intelligence_cache:
            score = intel.estimated_value
            
            if needed_commodities:
                for commodity in needed_commodities:
                    if commodity in intel.cargo_manifest:
                        score *= 2
                        
            age_hours = (time.time() - intel.intel_timestamp) / 3600
            if age_hours > 24:
                continue
                
            if score > best_score:
                best_score = score
                best_target = intel
                
        return best_target
        
    def receive_intelligence(self, intelligence):
        """Receive intelligence about cargo movements"""
        # Remove old intelligence
        self.intelligence_cache = [intel for intel in self.intelligence_cache 
                                 if time.time() - intel.intel_timestamp < 86400]  # 24 hours
                                 
        self.intelligence_cache.append(intelligence)
        print(f"🕵️ {self.planet_name} received cargo intelligence: {intelligence.cargo_manifest}")
        
    def receive_stolen_goods(self, stolen_cargo):
        """Process stolen goods from successful raids"""
        for commodity, quantity in stolen_cargo.items():
            self.stockpiles[commodity] = self.stockpiles.get(commodity, 0) + quantity
            
        print(f"🏴‍☠️ {self.planet_name} received stolen goods: {stolen_cargo}")

# ===== UNIFIED TRANSPORT SYSTEM MANAGER =====

class UnifiedTransportSystemManager:
    """Manager for all transport ships and systems"""
    
    def __init__(self):
        self.message_ships = []
        self.cargo_ships = []
        self.payment_ships = []
        self.raiders = []
        self.smugglers = []
        
    def update(self):
        """Update all transport ships"""
        all_ships = (self.message_ships + self.cargo_ships + self.payment_ships + 
                    self.raiders + self.smugglers)
        
        for ship in all_ships[:]:  # Copy to avoid modification during iteration
            if hasattr(ship, 'update'):
                ship.update()
                
            # Remove delivered ships
            if hasattr(ship, 'delivered') and ship.delivered:
                self.remove_ship(ship)
                    
    def remove_ship(self, ship):
        """Remove ship from appropriate list"""
        lists_to_check = [
            self.message_ships, self.cargo_ships, self.payment_ships,
            self.raiders, self.smugglers
        ]
        
        for ship_list in lists_to_check:
            if ship in ship_list:
                ship_list.remove(ship)
                break
        # Defer destruction to here to avoid accessing a destroyed NodePath mid-update
        try:
            destroy(ship)
        except Exception:
            pass
                
    def get_statistics(self):
        """Get comprehensive transport statistics"""
        return {
            'message_ships': len(self.message_ships),
            'cargo_ships': len(self.cargo_ships), 
            'payment_ships': len(self.payment_ships),
            'raiders': len(self.raiders),
            'smugglers': len(self.smugglers),
            'total_ships': (len(self.message_ships) + len(self.cargo_ships) + 
                          len(self.payment_ships) + len(self.raiders) + len(self.smugglers)),
            'active_trade_routes': self.count_active_routes(),
            'pirate_threat_level': self.calculate_threat_level()
        }
        
    def count_active_routes(self):
        """Count active trade routes"""
        routes = set()
        for ship in self.cargo_ships:
            if hasattr(ship, 'origin') and hasattr(ship, 'destination'):
                origin_name = getattr(ship.origin, 'name', 'Unknown')
                dest_name = getattr(ship.destination, 'name', 'Unknown')
                routes.add(f"{origin_name}->{dest_name}")
        return len(routes)
        
    def calculate_threat_level(self):
        """Calculate current pirate threat level"""
        if len(self.raiders) == 0:
            return "LOW"
        elif len(self.raiders) < 3:
            return "MEDIUM"
        elif len(self.raiders) < 6:
            return "HIGH"
        else:
            return "EXTREME"
            
    def create_pirate_base(self, planet):
        """Convert a planet to a pirate base"""
        planet.enhanced_economy = PirateBaseEconomy(planet.name, planet)
        planet.planet_type = "pirate_hideout"
        # Fallback to a valid Ursina color similar to dark red
        planet.color = color.red.tint(-.4)
        print(f"🏴‍☠️ {planet.name} has become a pirate base!")
        return True

    def spawn_escorts_for_cargo(self, cargo_ship, faction_id: str, num_escorts: int = 2):
        """Spawn escort military ships near a valuable cargo ship."""
        if 'military_manager' not in globals():
            return
        try:
            for i in range(max(1, num_escorts)):
                offset = Vec3(random.uniform(-15, 15), 0, random.uniform(-15, 15))
                pos = cargo_ship.position + offset if hasattr(cargo_ship, 'position') else Vec3(0, 0, 0)
                escort = MilitaryShip(faction_id, MilitaryShipType.ESCORT, pos, patrol_radius=120)
                escort.target_position = pos
                escort.patrol_center = pos
                military_manager.military_ships.append(escort)
        except Exception:
            pass

# Create global unified transport system
unified_transport_system = UnifiedTransportSystemManager()

# ===== TRANSPORT CONTRACT REGISTRY =====

class TransportContractRegistry:
    """Tracks cargo-payment contracts to ensure persistent consequences."""
    def __init__(self):
        self._contracts = {}
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f"CONTRACT-{int(time.time())}-{self._counter}"

    def register_contract(self, origin_planet, dest_planet, commodity, quantity, unit_price, total_cost) -> str:
        cid = self._next_id()
        self._contracts[cid] = {
            'origin': origin_planet,
            'dest': dest_planet,
            'commodity': commodity,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_cost': total_cost,
            'status': 'cargo_in_transit'
        }
        return cid

    def cargo_delivered(self, contract_id: str):
        data = self._contracts.get(contract_id)
        if not data:
            return
        # Spawn payment ship from dest to origin carrying reserved credits
        payment_ship = PaymentShip(data['dest'], data['origin'], int(data['total_cost']))
        payment_ship.contract_id = contract_id
        unified_transport_system.payment_ships.append(payment_ship)
        data['status'] = 'payment_in_transit'

    def cargo_lost(self, contract_id: str):
        data = self._contracts.get(contract_id)
        if not data:
            return
        # Refund escrow to destination since goods never arrived
        if hasattr(data['dest'], 'enhanced_economy') and data['dest'].enhanced_economy:
            data['dest'].enhanced_economy.credits += int(data['total_cost'])
            # Remove expected delivery
            exp = data['dest'].enhanced_economy.expected_deliveries
            exp[data['commodity']] = max(0, exp.get(data['commodity'], 0) - data['quantity'])
        data['status'] = 'failed_cargo_lost'

    def payment_delivered(self, contract_id: str):
        data = self._contracts.get(contract_id)
        if not data:
            return
        # Credit supplier upon payment arrival
        if hasattr(data['origin'], 'enhanced_economy') and data['origin'].enhanced_economy:
            data['origin'].enhanced_economy.credits += int(data['total_cost'])
        data['status'] = 'completed'

contract_registry = TransportContractRegistry()

# ===== TRADE LANE WAYPOINTS =====

def compute_trade_waypoints(origin_pos: 'Vec3', dest_pos: 'Vec3', segments: int = 5):
    """Create simple intermediate waypoints along a curved corridor between origin and destination.
    Uses a slight lateral offset to avoid perfectly straight lines (more life-like lanes)."""
    waypoints = []
    try:
        delta = dest_pos - origin_pos
        right = Vec3(1, 0, 0)
        lateral = Vec3(delta.z, 0, -delta.x).normalized() if hasattr(delta, 'length') and delta.length() > 0 else right
        curve_strength = min(50.0, max(10.0, delta.length() * 0.1)) if hasattr(delta, 'length') else 20.0
        for i in range(1, segments):
            t = i / segments
            base = origin_pos + delta * t
            # Sine-bend offset for a gentle arc
            offset = lateral * curve_strength * math.sin(math.pi * t)
            waypoints.append(base + offset)
    except Exception:
        pass
    # Always end at destination
    return waypoints

def initialize_enhanced_economies():
    """Initialize enhanced economies for all planets"""
    print("🔄 Initializing enhanced transport system...")
    
    # Convert existing planets to enhanced economy system
    for planet in planets:
        if not hasattr(planet, 'enhanced_economy') or planet.enhanced_economy is None:
            planet.enhanced_economy = EnhancedPlanetEconomy(planet.name, planet.planet_type, planet)
            
    # Create some pirate bases
    pirate_base_count = 0
    for planet in planets:
        if random.random() < 0.15 and pirate_base_count < 3:  # 15% chance, max 3 bases
            unified_transport_system.create_pirate_base(planet)
            pirate_base_count += 1
            
    print(f"✅ Enhanced transport system initialized with {pirate_base_count} pirate bases")
    # Build a global mapping of planet name -> enhanced economy for systems that expect it
    globals()['enhanced_planet_economies'] = {p.name: p.enhanced_economy for p in planets if hasattr(p, 'enhanced_economy') and p.enhanced_economy}

# Create systems
random_event_system = RandomEventSystem()
combat_system = CombatSystem()
faction_system = FactionSystem()
crew_system = CrewSystem()
time_system = TimeSystem()
mission_system = MissionSystem()

# Initialize enhanced economies after planets are created
initialize_enhanced_economies()

# ===== CENTRALIZED UI STATE MANAGER =====

class UIManager:
    """Central manager to keep UI state consistent and cursor logic correct."""
    def __init__(self):
        self._uis = []

    def register(self, ui):
        if ui not in self._uis:
            self._uis.append(ui)

    def any_active(self):
        return any(getattr(ui, 'active', False) for ui in self._uis)

    def update_cursor(self):
        # Show cursor if any UI is active or game is paused
        try:
            paused_state = paused  # may not be defined yet during import
        except NameError:
            paused_state = False
        should_show_cursor = paused_state or self.any_active()
        mouse.locked = not should_show_cursor
        mouse.visible = should_show_cursor

    def hide_all(self):
        for ui in self._uis:
            if getattr(ui, 'active', False):
                ui.active = False
                if hasattr(ui, 'panel'):
                    ui.panel.enabled = False
        self.update_cursor()

    def show(self, ui):
        # Ensure only one UI visible at a time
        for other in self._uis:
            if other is not ui and getattr(other, 'active', False):
                other.active = False
                if hasattr(other, 'panel'):
                    other.panel.enabled = False
        ui.active = True
        if hasattr(ui, 'panel'):
            ui.panel.enabled = True
        self.update_cursor()

    def hide(self, ui):
        ui.active = False
        if hasattr(ui, 'panel'):
            ui.panel.enabled = False
        self.update_cursor()

ui_manager = UIManager()

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
        self.current_planet = planet_name
        ui_manager.show(self)
        self.update_display()
        
    def hide(self):
        self.current_planet = None
        ui_manager.hide(self)
        
    def update_display(self):
        if not self.current_planet:
            return
            
        # Update planet info with realistic economic data
        planet_info = market_system.get_planet_info(self.current_planet)
        if planet_info:
            blockade_status = " [BLOCKADED]" if planet_info['blockaded'] else ""
            self.planet_info.text = f'Planet: {self.current_planet}{blockade_status}\nType: {planet_info["type"].title()}\nPopulation: {planet_info["population"]:,}'
        else:
            self.planet_info.text = f'Planet: {self.current_planet}\nType: Unknown'
        
        # Update player info
        self.player_info.text = f'Credits: {player_wallet.credits}\nCargo: {player_cargo.get_used_capacity()}/{player_cargo.max_capacity}'
        
        # Update commodity list with realistic supply data
        commodity_text = "COMMODITIES:\n\n"
        commodities = list(market_system.commodities.keys())
        for i, commodity_name in enumerate(commodities[:8]):  # Show first 8 commodities
            buy_price = market_system.get_buy_price(self.current_planet, commodity_name)
            sell_price = market_system.get_sell_price(self.current_planet, commodity_name)
            available = market_system.get_available_supply(self.current_planet, commodity_name)
            player_has = player_cargo.cargo.get(commodity_name, 0)
            
            # Show supply status
            if available == 0:
                supply_status = "OUT OF STOCK"
            elif available < 10:
                supply_status = f"LOW ({available})"
            else:
                supply_status = f"Available: {available}"
                
            commodity_text += f"{i+1}. {commodity_name.replace('_', ' ').title()}\n"
            commodity_text += f"   Buy: {buy_price} ({supply_status})\n"
            commodity_text += f"   Sell: {sell_price}  Have: {player_has}\n\n"
        
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
        available = market_system.get_available_supply(self.current_planet, commodity_name)
        
        if available <= 0:
            print(f"❌ {self.current_planet} is out of {commodity_name.replace('_', ' ')}!")
            return
            
        if player_wallet.can_afford(buy_price) and player_cargo.can_add(commodity_name, 1):
            # Execute the trade through the persistent economy
            actual_quantity = market_system.execute_trade(self.current_planet, commodity_name, 1, True)
            
            if actual_quantity > 0:
                player_wallet.spend(buy_price)
                player_cargo.add_cargo(commodity_name, actual_quantity)
                print(f"✅ Bought {actual_quantity} {commodity_name.replace('_', ' ')} for {buy_price} credits")
                
                # Check if this purchase created shortage
                remaining = market_system.get_available_supply(self.current_planet, commodity_name)
                if remaining < 5:
                    print(f"⚠️ {self.current_planet} is running low on {commodity_name.replace('_', ' ')}!")
            else:
                print(f"❌ Failed to purchase {commodity_name.replace('_', ' ')}")
                
            self.update_display()
        elif not player_wallet.can_afford(buy_price):
            print("💰 Not enough credits!")
        else:
            print("📦 Cargo hold full!")
            
    def sell_commodity(self, commodity_name):
        if player_cargo.cargo.get(commodity_name, 0) > 0:
            sell_price = market_system.get_sell_price(self.current_planet, commodity_name)
            
            # Execute the trade through the persistent economy
            market_system.execute_trade(self.current_planet, commodity_name, 1, False)
            player_cargo.remove_cargo(commodity_name, 1)
            player_wallet.earn(sell_price)
            print(f"✅ Sold 1 {commodity_name.replace('_', ' ')} for {sell_price} credits")
            
            # Check if this sale helped with shortages
            planet_info = market_system.get_planet_info(self.current_planet)
            if planet_info:
                stockpile = planet_info['stockpiles'].get(commodity_name, 0)
                if stockpile < 50:
                    print(f"📈 Your sale helps alleviate {self.current_planet}'s {commodity_name.replace('_', ' ')} shortage!")
            
            self.update_display()
        else:
            print(f"❌ You don't have any {commodity_name.replace('_', ' ')}!")

# Create trading UI
trading_ui = TradingUI()
ui_manager.register(trading_ui)

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
        ui_manager.show(self)
        self.update_display()
        
    def hide(self):
        ui_manager.hide(self)
        
    def update_display(self):
        # Update player info
        self.player_info.text = f'Credits: {player_wallet.credits}'
        
        # Update upgrade options
        upgrade_text = "AVAILABLE UPGRADES:\n\n"
        
        # Ship component upgrades
        components = [
            ("cargo", "Cargo Bay", ComponentType.CARGO_BAY),
            ("engine", "Engine", ComponentType.ENGINE),
            ("fuel_tank", "Fuel Tank", ComponentType.FUEL_TANK),
            ("shields", "Shields", ComponentType.SHIELDS),
            ("weapons", "Weapons", ComponentType.WEAPONS),
            ("life_support", "Life Support", ComponentType.LIFE_SUPPORT)
        ]
        
        for i, (upgrade_key, display_name, component_type) in enumerate(components[:6]):
            cost = ship_systems.upgrade_costs.get(upgrade_key, 999999)
            affordable = "✓" if player_wallet.can_afford(cost) else "✗"
            current_level = ship_systems.components[component_type].level
            condition = ship_systems.components[component_type].condition.value
            
            upgrade_text += f"{i+1}. {display_name} Upgrade - {cost} credits {affordable}\n"
            upgrade_text += f"   Level {current_level} ({condition}) -> Level {current_level + 1}\n\n"
        
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
            
        # Handle component upgrades
        components = [
            ("cargo", ComponentType.CARGO_BAY),
            ("engine", ComponentType.ENGINE),
            ("fuel_tank", ComponentType.FUEL_TANK),
            ("shields", ComponentType.SHIELDS),
            ("weapons", ComponentType.WEAPONS),
            ("life_support", ComponentType.LIFE_SUPPORT)
        ]
        
        if key in '123456':
            index = int(key) - 1
            if index < len(components):
                upgrade_key, component_type = components[index]
                if ship_systems.upgrade_component(component_type):
                    self.update_display()
                else:
                    print(f"Cannot afford {component_type.value.lower()} upgrade!")
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
ui_manager.register(upgrade_ui)

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
        ui_manager.hide_all()
        self.current_event = event
        ui_manager.show(self)
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
        
        # Cursor handled by UI manager
        
    def handle_option(self, action):
        if action != 'ignore':
            random_event_system.handle_event_action(action)
        
        self.hide()
        
    def hide(self):
        self.current_event = None
        # Clear buttons
        for button in self.option_buttons:
            destroy(button)
        self.option_buttons.clear()
        ui_manager.hide(self)

# Create event UI
event_ui = EventUI()
ui_manager.register(event_ui)

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
        ui_manager.show(self)
        self.update_display()
        
    def hide(self):
        ui_manager.hide(self)
        
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
        ui_manager.show(self)
        self.update_display()
        
    def hide(self):
        ui_manager.hide(self)
        
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
        ui_manager.show(self)
        mission_system.generate_missions()
        self.update_display()
        
    def hide(self):
        ui_manager.hide(self)
        
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
ui_manager.register(faction_ui)
ui_manager.register(crew_ui)
ui_manager.register(mission_ui)

def update():
    global nearby_planet
    
    if not paused and not ui_manager.any_active():
        if scene_manager.current_state == GameState.SPACE:
            # Check if player is near any planet (anti-flicker via hysteresis)
            nearest_planet = None
            nearest_dist = float('inf')
            for planet in planets:
                d = (planet.position - player.position).length()
                if d < nearest_dist:
                    nearest_dist = d
                    nearest_planet = planet

            # Evaluate show/hide using thresholds
            if landing_prompt_active:
                if nearest_planet is None or nearest_dist > landing_hide_threshold:
                    landing_prompt.enabled = False
                    land_button.enabled = False
                    cancel_button.enabled = False
                    # Unfreeze player; cursor decided by UI manager
                    player.enabled = True
                    if 'ui_manager' in globals():
                        ui_manager.update_cursor()
                    globals()['landing_prompt_active'] = False
                    globals()['nearby_planet'] = None
                else:
                    # Keep the panel visible; update text if planet changed
                    if nearest_planet is not None and nearest_planet is not nearby_planet:
                        landing_text.text = f"Approaching {nearest_planet.name}\nDo you want to land?"
                        globals()['nearby_planet'] = nearest_planet
            else:
                if nearest_planet is not None and nearest_dist < landing_show_threshold and not ui_manager.any_active():
                    landing_text.text = f"Approaching {nearest_planet.name}\nDo you want to land?"
                    landing_prompt.enabled = True
                    land_button.enabled = True
                    cancel_button.enabled = True
                    # Freeze player; let UI manager show cursor
                    player.enabled = False
                    globals()['nearby_planet'] = nearest_planet
                    globals()['landing_prompt_active'] = True
                    if 'ui_manager' in globals():
                        ui_manager.update_cursor()

            # Random events only when not near planets and no landing prompt
            if (nearest_planet is None or nearest_dist > landing_hide_threshold) and not landing_prompt.enabled:
                random_event_system.check_for_event()
                
        elif scene_manager.current_state == GameState.TOWN:
            # Check if player is near trading post in town
            if scene_manager.town_controller:
                player_pos = scene_manager.town_controller.position
                # Anti-flicker interact prompt with hysteresis
                nearest_kind = None
                nearest_dist = float('inf')

                def consider(kind, ent):
                    nonlocal nearest_kind, nearest_dist
                    if ent is None:
                        return
                    d = (player_pos - ent.position).length()
                    if d < nearest_dist:
                        nearest_dist = d
                        nearest_kind = kind

                consider('Trade (E)', getattr(scene_manager, 'trading_post_entity', None))
                consider('Upgrades (E)', getattr(scene_manager, 'shipyard_entity', None))
                consider('Relations (E)', getattr(scene_manager, 'embassy_entity', None))
                consider('Crew (E)', getattr(scene_manager, 'crew_quarters_entity', None))
                consider('Missions (E)', getattr(scene_manager, 'mission_board_entity', None))

                # Decide show/hide with hysteresis thresholds
                if scene_manager._prompt_active:
                    if nearest_dist > scene_manager._prompt_hide_threshold:
                        scene_manager.interact_prompt.enabled = False
                        scene_manager._prompt_active = False
                        scene_manager._prompt_target_kind = None
                    else:
                        # Keep showing, update text if a different target is clearly closer
                        if nearest_kind and nearest_kind != scene_manager._prompt_target_kind and nearest_dist < scene_manager._prompt_show_threshold * 0.8:
                            scene_manager._prompt_target_kind = nearest_kind
                            scene_manager.interact_prompt.text = f"Press E for {nearest_kind}"
                else:
                    if nearest_dist < scene_manager._prompt_show_threshold and nearest_kind:
                        scene_manager._prompt_active = True
                        scene_manager._prompt_target_kind = nearest_kind
                        scene_manager.interact_prompt.text = f"Press E for {nearest_kind}"
                        scene_manager.interact_prompt.enabled = True
                    
    # Update time system
    time_system.update()
    
    # Update physical communication system
    physical_communication.update()
    
    # Update enhanced Pirates! features
    enhanced_features.update(time.dt, player.position, time.time())
    
    # Update unified transport system
    unified_transport_system.update()
    
    # Update planet economies
    for planet in planets:
        if hasattr(planet, 'enhanced_economy') and planet.enhanced_economy:
            planet.enhanced_economy.update()
            
    # Update new persistent systems
    weather_system.update()
    military_manager.update()
    dynamic_contracts.update()

# Function to handle landing
def land_on_planet():
    global nearby_planet
    if nearby_planet:
        # Check if planet is blockaded
        if military_manager.is_planet_blockaded(nearby_planet.name):
            if not military_manager.can_player_access_planet(nearby_planet.name):
                # Find blockading faction
                blockade_ships = military_manager.blockade_zones[nearby_planet.name]
                if blockade_ships:
                    blockading_faction = blockade_ships[0].faction_id
                    print(f"🚫 Access to {nearby_planet.name} blocked by {blockading_faction} forces!")
                    print(f"💡 Improve reputation with {blockading_faction} or break the blockade to land.")
                    
                    # Hide landing prompt but don't land
                    landing_prompt.enabled = False
                    nearby_planet = None
                    
                    # Unfreeze player and capture mouse
                    player.enabled = True
                    mouse.locked = True
                    mouse.visible = False
                    return
        
        # PHYSICAL COMMUNICATION: Player learns local news upon landing
        print(f"\n🚀 Landing on {nearby_planet.name}...")
        physical_communication.player_visits_planet(nearby_planet.name)
        
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
ui_manager.register(type('LandingWrapper', (), {'active': False, 'panel': landing_prompt}))

# Lighting
DirectionalLight(y=2, z=3, rotation=(45, -45, 45))
AmbientLight(color=Vec4(0.1, 0.1, 0.1, 1))  # Darker ambient light

# Initialize scene manager after all entities are created
scene_manager.initialize_space()

# Initialize military and contract systems
military_manager.initialize_military_presence()

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
        if event_ui.active:
            event_ui.hide()
            return
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

        # Centralized cursor control
        if 'ui_manager' in globals():
            ui_manager.update_cursor()
    
    if key == 'f6':  # Screenshot
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        base.win.saveScreenshot(Filename(f'screenshots/screenshot_{time.time()}.png'))
        print(f'Screenshot saved to screenshots folder')
    
    if key == 'e' and not paused:
        # Context-sensitive interact
        if scene_manager.current_state == GameState.TOWN and scene_manager.town_controller:
            player_pos = scene_manager.town_controller.position
            # Prioritize buildings before NPCs
            interactables = []
            if getattr(scene_manager, 'trading_post_entity', None):
                interactables.append(('trading', scene_manager.trading_post_entity, 10, None))
            if getattr(scene_manager, 'shipyard_entity', None):
                interactables.append(('shipyard', scene_manager.shipyard_entity, 10, None))
            if getattr(scene_manager, 'embassy_entity', None):
                interactables.append(('embassy', scene_manager.embassy_entity, 10, None))
            if getattr(scene_manager, 'crew_quarters_entity', None):
                interactables.append(('crew', scene_manager.crew_quarters_entity, 10, None))
            if getattr(scene_manager, 'mission_board_entity', None):
                interactables.append(('mission', scene_manager.mission_board_entity, 10, None))

            # Find nearest interactable within its range
            nearest = None
            nearest_dist = float('inf')
            for kind, ent, rng, extra in interactables:
                dist = (player_pos - ent.position).length()
                if dist < rng and dist < nearest_dist:
                    nearest = (kind, ent)
                    nearest_dist = dist

            if nearest:
                ui_manager.hide_all()
                kind, _ = nearest
                if kind == 'trading':
                    if scene_manager.current_planet:
                        trading_ui.show(scene_manager.current_planet.name)
                    else:
                        planet_name = "Local Trading Post"
                        if planet_name not in market_system.planet_economies:
                            market_system.generate_market_for_planet(planet_name, "generic")
                        trading_ui.show(planet_name)
                elif kind == 'shipyard':
                    upgrade_ui.show()
                elif kind == 'embassy':
                    faction_ui.show()
                elif kind == 'crew':
                    crew_ui.show()
                elif kind == 'mission':
                    mission_ui.show()
                return

            # Otherwise, talk to NPCs if close
            for npc in scene_manager.town_npcs:
                distance = (npc.position - player_pos).length()
                if distance < 5:
                    dialogue = random.choice(npc.dialogue)
                    print(f"💬 {npc.name_tag.text}: {dialogue}")
                    return
    
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
            trading_post_pos = getattr(scene_manager, 'trading_post_entity', None).position if getattr(scene_manager, 'trading_post_entity', None) else Vec3(10, 3, 0)
            distance = (player_pos - trading_post_pos).length()
            
            if distance < 10:  # Within range of trading post
                ui_manager.hide_all()
                # Use the current planet the player landed on
                if scene_manager.current_planet:
                    trading_ui.show(scene_manager.current_planet.name)
                else:
                    # Fallback for testing
                    planet_name = "Local Trading Post"
                    if planet_name not in market_system.planet_economies:
                        market_system.generate_market_for_planet(planet_name, "generic")
                    trading_ui.show(planet_name)
            else:
                print("You need to be closer to the trading post!")
    
    if key == 'u' and scene_manager.current_state == GameState.TOWN and not paused:
        # Open upgrades if near shipyard
        if scene_manager.town_controller:
            player_pos = scene_manager.town_controller.position
            shipyard_pos = getattr(scene_manager, 'shipyard_entity', None).position if getattr(scene_manager, 'shipyard_entity', None) else Vec3(-10, 3, 0)
            distance = (player_pos - shipyard_pos).length()
            
            if distance < 10:  # Within range of shipyard
                ui_manager.hide_all()
                upgrade_ui.show()
            else:
                print("You need to be closer to the shipyard!")
    
    if key == 'r' and scene_manager.current_state == GameState.TOWN and not paused:
        # Open faction relations if near embassy
        if scene_manager.town_controller:
            player_pos = scene_manager.town_controller.position
            embassy_pos = getattr(scene_manager, 'embassy_entity', None).position if getattr(scene_manager, 'embassy_entity', None) else Vec3(0, 3, -10)
            distance = (player_pos - embassy_pos).length()
            
            if distance < 10:  # Within range of embassy
                ui_manager.hide_all()
                faction_ui.show()
            else:
                print("You need to be closer to the embassy!")
    
    if key == 'c' and scene_manager.current_state == GameState.TOWN and not paused:
        # Open crew management if near crew quarters
        if scene_manager.town_controller:
            player_pos = scene_manager.town_controller.position
            crew_quarters_pos = getattr(scene_manager, 'crew_quarters_entity', None).position if getattr(scene_manager, 'crew_quarters_entity', None) else Vec3(0, 3, 10)
            distance = (player_pos - crew_quarters_pos).length()
            
            if distance < 10:  # Within range of crew quarters
                ui_manager.hide_all()
                crew_ui.show()
            else:
                print("You need to be closer to the crew quarters!")
    
    if key == 'm' and scene_manager.current_state == GameState.TOWN and not paused:
        # Open mission board if near mission board
        if scene_manager.town_controller:
            player_pos = scene_manager.town_controller.position
            mission_board_pos = getattr(scene_manager, 'mission_board_entity', None).position if getattr(scene_manager, 'mission_board_entity', None) else Vec3(-10, 3, -10)
            distance = (player_pos - mission_board_pos).length()
            
            if distance < 10:  # Within range of mission board
                ui_manager.hide_all()
                mission_ui.show()
            else:
                print("You need to be closer to the mission board!")
                
    if key == 'k' and not paused:
        # Show available contracts (can be accessed anywhere)
        print("\n📋 AVAILABLE CONTRACTS:")
        for i, contract in enumerate(dynamic_contracts.available_contracts[:5]):
            print(f"{i+1}. {contract.title}")
            print(f"   Client: {contract.client_faction}")
            print(f"   Reward: {contract.rewards.get('credits', 0)} credits")
            print(f"   Difficulty: {'⭐' * contract.difficulty}")
            print(f"   Time limit: {contract.time_limit/60:.0f} minutes")
            print()
        if not dynamic_contracts.available_contracts:
            print("No contracts available.")
            
    if key == 'j' and not paused:
        # Show active contracts
        print("\n📋 ACTIVE CONTRACTS:")
        for i, contract in enumerate(dynamic_contracts.active_contracts):
            elapsed_time = time.time() - contract.start_time
            remaining_time = contract.time_limit - elapsed_time
            print(f"{i+1}. {contract.title}")
            print(f"   Status: {contract.status.value}")
            print(f"   Time remaining: {remaining_time/60:.1f} minutes")
            print(f"   Objectives:")
            for obj in contract.objectives:
                print(f"     • {obj}")
            print()
        if not dynamic_contracts.active_contracts:
            print("No active contracts.")
    
    # TESTING COMMANDS for the persistent economy
    if key == 'b' and scene_manager.current_state == GameState.TOWN and not paused:
        # Toggle blockade on current planet (for testing)
        if scene_manager.current_planet:
            planet_info = market_system.get_planet_info(scene_manager.current_planet.name)
            if planet_info:
                current_status = planet_info['blockaded']
                market_system.set_blockade(scene_manager.current_planet.name, not current_status)
                
    if key == 'i' and scene_manager.current_state == GameState.TOWN and not paused:
        # Show detailed economic info for current planet
        if scene_manager.current_planet:
            show_economic_info(scene_manager.current_planet.name)
            
    if key == 'n' and not paused:
        # Advance time quickly (for testing)
        print("⏰ Fast-forwarding time...")
        time_system.advance_day()
        
    if key == 'f' and scene_manager.current_state == GameState.SPACE and not paused:
        # Refuel if near a planet with fuel station
        if nearby_planet and nearby_planet.has_fuel_station:
            fuel_needed = ship_systems.fuel_system.max_fuel - ship_systems.fuel_system.current_fuel
            if fuel_needed > 0:
                total_cost = int(fuel_needed * nearby_planet.fuel_price)
                if player_wallet.can_afford(total_cost):
                    player_wallet.spend(total_cost)
                    ship_systems.fuel_system.refuel(fuel_needed)
                    print(f"⛽ Refueled at {nearby_planet.name} for {total_cost} credits")
                else:
                    print(f"💰 Not enough credits! Refueling costs {total_cost} credits")
            else:
                print("⛽ Fuel tank already full!")
        else:
            if nearby_planet:
                print(f"❌ {nearby_planet.name} has no fuel station")
            else:
                print("❌ No planet nearby for refueling")
                
    if key == 'g' and not paused:
        # Emergency repair using spare parts
        damaged_components = ship_systems.get_system_status()['damaged_components']
        if damaged_components:
            component_name = damaged_components[0]['type']
            component_type = ComponentType(component_name)
            if ship_systems.repair_component(component_type, 1):
                print(f"🔧 Emergency repair completed on {component_name}")
            else:
                print("🔧 No spare parts available for repairs")
        else:
            print("🔧 All systems operating normally")
    
    # ===== ENHANCED PIRATES! FEATURES CONTROLS =====
    
    if key == 'v' and not paused:
        # Fleet Management
        fleet = enhanced_features.fleet_manager.fleet
        if fleet:
            print("\n🚢 FLEET STATUS:")
            for i, ship in enumerate(fleet):
                stats = ship.get_effective_stats()
                print(f"{i+1}. {ship.name} ({ship.ship_class.value})")
                print(f"   Role: {ship.role} | Condition: {ship.condition*100:.0f}%")
                print(f"   Combat Rating: {stats['combat_rating']:.0f}")
            total_strength = enhanced_features.fleet_manager.get_fleet_combat_strength()
            print(f"\nTotal Fleet Combat Strength: {total_strength:.0f}")
        else:
            print("🚢 No ships in fleet. Capture ships through boarding actions!")
    
    if key == 'z' and not paused:
        # Treasure Scanner
        treasures = enhanced_features.treasure_hunting.scan_for_treasures(player.position)
        if treasures:
            print("📡 TREASURE SCANNER ACTIVE")
        else:
            print("📡 No treasures detected in range. Fly around to scan more areas!")
    
    if key == 'x' and not paused:
        # Character Profile
        char = enhanced_features.character_development
        print(f"\n👤 CHARACTER PROFILE:")
        print(f"Age: {int(char.age)} years old")
        print(f"Years Active: {char.years_active:.1f}")
        print(f"\n📊 SKILLS:")
        for skill, level in char.skills.items():
            print(f"  {skill.value}: {level:.1f}")
        if char.legendary_achievements:
            print(f"\n🏆 ACHIEVEMENTS:")
            for achievement in char.legendary_achievements:
                print(f"  • {achievement['name']} (Age {achievement['age_earned']})")
    
    if key == 'o' and not paused:
        # Orbital Operations Menu
        if scene_manager.current_state == GameState.SPACE and nearby_planet:
            fleet_strength = enhanced_features.fleet_manager.get_fleet_combat_strength()
            print(f"\n🚀 ORBITAL OPERATIONS - {nearby_planet.name}")
            print(f"Fleet Combat Strength: {fleet_strength:.0f}")
            print("1. Orbital Bombardment (High damage, major reputation loss)")
            print("2. Surgical Strike (Precise, moderate reputation loss)")
            print("3. Establish Blockade (Economic pressure)")
            print("Press 1-3 to execute, or any other key to cancel")
        else:
            print("🚀 Must be near a planet in space to conduct orbital operations!")
    
    if key in '123' and not paused:
        # Execute orbital operations
        if scene_manager.current_state == GameState.SPACE and nearby_planet:
            fleet_strength = enhanced_features.fleet_manager.get_fleet_combat_strength()
            if fleet_strength < 100:
                print("⚠️ Warning: Fleet strength too low for major operations!")
                
            if key == '1':
                result = enhanced_features.orbital_combat.initiate_orbital_assault(
                    nearby_planet.name, AssaultType.ORBITAL_BOMBARDMENT, fleet_strength)
            elif key == '2':
                result = enhanced_features.orbital_combat.initiate_orbital_assault(
                    nearby_planet.name, AssaultType.SURGICAL_STRIKE, fleet_strength)
            elif key == '3':
                result = enhanced_features.orbital_combat.initiate_orbital_assault(
                    nearby_planet.name, AssaultType.BLOCKADE, fleet_strength)
                    
            if 'result' in locals() and result['success']:
                player_wallet.earn(result['credits'])
                if 'reputation' in result:
                    # Apply reputation changes to all factions
                    for faction_id in faction_system.factions.keys():
                        faction_system.change_reputation(faction_id, result['reputation'])
    
    if key == 'y' and not paused:
        # Attempt treasure excavation at current location
        for site in enhanced_features.treasure_hunting.treasure_sites:
            distance = (site.position - player.position).length()
            if distance < 5.0 and not site.discovered:  # Within 5 units
                skill_level = enhanced_features.character_development.skills[PersonalSkill.ENGINEERING]
                treasure_value = enhanced_features.treasure_hunting.excavate_treasure(site)
                if treasure_value:
                    player_wallet.earn(treasure_value)
                    enhanced_features.character_development.gain_experience(PersonalSkill.ENGINEERING, 10)
                break
        else:
            print("🔍 No treasure sites within excavation range.")
    
    if key == 'l' and not paused:
        # Simulate boarding action (when encountering ships)
        if scene_manager.current_state == GameState.SPACE:
            print("\n⚔️ BOARDING ACTION SIMULATION")
            print("1. Breach and Clear (High success, moderate damage)")
            print("2. Stealth Infiltration (Moderate success, minimal damage)")
            print("3. Negotiated Surrender (Low success, no damage)")
            print("Press 1-3 to board, or any other key to cancel")
            
    if key in '123' and scene_manager.current_state == GameState.SPACE:
        # Execute boarding action
        boarding_actions = {
            '1': BoardingAction.BREACH_AND_CLEAR,
            '2': BoardingAction.STEALTH_INFILTRATION,
            '3': BoardingAction.NEGOTIATED_SURRENDER
        }
        
        action = boarding_actions.get(key)
        if action:
            result = enhanced_features.ship_boarding.initiate_boarding("Enemy Merchant", action)
            if result['success']:
                player_wallet.earn(result['cargo'])
                enhanced_features.character_development.gain_experience(PersonalSkill.COMBAT, 5)
                
                if result.get('ship'):
                    captured_ship = result['ship']
                    if enhanced_features.fleet_manager.add_ship(captured_ship):
                        print(f"🚢 {captured_ship.name} added to your fleet!")
                    else:
                        print(f"🚢 Fleet at maximum capacity. {captured_ship.name} abandoned.")
    
    if key == 'p' and not paused:
        # Show enhanced skills and advancement opportunities
        char = enhanced_features.character_development
        print(f"\n📈 SKILL ADVANCEMENT:")
        for skill, level in char.skills.items():
            exp = char.experience_points[skill]
            needed = int(level * 100)
            print(f"  {skill.value}: {level:.1f} ({exp}/{needed} XP)")
        print(f"\n🎯 Gain experience by:")
        print(f"  • Trading (Trading skill)")
        print(f"  • Combat/Boarding (Combat skill)")
        print(f"  • Treasure hunting (Engineering skill)")
        print(f"  • Diplomatic missions (Diplomacy skill)")
        print(f"  • Fleet operations (Leadership skill)")
        print(f"  • Flying and exploration (Piloting skill)")
        
    # TESTING PHYSICAL COMMUNICATION SYSTEM
    if key == 'w' and not paused:
        # Test war declaration system
        print("\n⚔️ TESTING WAR DECLARATION SYSTEM")
        result = physical_communication.declare_war(
            declaring_faction="Terran Federation",
            target_faction="Mars Republic", 
            declaration_text="Mars Republic has violated trade agreements and territorial boundaries."
        )
        if result:
            print("📜 War declaration letters are being dispatched by courier ships!")
        else:
            print("❌ War declaration failed!")
            
    if key == 'e' and not paused:
        # Test letter sending system
        if len(planets) >= 2:
            sender = planets[0]
            recipient = planets[1]
            physical_communication.send_letter(
                sender_planet=sender,
                recipient_planet=recipient,
                letter_type=MessageType.DIPLOMATIC_LETTER,
                subject="Trade Proposal",
                content="We propose a mutual trade agreement for the benefit of both our peoples.",
                urgency=UrgencyLevel.NORMAL
            )
            print(f"📨 Test letter sent from {sender.name} to {recipient.name}")
        else:
            print("❌ Need at least 2 planets for letter test!")
            
    if key == 'q' and not paused:
        # Show communication system status
        print("\n📡 PHYSICAL COMMUNICATION SYSTEM STATUS")
        print(f"Active Letter Ships: {len(unified_transport_system.message_ships)}")
        print(f"Active Rumors: {len(physical_communication.word_of_mouth_pool)}")
        
        # Show planets with mail/news
        planets_with_mail = 0
        planets_with_news = 0
        for planet_name in physical_communication.planetary_mailboxes:
            if physical_communication.planetary_mailboxes[planet_name]:
                planets_with_mail += 1
        for planet_name in physical_communication.planetary_news:
            if physical_communication.planetary_news[planet_name]:
                planets_with_news += 1
                
        print(f"Planets with Mail: {planets_with_mail}")
        print(f"Planets with News/Rumors: {planets_with_news}")
        
        if physical_communication.word_of_mouth_pool:
            print("\n💬 ACTIVE RUMORS:")
            for rumor in physical_communication.word_of_mouth_pool[:3]:  # Show first 3
                age_str = f"{rumor.age_hours:.1f}h old"
                accuracy_str = f"{rumor.current_accuracy:.0%} accurate"
                spread_str = f"spread to {len(rumor.visited_planets)} planets"
                print(f"   • {rumor.content[:40]}... ({age_str}, {accuracy_str}, {spread_str})")
        
def show_economic_info(planet_name):
    """Display detailed economic information about a planet"""
    planet_info = market_system.get_planet_info(planet_name)
    if not planet_info:
        print(f"❌ No economic data for {planet_name}")
        return
        
    print(f"\n📊 ECONOMIC REPORT: {planet_name}")
    print(f"Population: {planet_info['population']:,}")
    print(f"Type: {planet_info['type'].title()}")
    print(f"Blockaded: {'YES' if planet_info['blockaded'] else 'NO'}")
    if planet_info['blockaded']:
        print(f"Blockade Duration: {planet_info['blockade_days']} days")
        
    print("\n📦 STOCKPILES:")
    economy = market_system.planet_economies[planet_name]
    for commodity, amount in sorted(planet_info['stockpiles'].items()):
        consumption = economy.daily_consumption.get(commodity, 0)
        production = economy.daily_production.get(commodity, 0)
        
        # Calculate days of supply
        if consumption > 0:
            days_supply = amount / consumption
            supply_status = f"({days_supply:.1f} days)"
        else:
            supply_status = "(not consumed)"
            
        # Show production/consumption balance
        if production > consumption:
            balance = f"+{production - consumption}/day"
        elif consumption > production:
            balance = f"-{consumption - production}/day"
        else:
            balance = "balanced"
            
        print(f"  {commodity}: {amount} {supply_status} {balance}")
        
    print(f"\n💰 Current market prices:")
    for commodity in ['food', 'technology', 'minerals', 'luxury_goods']:
        buy_price = market_system.get_buy_price(planet_name, commodity)
        sell_price = market_system.get_sell_price(planet_name, commodity)
        available = market_system.get_available_supply(planet_name, commodity)
        print(f"  {commodity}: Buy {buy_price}, Sell {sell_price}, Available: {available}")
    
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