import time
from datetime import datetime
from enum import Enum

class TransactionType(Enum):
    TRADE_BUY = "Trade Purchase"
    TRADE_SELL = "Trade Sale"
    MISSION_REWARD = "Mission Reward"
    COMBAT_REWARD = "Combat Reward"
    REPAIR_COST = "Ship Repair"
    FUEL_COST = "Fuel Purchase"
    UPGRADE_COST = "Ship Upgrade"
    DOCK_FEES = "Docking Fees"
    FINE = "Fine/Penalty"

class EconomySystem:
    def __init__(self, starting_credits=1000):
        self.credits = starting_credits
        self.transaction_history = []
        self.reputation_multiplier = 1.0
        
        # Economic constants
        self.base_repair_cost = 50
        self.base_fuel_cost = 20
        self.dock_fee_base = 25
        
    def add_credits(self, amount, transaction_type=TransactionType.MISSION_REWARD, description=""):
        """Add credits to player account"""
        if amount <= 0:
            return False
            
        # Apply reputation multiplier for positive transactions
        if amount > 0:
            amount = int(amount * self.reputation_multiplier)
            
        self.credits += amount
        
        # Record transaction
        self.transaction_history.append({
            'type': transaction_type.value,
            'amount': amount,
            'balance': self.credits,
            'description': description,
            'timestamp': datetime.now()
        })
        
        return True
    
    def spend_credits(self, amount, transaction_type=TransactionType.REPAIR_COST, description=""):
        """Spend credits if available"""
        if amount <= 0:
            return False, "Invalid amount"
            
        if self.credits < amount:
            return False, "Insufficient credits"
        
        self.credits -= amount
        
        # Record transaction
        self.transaction_history.append({
            'type': transaction_type.value,
            'amount': -amount,
            'balance': self.credits,
            'description': description,
            'timestamp': datetime.now()
        })
        
        return True, "Transaction completed"
    
    def can_afford(self, amount):
        """Check if player can afford a purchase"""
        return self.credits >= amount
    
    def calculate_repair_cost(self, ship_health, max_health):
        """Calculate cost to repair ship"""
        damage_percentage = 1.0 - (ship_health / max_health)
        return int(self.base_repair_cost * damage_percentage * 5)
    
    def calculate_fuel_cost(self, fuel_needed, max_fuel):
        """Calculate cost to refuel ship"""
        fuel_percentage = fuel_needed / max_fuel
        return int(self.base_fuel_cost * fuel_percentage * 3)
    
    def calculate_dock_fees(self, port_name="Generic Port", reputation=0):
        """Calculate docking fees based on port and reputation"""
        base_fee = self.dock_fee_base
        
        # Port-specific multipliers
        port_multipliers = {
            "New Terra": 1.0,
            "Nova Prime": 1.2,
            "Shadow Port": 0.8,
            "Freeport": 0.6
        }
        
        multiplier = port_multipliers.get(port_name, 1.0)
        
        # Reputation discount (max 50% discount)
        rep_discount = min(0.5, reputation * 0.01)
        
        fee = int(base_fee * multiplier * (1.0 - rep_discount))
        return max(5, fee)  # Minimum fee of 5 credits
    
    def update_reputation_multiplier(self, reputation):
        """Update the reputation multiplier for economic benefits"""
        # Reputation ranges from -100 to 100
        # Multiplier ranges from 0.5 to 1.5
        self.reputation_multiplier = 1.0 + (reputation * 0.005)
        self.reputation_multiplier = max(0.5, min(1.5, self.reputation_multiplier))
    
    def get_net_worth_estimate(self, cargo_value=0, ship_value=0):
        """Calculate estimated net worth"""
        return self.credits + cargo_value + ship_value
    
    def get_income_summary(self, days=7):
        """Get income summary for the last N days"""
        cutoff_time = time.time() - (days * 24 * 3600)
        
        income = 0
        expenses = 0
        
        for transaction in self.transaction_history:
            if hasattr(transaction['timestamp'], 'timestamp'):
                trans_time = transaction['timestamp'].timestamp()
            else:
                trans_time = time.time()  # Fallback for older transactions
                
            if trans_time >= cutoff_time:
                if transaction['amount'] > 0:
                    income += transaction['amount']
                else:
                    expenses += abs(transaction['amount'])
        
        return {
            'income': income,
            'expenses': expenses,
            'net': income - expenses,
            'days': days
        }
    
    def get_transaction_summary(self, limit=10):
        """Get recent transactions"""
        return self.transaction_history[-limit:] if self.transaction_history else []
    
    def clear_old_transactions(self, max_age_days=30):
        """Clear transactions older than specified days"""
        cutoff_time = time.time() - (max_age_days * 24 * 3600)
        
        self.transaction_history = [
            t for t in self.transaction_history 
            if hasattr(t['timestamp'], 'timestamp') and 
            t['timestamp'].timestamp() >= cutoff_time
        ]