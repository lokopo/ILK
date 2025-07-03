#!/usr/bin/env python3
"""
PIRATE TRANSPORT SYSTEM for ILK Space Game

Extends the realistic transport system with pirate-specific mechanics:
- Pirate bases with actual supply needs
- Raider ships that target real cargo based on intelligence
- Contraband smuggling networks
- Black market payment systems
- Intelligence sharing between pirate groups

ADD THIS CODE AFTER THE MAIN TRANSPORT SYSTEM PATCH
"""

# ===== PIRATE TRANSPORT EXTENSIONS =====

from enum import Enum
from dataclasses import dataclass
import random
import time

class ContrabandType(Enum):
    STOLEN_GOODS = "STOLEN_GOODS"
    WEAPONS = "WEAPONS" 
    ILLEGAL_TECH = "ILLEGAL_TECH"
    NARCOTICS = "NARCOTICS"
    SLAVES = "SLAVES"

class PirateMessageType(Enum):
    RAID_INTELLIGENCE = "RAID_INTELLIGENCE"
    CONTRABAND_REQUEST = "CONTRABAND_REQUEST"
    FENCE_PAYMENT = "FENCE_PAYMENT"
    TERRITORY_WARNING = "TERRITORY_WARNING"

@dataclass
class CargoIntelligence:
    """Intelligence about cargo ships for pirate targeting"""
    ship_id: str
    origin_planet: str
    destination_planet: str
    cargo_manifest: dict
    estimated_value: float
    escort_level: str  # "NONE", "LIGHT", "HEAVY"
    route_danger: float
    intel_timestamp: float

@dataclass
class RaidRequest:
    """Request for pirate raiders to target specific cargo"""
    target_commodity: str
    min_cargo_value: float
    preferred_routes: list
    payment_offered: float
    urgency: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    requesting_base: str

@dataclass
class ContrabandOrder:
    """Order for contraband goods"""
    contraband_type: ContrabandType
    quantity: int
    max_price: float
    drop_location: str
    payment_method: str  # "CREDITS", "BARTER", "SERVICES"
    requesting_contact: str

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
        self.speed = 10.0  # Fast raiders
        self.weapons_rating = random.randint(20, 50)
        self.crew_size = random.randint(4, 12)
        self.cargo_stolen = {}
        self.raid_range = 200  # How far they'll hunt
        
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
        if hasattr(transport_system, 'cargo_ships'):
            for cargo_ship in transport_system.cargo_ships:
                if not hasattr(cargo_ship, 'position'):
                    continue
                    
                distance = (self.position - cargo_ship.position).length()
                
                if distance < self.raid_range:
                    # Check if this cargo ship matches our target intelligence
                    if self.should_attack_cargo_ship(cargo_ship):
                        self.attack_cargo_ship(cargo_ship)
                        return
                        
        # If no targets found, patrol randomly
        self.patrol_movement()
        
    def should_attack_cargo_ship(self, cargo_ship):
        """Decide whether to attack this cargo ship"""
        # If we have specific intelligence, target matching ships
        if self.target_intelligence:
            intel = self.target_intelligence
            
            # Check if cargo matches intelligence
            if hasattr(cargo_ship, 'cargo'):
                for commodity in intel.cargo_manifest:
                    if commodity in cargo_ship.cargo:
                        return True
                        
        # Otherwise, attack valuable cargo
        if hasattr(cargo_ship, 'contract_value'):
            return cargo_ship.contract_value > 500  # Only attack valuable cargo
            
        return False
    
    def attack_cargo_ship(self, cargo_ship):
        """Attack and rob cargo ship"""
        print(f"🏴‍☠️ PIRATE ATTACK!")
        print(f"Raider attacking cargo ship: {cargo_ship.get_cargo_description()}")
        
        # Calculate attack success based on weapons and crew
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
            if cargo_ship in transport_system.cargo_ships:
                transport_system.cargo_ships.remove(cargo_ship)
                destroy(cargo_ship)
                
            # Create supply chain disruption
            self.create_supply_disruption(cargo_ship)
            
            # Return to base with stolen goods
            self.hunting_mode = False
            
            # Generate intelligence for other pirates
            self.share_intelligence(cargo_ship)
            
        else:
            # Failed raid
            print(f"⚔️ Cargo ship fought off pirate attack!")
            # Raider retreats
            self.hunting_mode = False
            
    def patrol_movement(self):
        """Random patrol movement when no targets found"""
        # Simple random movement around current position
        random_offset = Vec3(
            random.uniform(-5, 5),
            random.uniform(-5, 5), 
            random.uniform(-5, 5)
        )
        self.position += random_offset * time.dt
        
    def create_supply_disruption(self, destroyed_cargo_ship):
        """Create real economic consequences from successful piracy"""
        if hasattr(destroyed_cargo_ship, 'destination') and hasattr(destroyed_cargo_ship.destination, 'economy'):
            destination_economy = destroyed_cargo_ship.destination.economy
            
            # Mark expected delivery as failed
            for commodity, quantity in destroyed_cargo_ship.cargo.items():
                current_expected = destination_economy.expected_deliveries.get(commodity, 0)
                destination_economy.expected_deliveries[commodity] = max(0, current_expected - quantity)
                
                print(f"📉 {destroyed_cargo_ship.destination.name} supply disruption: -{quantity} {commodity}")
                
    def share_intelligence(self, cargo_ship):
        """Share intelligence about cargo routes with other pirate bases"""
        intelligence = CargoIntelligence(
            ship_id=f"CARGO-{time.time()}",
            origin_planet=getattr(cargo_ship.origin, 'name', 'Unknown'),
            destination_planet=getattr(cargo_ship.destination, 'name', 'Unknown'),
            cargo_manifest=cargo_ship.cargo.copy(),
            estimated_value=cargo_ship.contract_value,
            escort_level="NONE",  # TODO: Add escort detection
            route_danger=0.3,  # Medium danger route
            intel_timestamp=time.time()
        )
        
        # Send intelligence to other pirate bases
        pirate_bases = self.find_nearby_pirate_bases()
        for base in pirate_bases:
            if hasattr(base, 'economy') and hasattr(base.economy, 'receive_intelligence'):
                base.economy.receive_intelligence(intelligence)
                
    def find_nearby_pirate_bases(self):
        """Find other pirate bases to share intelligence with"""
        pirate_bases = []
        
        if 'planets' in globals():
            for planet in planets:
                if hasattr(planet, 'economy') and isinstance(planet.economy, PirateBaseEconomy):
                    distance = (self.position - planet.position).length()
                    if distance < 500:  # Share intel within 500 units
                        pirate_bases.append(planet)
                        
        return pirate_bases
        
    def return_to_base(self):
        """Return stolen goods to pirate base"""
        self.delivered = True
        
        if hasattr(self.pirate_base, 'economy') and hasattr(self.pirate_base.economy, 'receive_stolen_goods'):
            self.pirate_base.economy.receive_stolen_goods(self.cargo_stolen)
            
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

class SmugglerShip(TransportShip):
    """Ship that transports contraband goods"""
    
    def __init__(self, origin_base, destination_contact, contraband_manifest):
        super().__init__(
            origin_base,
            destination_contact,
            "SMUGGLER",
            color=color.violet,
            scale=(0.8, 0.4, 1.5)
        )
        
        self.contraband = contraband_manifest.copy()
        self.speed = 12.0  # Fast but not as fast as raiders
        self.stealth_rating = random.randint(30, 70)
        self.detection_risk = 0.1  # 10% base chance of detection
        
        print(f"🚭 Smuggler launched: {getattr(origin_base, 'name', 'Unknown')} → {getattr(destination_contact, 'name', 'Unknown')}")
        print(f"   Contraband: {self.get_contraband_description()}")
        
    def update(self):
        """Move while avoiding detection"""
        super().update()
        
        # Check for law enforcement encounters
        if random.random() < self.detection_risk * time.dt:
            self.law_enforcement_encounter()
            
    def get_contraband_description(self):
        """Get description of contraband cargo"""
        if not self.contraband:
            return "Empty"
        items = []
        for contraband_type, quantity in self.contraband.items():
            items.append(f"{quantity} {contraband_type}")
        return ", ".join(items)
        
    def law_enforcement_encounter(self):
        """Handle encounter with law enforcement"""
        print(f"🚔 Law enforcement scanning smuggler ship!")
        
        # Calculate detection success
        detection_chance = 0.5 - (self.stealth_rating / 200)
        
        if random.random() < detection_chance:
            print(f"🚨 CONTRABAND DETECTED! Smuggler ship intercepted!")
            # Ship destroyed, contraband lost
            if self in transport_system.cargo_ships:  # Smugglers tracked as cargo ships
                transport_system.cargo_ships.remove(self)
            destroy(self)
        else:
            print(f"🤐 Smuggler evaded detection")
            
    def on_arrival(self):
        """Deliver contraband"""
        if hasattr(self.destination, 'economy') and hasattr(self.destination.economy, 'receive_contraband'):
            self.destination.economy.receive_contraband(self.contraband)
            
        print(f"🚭 Contraband delivered to {getattr(self.destination, 'name', 'Unknown')}")
        
        # Spawn payment through black market
        payment_value = self.calculate_contraband_value()
        if payment_value > 0:
            # Send payment through fence network
            fence_payment = FencePayment(self.destination, self.origin, payment_value)
            pirate_transport_system.fence_payments.append(fence_payment)
            
        super().on_arrival()
        
    def calculate_contraband_value(self):
        """Calculate value of contraband cargo"""
        contraband_prices = {
            ContrabandType.STOLEN_GOODS: 50,
            ContrabandType.WEAPONS: 100,
            ContrabandType.ILLEGAL_TECH: 200,
            ContrabandType.NARCOTICS: 150,
            ContrabandType.SLAVES: 300
        }
        
        total_value = 0
        for contraband_type, quantity in self.contraband.items():
            if isinstance(contraband_type, str):
                # Convert string to enum if needed
                try:
                    contraband_type = ContrabandType(contraband_type)
                except:
                    continue
                    
            base_price = contraband_prices.get(contraband_type, 75)
            total_value += base_price * quantity
            
        return int(total_value * random.uniform(0.8, 1.4))  # Market variation

class FencePayment(TransportShip):
    """Underground payment through fence networks"""
    
    def __init__(self, origin_contact, destination_base, credits):
        super().__init__(
            origin_contact,
            destination_base,
            "FENCE",
            color=color.brown,
            scale=(0.6, 0.3, 0.8)
        )
        
        self.credits = credits
        self.speed = 8.0  # Slower, more careful
        self.detection_risk = 0.05  # Lower detection risk than smugglers
        
        print(f"💰 Fence payment: {getattr(origin_contact, 'name', 'Unknown')} → {getattr(destination_base, 'name', 'Unknown')} ({credits} credits)")
        
    def update(self):
        """Move payment while avoiding law enforcement"""
        super().update()
        
        # Lower detection risk than smugglers
        if random.random() < self.detection_risk * time.dt:
            print(f"🚔 Fence payment intercepted by authorities!")
            self.credits = 0  # Money confiscated
            
    def on_arrival(self):
        """Deliver payment to pirate base"""
        if hasattr(self.destination, 'economy') and hasattr(self.destination.economy, 'credits'):
            self.destination.economy.credits += self.credits
            
        print(f"💰 Fence payment delivered: {self.credits} credits")
        super().on_arrival()

class PirateBaseEconomy(RealisticPlanetEconomy):
    """Economy for pirate bases with contraband and raiding needs"""
    
    def __init__(self, base_name, base_type="pirate_hideout"):
        super().__init__(base_name, base_type)
        
        # Pirate-specific stockpiles
        self.contraband_stockpiles = {}
        self.intelligence_cache = []
        self.raid_requests = {}
        self.last_raid_launch = 0
        self.raid_interval = 90  # Launch raiders every 90 seconds
        
        # Override standard economy with pirate needs
        self.initialize_pirate_economy()
        
    def initialize_pirate_economy(self):
        """Set up pirate base economy"""
        # Pirates need weapons, fuel, food, and stolen goods
        self.daily_production = {
            "weapons": 20,  # Pirate armories produce some weapons
        }
        
        self.daily_consumption = {
            "food": 50,
            "fuel": 30,
            "weapons": 10,
            "medicine": 15
        }
        
        # Starting stockpiles
        self.stockpiles = {
            "food": 200,
            "fuel": 150,
            "weapons": 100,
            "medicine": 50
        }
        
        # Contraband stockpiles
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
            
        # Process contraband orders
        self.process_contraband_orders()
        
        # Share intelligence with other pirate bases
        self.share_intelligence_network()
        
    def consider_launching_raiders(self):
        """Decide whether to launch raiders based on needs and intelligence"""
        # Check if we need supplies
        critical_needs = []
        for commodity, consumption in self.daily_consumption.items():
            current_stock = self.stockpiles.get(commodity, 0)
            days_remaining = current_stock / consumption if consumption > 0 else float('inf')
            
            if days_remaining < 20:  # Pirates plan raids when low on supplies
                critical_needs.append(commodity)
                
        if critical_needs or random.random() < 0.3:  # Always some chance of opportunistic raiding
            self.launch_raider(critical_needs)
            
    def launch_raider(self, target_commodities=None):
        """Launch a pirate raider"""
        # Look for intelligence about valuable cargo
        target_intel = self.select_raid_target(target_commodities)
        
        raider = PirateRaider(
            pirate_base=self.planet_object if hasattr(self, 'planet_object') else None,
            target_intelligence=target_intel
        )
        
        pirate_transport_system.raiders.append(raider)
        
    def select_raid_target(self, needed_commodities=None):
        """Select the best raid target from intelligence cache"""
        if not self.intelligence_cache:
            return None
            
        best_target = None
        best_score = 0
        
        for intel in self.intelligence_cache:
            score = intel.estimated_value
            
            # Bonus score for needed commodities
            if needed_commodities:
                for commodity in needed_commodities:
                    if commodity in intel.cargo_manifest:
                        score *= 2
                        
            # Penalty for old intelligence
            age_hours = (time.time() - intel.intel_timestamp) / 3600
            if age_hours > 24:  # Intelligence expires after 24 hours
                continue
                
            score *= max(0.1, 1 - (age_hours / 24))
            
            if score > best_score:
                best_score = score
                best_target = intel
                
        return best_target
        
    def receive_intelligence(self, intelligence):
        """Receive intelligence about cargo ships"""
        self.intelligence_cache.append(intelligence)
        
        # Keep cache size manageable
        if len(self.intelligence_cache) > 50:
            # Remove oldest intelligence
            self.intelligence_cache.sort(key=lambda x: x.intel_timestamp)
            self.intelligence_cache = self.intelligence_cache[-30:]
            
        print(f"🕵️ {self.planet_name} received intelligence: {intelligence.cargo_manifest} worth {intelligence.estimated_value}")
        
    def receive_stolen_goods(self, stolen_cargo):
        """Receive stolen goods from successful raids"""
        for commodity, quantity in stolen_cargo.items():
            # Add to regular stockpiles
            current = self.stockpiles.get(commodity, 0)
            self.stockpiles[commodity] = current + quantity
            
            # Also add to contraband stockpiles
            if ContrabandType.STOLEN_GOODS in self.contraband_stockpiles:
                self.contraband_stockpiles[ContrabandType.STOLEN_GOODS] += quantity
                
        print(f"📦 {self.planet_name} received stolen goods: {stolen_cargo}")
        
    def receive_contraband(self, contraband_cargo):
        """Receive contraband from smuggler deliveries"""
        for contraband_type, quantity in contraband_cargo.items():
            if isinstance(contraband_type, str):
                try:
                    contraband_type = ContrabandType(contraband_type)
                except:
                    continue
                    
            current = self.contraband_stockpiles.get(contraband_type, 0)
            self.contraband_stockpiles[contraband_type] = current + quantity
            
        print(f"🚭 {self.planet_name} received contraband: {contraband_cargo}")
        
    def process_contraband_orders(self):
        """Handle contraband trade orders"""
        # Check if we have contraband to sell
        for contraband_type, quantity in self.contraband_stockpiles.items():
            if quantity > 10:  # Only sell when we have surplus
                self.find_contraband_buyers(contraband_type, quantity)
                
    def find_contraband_buyers(self, contraband_type, available_quantity):
        """Find buyers for contraband goods"""
        # For now, create random demand
        if random.random() < 0.1:  # 10% chance per update cycle
            # Find underground contacts (other pirate bases, criminal planets)
            buyers = self.find_underground_contacts()
            
            if buyers:
                buyer = random.choice(buyers)
                sell_quantity = min(available_quantity // 2, random.randint(1, 10))
                
                if sell_quantity > 0:
                    # Launch smuggler to deliver contraband
                    smuggler = SmugglerShip(
                        self.planet_object if hasattr(self, 'planet_object') else None,
                        buyer,
                        {contraband_type: sell_quantity}
                    )
                    
                    pirate_transport_system.smugglers.append(smuggler)
                    
                    # Remove contraband from stockpile
                    self.contraband_stockpiles[contraband_type] -= sell_quantity
                    
    def find_underground_contacts(self):
        """Find other criminal organizations to trade with"""
        contacts = []
        
        if 'planets' in globals():
            for planet in planets:
                if hasattr(planet, 'economy'):
                    # Other pirate bases
                    if isinstance(planet.economy, PirateBaseEconomy) and planet.name != self.planet_name:
                        contacts.append(planet)
                    # Criminal-friendly planets (add faction check here)
                    elif hasattr(planet.economy, 'criminal_tolerance') and planet.economy.criminal_tolerance > 0.5:
                        contacts.append(planet)
                        
        return contacts
        
    def share_intelligence_network(self):
        """Share intelligence with allied pirate bases"""
        if random.random() < 0.1 and self.intelligence_cache:  # 10% chance to share intel
            allied_bases = self.find_allied_pirate_bases()
            
            if allied_bases:
                # Share recent valuable intelligence
                recent_intel = [intel for intel in self.intelligence_cache 
                              if time.time() - intel.intel_timestamp < 3600]  # Last hour
                
                if recent_intel:
                    intel_to_share = random.choice(recent_intel)
                    target_base = random.choice(allied_bases)
                    
                    # Send intelligence message
                    message_ship = MessageShip(
                        self.planet_object if hasattr(self, 'planet_object') else None,
                        target_base,
                        PirateMessageType.RAID_INTELLIGENCE,
                        intel_to_share
                    )
                    
                    pirate_transport_system.intelligence_messages.append(message_ship)
                    
    def find_allied_pirate_bases(self):
        """Find allied pirate bases for intelligence sharing"""
        allies = []
        
        if 'planets' in globals():
            for planet in planets:
                if hasattr(planet, 'economy') and isinstance(planet.economy, PirateBaseEconomy):
                    if planet.name != self.planet_name:
                        allies.append(planet)
                        
        return allies

class PirateTransportManager:
    """Manager for pirate-specific transport operations"""
    
    def __init__(self):
        self.raiders = []
        self.smugglers = []
        self.fence_payments = []
        self.intelligence_messages = []
        
    def update(self):
        """Update all pirate transport operations"""
        all_pirate_ships = (self.raiders + self.smugglers + 
                           self.fence_payments + self.intelligence_messages)
        
        for ship in all_pirate_ships[:]:
            if hasattr(ship, 'update'):
                ship.update()
                
            # Remove delivered ships
            if hasattr(ship, 'delivered') and ship.delivered:
                if ship in self.raiders:
                    self.raiders.remove(ship)
                elif ship in self.smugglers:
                    self.smugglers.remove(ship)
                elif ship in self.fence_payments:
                    self.fence_payments.remove(ship)
                elif ship in self.intelligence_messages:
                    self.intelligence_messages.remove(ship)
                    
    def get_pirate_statistics(self):
        """Get pirate transport statistics"""
        return {
            'active_raiders': len(self.raiders),
            'active_smugglers': len(self.smugglers),
            'fence_payments': len(self.fence_payments),
            'intelligence_messages': len(self.intelligence_messages),
            'total_pirate_ships': len(self.raiders) + len(self.smugglers) + len(self.fence_payments) + len(self.intelligence_messages)
        }
        
    def create_pirate_base(self, planet_name):
        """Convert a planet to a pirate base"""
        pirate_economy = PirateBaseEconomy(planet_name)
        return pirate_economy

# Create global pirate transport system
pirate_transport_system = PirateTransportManager()

# INTEGRATION INSTRUCTIONS:
# 
# 1. Add this code after the main transport system patch
# 
# 2. In the main update() function, add:
#    pirate_transport_system.update()
#
# 3. Create some pirate bases by replacing planet economies:
#    for planet in planets:
#        if "pirate" in planet.name.lower() or planet.planet_type == "pirate_base":
#            planet.economy = PirateBaseEconomy(planet.name)
#            planet.economy.planet_object = planet
#
# 4. Add pirate statistics to UI:
#    pirate_stats = pirate_transport_system.get_pirate_statistics()
#    self.pirate_text.text = f"Pirates: {pirate_stats['total_pirate_ships']} (R:{pirate_stats['active_raiders']} S:{pirate_stats['active_smugglers']})"

print("🏴‍☠️ Pirate Transport System loaded!")
print("Pirates now have realistic supply chains, raiding operations, and contraband networks!")
print("They'll target real cargo ships based on intelligence and need supplies like any other faction.")