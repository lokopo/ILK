#!/usr/bin/env python3
"""
ILK Space Game - Playable Headless Mode
A fully playable text-based version of the 3D space game with all core mechanics.
"""

import os
import sys
import logging
import random
import math
import json
import time
from dataclasses import dataclass
from typing import List, Dict, Optional

# Setup logging
verbose = os.environ.get('GAME_VERBOSE', '0') == '1'
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Import game components
try:
    from headless_game_test import Vec3, MarketSystem, PersonalSkill, CharacterDevelopment, FleetManager, CapturedShip, ShipClass
    logger.info("🚀 Loading ILK Space Game - Text Mode...")
except ImportError as e:
    print(f"❌ Failed to load game components: {e}")
    sys.exit(1)

# Simple Enhanced Features for playable mode
class SimpleEnhancedFeatures:
    def __init__(self):
        self.fleet_manager = FleetManager()
        self.character_development = CharacterDevelopment()

@dataclass
class PlayerState:
    """Player's current state in the game"""
    name: str
    position: Vec3
    velocity: Vec3
    credits: int
    fuel: float
    max_fuel: float
    cargo: Dict[str, int]
    max_cargo: int
    health: int
    max_health: int
    level: int
    experience: int
    current_planet: Optional[str]

@dataclass
class GamePlanet:
    """A planet in the game world"""
    name: str
    position: Vec3
    planet_type: str
    population: int
    description: str
    has_trading_post: bool
    has_fuel_station: bool
    has_shipyard: bool
    discovered: bool
    economy: Optional[object]

class PlayableSpaceGame:
    """Main playable headless space game"""
    
    def __init__(self):
        self.running = False
        self.game_time = 0.0
        self.day = 1
        
        # Initialize game world
        self.planets = self.generate_galaxy()
        self.market_system = MarketSystem()
        self.enhanced_features = SimpleEnhancedFeatures()
        
        # Initialize player
        self.player = PlayerState(
            name="Captain",
            position=Vec3(0, 0, 0),
            velocity=Vec3(0, 0, 0),
            credits=1000,
            fuel=100.0,
            max_fuel=100.0,
            cargo={},
            max_cargo=50,
            health=100,
            max_health=100,
            level=1,
            experience=0,
            current_planet=None
        )
        
        # Setup economies for planets
        for planet in self.planets:
            self.market_system.generate_market_for_planet(planet.name, planet.planet_type)
            planet.economy = self.market_system.planet_economies[planet.name]
        
        logger.info("🌌 Galaxy initialized with %d planets", len(self.planets))
        
    def generate_galaxy(self) -> List[GamePlanet]:
        """Generate a galaxy of planets"""
        planets = []
        planet_types = ["agricultural", "industrial", "mining", "tech", "luxury", "desert", "ice", "volcanic"]
        
        # Generate 15 planets in a 3D space
        for i in range(15):
            angle = (i / 15) * 2 * math.pi
            distance = random.uniform(50, 200)
            height = random.uniform(-30, 30)
            
            x = math.cos(angle) * distance
            z = math.sin(angle) * distance
            y = height
            
            planet_type = random.choice(planet_types)
            planet = GamePlanet(
                name=f"Planet {chr(65 + i)}-{random.randint(100, 999)}",
                position=Vec3(x, y, z),
                planet_type=planet_type,
                population=random.randint(100000, 5000000),
                description=self.generate_planet_description(planet_type),
                has_trading_post=random.random() > 0.3,
                has_fuel_station=random.random() > 0.4,
                has_shipyard=random.random() > 0.7,
                discovered=False,
                economy=None
            )
            planets.append(planet)
        
        # Make starting planet discovered
        if planets:
            planets[0].discovered = True
            
        return planets
    
    def generate_planet_description(self, planet_type: str) -> str:
        """Generate a description for a planet based on its type"""
        descriptions = {
            "agricultural": "Vast green fields and farming complexes stretch across the surface. The air smells of fresh crops.",
            "industrial": "Massive factories and refineries dominate the landscape. Smoke stacks reach toward the sky.",
            "mining": "Strip mines and excavation sites cover the planet. Rich mineral deposits gleam in the rock.",
            "tech": "Gleaming cities with advanced technology. Holographic displays and flying vehicles are common.",
            "luxury": "Opulent resorts and entertainment districts. This is where the wealthy come to relax.",
            "desert": "Endless sand dunes and rocky outcroppings. Water is scarce but precious minerals abound.",
            "ice": "Frozen tundra and ice sheets cover the surface. Aurora-like phenomena dance in the sky.",
            "volcanic": "Active volcanoes and lava flows. The ground is rich in rare minerals but dangerous."
        }
        return descriptions.get(planet_type, "A mysterious world with unknown characteristics.")
    
    def show_status(self):
        """Display current player status"""
        print("\n" + "="*60)
        print(f"👨‍🚀 CAPTAIN {self.player.name.upper()}")
        print("="*60)
        print(f"📍 Position: ({self.player.position.x:.1f}, {self.player.position.y:.1f}, {self.player.position.z:.1f})")
        print(f"💰 Credits: {self.player.credits:,}")
        print(f"⛽ Fuel: {self.player.fuel:.1f}/{self.player.max_fuel:.1f}")
        print(f"❤️  Health: {self.player.health}/{self.player.max_health}")
        print(f"📦 Cargo: {sum(self.player.cargo.values())}/{self.player.max_cargo}")
        print(f"🏆 Level: {self.player.level} (XP: {self.player.experience})")
        print(f"📅 Day: {self.day}")
        
        if self.player.current_planet:
            print(f"🌍 Current Planet: {self.player.current_planet}")
        
        if self.player.cargo:
            print("\n📦 CARGO HOLD:")
            for item, quantity in self.player.cargo.items():
                print(f"   {item}: {quantity}")
        
        print("="*60)
    
    def show_galaxy_map(self):
        """Show discovered planets and distances"""
        print("\n🌌 GALAXY MAP")
        print("="*50)
        print("Discovered Planets:")
        
        discovered_planets = [p for p in self.planets if p.discovered]
        
        for planet in discovered_planets:
            distance = (planet.position - self.player.position).length()
            status = "🌍 [CURRENT]" if self.player.current_planet == planet.name else f"📏 {distance:.1f} units"
            print(f"  {planet.name} ({planet.planet_type}) - {status}")
        
        print(f"\nTotal discovered: {len(discovered_planets)}/{len(self.planets)}")
        print("="*50)
    
    def scan_for_planets(self):
        """Scan for nearby undiscovered planets"""
        print("\n🔍 SCANNING FOR PLANETS...")
        
        scan_range = 75.0
        found_any = False
        
        for planet in self.planets:
            if not planet.discovered:
                distance = (planet.position - self.player.position).length()
                if distance <= scan_range:
                    planet.discovered = True
                    found_any = True
                    print(f"📡 Discovered: {planet.name} ({planet.planet_type})")
                    print(f"   Distance: {distance:.1f} units")
                    print(f"   Population: {planet.population:,}")
                    print(f"   {planet.description}")
                    
                    # Gain experience for discovery
                    self.gain_experience(50)
        
        if not found_any:
            print("❌ No new planets detected in range (75 units)")
            print("💡 Try moving to a different location and scanning again")
    
    def move_to_planet(self, planet_name: str):
        """Move to a specific planet"""
        planet = next((p for p in self.planets if p.name.lower() == planet_name.lower() and p.discovered), None)
        
        if not planet:
            print(f"❌ Planet '{planet_name}' not found or not discovered")
            return False
        
        # Calculate fuel cost
        distance = (planet.position - self.player.position).length()
        fuel_cost = distance * 0.1  # 0.1 fuel per unit distance
        
        if fuel_cost > self.player.fuel:
            print(f"❌ Insufficient fuel! Need {fuel_cost:.1f}, have {self.player.fuel:.1f}")
            print("💡 Find a fuel station or refuel at a planet")
            return False
        
        # Make the journey
        print(f"🚀 Traveling to {planet.name}...")
        print(f"📏 Distance: {distance:.1f} units")
        print(f"⛽ Fuel cost: {fuel_cost:.1f}")
        
        self.player.position = planet.position
        self.player.fuel -= fuel_cost
        self.player.current_planet = None  # In space near planet
        
        print(f"✅ Arrived at {planet.name}")
        print(f"🌍 {planet.description}")
        
        # Show available facilities
        facilities = []
        if planet.has_trading_post:
            facilities.append("🏪 Trading Post")
        if planet.has_fuel_station:
            facilities.append("⛽ Fuel Station")
        if planet.has_shipyard:
            facilities.append("🔧 Shipyard")
        
        if facilities:
            print(f"🏢 Available facilities: {', '.join(facilities)}")
        else:
            print("🏜️ No facilities available on this planet")
        
        self.gain_experience(20)
        return True
    
    def land_on_planet(self):
        """Land on the nearest planet"""
        # Find closest planet
        closest_planet = None
        closest_distance = float('inf')
        
        for planet in self.planets:
            if planet.discovered:
                distance = (planet.position - self.player.position).length()
                if distance < closest_distance:
                    closest_distance = distance
                    closest_planet = planet
        
        if not closest_planet or closest_distance > 5.0:
            print("❌ No planet close enough to land (must be within 5 units)")
            print("💡 Use 'move <planet_name>' to get closer to a planet first")
            return False
        
        print(f"🛬 Landing on {closest_planet.name}...")
        self.player.current_planet = closest_planet.name
        print(f"✅ Successfully landed on {closest_planet.name}")
        print(f"🌍 {closest_planet.description}")
        
        # Refuel and repair if available
        if closest_planet.has_fuel_station and self.player.fuel < self.player.max_fuel:
            fuel_needed = self.player.max_fuel - self.player.fuel
            fuel_cost = int(fuel_needed * 2)  # 2 credits per fuel unit
            
            if self.player.credits >= fuel_cost:
                print(f"⛽ Auto-refueling... Cost: {fuel_cost} credits")
                self.player.fuel = self.player.max_fuel
                self.player.credits -= fuel_cost
            else:
                print(f"💰 Cannot afford full refuel (need {fuel_cost} credits)")
        
        return True
    
    def open_trading_post(self):
        """Open trading interface"""
        if not self.player.current_planet:
            print("❌ You must be landed on a planet to trade")
            return
        
        planet = next(p for p in self.planets if p.name == self.player.current_planet)
        
        if not planet.has_trading_post:
            print("❌ This planet has no trading post")
            return
        
        print(f"\n🏪 TRADING POST - {planet.name}")
        print("="*40)
        
        # Show available commodities
        economy = planet.economy
        commodities = ["food", "minerals", "technology", "luxury_goods", "medicine", "weapons", "fuel"]
        
        print("AVAILABLE COMMODITIES:")
        for i, commodity in enumerate(commodities, 1):
            available = economy.get_available_supply(commodity)
            buy_price = economy.get_buy_price(commodity)
            sell_price = economy.get_sell_price(commodity)
            
            player_has = self.player.cargo.get(commodity, 0)
            
            print(f"{i}. {commodity.title()}")
            print(f"   Buy: {buy_price} credits (Stock: {available})")
            print(f"   Sell: {sell_price} credits (You have: {player_has})")
        
        print("\nCommands: buy <item> <qty>, sell <item> <qty>, exit")
        
        while True:
            choice = input("Trade> ").strip().lower()
            
            if choice == "exit":
                break
            elif choice.startswith("buy "):
                self.handle_buy_command(choice, commodities, economy)
            elif choice.startswith("sell "):
                self.handle_sell_command(choice, commodities, economy)
            else:
                print("❌ Invalid command. Use: buy <item> <qty>, sell <item> <qty>, or exit")
    
    def handle_buy_command(self, command: str, commodities: List[str], economy):
        """Handle buy command"""
        try:
            parts = command.split()
            item_name = parts[1]
            quantity = int(parts[2])
            
            # Find matching commodity
            commodity = None
            for c in commodities:
                if c.startswith(item_name):
                    commodity = c
                    break
            
            if not commodity:
                print(f"❌ Unknown item: {item_name}")
                return
            
            # Check availability
            available = economy.get_available_supply(commodity)
            if quantity > available:
                print(f"❌ Not enough {commodity} available (only {available})")
                return
            
            # Check cargo space
            cargo_used = sum(self.player.cargo.values())
            if cargo_used + quantity > self.player.max_cargo:
                print(f"❌ Not enough cargo space (need {quantity}, have {self.player.max_cargo - cargo_used})")
                return
            
            # Check credits
            price = economy.get_buy_price(commodity)
            total_cost = price * quantity
            
            if total_cost > self.player.credits:
                print(f"❌ Not enough credits (need {total_cost}, have {self.player.credits})")
                return
            
            # Execute trade
            self.player.credits -= total_cost
            self.player.cargo[commodity] = self.player.cargo.get(commodity, 0) + quantity
            economy.trade_transaction(commodity, quantity, True)
            
            print(f"✅ Bought {quantity} {commodity} for {total_cost} credits")
            self.gain_experience(5 * quantity)
            
        except (IndexError, ValueError):
            print("❌ Invalid command format. Use: buy <item> <quantity>")
    
    def handle_sell_command(self, command: str, commodities: List[str], economy):
        """Handle sell command"""
        try:
            parts = command.split()
            item_name = parts[1]
            quantity = int(parts[2])
            
            # Find matching commodity
            commodity = None
            for c in commodities:
                if c.startswith(item_name):
                    commodity = c
                    break
            
            if not commodity:
                print(f"❌ Unknown item: {item_name}")
                return
            
            # Check if player has enough
            player_has = self.player.cargo.get(commodity, 0)
            if quantity > player_has:
                print(f"❌ You don't have enough {commodity} (have {player_has})")
                return
            
            # Execute trade
            price = economy.get_sell_price(commodity)
            total_earnings = price * quantity
            
            self.player.credits += total_earnings
            self.player.cargo[commodity] -= quantity
            if self.player.cargo[commodity] == 0:
                del self.player.cargo[commodity]
            
            economy.trade_transaction(commodity, quantity, False)
            
            print(f"✅ Sold {quantity} {commodity} for {total_earnings} credits")
            self.gain_experience(3 * quantity)
            
        except (IndexError, ValueError):
            print("❌ Invalid command format. Use: sell <item> <quantity>")
    
    def gain_experience(self, amount: int):
        """Gain experience and check for level up"""
        self.player.experience += amount
        
        # Level up check (100 XP per level)
        next_level_xp = self.player.level * 100
        if self.player.experience >= next_level_xp:
            self.player.level += 1
            self.player.max_health += 10
            self.player.health = self.player.max_health
            self.player.max_cargo += 5
            self.player.max_fuel += 10
            print(f"🎉 LEVEL UP! You are now level {self.player.level}")
            print(f"   +10 Health, +5 Cargo, +10 Fuel capacity")
    
    def show_help(self):
        """Show available commands"""
        print("\n📚 SPACE GAME COMMANDS:")
        print("="*40)
        print("🚀 MOVEMENT:")
        print("  status           - Show player status")
        print("  map              - Show galaxy map")
        print("  scan             - Scan for planets")
        print("  move <planet>    - Travel to planet")
        print("  land             - Land on nearest planet")
        print("  takeoff          - Take off from planet")
        print("")
        print("💰 TRADING:")
        print("  trade            - Open trading post")
        print("  cargo            - Show cargo hold")
        print("")
        print("🚢 FLEET:")
        print("  fleet            - Show fleet status")
        print("  character        - Show character development")
        print("")
        print("🎮 GAME:")
        print("  save             - Save game")
        print("  load             - Load game")
        print("  time             - Advance time")
        print("  help             - Show this help")
        print("  quit             - Exit game")
        print("="*40)
    
    def save_game(self):
        """Save the current game state"""
        save_data = {
            "player": {
                "name": self.player.name,
                "position": [self.player.position.x, self.player.position.y, self.player.position.z],
                "credits": self.player.credits,
                "fuel": self.player.fuel,
                "max_fuel": self.player.max_fuel,
                "cargo": self.player.cargo,
                "max_cargo": self.player.max_cargo,
                "health": self.player.health,
                "max_health": self.player.max_health,
                "level": self.player.level,
                "experience": self.player.experience,
                "current_planet": self.player.current_planet
            },
            "game_time": self.game_time,
            "day": self.day,
            "discovered_planets": [p.name for p in self.planets if p.discovered]
        }
        
        try:
            with open("spacegame_save.json", "w") as f:
                json.dump(save_data, f, indent=2)
            print("✅ Game saved successfully!")
        except Exception as e:
            print(f"❌ Failed to save game: {e}")
    
    def load_game(self):
        """Load a saved game state"""
        try:
            with open("spacegame_save.json", "r") as f:
                save_data = json.load(f)
            
            # Restore player state
            p = save_data["player"]
            self.player.name = p["name"]
            self.player.position = Vec3(p["position"][0], p["position"][1], p["position"][2])
            self.player.credits = p["credits"]
            self.player.fuel = p["fuel"]
            self.player.max_fuel = p["max_fuel"]
            self.player.cargo = p["cargo"]
            self.player.max_cargo = p["max_cargo"]
            self.player.health = p["health"]
            self.player.max_health = p["max_health"]
            self.player.level = p["level"]
            self.player.experience = p["experience"]
            self.player.current_planet = p["current_planet"]
            
            # Restore game state
            self.game_time = save_data["game_time"]
            self.day = save_data["day"]
            
            # Restore discovered planets
            discovered_names = save_data["discovered_planets"]
            for planet in self.planets:
                planet.discovered = planet.name in discovered_names
            
            print("✅ Game loaded successfully!")
            
        except FileNotFoundError:
            print("❌ No save file found")
        except Exception as e:
            print(f"❌ Failed to load game: {e}")
    
    def advance_time(self):
        """Advance game time and update world"""
        self.day += 1
        self.game_time += 1.0
        
        print(f"⏰ Time advances... Day {self.day}")
        
        # Update market economies
        self.market_system.daily_economic_update()
        
        # Random events
        if random.random() < 0.1:  # 10% chance
            self.random_event()
    
    def random_event(self):
        """Trigger a random event"""
        events = [
            "📰 News: Trade prices fluctuating due to market instability",
            "🌟 Discovery: Scientists report unusual energy readings in distant sectors",
            "⚠️ Warning: Increased pirate activity reported in outer systems",
            "💰 Market: Luxury goods in high demand due to wealthy tourism",
            "🔧 Technology: New fuel efficiency improvements available"
        ]
        
        event = random.choice(events)
        print(f"📢 {event}")
    
    def run(self):
        """Main game loop"""
        print("🚀 ILK SPACE GAME - TEXT MODE")
        print("="*50)
        print("Welcome to the galaxy, Captain!")
        print("Type 'help' for commands, 'quit' to exit")
        print("="*50)
        
        self.running = True
        
        while self.running:
            try:
                command = input("\nCommand> ").strip().lower()
                
                if command == "quit" or command == "exit":
                    break
                elif command == "help":
                    self.show_help()
                elif command == "status":
                    self.show_status()
                elif command == "map":
                    self.show_galaxy_map()
                elif command == "scan":
                    self.scan_for_planets()
                elif command.startswith("move "):
                    planet_name = command[5:].strip()
                    self.move_to_planet(planet_name)
                elif command == "land":
                    self.land_on_planet()
                elif command == "takeoff":
                    if self.player.current_planet:
                        self.player.current_planet = None
                        print("🚀 Taking off from planet...")
                    else:
                        print("❌ You're not landed on a planet")
                elif command == "trade":
                    self.open_trading_post()
                elif command == "cargo":
                    if self.player.cargo:
                        print("\n📦 CARGO HOLD:")
                        for item, qty in self.player.cargo.items():
                            print(f"   {item}: {qty}")
                    else:
                        print("📦 Cargo hold is empty")
                elif command == "fleet":
                    fleet = self.enhanced_features.fleet_manager.fleet
                    if fleet:
                        print(f"\n🚢 FLEET STATUS ({len(fleet)} ships):")
                        for i, ship in enumerate(fleet, 1):
                            print(f"{i}. {ship.name} ({ship.ship_class.value}) - {ship.condition*100:.0f}%")
                    else:
                        print("🚢 No ships in fleet")
                elif command == "character":
                    char = self.enhanced_features.character_development
                    print(f"\n👤 CHARACTER DEVELOPMENT:")
                    print(f"Age: {int(char.age)} years old")
                    print(f"Years Active: {char.years_active:.1f}")
                    for skill, level in char.skills.items():
                        print(f"  {skill.value}: {level:.1f}")
                elif command == "save":
                    self.save_game()
                elif command == "load":
                    self.load_game()
                elif command == "time":
                    self.advance_time()
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n🛑 Game interrupted")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("👋 Thanks for playing ILK Space Game!")
        return 0

def main():
    """Main entry point"""
    try:
        game = PlayableSpaceGame()
        return game.run()
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())