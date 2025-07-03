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

# Transport System Imports
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

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
        """Process daily production, consumption, and trade effects"""
        
        # 1. PRODUCTION PHASE
        for commodity, amount in self.daily_production.items():
            production = amount
            
            # Blockades reduce production efficiency
            if self.blockaded:
                production = int(production * (0.5 - min(0.4, self.blockade_days * 0.05)))
                
            self.stockpiles[commodity] += production
            
        # 2. CONSUMPTION PHASE
        for commodity, amount in self.daily_consumption.items():
            consumption = amount
            
            # Starvation effects - increase consumption of scarce goods
            if self.stockpiles[commodity] < consumption * 3:  # Less than 3 days supply
                consumption = int(consumption * 1.2)  # Panic buying
                
            # Can't consume more than available
            actual_consumption = min(consumption, self.stockpiles[commodity])
            self.stockpiles[commodity] -= actual_consumption
            
            # Track shortages for realistic pricing
            if actual_consumption < consumption:
                if consumption > 0:  # Prevent division by zero
                    shortage_ratio = actual_consumption / consumption
                    print(f"{self.planet_name} experiencing {commodity} shortage! ({shortage_ratio:.1%} of needs met)")
                else:
                    print(f"{self.planet_name} experiencing {commodity} shortage! (No consumption data)")
                
        # 3. BLOCKADE EFFECTS
        if self.blockaded:
            self.blockade_days += 1
            # Increased consumption due to hoarding and waste
            for commodity in self.stockpiles:
                waste = int(self.stockpiles[commodity] * 0.02)  # 2% daily waste during blockade
                self.stockpiles[commodity] = max(0, self.stockpiles[commodity] - waste)
        else:
            self.blockade_days = 0
            
        # 4. RESET DAILY TRADE TRACKING
        self.trade_volume_today = {}
        
    def get_available_supply(self, commodity):
        """How much of this commodity can be purchased"""
        stockpile = self.stockpiles.get(commodity, 0)
        
        # Don't sell below strategic reserves (10 days consumption)
        consumption = self.daily_consumption.get(commodity, 0)
        strategic_reserve = consumption * 10
        
        return max(0, stockpile - strategic_reserve)
        
    def get_buy_price(self, commodity):
        """Calculate realistic buy price based on supply/demand"""
        base_commodity = market_system.commodities.get(commodity)
        if not base_commodity:
            return 0
            
        base_price = base_commodity.base_price
        
        # Supply factor
        available = self.get_available_supply(commodity)
        consumption = self.daily_consumption.get(commodity, 1)
        
        if available <= 0:
            supply_factor = 5.0  # Extreme scarcity
        elif available < consumption * 5:  # Less than 5 days supply
            if consumption > 0:  # Prevent division by zero
                supply_factor = 2.0 + (5 - available/consumption) * 0.5
            else:
                supply_factor = 5.0  # Treat as extreme scarcity
        elif available < consumption * 15:  # Less than 15 days supply
            if consumption > 0:  # Prevent division by zero
                supply_factor = 1.0 + (15 - available/consumption) * 0.1
            else:
                supply_factor = 1.0  # Default supply factor
        else:
            supply_factor = 0.8  # Abundant supply
            
        # Demand factor (production surplus = lower prices)
        production = self.daily_production.get(commodity, 0)
        if production > consumption:
            demand_factor = 0.7  # Surplus = cheap
        else:
            demand_factor = 1.2  # Deficit = expensive
            
        # Blockade factor
        blockade_factor = 1.0 + (self.blockade_days * 0.1) if self.blockaded else 1.0
        
        # Planet type modifier
        planet_modifiers = {
            "agricultural": {"food": 0.6, "technology": 1.4, "minerals": 1.2, "luxury_goods": 1.3},
            "industrial": {"minerals": 0.8, "technology": 0.7, "food": 1.5, "weapons": 0.8},
            "mining": {"minerals": 0.5, "fuel": 0.6, "technology": 1.6, "food": 1.4},
            "tech": {"technology": 0.6, "medicine": 0.7, "minerals": 1.3, "food": 1.3},
            "luxury": {"luxury_goods": 0.7, "spices": 0.6, "food": 1.2, "technology": 1.2}
        }
        
        planet_factor = planet_modifiers.get(self.planet_type, {}).get(
            base_commodity.category, 1.0)
            
        final_price = base_price * supply_factor * demand_factor * blockade_factor * planet_factor
        return max(1, int(final_price))
        
    def get_sell_price(self, commodity):
        """Price planet pays when buying from player"""
        buy_price = self.get_buy_price(commodity)
        
        # Higher demand = better sell prices
        available = self.get_available_supply(commodity)
        consumption = self.daily_consumption.get(commodity, 1)
        
        if available <= 0:
            sell_ratio = 0.95  # Desperate for supplies
        elif available < consumption * 3:
            sell_ratio = 0.85  # High demand
        else:
            sell_ratio = 0.75  # Normal demand
            
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
        """Gain experience in a skill"""
        self.experience += amount
        if skill_type in self.skills:
            # Chance to improve skill
            if random.random() < 0.1:  # 10% chance
                self.skills[skill_type] = min(20, self.skills[skill_type] + 1)
                print(f"{self.name} improved their {skill_type} skill!")

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
        if hasattr(self, 'last_position'):
            distance = (current_position - self.last_position).length()
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

# ===== TRANSPORT SYSTEM ENUMS AND DATA STRUCTURES =====

class MessageType(Enum):
    GOODS_REQUEST = "GOODS_REQUEST"
    PAYMENT = "PAYMENT"

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

# Global systems
market_system = MarketSystem()
player_cargo = CargoSystem(max_capacity=50)  # Start with small cargo hold
player_wallet = PlayerWallet(starting_credits=500)
ship_systems = RealisticShipSystems()

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
        # Add landing detection radius
        self.landing_radius = self.scale * 2
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

# ===== TRANSPORT SHIP CLASSES =====

class TransportShip(Entity):
    """Base class for all transport ships"""
    
    def __init__(self, origin_planet, destination_planet, ship_type, **kwargs):
        # Get position from planet objects
        if hasattr(origin_planet, 'position'):
            start_pos = origin_planet.position + Vec3(random.uniform(-10, 10), random.uniform(-5, 5), random.uniform(-10, 10))
        else:
            start_pos = Vec3(0, 0, 0)
            
        super().__init__(
            model='cube',
            position=start_pos,
            **kwargs
        )
        
        self.origin = origin_planet
        self.destination = destination_planet
        self.ship_type = ship_type
        self.delivered = False
        self.encounter_triggered = False
        
    def update(self):
        if self.delivered:
            return
            
        # Move toward destination
        if hasattr(self.destination, 'position'):
            direction = (self.destination.position - self.position).normalized()
            speed = getattr(self, 'speed', 10.0)
            self.position += direction * speed * time.dt
            
            # Check if arrived
            if (self.position - self.destination.position).length() < 5:
                self.on_arrival()
                
        # Check for player encounters
        self.check_player_encounter()
                
    def check_player_encounter(self):
        """Check if player is near this ship"""
        if hasattr(scene_manager, 'space_controller') and scene_manager.space_controller:
            player_pos = scene_manager.space_controller.position
            distance = (self.position - player_pos).length()
            
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
        destroy(self)

class MessageShip(TransportShip):
    """Ship carrying messages between planets"""
    
    def __init__(self, origin_planet, destination_planet, message_type, payload):
        super().__init__(
            origin_planet, 
            destination_planet, 
            "MESSAGE",
            color=color.cyan,
            scale=(0.5, 0.2, 0.8)
        )
        
        self.message_type = message_type
        self.payload = payload
        self.speed = 15.0
        
        print(f"📨 Message ship launched: {getattr(origin_planet, 'name', 'Unknown')} → {getattr(destination_planet, 'name', 'Unknown')}")
        
    def on_arrival(self):
        """Deliver message to destination"""
        if hasattr(self.destination, 'enhanced_economy') and self.destination.enhanced_economy:
            self.destination.enhanced_economy.receive_message(self.message_type, self.payload)
            
        print(f"📬 Message delivered to {getattr(self.destination, 'name', 'Unknown')}")
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
        
        # Spawn payment ship
        if hasattr(self, 'contract_value') and self.contract_value > 0:
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
            
            # Remove the cargo ship
            if 'unified_transport_system' in globals() and cargo_ship in unified_transport_system.cargo_ships:
                unified_transport_system.cargo_ships.remove(cargo_ship)
                destroy(cargo_ship)
                
            # Return to base with stolen goods
            self.hunting_mode = False
            
            # Share intelligence with other pirates
            self.share_intelligence(cargo_ship)
            
        else:
            print(f"⚔️ Cargo ship fought off pirate attack!")
            self.hunting_mode = False
            
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
        """Assess needs and send procurement messages"""
        needs = self.calculate_needs()
        
        for commodity, request in needs.items():
            # Don't spam requests
            if commodity not in self.outgoing_requests or time.time() - self.outgoing_requests[commodity] > 120:
                self.send_procurement_message(request)
                self.outgoing_requests[commodity] = time.time()
                
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
                    
            if requesting_planet:
                # Create cargo ship
                cargo_manifest = {commodity: can_supply}
                cargo_ship = CargoShip(
                    self.planet_object,
                    requesting_planet,
                    cargo_manifest
                )
                unified_transport_system.cargo_ships.append(cargo_ship)
                
                # Remove goods from stockpile
                self.stockpiles[commodity] -= can_supply
                
                # Track expected delivery
                current_expected = requesting_planet.enhanced_economy.expected_deliveries.get(commodity, 0)
                requesting_planet.enhanced_economy.expected_deliveries[commodity] = current_expected + can_supply
                
                print(f"📦 {self.planet_name} shipping {can_supply} {commodity} to {request.requesting_planet}")
                
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
        """Decide whether to launch raiders based on needs and intelligence"""
        critical_needs = []
        for commodity, consumption in self.daily_consumption.items():
            current_stock = self.stockpiles.get(commodity, 0)
            days_remaining = current_stock / consumption if consumption > 0 else float('inf')
            
            if days_remaining < 20:
                critical_needs.append(commodity)
                
        if critical_needs or random.random() < 0.4:  # 40% chance of opportunistic raiding
            self.launch_raider(critical_needs)
            
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
        planet.color = color.dark_red
        print(f"🏴‍☠️ {planet.name} has become a pirate base!")
        return True

# Create global unified transport system
unified_transport_system = UnifiedTransportSystemManager()

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

# Create systems
random_event_system = RandomEventSystem()
combat_system = CombatSystem()
faction_system = FactionSystem()
crew_system = CrewSystem()
time_system = TimeSystem()
mission_system = MissionSystem()

# Initialize enhanced economies after planets are created
initialize_enhanced_economies()

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
    
    # Update unified transport system
    unified_transport_system.update()
    
    # Update planet economies
    for planet in planets:
        if hasattr(planet, 'enhanced_economy') and planet.enhanced_economy:
            planet.enhanced_economy.update()

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
                    if planet_name not in market_system.planet_economies:
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