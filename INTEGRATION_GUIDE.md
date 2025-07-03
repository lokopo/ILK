# Integration Guide: Adding Realistic Transport System to ILK

## Overview

This guide shows how to integrate the realistic physical transport system into the existing ILK space game, replacing the abstract economic simulation with real ships carrying cargo, messages, and payments.

---

## 🔧 **STEP 1: Add Transport Classes to space_game.py**

Add these classes after the existing economic classes (around line 400):

```python
# ===== REALISTIC TRANSPORT SYSTEM =====

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional

class MessageType(Enum):
    GOODS_REQUEST = "GOODS_REQUEST"
    CONTRACT_OFFER = "CONTRACT_OFFER" 
    PAYMENT = "PAYMENT"
    URGENT_REQUEST = "URGENT_REQUEST"

class UrgencyLevel(Enum):
    LOW = "LOW"           # 30+ days supply
    NORMAL = "NORMAL"     # 15-30 days supply
    URGENT = "URGENT"     # 7-15 days supply
    CRITICAL = "CRITICAL" # <7 days supply

@dataclass
class GoodsRequest:
    commodity: str
    quantity: int
    max_price: float
    urgency: UrgencyLevel
    deadline: float
    requesting_planet: str

class MessageShip(Entity):
    """Physical ship that carries messages between planets"""
    
    def __init__(self, origin_planet, destination_planet, message_type, payload):
        super().__init__(
            model='cube',
            color=color.cyan,
            scale=(0.5, 0.2, 0.8)
        )
        
        self.origin = origin_planet
        self.destination = destination_planet
        self.message_type = message_type
        self.payload = payload
        self.position = Vec3(origin_planet.position)
        self.speed = 15.0
        self.delivered = False
        
        print(f"📨 Message ship: {origin_planet.name} → {destination_planet.name}")
        
    def update(self):
        if self.delivered:
            return
            
        # Move toward destination
        direction = (self.destination.position - self.position).normalized()
        self.position += direction * self.speed * time.dt
        
        # Check if arrived
        if (self.position - self.destination.position).length() < 5:
            self.deliver_message()
            
    def deliver_message(self):
        self.delivered = True
        if hasattr(self.destination, 'receive_message'):
            self.destination.receive_message(self.message_type, self.payload)
        print(f"📬 Message delivered to {self.destination.name}")
        destroy(self)

class CargoShip(Entity):
    """Physical ship that transports goods between planets"""
    
    def __init__(self, origin_planet, destination_planet, cargo_manifest):
        super().__init__(
            model='cube',
            color=color.orange,
            scale=(1.2, 0.6, 2.0)
        )
        
        self.origin = origin_planet
        self.destination = destination_planet
        self.cargo = cargo_manifest.copy()
        self.position = Vec3(origin_planet.position)
        self.speed = 8.0
        self.delivered = False
        self.contract_value = self.calculate_cargo_value()
        
        print(f"🚛 Cargo ship: {origin_planet.name} → {destination_planet.name}")
        print(f"   Cargo: {self.get_cargo_description()}")
        
    def update(self):
        if self.delivered:
            return
            
        # Move toward destination
        direction = (self.destination.position - self.position).normalized()
        self.position += direction * self.speed * time.dt
        
        # Check if arrived
        if (self.position - self.destination.position).length() < 5:
            self.complete_delivery()
            
        # Check for player interaction
        if hasattr(scene_manager, 'space_controller') and scene_manager.space_controller:
            player_pos = scene_manager.space_controller.position
            if (self.position - player_pos).length() < 50:
                self.trigger_cargo_encounter()
    
    def calculate_cargo_value(self):
        total_value = 0
        base_prices = {
            "food": 10, "minerals": 25, "technology": 50,
            "luxury_goods": 75, "medicine": 40, "weapons": 60,
            "fuel": 15, "spices": 35
        }
        
        for commodity, quantity in self.cargo.items():
            base_price = base_prices.get(commodity, 20)
            total_value += base_price * quantity
            
        return int(total_value)
    
    def get_cargo_description(self):
        if not self.cargo:
            return "Empty"
        items = []
        for commodity, quantity in self.cargo.items():
            items.append(f"{quantity} {commodity.replace('_', ' ')}")
        return ", ".join(items)
    
    def complete_delivery(self):
        self.delivered = True
        
        # Add cargo to destination planet
        if hasattr(self.destination, 'economy') and hasattr(self.destination.economy, 'stockpiles'):
            for commodity, quantity in self.cargo.items():
                current = self.destination.economy.stockpiles.get(commodity, 0)
                self.destination.economy.stockpiles[commodity] = current + quantity
                
        print(f"✅ Cargo delivered to {self.destination.name}: {self.get_cargo_description()}")
        
        # Spawn payment ship
        payment_ship = PaymentShip(self.destination, self.origin, self.contract_value)
        transport_system.payment_ships.append(payment_ship)
        
        destroy(self)
        
    def trigger_cargo_encounter(self):
        # Only trigger once per ship
        if not hasattr(self, 'encounter_triggered'):
            self.encounter_triggered = True
            self.show_cargo_encounter()
            
    def show_cargo_encounter(self):
        print(f"\n🚢 CARGO SHIP ENCOUNTER")
        print(f"Ship from {self.origin.name} to {self.destination.name}")
        print(f"Cargo: {self.get_cargo_description()}")
        print(f"Value: {self.contract_value} credits")

class PaymentShip(Entity):
    """Ship that carries payment between planets"""
    
    def __init__(self, origin_planet, destination_planet, credits):
        super().__init__(
            model='cube',
            color=color.yellow,
            scale=(0.8, 0.4, 1.0)
        )
        
        self.origin = origin_planet
        self.destination = destination_planet
        self.credits = credits
        self.position = Vec3(origin_planet.position)
        self.speed = 12.0
        self.delivered = False
        
        print(f"💰 Payment ship: {origin_planet.name} → {destination_planet.name} ({credits} credits)")
        
    def update(self):
        if self.delivered:
            return
            
        # Move toward destination
        direction = (self.destination.position - self.position).normalized()
        self.position += direction * self.speed * time.dt
        
        # Check if arrived
        if (self.position - self.destination.position).length() < 5:
            self.complete_payment()
            
    def complete_payment(self):
        self.delivered = True
        
        # Add credits to destination
        if hasattr(self.destination, 'economy') and hasattr(self.destination.economy, 'credits'):
            self.destination.economy.credits += self.credits
            
        print(f"💳 Payment delivered to {self.destination.name}: {self.credits} credits")
        destroy(self)
```

---

## 🔧 **STEP 2: Enhanced Planet Economy Class**

Replace the existing `PlanetEconomy` class with this enhanced version:

```python
class RealisticPlanetEconomy:
    """Enhanced planet economy with physical transport needs"""
    
    def __init__(self, planet_name, planet_type):
        self.planet_name = planet_name
        self.planet_type = planet_type
        self.stockpiles = {}
        self.daily_consumption = {}
        self.daily_production = {}
        self.outgoing_requests = {}
        self.expected_deliveries = {}
        self.credits = random.randint(10000, 50000)
        
        # Transport timing
        self.last_procurement_check = 0
        self.procurement_interval = 60  # Check every minute for demo
        
        self.initialize_economy()
        
    def initialize_economy(self):
        # Set up based on planet type (same as before)
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
        current_time = time.time()
        
        # Process production and consumption
        for commodity, amount in self.daily_production.items():
            per_second = amount / 300.0  # 1 day = 5 minutes = 300 seconds
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
        """Send procurement messages for needed goods"""
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
            days_remaining = current_stock / consumption if consumption > 0 else float('inf')
            
            if days_remaining < 30:  # Less than 30 days supply
                urgency = self.determine_urgency(days_remaining)
                quantity_needed = int(consumption * 60 - current_stock)  # Target 60 days
                
                if quantity_needed > 0:
                    needs[commodity] = GoodsRequest(
                        commodity=commodity,
                        quantity=quantity_needed,
                        max_price=self.calculate_max_price(commodity, urgency),
                        urgency=urgency,
                        deadline=0,
                        requesting_planet=self.planet_name
                    )
                    
        return needs
    
    def determine_urgency(self, days_remaining):
        if days_remaining < 7:
            return UrgencyLevel.CRITICAL
        elif days_remaining < 15:
            return UrgencyLevel.URGENT
        elif days_remaining < 25:
            return UrgencyLevel.NORMAL
        else:
            return UrgencyLevel.LOW
            
    def calculate_max_price(self, commodity, urgency):
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
        # Find planets that might supply this commodity
        suppliers = self.find_suppliers(request.commodity)
        
        for supplier_planet in suppliers:
            if supplier_planet.name != self.planet_name:
                message_ship = MessageShip(
                    self,  # Will need to connect to actual planet object
                    supplier_planet,
                    MessageType.GOODS_REQUEST,
                    request
                )
                transport_system.message_ships.append(message_ship)
                
    def find_suppliers(self, commodity):
        """Find planets that produce this commodity"""
        suppliers = []
        
        # Search through all planets
        for planet in planets:  # Reference to global planets list
            if hasattr(planet, 'economy') and planet.economy:
                if planet.economy.daily_production.get(commodity, 0) > planet.economy.daily_consumption.get(commodity, 0):
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
            # Create cargo ship
            cargo_manifest = {commodity: can_supply}
            
            # Find requesting planet
            requesting_planet = None
            for planet in planets:
                if planet.name == request.requesting_planet:
                    requesting_planet = planet
                    break
                    
            if requesting_planet:
                cargo_ship = CargoShip(
                    self,  # Will need planet object reference
                    requesting_planet,
                    cargo_manifest
                )
                transport_system.cargo_ships.append(cargo_ship)
                
                # Remove goods from stockpile
                self.stockpiles[commodity] -= can_supply
                
                print(f"📦 {self.planet_name} shipping {can_supply} {commodity} to {request.requesting_planet}")
```

---

## 🔧 **STEP 3: Transport System Manager**

Add this class to manage all transport:

```python
class TransportSystemManager:
    """Main manager for the realistic transport system"""
    
    def __init__(self):
        self.message_ships = []
        self.cargo_ships = []
        self.payment_ships = []
        
    def update(self):
        """Update all transport ships"""
        # Update all ships
        all_ships = self.message_ships + self.cargo_ships + self.payment_ships
        
        for ship in all_ships[:]:  # Copy list to avoid modification issues
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
        """Get transport activity statistics"""
        return {
            'message_ships': len(self.message_ships),
            'cargo_ships': len(self.cargo_ships),
            'payment_ships': len(self.payment_ships),
            'total_ships': len(self.message_ships) + len(self.cargo_ships) + len(self.payment_ships)
        }
```

---

## 🔧 **STEP 4: Modify Planet Class**

Update the Planet class to use the new economy:

```python
# In the Planet class __init__ method, replace the economy initialization:

def __init__(self, position=(0,0,0)):
    # ... existing code ...
    
    # Replace this line:
    # economy = market_system.generate_market_for_planet(self.name, self.planet_type)
    
    # With this:
    self.economy = RealisticPlanetEconomy(self.name, self.planet_type)
    
    # Connect to planet object for transport system
    if hasattr(self.economy, 'planet_object'):
        self.economy.planet_object = self
```

---

## 🔧 **STEP 5: Update Main Game Loop**

In the main `update()` function, add transport system updates:

```python
def update():
    global nearby_planet
    
    # Add this line to update transport system
    transport_system.update()
    
    # Update planet economies
    for planet in planets:
        if hasattr(planet, 'economy'):
            planet.economy.update()
    
    # ... rest of existing update code ...
```

---

## 🔧 **STEP 6: Create Global Transport System**

After creating all the classes, add this near the end of the file:

```python
# Create global transport system
transport_system = TransportSystemManager()

# Update planets to use new economy system
for planet in planets:
    planet.economy = RealisticPlanetEconomy(planet.name, planet.planet_type)
    planet.economy.planet_object = planet

print("🚀 Realistic Transport System activated!")
print("Ships will now physically carry cargo, messages, and payments between planets.")
```

---

## 🔧 **STEP 7: Add Transport Statistics Display**

Add a new UI element to show transport activity:

```python
# Add to the SpaceController class:
self.transport_text = Text(
    parent=camera.ui,
    text='Ships: 0',
    position=(-0.45, 0.2),
    scale=0.8,
    color=color.white
)

# In the SpaceController update method:
def update(self):
    # ... existing code ...
    
    # Update transport statistics
    stats = transport_system.get_statistics()
    self.transport_text.text = f"Ships: {stats['total_ships']} (M:{stats['message_ships']} C:{stats['cargo_ships']} P:{stats['payment_ships']})"
```

---

## 🎯 **EXPECTED RESULTS**

After integration, you should see:

1. **Message Ships (Cyan)**: Small ships carrying requests between planets
2. **Cargo Ships (Orange)**: Larger ships carrying actual goods
3. **Payment Ships (Yellow)**: Ships returning with payment for deliveries
4. **Console Output**: Real-time transport activity logs
5. **Living Economy**: Planets actually running out of goods when transport fails
6. **Player Encounters**: Real cargo ships to interact with instead of random encounters

---

## 🚨 **TESTING THE SYSTEM**

1. **Watch Console**: You'll see transport activity messages
2. **Use 'I' Key**: Check planet economics to see real stockpile changes
3. **Observe Space**: Look for colored ships moving between planets
4. **Monitor Statistics**: Transport counter shows active ships

---

This integration transforms ILK from an abstract economy into a **living universe** where actual ships carry real cargo based on genuine planetary needs!