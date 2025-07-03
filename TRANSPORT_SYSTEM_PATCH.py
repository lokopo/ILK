#!/usr/bin/env python3
"""
TRANSPORT SYSTEM PATCH for ILK Space Game

Add this code to space_game.py to enable realistic physical transport.
This demonstrates the real ship transport system with:
- Message ships carrying requests
- Cargo ships carrying actual goods  
- Payment ships returning credits
- Real supply chain mechanics

INSERT THIS CODE AFTER LINE 400 in space_game.py (after existing economic classes)
"""

# ===== REALISTIC TRANSPORT SYSTEM =====

from enum import Enum
from dataclasses import dataclass

class MessageType(Enum):
    GOODS_REQUEST = "GOODS_REQUEST"
    PAYMENT = "PAYMENT"

class UrgencyLevel(Enum):
    LOW = "LOW"
    NORMAL = "NORMAL" 
    URGENT = "URGENT"
    CRITICAL = "CRITICAL"

@dataclass
class GoodsRequest:
    commodity: str
    quantity: int
    max_price: float
    urgency: UrgencyLevel
    requesting_planet: str

class TransportShip(Entity):
    """Base class for all transport ships"""
    
    def __init__(self, origin_planet, destination_planet, ship_type, **kwargs):
        super().__init__(
            model='cube',
            **kwargs
        )
        
        self.origin = origin_planet
        self.destination = destination_planet
        self.ship_type = ship_type
        self.position = Vec3(origin_planet.position if hasattr(origin_planet, 'position') else (0,0,0))
        self.delivered = False
        
    def update(self):
        if self.delivered:
            return
            
        # Move toward destination
        if hasattr(self.destination, 'position'):
            direction = (self.destination.position - self.position).normalized()
            self.position += direction * self.speed * time.dt
            
            # Check if arrived
            if (self.position - self.destination.position).length() < 5:
                self.on_arrival()
                
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
        if hasattr(self.destination, 'economy') and hasattr(self.destination.economy, 'receive_message'):
            self.destination.economy.receive_message(self.message_type, self.payload)
            
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
        if hasattr(self.destination, 'economy') and hasattr(self.destination.economy, 'stockpiles'):
            for commodity, quantity in self.cargo.items():
                current = self.destination.economy.stockpiles.get(commodity, 0)
                self.destination.economy.stockpiles[commodity] = current + quantity
                
        print(f"✅ Cargo delivered to {getattr(self.destination, 'name', 'Unknown')}: {self.get_cargo_description()}")
        
        # Spawn payment ship
        if hasattr(self, 'contract_value') and self.contract_value > 0:
            payment_ship = PaymentShip(self.destination, self.origin, self.contract_value)
            transport_system.payment_ships.append(payment_ship)
        
        super().on_arrival()
    
    def update(self):
        """Override to add player encounter detection"""
        super().update()
        
        # Check for player encounter
        if not self.delivered and hasattr(scene_manager, 'space_controller') and scene_manager.space_controller:
            player_pos = scene_manager.space_controller.position
            if (self.position - player_pos).length() < 50:
                self.trigger_encounter()
    
    def trigger_encounter(self):
        """Trigger cargo ship encounter with player"""
        if not hasattr(self, 'encounter_triggered'):
            self.encounter_triggered = True
            print(f"\n🚢 CARGO SHIP ENCOUNTER!")
            print(f"Ship from {getattr(self.origin, 'name', 'Unknown')} to {getattr(self.destination, 'name', 'Unknown')}")
            print(f"Cargo: {self.get_cargo_description()}")
            print(f"Value: {self.contract_value} credits")

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
        if hasattr(self.destination, 'economy') and hasattr(self.destination.economy, 'credits'):
            self.destination.economy.credits += self.credits
            
        print(f"💳 Payment delivered to {getattr(self.destination, 'name', 'Unknown')}: {self.credits} credits")
        super().on_arrival()

class RealisticPlanetEconomy:
    """Enhanced planet economy with physical transport"""
    
    def __init__(self, planet_name, planet_type):
        self.planet_name = planet_name
        self.planet_type = planet_type
        self.stockpiles = {}
        self.daily_consumption = {}
        self.daily_production = {}
        self.outgoing_requests = {}
        self.credits = random.randint(10000, 50000)
        
        # Transport timing
        self.last_procurement_check = 0
        self.procurement_interval = 30  # Check every 30 seconds for demo
        
        self.initialize_economy()
        
    def initialize_economy(self):
        """Set up production/consumption based on planet type"""
        economy_templates = {
            "agricultural": {
                "production": {"food": 200, "spices": 50},
                "consumption": {"technology": 30, "minerals": 40},
                "stockpiles": {"food": 2000, "spices": 500, "technology": 100}
            },
            "industrial": {
                "production": {"technology": 100, "weapons": 40}, 
                "consumption": {"food": 180, "fuel": 60},
                "stockpiles": {"technology": 800, "weapons": 300, "food": 600}
            },
            "mining": {
                "production": {"minerals": 300, "fuel": 100},
                "consumption": {"food": 150, "technology": 50},
                "stockpiles": {"minerals": 3000, "fuel": 800, "food": 500}
            }
        }
        
        template = economy_templates.get(self.planet_type, economy_templates["agricultural"])
        
        self.daily_production = template["production"].copy()
        self.daily_consumption = template["consumption"].copy()
        self.stockpiles = template["stockpiles"].copy()
        
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
            if commodity not in self.outgoing_requests or time.time() - self.outgoing_requests[commodity] > 60:
                self.send_procurement_message(request)
                self.outgoing_requests[commodity] = time.time()
                
    def calculate_needs(self):
        """Calculate what goods this planet needs"""
        needs = {}
        
        for commodity, consumption in self.daily_consumption.items():
            if consumption <= 0:
                continue
                
            current_stock = self.stockpiles.get(commodity, 0)
            days_remaining = current_stock / consumption if consumption > 0 else float('inf')
            
            if days_remaining < 30:  # Less than 30 days supply
                urgency = self.determine_urgency(days_remaining)
                quantity_needed = int(consumption * 60 - current_stock)  # Target 60 days supply
                
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
            if hasattr(supplier_planet, 'name') and supplier_planet.name != self.planet_name:
                message_ship = MessageShip(
                    self.planet_object if hasattr(self, 'planet_object') else None,
                    supplier_planet,
                    MessageType.GOODS_REQUEST,
                    request
                )
                transport_system.message_ships.append(message_ship)
                
    def find_suppliers(self, commodity):
        """Find planets that produce this commodity"""
        suppliers = []
        
        # Access global planets list
        if 'planets' in globals():
            for planet in planets:
                if hasattr(planet, 'economy') and planet.economy:
                    production = planet.economy.daily_production.get(commodity, 0)
                    consumption = planet.economy.daily_consumption.get(commodity, 0)
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
            if 'planets' in globals():
                for planet in planets:
                    if hasattr(planet, 'name') and planet.name == request.requesting_planet:
                        requesting_planet = planet
                        break
                        
            if requesting_planet:
                # Create cargo ship
                cargo_manifest = {commodity: can_supply}
                cargo_ship = CargoShip(
                    self.planet_object if hasattr(self, 'planet_object') else None,
                    requesting_planet,
                    cargo_manifest
                )
                transport_system.cargo_ships.append(cargo_ship)
                
                # Remove goods from stockpile
                self.stockpiles[commodity] -= can_supply
                
                print(f"📦 {self.planet_name} shipping {can_supply} {commodity} to {request.requesting_planet}")

class TransportSystemManager:
    """Manager for all transport ships"""
    
    def __init__(self):
        self.message_ships = []
        self.cargo_ships = []
        self.payment_ships = []
        
    def update(self):
        """Update all transport ships"""
        all_ships = self.message_ships + self.cargo_ships + self.payment_ships
        
        for ship in all_ships[:]:  # Copy to avoid modification during iteration
            if hasattr(ship, 'update'):
                ship.update()
                
            # Remove delivered ships
            if hasattr(ship, 'delivered') and ship.delivered:
                if ship in self.message_ships:
                    self.message_ships.remove(ship)
                elif ship in self.cargo_ships:
                    self.cargo_ships.remove(ship)
                elif ship in self.payment_ships:
                    self.payment_ships.remove(ship)
                    
    def get_statistics(self):
        """Get transport statistics"""
        return {
            'message_ships': len(self.message_ships),
            'cargo_ships': len(self.cargo_ships), 
            'payment_ships': len(self.payment_ships),
            'total_ships': len(self.message_ships) + len(self.cargo_ships) + len(self.payment_ships)
        }

# Create global transport system
transport_system = TransportSystemManager()

# INTEGRATION INSTRUCTIONS:
# 
# 1. Add this entire code block to space_game.py after line 400
# 
# 2. In the Planet class __init__ method, replace:
#    market_system.generate_market_for_planet(self.name, self.planet_type)
#    With:
#    self.economy = RealisticPlanetEconomy(self.name, self.planet_type)
#    self.economy.planet_object = self
#
# 3. In the main update() function, add these lines:
#    transport_system.update()
#    for planet in planets:
#        if hasattr(planet, 'economy'):
#            planet.economy.update()
#
# 4. In SpaceController class, add transport statistics display:
#    self.transport_text = Text(
#        parent=camera.ui,
#        text='Ships: 0',
#        position=(-0.45, 0.2),
#        scale=0.8,
#        color=color.white
#    )
#
# 5. In SpaceController.update(), add:
#    stats = transport_system.get_statistics()
#    self.transport_text.text = f"Ships: {stats['total_ships']} (M:{stats['message_ships']} C:{stats['cargo_ships']} P:{stats['payment_ships']})"

print("🚀 Transport System Patch loaded!")
print("Follow integration instructions to activate realistic ship transport.")
print("This will replace abstract economics with physical cargo movement!")