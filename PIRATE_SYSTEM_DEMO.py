#!/usr/bin/env python3
"""
PIRATE TRANSPORT SYSTEM DEMO

This script simulates the pirate transport system behavior for testing
without requiring the full ILK game environment.
"""

import random
import time
from dataclasses import dataclass
from enum import Enum

# Simulate game entities and basic mechanics
class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x, self.y, self.z = float(x), float(y), float(z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __mul__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def normalized(self):
        length = self.length()
        if length == 0:
            return Vec3(0, 0, 0)
        return Vec3(self.x/length, self.y/length, self.z/length)

class MockEntity:
    def __init__(self, name="Entity"):
        self.name = name
        self.position = Vec3(random.uniform(-100, 100), 0, random.uniform(-100, 100))

# Transport system components
class MessageType(Enum):
    GOODS_REQUEST = "GOODS_REQUEST"
    RAID_INTELLIGENCE = "RAID_INTELLIGENCE"

class ContrabandType(Enum):
    STOLEN_GOODS = "STOLEN_GOODS"
    WEAPONS = "WEAPONS"
    ILLEGAL_TECH = "ILLEGAL_TECH"

@dataclass
class CargoIntelligence:
    ship_id: str
    origin_planet: str
    destination_planet: str
    cargo_manifest: dict
    estimated_value: float
    intel_timestamp: float

class CargoShip:
    def __init__(self, origin, destination, cargo_manifest):
        self.origin = origin
        self.destination = destination
        self.cargo = cargo_manifest.copy()
        self.position = Vec3(origin.position.x, origin.position.y, origin.position.z)
        self.contract_value = sum(cargo_manifest.values()) * 10  # Simple value calculation
        self.delivered = False
        self.speed = 8.0
        
    def get_cargo_description(self):
        if not self.cargo:
            return "Empty"
        items = []
        for commodity, quantity in self.cargo.items():
            items.append(f"{quantity} {commodity}")
        return ", ".join(items)
        
    def update(self, dt):
        if self.delivered:
            return
            
        # Move toward destination
        direction = (self.destination.position - self.position).normalized()
        self.position = self.position + direction * (self.speed * dt)
        
        # Check if arrived
        if (self.position - self.destination.position).length() < 5:
            self.delivered = True
            print(f"✅ Cargo delivered to {self.destination.name}: {self.get_cargo_description()}")

class PirateRaider:
    def __init__(self, pirate_base, target_intelligence=None):
        self.pirate_base = pirate_base
        self.target_intelligence = target_intelligence
        self.position = Vec3(pirate_base.position.x, pirate_base.position.y, pirate_base.position.z)
        self.hunting_mode = True
        self.speed = 10.0
        self.weapons_rating = random.randint(20, 50)
        self.crew_size = random.randint(4, 12)
        self.cargo_stolen = {}
        self.raid_range = 200
        self.delivered = False
        
        if target_intelligence:
            print(f"🏴‍☠️ Pirate raider launched from {pirate_base.name}")
            print(f"   Target: {target_intelligence.cargo_manifest} worth {target_intelligence.estimated_value} credits")
        else:
            print(f"🏴‍☠️ Pirate patrol launched from {pirate_base.name}")
            
    def update(self, dt, cargo_ships):
        if self.delivered:
            return
            
        if self.hunting_mode:
            self.hunt_cargo_ships(cargo_ships, dt)
        else:
            # Return to base
            direction = (self.pirate_base.position - self.position).normalized()
            self.position = self.position + direction * (self.speed * dt)
            
            if (self.position - self.pirate_base.position).length() < 5:
                self.return_to_base()
                
    def hunt_cargo_ships(self, cargo_ships, dt):
        # Look for cargo ships in range
        for cargo_ship in cargo_ships:
            if cargo_ship.delivered:
                continue
                
            distance = (self.position - cargo_ship.position).length()
            
            if distance < self.raid_range:
                if self.should_attack_cargo_ship(cargo_ship):
                    self.attack_cargo_ship(cargo_ship, cargo_ships)
                    return
                    
        # Patrol movement
        self.patrol_movement(dt)
        
    def should_attack_cargo_ship(self, cargo_ship):
        # If we have specific intelligence, target matching ships
        if self.target_intelligence:
            intel = self.target_intelligence
            for commodity in intel.cargo_manifest:
                if commodity in cargo_ship.cargo:
                    return True
                    
        # Otherwise, attack valuable cargo
        return cargo_ship.contract_value > 500
    
    def attack_cargo_ship(self, cargo_ship, cargo_ships):
        print(f"🏴‍☠️ PIRATE ATTACK!")
        print(f"Raider attacking cargo ship: {cargo_ship.get_cargo_description()}")
        
        # Calculate attack success
        attack_strength = self.weapons_rating + (self.crew_size * 2)
        defense_strength = 25 + random.randint(10, 30)
        
        success_chance = attack_strength / (attack_strength + defense_strength)
        
        if random.random() < success_chance:
            # Successful raid
            self.cargo_stolen = cargo_ship.cargo.copy()
            stolen_value = cargo_ship.contract_value
            
            print(f"💀 Pirate raid successful! Stolen: {cargo_ship.get_cargo_description()}")
            print(f"   Value: {stolen_value} credits")
            
            # Remove the cargo ship
            cargo_ships.remove(cargo_ship)
            
            # Create supply chain disruption
            print(f"📉 {cargo_ship.destination.name} supply disruption: -{sum(cargo_ship.cargo.values())} units")
            
            # Return to base with stolen goods
            self.hunting_mode = False
            
        else:
            # Failed raid
            print(f"⚔️ Cargo ship fought off pirate attack!")
            self.hunting_mode = False
            
    def patrol_movement(self, dt):
        # Random patrol movement
        random_offset = Vec3(
            random.uniform(-5, 5),
            0,
            random.uniform(-5, 5)
        )
        self.position = self.position + random_offset * dt
        
    def return_to_base(self):
        self.delivered = True
        print(f"🏴‍☠️ Raider returned to {self.pirate_base.name}")
        print(f"   Delivered stolen goods: {self.get_stolen_cargo_description()}")
        
    def get_stolen_cargo_description(self):
        if not self.cargo_stolen:
            return "Nothing"
        items = []
        for commodity, quantity in self.cargo_stolen.items():
            items.append(f"{quantity} {commodity}")
        return ", ".join(items)

class PirateBaseEconomy:
    def __init__(self, base_name):
        self.base_name = base_name
        self.stockpiles = {
            "food": 200,
            "fuel": 150,
            "weapons": 100,
            "medicine": 50
        }
        self.daily_consumption = {
            "food": 50,
            "fuel": 30,
            "weapons": 10,
            "medicine": 15
        }
        self.intelligence_cache = []
        self.last_raid_launch = 0
        self.raid_interval = 30  # Launch raiders every 30 seconds for demo
        
    def update(self, dt):
        current_time = time.time()
        
        # Consume resources
        for commodity, consumption in self.daily_consumption.items():
            per_second = consumption / 300.0  # 1 game day = 5 minutes
            self.stockpiles[commodity] = max(0, self.stockpiles[commodity] - (per_second * dt))
            
        # Launch raiders based on needs
        if current_time - self.last_raid_launch > self.raid_interval:
            if self.should_launch_raider():
                return self.launch_raider()
            self.last_raid_launch = current_time
            
        return None
        
    def should_launch_raider(self):
        # Check if we need supplies
        for commodity, consumption in self.daily_consumption.items():
            current_stock = self.stockpiles.get(commodity, 0)
            days_remaining = current_stock / consumption if consumption > 0 else float('inf')
            
            if days_remaining < 20:  # Launch raids when supplies low
                return True
                
        return random.random() < 0.3  # 30% chance of opportunistic raiding
        
    def launch_raider(self):
        # Look for intelligence about valuable cargo
        target_intel = self.select_raid_target()
        
        raider = PirateRaider(
            pirate_base=MockEntity(self.base_name),
            target_intelligence=target_intel
        )
        
        return raider
        
    def select_raid_target(self):
        if not self.intelligence_cache:
            return None
            
        # Select most valuable recent intelligence
        recent_intel = [intel for intel in self.intelligence_cache 
                       if time.time() - intel.intel_timestamp < 3600]  # Last hour
        
        if recent_intel:
            return max(recent_intel, key=lambda x: x.estimated_value)
        
        return None
        
    def receive_intelligence(self, intelligence):
        self.intelligence_cache.append(intelligence)
        print(f"🕵️ {self.base_name} received intelligence: {intelligence.cargo_manifest} worth {intelligence.estimated_value}")

# Simulation setup
class TransportSimulation:
    def __init__(self):
        # Create planets
        self.agricultural_planet = MockEntity("Agricultural Planet")
        self.mining_planet = MockEntity("Mining Planet") 
        self.tech_planet = MockEntity("Tech Planet")
        self.pirate_base = MockEntity("Pirate Base Skull Island")
        
        # Position planets
        self.agricultural_planet.position = Vec3(-50, 0, 0)
        self.mining_planet.position = Vec3(50, 0, 0)
        self.tech_planet.position = Vec3(0, 0, 50)
        self.pirate_base.position = Vec3(0, 0, -50)
        
        # Create pirate base economy
        self.pirate_economy = PirateBaseEconomy("Pirate Base Skull Island")
        
        # Active ships
        self.cargo_ships = []
        self.raiders = []
        
        # Simulation time
        self.start_time = time.time()
        self.last_cargo_spawn = 0
        self.cargo_spawn_interval = 20  # Spawn cargo every 20 seconds
        
    def spawn_cargo_ship(self):
        # Random cargo route
        routes = [
            (self.agricultural_planet, self.mining_planet, {"food": 150}),
            (self.tech_planet, self.agricultural_planet, {"technology": 50}),
            (self.mining_planet, self.tech_planet, {"minerals": 200}),
        ]
        
        origin, destination, cargo = random.choice(routes)
        cargo_ship = CargoShip(origin, destination, cargo)
        self.cargo_ships.append(cargo_ship)
        
        print(f"🚛 Cargo ship launched: {origin.name} → {destination.name}")
        print(f"   Cargo: {cargo_ship.get_cargo_description()}")
        
        # Generate intelligence for pirates
        intelligence = CargoIntelligence(
            ship_id=f"CARGO-{time.time()}",
            origin_planet=origin.name,
            destination_planet=destination.name,
            cargo_manifest=cargo.copy(),
            estimated_value=cargo_ship.contract_value,
            intel_timestamp=time.time()
        )
        
        # Pirates may observe this cargo ship
        if random.random() < 0.7:  # 70% chance pirates notice
            self.pirate_economy.receive_intelligence(intelligence)
            
    def update(self, dt):
        current_time = time.time()
        
        # Spawn new cargo ships
        if current_time - self.last_cargo_spawn > self.cargo_spawn_interval:
            self.spawn_cargo_ship()
            self.last_cargo_spawn = current_time
            
        # Update pirate base (may launch raiders)
        new_raider = self.pirate_economy.update(dt)
        if new_raider:
            self.raiders.append(new_raider)
            
        # Update cargo ships
        for cargo_ship in self.cargo_ships[:]:
            cargo_ship.update(dt)
            if cargo_ship.delivered:
                self.cargo_ships.remove(cargo_ship)
                
        # Update raiders
        for raider in self.raiders[:]:
            raider.update(dt, self.cargo_ships)
            if raider.delivered:
                self.raiders.remove(raider)
                
        # Display status
        if int(current_time) % 10 == 0 and current_time - self.start_time > 1:  # Every 10 seconds
            self.display_status()
            time.sleep(1)  # Prevent spam
            
    def display_status(self):
        print(f"\n📊 SIMULATION STATUS:")
        print(f"Active Cargo Ships: {len(self.cargo_ships)}")
        print(f"Active Raiders: {len(self.raiders)}")
        print(f"Pirate Base Stockpiles: {self.pirate_economy.stockpiles}")
        print(f"Intelligence Cache: {len(self.pirate_economy.intelligence_cache)} reports")
        print("=" * 50)

def run_simulation():
    """Run the pirate transport system simulation"""
    print("🏴‍☠️ Starting Pirate Transport System Demo")
    print("This simulates realistic pirate behavior with supply chains and intelligence")
    print("=" * 70)
    
    sim = TransportSimulation()
    
    # Run simulation for 5 minutes
    end_time = time.time() + 300  # 5 minutes
    last_update = time.time()
    
    try:
        while time.time() < end_time:
            current_time = time.time()
            dt = current_time - last_update
            last_update = current_time
            
            sim.update(dt)
            time.sleep(0.1)  # 10 FPS simulation
            
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped by user")
        
    print("\n🏁 Simulation completed!")
    print("Final Statistics:")
    print(f"Cargo Ships Active: {len(sim.cargo_ships)}")
    print(f"Raiders Active: {len(sim.raiders)}")
    print(f"Intelligence Reports: {len(sim.pirate_economy.intelligence_cache)}")

if __name__ == "__main__":
    run_simulation()