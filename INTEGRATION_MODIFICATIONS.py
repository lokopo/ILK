#!/usr/bin/env python3
"""
INTEGRATION MODIFICATIONS for space_game.py

Step-by-step instructions to integrate the unified transport system into ILK.

BEFORE STARTING:
1. Make a backup copy of space_game.py
2. Apply these modifications in order
3. Test each step before proceeding

INTEGRATION STEPS:
"""

# ===== STEP 1: ADD IMPORTS =====
# Add these lines after the existing imports in space_game.py (around line 12)

"""
# Transport System Imports
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
"""

# ===== STEP 2: ADD ENUMS AND DATACLASSES =====
# Add these after the existing classes but before Planet class (around line 400)

"""
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
"""

# ===== STEP 3: MODIFY PLANET CLASS =====
# In the Planet.__init__ method, find this line:
# market_system.generate_market_for_planet(self.name, self.planet_type)
# 
# REPLACE IT WITH:
"""
        # Initialize enhanced economy
        self.enhanced_economy = EnhancedPlanetEconomy(self.name, self.planet_type, self)
        
        # Keep existing market system for compatibility
        market_system.generate_market_for_planet(self.name, self.planet_type)
"""

# ===== STEP 4: ADD TRANSPORT SHIP CLASSES =====
# Add these classes after the Planet class (around line 1300)

TRANSPORT_SHIP_CLASSES = '''
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
        encounter_text = f"\\n🚢 SHIP ENCOUNTER!\\n"
        encounter_text += f"Ship Type: {self.ship_type}\\n"
        encounter_text += f"Origin: {getattr(self.origin, 'name', 'Unknown')}\\n"
        encounter_text += f"Destination: {getattr(self.destination, 'name', 'Unknown')}\\n"
        
        if hasattr(self, 'cargo'):
            encounter_text += f"Cargo: {self.get_cargo_description()}\\n"
        if hasattr(self, 'contract_value'):
            encounter_text += f"Value: {self.contract_value} credits\\n"
            
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
        if hasattr(self.destination, 'enhanced_economy'):
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
        if hasattr(self.destination, 'enhanced_economy'):
            for commodity, quantity in self.cargo.items():
                current = self.destination.enhanced_economy.stockpiles.get(commodity, 0)
                self.destination.enhanced_economy.stockpiles[commodity] = current + quantity
                
        print(f"✅ Cargo delivered to {getattr(self.destination, 'name', 'Unknown')}: {self.get_cargo_description()}")
        
        # Spawn payment ship
        if hasattr(self, 'contract_value') and self.contract_value > 0:
            payment_ship = PaymentShip(self.destination, self.origin, self.contract_value)
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
        if hasattr(self.destination, 'enhanced_economy'):
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
            if cargo_ship in unified_transport_system.cargo_ships:
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
        for planet in planets:
            if hasattr(planet, 'enhanced_economy') and isinstance(planet.enhanced_economy, PirateBaseEconomy):
                if (self.position - planet.position).length() < 500:
                    planet.enhanced_economy.receive_intelligence(intelligence)
                
    def return_to_base(self):
        """Return stolen goods to pirate base"""
        self.delivered = True
        
        if hasattr(self.pirate_base, 'enhanced_economy'):
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
'''

# ===== STEP 5: ADD ENHANCED ECONOMY CLASSES =====
# Add these after the transport ship classes

ENHANCED_ECONOMY_CLASSES = '''
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
'''

# ===== STEP 6: ADD TRANSPORT SYSTEM MANAGER =====
# Add this after the economy classes

TRANSPORT_MANAGER_CLASS = '''
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
        if hasattr(planet, 'enhanced_economy'):
            planet.enhanced_economy = PirateBaseEconomy(planet.name, planet)
            planet.planet_type = "pirate_hideout"
            planet.color = color.dark_red
            print(f"🏴‍☠️ {planet.name} has become a pirate base!")
            return True
        return False

# Create global unified transport system
unified_transport_system = UnifiedTransportSystemManager()
'''

# ===== STEP 7: MODIFY SPACE CONTROLLER =====
# In the SpaceController.__init__ method, add these lines after the existing UI text elements:

SPACE_CONTROLLER_ADDITIONS = '''
        # Transport system status display
        self.transport_text = Text(
            parent=camera.ui,
            text='🚢 Ships: 0',
            position=(-0.45, 0.15),
            scale=0.6,
            color=color.cyan
        )
'''

# ===== STEP 8: MODIFY SPACE CONTROLLER UPDATE =====
# In the SpaceController.update() method, add these lines before the end:

SPACE_CONTROLLER_UPDATE_ADDITIONS = '''
        # Update transport status display
        if 'unified_transport_system' in globals():
            stats = unified_transport_system.get_statistics()
            self.transport_text.text = f"🚢 Ships: {stats['total_ships']} | 🚛 Cargo: {stats['cargo_ships']} | 🏴‍☠️ Raiders: {stats['raiders']} | ⚠️ Threat: {stats['pirate_threat_level']}"
'''

# ===== STEP 9: MODIFY MAIN UPDATE FUNCTION =====
# In the main update() function, add these lines before the end:

MAIN_UPDATE_ADDITIONS = '''
    # Update unified transport system
    if 'unified_transport_system' in globals():
        unified_transport_system.update()
        
        # Update planet economies
        for planet in planets:
            if hasattr(planet, 'enhanced_economy'):
                planet.enhanced_economy.update()
'''

# ===== STEP 10: ADD INITIALIZATION FUNCTION =====
# Add this after all the classes and before the main update() function:

INITIALIZATION_FUNCTION = '''
def initialize_enhanced_economies():
    """Initialize enhanced economies for all planets"""
    print("🔄 Initializing enhanced transport system...")
    
    # Convert existing planets to enhanced economy system
    for planet in planets:
        if not hasattr(planet, 'enhanced_economy'):
            planet.enhanced_economy = EnhancedPlanetEconomy(planet.name, planet.planet_type, planet)
            
    # Create some pirate bases
    pirate_base_count = 0
    for planet in planets:
        if random.random() < 0.15 and pirate_base_count < 3:  # 15% chance, max 3 bases
            unified_transport_system.create_pirate_base(planet)
            pirate_base_count += 1
            
    print(f"✅ Enhanced transport system initialized with {pirate_base_count} pirate bases")

# Initialize the system
initialize_enhanced_economies()
'''

# ===== STEP 11: TEST THE INTEGRATION =====
TESTING_INSTRUCTIONS = """
TESTING THE INTEGRATION:

1. Start the game and check for any errors in the console
2. Look for transport system initialization message
3. Watch for transport ships appearing:
   - Cyan cubes = Message ships
   - Orange cubes = Cargo ships  
   - Yellow cubes = Payment ships
   - Dark gray cubes = Pirate raiders
4. Check the transport status display in the upper left
5. Look for console messages about:
   - Message ships launching
   - Cargo ships launching  
   - Pirate attacks
   - Deliveries being made

EXPECTED BEHAVIOR:
- Within 1-2 minutes, you should see message ships launching
- Shortly after, cargo ships should start moving goods
- Pirates should launch raiders periodically
- Real supply chain disruptions from pirate attacks
- Dynamic transport activity based on planet needs

TROUBLESHOOTING:
- If no ships appear, check for errors in console
- If pirates don't appear, wait longer or check pirate base creation
- Transport status should update in real-time
- Ships should be visible as colored cubes moving between planets
"""

print("📋 Integration modifications prepared!")
print("Follow the steps above to integrate the unified transport system into ILK.")
print("This will create a living universe with realistic supply chains and intelligent pirates!")