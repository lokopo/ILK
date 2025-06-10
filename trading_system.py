import random
import time
from datetime import datetime
from enum import Enum

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
        self.demand_multiplier = random.uniform(0.8, 1.2)
        self.supply_multiplier = random.uniform(0.8, 1.2)

class TradeOffer:
    def __init__(self, item, quantity, price, expires_at, is_buy_offer=True):
        self.item = item
        self.quantity = quantity
        self.price = price
        self.expires_at = expires_at
        self.is_buy_offer = is_buy_offer

class TradingSystem:
    def __init__(self, player_reputation=0):
        self.player_reputation = player_reputation
        
        # Initialize trade items
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
        
        # Player cargo
        self.cargo = {}
        self.cargo_capacity = 100
        self.current_cargo = 0
        
        # Market state
        self.market_trends = {}
        self.trade_offers = []
        self.transaction_history = []
        
        # Initialize market trends
        for item_name in self.items:
            self.market_trends[item_name] = {
                'demand': random.uniform(0.5, 1.5),
                'supply': random.uniform(0.5, 1.5),
                'trend': random.choice(['rising', 'falling', 'stable'])
            }
    
    def get_item_price(self, item_name, port_name="Generic Port", is_selling=False):
        """Calculate current market price for an item"""
        if item_name not in self.items:
            return 0
            
        item = self.items[item_name]
        base_price = item.base_price
        
        # Apply market trends
        trend_data = self.market_trends[item_name]
        price = base_price * trend_data['demand'] / trend_data['supply']
        
        # Apply rarity multiplier
        rarity_multipliers = {
            Rarity.COMMON: 1.0,
            Rarity.UNCOMMON: 1.5,
            Rarity.RARE: 2.5,
            Rarity.LEGENDARY: 4.0
        }
        price *= rarity_multipliers[item.rarity]
        
        # Apply reputation bonus/penalty (better prices with higher rep)
        rep_modifier = 1.0 + (self.player_reputation * 0.01)  # 1% per reputation point
        if is_selling:
            price *= rep_modifier
        else:
            price /= rep_modifier
        
        # Random variation
        price *= random.uniform(0.9, 1.1)
        
        return max(1, int(price))
    
    def can_buy(self, item_name, quantity):
        """Check if player can buy items"""
        if self.current_cargo + quantity > self.cargo_capacity:
            return False, "Not enough cargo space"
        return True, "OK"
    
    def buy_item(self, item_name, quantity, price_per_unit, credits):
        """Buy items from market"""
        total_cost = price_per_unit * quantity
        can_buy, reason = self.can_buy(item_name, quantity)
        
        if not can_buy:
            return False, reason, credits
        
        if credits < total_cost:
            return False, "Not enough credits", credits
        
        # Add to cargo
        if item_name in self.cargo:
            self.cargo[item_name] += quantity
        else:
            self.cargo[item_name] = quantity
        
        self.current_cargo += quantity
        credits -= total_cost
        
        # Record transaction
        self.transaction_history.append({
            'type': 'buy',
            'item': item_name,
            'quantity': quantity,
            'price': price_per_unit,
            'total': total_cost,
            'timestamp': datetime.now()
        })
        
        return True, f"Bought {quantity} {item_name} for {total_cost} credits", credits
    
    def sell_item(self, item_name, quantity, price_per_unit, credits):
        """Sell items to market"""
        if item_name not in self.cargo or self.cargo[item_name] < quantity:
            return False, "Not enough items to sell", credits
        
        total_earned = price_per_unit * quantity
        
        # Remove from cargo
        self.cargo[item_name] -= quantity
        if self.cargo[item_name] == 0:
            del self.cargo[item_name]
        
        self.current_cargo -= quantity
        credits += total_earned
        
        # Record transaction
        self.transaction_history.append({
            'type': 'sell',
            'item': item_name,
            'quantity': quantity,
            'price': price_per_unit,
            'total': total_earned,
            'timestamp': datetime.now()
        })
        
        return True, f"Sold {quantity} {item_name} for {total_earned} credits", credits
    
    def update_market_trends(self):
        """Update market trends over time"""
        for item_name in self.market_trends:
            trend_data = self.market_trends[item_name]
            
            # Randomly change demand and supply
            trend_data['demand'] *= random.uniform(0.95, 1.05)
            trend_data['supply'] *= random.uniform(0.95, 1.05)
            
            # Keep values in reasonable bounds
            trend_data['demand'] = max(0.3, min(2.0, trend_data['demand']))
            trend_data['supply'] = max(0.3, min(2.0, trend_data['supply']))
            
            # Update trend direction
            if random.random() < 0.1:  # 10% chance to change trend
                trend_data['trend'] = random.choice(['rising', 'falling', 'stable'])
    
    def generate_trade_offers(self, port_name="Generic Port"):
        """Generate random trade offers for current port"""
        self.trade_offers.clear()
        
        # Generate 3-6 offers
        num_offers = random.randint(3, 6)
        
        for _ in range(num_offers):
            item_name = random.choice(list(self.items.keys()))
            quantity = random.randint(1, 20)
            is_buy_offer = random.choice([True, False])
            
            # Calculate price with some variation
            base_price = self.get_item_price(item_name, port_name, not is_buy_offer)
            price_variation = random.uniform(0.8, 1.2)
            price = int(base_price * price_variation)
            
            # Offers expire in 5-15 minutes
            expires_at = time.time() + random.randint(300, 900)
            
            offer = TradeOffer(item_name, quantity, price, expires_at, is_buy_offer)
            self.trade_offers.append(offer)
    
    def get_cargo_info(self):
        """Get current cargo information"""
        return {
            'cargo': self.cargo.copy(),
            'current_cargo': self.current_cargo,
            'cargo_capacity': self.cargo_capacity,
            'cargo_percentage': (self.current_cargo / self.cargo_capacity) * 100
        }
    
    def get_market_summary(self, port_name="Generic Port"):
        """Get market summary for current port"""
        summary = {}
        for item_name, item in self.items.items():
            buy_price = self.get_item_price(item_name, port_name, False)
            sell_price = self.get_item_price(item_name, port_name, True)
            trend = self.market_trends[item_name]['trend']
            
            summary[item_name] = {
                'item': item,
                'buy_price': buy_price,
                'sell_price': sell_price,
                'trend': trend,
                'player_quantity': self.cargo.get(item_name, 0)
            }
        
        return summary