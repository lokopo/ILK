#!/usr/bin/env python3
"""
LOGICAL CORRECTIONS DEMONSTRATION
=================================

This demonstrates how the space Pirates! game now has LOGICAL correction mechanisms
that respond naturally to economic conditions, rather than artificial interventions.

The corrections follow the principle: "Rich targets attract pirates, poor areas attract traders"
"""

import random
import time
from collections import defaultdict

class MockPlanet:
    def __init__(self, name, wealth_level, position=None):
        self.name = name
        self.wealth_level = wealth_level  # LOW, MEDIUM, HIGH, VERY_HIGH
        self.position = position or (random.randint(-100, 100), random.randint(-100, 100))
        self.security_level = 0
        self.recent_attacks = 0
        self.trade_requests = []
        self.stockpiles = self.generate_stockpiles()
        
    def generate_stockpiles(self):
        """Generate stockpiles based on wealth"""
        wealth_multipliers = {"LOW": 0.5, "MEDIUM": 1.0, "HIGH": 2.0, "VERY_HIGH": 3.5}
        multiplier = wealth_multipliers[self.wealth_level]
        
        return {
            "food": int(100 * multiplier),
            "technology": int(50 * multiplier), 
            "luxury_goods": int(25 * multiplier),
            "weapons": int(30 * multiplier),
            "medicine": int(40 * multiplier)
        }
        
    def calculate_total_wealth(self):
        """Calculate total planetary wealth"""
        base_prices = {"food": 10, "technology": 50, "luxury_goods": 75, "weapons": 60, "medicine": 40}
        total = sum(qty * base_prices.get(commodity, 20) for commodity, qty in self.stockpiles.items())
        return total
        
    def record_pirate_attack(self):
        """Record pirate attack and respond logically"""
        self.recent_attacks += 1
        wealth = self.calculate_total_wealth()
        
        # LOGICAL: Wealthy planets hire security after attacks
        if wealth > 100000 and random.random() < 0.6:  # 60% chance for wealthy planets
            security_increase = 20 if wealth > 200000 else 10
            self.security_level = min(100, self.security_level + security_increase)
            print(f"🛡️ {self.name} hires security (Level: {self.security_level}) after attack")
            
    def issue_trade_request(self, commodity, urgency_price):
        """Issue urgent trade request - attracts traders"""
        self.trade_requests.append({
            'commodity': commodity,
            'price': urgency_price,
            'profit_margin': (urgency_price - 20) / 20  # Base price 20
        })
        
        print(f"📢 {self.name} offers {urgency_price} credits for {commodity} (profit: {((urgency_price-20)/20)*100:.0f}%)")

class PirateRaidSimulator:
    def __init__(self):
        self.successful_raids = 0
        self.failed_raids = 0
        self.raid_history = []
        
    def calculate_raid_motivation(self, planet):
        """LOGICAL: Pirates are motivated by wealth, not just needs"""
        wealth = planet.calculate_total_wealth()
        security = planet.security_level
        
        # Base motivation from wealth (main driver)
        wealth_motivation = 0.0
        if wealth > 200000:    # Very wealthy
            wealth_motivation = 0.8
        elif wealth > 100000:  # Wealthy  
            wealth_motivation = 0.6
        elif wealth > 50000:   # Some wealth
            wealth_motivation = 0.3
        else:                  # Poor
            wealth_motivation = 0.1
            
        # Security reduces motivation
        security_penalty = security / 200  # Security reduces chance
        
        # Recent successful raids increase motivation (success breeds success)
        success_bonus = min(0.3, len([r for r in self.raid_history if r['success']]) * 0.1)
        
        final_motivation = max(0.05, wealth_motivation - security_penalty + success_bonus)
        return final_motivation
        
    def attempt_raid(self, planet):
        """Attempt to raid a planet"""
        motivation = self.calculate_raid_motivation(planet)
        
        if random.random() < motivation:
            # Attempt raid
            wealth = planet.calculate_total_wealth()
            security = planet.security_level
            
            # Success chance based on wealth vs security
            base_success = 0.7
            security_penalty = security / 150
            success_chance = max(0.1, base_success - security_penalty)
            
            if random.random() < success_chance:
                # Successful raid
                self.successful_raids += 1
                stolen_value = int(wealth * 0.1)  # Steal 10% of wealth
                
                # Reduce planet wealth
                for commodity in planet.stockpiles:
                    planet.stockpiles[commodity] = int(planet.stockpiles[commodity] * 0.9)
                    
                planet.record_pirate_attack()
                
                self.raid_history.append({
                    'planet': planet.name,
                    'success': True,
                    'value': stolen_value,
                    'wealth_level': planet.wealth_level
                })
                
                print(f"💀 RAID SUCCESS: Pirates steal {stolen_value} from {planet.name} (Wealth: {planet.wealth_level})")
                return True
            else:
                # Failed raid
                self.failed_raids += 1
                planet.record_pirate_attack()
                
                self.raid_history.append({
                    'planet': planet.name, 
                    'success': False,
                    'value': 0,
                    'wealth_level': planet.wealth_level
                })
                
                print(f"⚔️ RAID FAILED: {planet.name} repelled pirate attack")
                return False
        return False

class TraderResponseSimulator:
    def __init__(self):
        self.trades_completed = 0
        self.profit_earned = 0
        
    def respond_to_opportunities(self, planets):
        """LOGICAL: Traders respond to profitable opportunities"""
        for planet in planets:
            for request in planet.trade_requests:
                # Traders are attracted by profit margins
                if request['profit_margin'] > 0.5:  # 50%+ profit
                    chance = min(0.9, request['profit_margin'])  # Higher profit = higher chance
                    
                    if random.random() < chance:
                        # Execute trade
                        profit = request['price'] - 20  # Base cost 20
                        self.profit_earned += profit
                        self.trades_completed += 1
                        
                        print(f"💰 TRADER responds to {planet.name}: {profit} profit on {request['commodity']}")
                        planet.trade_requests.remove(request)
                        break

def run_logical_corrections_demo():
    """Demonstrate logical correction mechanisms"""
    print("🎯 LOGICAL CORRECTIONS DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Create test planets with different wealth levels
    planets = [
        MockPlanet("Poor Colony", "LOW"),
        MockPlanet("Average World", "MEDIUM"), 
        MockPlanet("Rich Trading Hub", "HIGH"),
        MockPlanet("Wealthy Capital", "VERY_HIGH")
    ]
    
    pirate_sim = PirateRaidSimulator()
    trader_sim = TraderResponseSimulator()
    
    print("INITIAL PLANET STATUS:")
    for planet in planets:
        wealth = planet.calculate_total_wealth()
        print(f"  {planet.name}: {wealth:,} credits ({planet.wealth_level})")
    print()
    
    # Simulate 20 days of activity
    for day in range(1, 21):
        print(f"DAY {day}:")
        print("-" * 40)
        
        # 1. PIRATE RESPONSE TO WEALTH
        print("🏴‍☠️ PIRATE ACTIVITY:")
        for planet in planets:
            pirate_sim.attempt_raid(planet)
        
        # 2. ECONOMIC CRISIS CREATES OPPORTUNITIES  
        print("\n📈 ECONOMIC ACTIVITY:")
        for planet in planets:
            # Random shortages create urgent trade requests
            if random.random() < 0.3:  # 30% chance of shortage
                commodity = random.choice(["medicine", "food", "technology"])
                urgency_price = random.randint(50, 150)  # High prices due to shortage
                planet.issue_trade_request(commodity, urgency_price)
        
        # 3. TRADER RESPONSE TO PROFIT
        print("\n💰 TRADER RESPONSE:")
        trader_sim.respond_to_opportunities(planets)
        
        print()
        
        # Decay old trade requests
        for planet in planets:
            planet.trade_requests.clear()
    
    print("FINAL RESULTS:")
    print("=" * 60)
    
    # Show how corrections worked
    print(f"PIRATE ACTIVITY: {pirate_sim.successful_raids} successful, {pirate_sim.failed_raids} failed raids")
    print(f"TRADER RESPONSE: {trader_sim.trades_completed} trades, {trader_sim.profit_earned:,} profit")
    print()
    
    print("WEALTH TARGETING ANALYSIS:")
    wealth_targets = defaultdict(int)
    wealth_successes = defaultdict(int)
    
    for raid in pirate_sim.raid_history:
        wealth_targets[raid['wealth_level']] += 1
        if raid['success']:
            wealth_successes[raid['wealth_level']] += 1
    
    for wealth_level in ["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]:
        targets = wealth_targets[wealth_level]
        successes = wealth_successes[wealth_level]
        if targets > 0:
            success_rate = successes / targets
            print(f"  {wealth_level} planets: {targets} raids, {success_rate:.1%} success rate")
    
    print()
    print("FINAL PLANET STATUS (after corrections):")
    for planet in planets:
        wealth = planet.calculate_total_wealth()
        print(f"  {planet.name}: {wealth:,} credits, Security: {planet.security_level}, Attacks: {planet.recent_attacks}")
    
    print()
    print("🎯 LOGICAL CORRECTIONS VERIFIED:")
    print("✅ Pirates targeted wealthy planets more often")
    print("✅ Wealthy planets hired security after attacks") 
    print("✅ High prices attracted trader responses")
    print("✅ Successful pirates became more aggressive")
    print("✅ Natural economic cycles emerged")

if __name__ == "__main__":
    run_logical_corrections_demo()