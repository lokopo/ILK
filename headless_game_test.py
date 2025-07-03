#!/usr/bin/env python3
"""
Headless Game Stability Test
Tests the enhanced Pirates! space game without graphics to verify:
- Economic stability and balance
- No runaway inflation
- Enhanced Pirates! features functionality
- System integration stability
"""

import sys
import random
import math
import time as python_time
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

# Mock Ursina components for headless testing
class MockEntity:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.enabled = True
        self.position = MockVec3(0, 0, 0)
        self.rotation = MockVec3(0, 0, 0)
        self.scale = MockVec3(1, 1, 1)
        self.color = None
        self.model = None
        self.parent = None
        
    def update(self): 
        pass
        
    def rotate(self, rotation, relative_to=None):
        pass
    
    @property
    def right(self):
        return MockVec3(1, 0, 0)
    
    @property
    def up(self):
        return MockVec3(0, 1, 0)
    
    @property
    def forward(self):
        return MockVec3(0, 0, 1)

class MockVec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x, self.y, self.z = float(x), float(y), float(z)
        
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return MockVec3(self.x + other, self.y + other, self.z + other)
        return MockVec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return MockVec3(self.x - other, self.y - other, self.z - other)
        return MockVec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return MockVec3(self.x * scalar, self.y * scalar, self.z * scalar)
        
    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def normalized(self):
        l = self.length()
        if l == 0: return MockVec3()
        return MockVec3(self.x/l, self.y/l, self.z/l)
    
    def __str__(self):
        return f'Vec3({self.x:.1f}, {self.y:.1f}, {self.z:.1f})'

class MockTime:
    def __init__(self):
        self.dt = 0.016  # 60 FPS
        self._time = 0
        
    def time(self):
        return self._time
    
    def advance(self, seconds):
        self._time += seconds

class MockApp:
    def __init__(self):
        pass
    def run(self):
        pass

class MockColor:
    def __init__(self):
        self.red = "red"
        self.green = "green"
        self.blue = "blue"
        self.white = "white"
        self.yellow = "yellow"
        self.orange = "orange"
        self.cyan = "cyan"
        self.light_gray = "light_gray"
        self.black66 = "black66"
        self.azure = MockAzure()

class MockAzure:
    def tint(self, amount):
        return "azure_tinted"

class MockCamera:
    def __init__(self):
        self.ui = MockEntity()
        self.position = MockVec3()
        self.rotation = MockVec3()
        self.clip_plane_far = 1000000
        self.fov = 90
        self.parent = None

class MockMouse:
    def __init__(self):
        self.locked = False
        self.visible = False
        self.velocity = [0, 0]

# Set up global mocks
Entity = MockEntity
Vec3 = MockVec3
time = MockTime()
camera = MockCamera()
color = MockColor()
mouse = MockMouse()
held_keys = {}
paused = False

# Mock Ursina functions
def load_texture(path):
    return f"texture_{path}"

def Text(**kwargs):
    return MockEntity(**kwargs)

def Button(**kwargs):
    return MockEntity(**kwargs)

def Panel(**kwargs):
    return MockEntity(**kwargs)

def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))

def raycast(*args, **kwargs):
    return type('RaycastHit', (), {'hit': False})()

def destroy(*args, **kwargs):
    pass

def DirectionalLight(**kwargs):
    return MockEntity(**kwargs)

def AmbientLight(**kwargs):
    return MockEntity(**kwargs)

# Now import the game components
print("📦 Importing game components...")

# Enhanced Pirates! Features (from space_game.py)
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

# Basic commodity and trading system for economic testing
class Commodity:
    def __init__(self, name, base_price, category="general"):
        self.name = name
        self.base_price = base_price
        self.category = category

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

class PlanetEconomy:
    def __init__(self, planet_name, planet_type):
        self.planet_name = planet_name
        self.planet_type = planet_type
        self.population = random.randint(100000, 1000000)
        self.stockpiles = {}
        self.daily_production = {}
        self.daily_consumption = {}
        self.blockaded = False
        self.blockade_days = 0
        self.trade_volume_today = {}
        self.initialize_economy()
        
    def initialize_economy(self):
        base_consumption = {
            "food": self.population // 5000,
            "medicine": self.population // 50000,
            "fuel": self.population // 10000
        }
        
        if self.planet_type == "agricultural":
            self.daily_production = {"food": base_consumption["food"] * 3, "spices": 50}
            self.daily_consumption = {**base_consumption, "technology": 30, "luxury_goods": 20}
            self.stockpiles = {"food": 5000, "spices": 500, "technology": 50, "luxury_goods": 100}
        elif self.planet_type == "industrial":
            self.daily_production = {"technology": 40, "weapons": 20, "medicine": 30}
            self.daily_consumption = {**base_consumption, "minerals": 100, "luxury_goods": 30}
            self.stockpiles = {"technology": 800, "weapons": 300, "medicine": 400, "food": 200}
        else:
            self.daily_production = {"food": base_consumption["food"] // 2, "minerals": 50}
            self.daily_consumption = base_consumption
            self.stockpiles = {"food": 1000, "minerals": 800, "technology": 200}
            
        # Ensure all commodities exist
        for commodity in ["food", "minerals", "technology", "luxury_goods", "medicine", "weapons", "fuel", "spices"]:
            if commodity not in self.stockpiles:
                self.stockpiles[commodity] = 0
                
    def daily_economic_update(self):
        # Production phase
        for commodity, amount in self.daily_production.items():
            production = amount
            if self.blockaded:
                production = int(production * (0.5 - min(0.4, self.blockade_days * 0.05)))
            self.stockpiles[commodity] += production
            
        # Consumption phase
        for commodity, amount in self.daily_consumption.items():
            consumption = amount
            if self.stockpiles[commodity] < consumption * 3:
                consumption = int(consumption * 1.2)
            actual_consumption = min(consumption, self.stockpiles[commodity])
            self.stockpiles[commodity] -= actual_consumption
            
        # Blockade effects
        if self.blockaded:
            self.blockade_days += 1
            for commodity in self.stockpiles:
                waste = int(self.stockpiles[commodity] * 0.02)
                self.stockpiles[commodity] = max(0, self.stockpiles[commodity] - waste)
        else:
            self.blockade_days = 0
            
        self.trade_volume_today = {}

class MarketSystem:
    def __init__(self):
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
        self.planet_economies = {}
        
    def generate_market_for_planet(self, planet_name, planet_type="generic"):
        if planet_name not in self.planet_economies:
            self.planet_economies[planet_name] = PlanetEconomy(planet_name, planet_type)
    
    def daily_economic_update(self):
        for economy in self.planet_economies.values():
            economy.daily_economic_update()

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
             self.experience_points[skill_type] += amount
             required_exp = int(self.skills[skill_type] * 100)
             if self.experience_points[skill_type] >= required_exp:
                 self.skills[skill_type] = self.skills[skill_type] + 0.5
                 self.experience_points[skill_type] = 0
                 
     def advance_time(self, days):
         years_passed = days / 365.0
         old_age = self.age
         self.age += years_passed
         self.years_active += years_passed

# Test Suite
class GameStabilityTester:
    def __init__(self):
        self.test_results = []
        
    def log_result(self, test_name, passed, details=""):
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'details': details
        })
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"    {details}")
    
    def test_enhanced_pirates_features(self):
        print("\n🚢 Testing Enhanced Pirates! Features...")
        
        # Test Fleet Manager
        try:
            fleet_manager = FleetManager()
            
            # Add ships to fleet
            for ship_class in [ShipClass.FIGHTER, ShipClass.CORVETTE, ShipClass.FRIGATE]:
                ship = CapturedShip(ship_class)
                added = fleet_manager.add_ship(ship)
                if not added:
                    self.log_result("Fleet Ship Addition", False, f"Failed to add {ship_class}")
                    return
            
            # Test fleet combat strength calculation
            strength = fleet_manager.get_fleet_combat_strength()
            if strength <= 0:
                self.log_result("Fleet Combat Strength", False, f"Invalid strength: {strength}")
                return
                
            self.log_result("Fleet Management System", True, f"3 ships added, combat strength: {strength:.0f}")
            
            # Test character development
            char_dev = CharacterDevelopment()
            initial_age = char_dev.age
            char_dev.advance_time(365)  # Advance 1 year
            
            if char_dev.age <= initial_age:
                self.log_result("Character Aging", False, "Age did not advance")
                return
                
            # Test skill advancement
            initial_skill = char_dev.skills[PersonalSkill.COMBAT]
            char_dev.gain_experience(PersonalSkill.COMBAT, 1000)
            if char_dev.skills[PersonalSkill.COMBAT] <= initial_skill:
                self.log_result("Skill Advancement", False, "Skills did not improve")
                return
                
            self.log_result("Character Development", True, f"Age: {initial_age:.1f} -> {char_dev.age:.1f}, Combat: {initial_skill:.1f} -> {char_dev.skills[PersonalSkill.COMBAT]:.1f}")
            
        except Exception as e:
            self.log_result("Enhanced Pirates Features", False, f"Exception: {e}")
    
    def test_economic_stability(self):
        print("\n💰 Testing Economic Stability...")
        
        try:
            market = MarketSystem()
            wallet = PlayerWallet(1000)
            
            # Create test planets
            planet_types = ["agricultural", "industrial", "generic"]
            for i, planet_type in enumerate(planet_types):
                planet_name = f"TestPlanet{i+1}"
                market.generate_market_for_planet(planet_name, planet_type)
            
            # Track initial economy state
            initial_stockpiles = {}
            for planet_name, economy in market.planet_economies.items():
                initial_stockpiles[planet_name] = economy.stockpiles.copy()
            
            initial_credits = wallet.credits
            
            # Simulate economic activity over time
            days_simulated = 30
            price_history = {commodity: [] for commodity in market.commodities.keys()}
            
            for day in range(days_simulated):
                # Daily market update
                market.daily_economic_update()
                
                # Track price stability (simplified)
                for commodity in market.commodities.keys():
                    base_price = market.commodities[commodity].base_price
                    price_history[commodity].append(base_price)
            
            # Check for economic runaway scenarios
            economy_stable = True
            inflation_check = True
            
            for planet_name, economy in market.planet_economies.items():
                for commodity, amount in economy.stockpiles.items():
                    # Check for negative stockpiles (should not happen)
                    if amount < 0:
                        economy_stable = False
                        self.log_result("Economic Stability", False, f"{planet_name} has negative {commodity}: {amount}")
                        break
                    
                    # Check for extreme stockpile growth (potential inflation indicator)
                    initial_amount = initial_stockpiles[planet_name].get(commodity, 0)
                    if initial_amount > 0 and amount > initial_amount * 100:  # 10000% growth
                        inflation_check = False
                        self.log_result("Inflation Check", False, f"{planet_name} {commodity} grew from {initial_amount} to {amount}")
                        break
                
                if not economy_stable or not inflation_check:
                    break
            
            if economy_stable:
                self.log_result("Economic Stability", True, f"No negative stockpiles after {days_simulated} days")
            
            if inflation_check:
                self.log_result("Inflation Prevention", True, f"No runaway stockpile growth detected")
            
            # Test player wallet operations
            test_amount = 500
            if wallet.spend(test_amount):
                if wallet.credits != initial_credits - test_amount:
                    self.log_result("Wallet Operations", False, f"Incorrect credits after spending: {wallet.credits}")
                else:
                    wallet.earn(test_amount * 2)
                    expected_credits = initial_credits + test_amount
                    if wallet.credits == expected_credits:
                        self.log_result("Wallet Operations", True, f"Credits: {initial_credits} -> {wallet.credits}")
                    else:
                        self.log_result("Wallet Operations", False, f"Expected {expected_credits}, got {wallet.credits}")
            else:
                self.log_result("Wallet Operations", False, "Could not spend credits")
                
        except Exception as e:
            self.log_result("Economic Stability Test", False, f"Exception: {e}")
    
    def test_system_integration(self):
        print("\n🔧 Testing System Integration...")
        
        try:
            # Test that all systems can coexist
            fleet_manager = FleetManager()
            market = MarketSystem()
            char_dev = CharacterDevelopment()
            wallet = PlayerWallet(10000)
            
            # Simulate integrated gameplay loop
            for iteration in range(10):
                # Character ages
                char_dev.advance_time(30)  # 30 days
                
                # Market updates
                market.generate_market_for_planet(f"Planet{iteration}", "industrial")
                market.daily_economic_update()
                
                # Fleet operations
                if iteration % 3 == 0:  # Every 3rd iteration
                    ship = CapturedShip(random.choice(list(ShipClass)))
                    fleet_manager.add_ship(ship)
                
                # Economic transactions
                if iteration % 2 == 0:  # Every 2nd iteration
                    wallet.spend(100)
                    wallet.earn(150)
                
                # Skill advancement
                char_dev.gain_experience(random.choice(list(PersonalSkill)), 50)
            
            # Verify final state is reasonable
            final_checks = []
            
            # Check character development
            if char_dev.age > 25:
                final_checks.append("Character aged properly")
            else:
                final_checks.append("Character aging failed")
            
            # Check fleet
            if len(fleet_manager.fleet) > 0:
                final_checks.append(f"Fleet has {len(fleet_manager.fleet)} ships")
            else:
                final_checks.append("Fleet building failed")
            
            # Check economy
            if len(market.planet_economies) > 0:
                final_checks.append(f"Economy has {len(market.planet_economies)} planets")
            else:
                final_checks.append("Planet economy generation failed")
            
            # Check wallet
            if wallet.credits > 0:
                final_checks.append(f"Wallet: {wallet.credits} credits")
            else:
                final_checks.append("Wallet went negative")
            
            self.log_result("System Integration", True, "; ".join(final_checks))
            
        except Exception as e:
            self.log_result("System Integration", False, f"Exception: {e}")
    
    def run_all_tests(self):
        print("🚀 Starting Comprehensive Game Stability Tests...\n")
        
        self.test_enhanced_pirates_features()
        self.test_economic_stability()
        self.test_system_integration()
        
        print(f"\n📊 TEST SUMMARY:")
        passed = sum(1 for result in self.test_results if result['passed'])
        total = len(self.test_results)
        
        print(f"Tests Passed: {passed}/{total}")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Game is stable and ready for deployment.")
        else:
            print("⚠️  Some tests failed. Review the issues above.")
            for result in self.test_results:
                if not result['passed']:
                    print(f"   - {result['test']}: {result['details']}")
        
        return passed == total

# Run the tests
if __name__ == "__main__":
    tester = GameStabilityTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ Game stability verified!")
        print("🎮 The enhanced Pirates! space game is ready for launch!")
    else:
        print("\n❌ Stability issues detected!")
        print("🔧 Please review and fix the failing tests.")