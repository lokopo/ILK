#!/usr/bin/env python3
"""
PHYSICAL COMMUNICATION DEMONSTRATION
===================================

This demonstrates the new physical communication system in the space Pirates! game.
All communication is now done through physical letters delivered by ships and word-of-mouth
spreading through traders, just like in the historical Pirates! era.

KEY FEATURES:
- No instant communication/texts/calls
- Letters must be physically delivered by courier ships  
- War declarations require physical delivery to each faction planet
- News spreads through word-of-mouth via cargo ships and travelers
- Information accuracy degrades as it spreads
- Planets only know what they've been told or experienced directly
"""

import random
import time
from collections import defaultdict

# Mock classes for demonstration
class MockPlanet:
    def __init__(self, name, faction=None, position=None):
        self.name = name
        self.faction = faction or "independent"
        self.position = position or (random.randint(-100, 100), random.randint(-100, 100))
        self.mail_received = []
        self.local_news = []
        self.visitors_count = 0
        
    def receive_letter(self, letter):
        self.mail_received.append(letter)
        delivery_time = time.time() - letter['sent_time']
        print(f"📬 {self.name} receives letter: '{letter['subject']}' (delivered in {delivery_time:.1f}s)")
        if letter['type'] == 'WAR_DECLARATION':
            print(f"🚨 {self.name} NOW KNOWS about war between {letter['sender_faction']} and {letter['recipient_faction']}!")
            
    def add_news(self, news):
        self.local_news.append(news)
        
    def player_visits(self):
        self.visitors_count += 1
        print(f"\n🚀 Player lands on {self.name}")
        
        # Show mail
        if self.mail_received:
            print(f"📨 Local Mail ({len(self.mail_received)} letters):")
            for letter in self.mail_received[-3:]:  # Last 3 letters
                age = time.time() - letter['sent_time']
                print(f"   • {letter['subject']} (from {letter['sender']}, {age:.1f}s ago)")
                
        # Show news/rumors
        if self.local_news:
            print(f"📰 Local News & Rumors ({len(self.local_news)} items):")
            for news in self.local_news[-3:]:  # Last 3 news items
                age = time.time() - news['timestamp']
                reliability = f"{news['reliability']:.0%} reliable" if news['reliability'] < 0.9 else "confirmed"
                print(f"   • {news['content']} ({reliability}, {age:.1f}s ago)")
        
        if not self.mail_received and not self.local_news:
            print("📰 No mail or local news available")

class PhysicalCommunicationDemo:
    def __init__(self):
        self.planets = [
            MockPlanet("Terra Prime", "Terran Federation", (0, 0)),
            MockPlanet("New Mars", "Mars Republic", (50, 30)), 
            MockPlanet("Europa Station", "Jupiter Consortium", (-40, 60)),
            MockPlanet("Ceres Outpost", "independent", (80, -20)),
            MockPlanet("Titan Base", "Jupiter Consortium", (-60, -40)),
            MockPlanet("Vesta Mining", "independent", (30, -50))
        ]
        
        self.letter_ships = []  # Ships delivering letters
        self.rumors = []        # Word-of-mouth information
        self.letter_counter = 0
        
    def send_letter(self, sender_planet, recipient_planet, letter_type, subject, content, sender_faction="", recipient_faction=""):
        """Send a physical letter via courier ship"""
        self.letter_counter += 1
        
        # Calculate travel time based on distance
        distance = ((sender_planet.position[0] - recipient_planet.position[0])**2 + 
                   (sender_planet.position[1] - recipient_planet.position[1])**2)**0.5
        travel_time = max(2, distance / 20)  # Minimum 2 seconds, based on distance
        
        letter = {
            'id': f"LETTER-{self.letter_counter}",
            'type': letter_type,
            'sender': sender_planet.name,
            'recipient': recipient_planet.name,
            'sender_faction': sender_faction,
            'recipient_faction': recipient_faction,
            'subject': subject,
            'content': content,
            'sent_time': time.time(),
            'arrival_time': time.time() + travel_time
        }
        
        self.letter_ships.append({
            'letter': letter,
            'destination': recipient_planet,
            'arrival_time': letter['arrival_time']
        })
        
        print(f"📨 Letter courier dispatched: {sender_planet.name} → {recipient_planet.name}")
        print(f"   Subject: {subject}")
        print(f"   ETA: {travel_time:.1f} seconds")
        
        return letter
        
    def declare_war(self, declaring_faction, target_faction, declaration_text):
        """PHYSICAL WAR DECLARATION - must send letters to all faction planets"""
        print(f"\n⚔️ {declaring_faction.upper()} DECLARES WAR ON {target_faction.upper()}!")
        print(f"📜 Declaration: {declaration_text}")
        
        # Find faction capital and planets
        declaring_capital = self.find_faction_capital(declaring_faction)
        target_planets = self.find_faction_planets(target_faction)
        own_planets = self.find_faction_planets(declaring_faction)
        
        if not declaring_capital:
            print(f"❌ Cannot declare war - {declaring_faction} has no capital!")
            return False
            
        letters_sent = 0
        
        # Send war declaration to enemy planets
        for planet in target_planets:
            self.send_letter(
                sender_planet=declaring_capital,
                recipient_planet=planet,
                letter_type="WAR_DECLARATION",
                subject="DECLARATION OF WAR",
                content=f"By order of {declaring_faction}, we hereby declare WAR upon {target_faction}. {declaration_text}",
                sender_faction=declaring_faction,
                recipient_faction=target_faction
            )
            letters_sent += 1
            
        # Send military orders to own planets
        for planet in own_planets:
            if planet != declaring_capital:
                self.send_letter(
                    sender_planet=declaring_capital,
                    recipient_planet=planet,
                    letter_type="MILITARY_ORDERS",
                    subject="WAR ORDERS",
                    content=f"We are now at WAR with {target_faction}. Prepare defenses and mobilize forces.",
                    sender_faction=declaring_faction,
                    recipient_faction=declaring_faction
                )
                
        print(f"📫 {letters_sent} war declaration letters dispatched by courier ships")
        
        # Start a rumor about the war
        self.create_rumor(
            "war_declaration",
            f"{declaring_faction} has declared war on {target_faction}",
            declaring_capital.name,
            0.9
        )
        
        return True
        
    def find_faction_capital(self, faction_name):
        """Find the faction's capital planet"""
        faction_planets = self.find_faction_planets(faction_name)
        return faction_planets[0] if faction_planets else None
        
    def find_faction_planets(self, faction_name):
        """Find all planets belonging to a faction"""
        return [p for p in self.planets if p.faction == faction_name]
        
    def create_rumor(self, rumor_type, content, origin_planet, accuracy=0.8):
        """Create a word-of-mouth rumor"""
        rumor = {
            'id': f"RUMOR-{int(time.time())}-{random.randint(1000, 9999)}",
            'type': rumor_type,
            'content': content,
            'origin': origin_planet,
            'accuracy': accuracy,
            'age': 0,
            'visited_planets': {origin_planet},
            'spread_count': 0
        }
        
        self.rumors.append(rumor)
        print(f"💬 Rumor started at {origin_planet}: {content}")
        
    def spread_rumors(self):
        """Spread rumors through word-of-mouth"""
        for rumor in self.rumors[:]:
            # Age the rumor
            rumor['age'] += 0.1
            
            # Accuracy degrades as it spreads
            if rumor['spread_count'] > 0:
                rumor['accuracy'] *= 0.95
                
            # Remove very old or inaccurate rumors
            if rumor['age'] > 30 or rumor['accuracy'] < 0.3:
                self.rumors.remove(rumor)
                continue
                
            # Spread to nearby planets (simulate traders/travelers)
            if random.random() < 0.3:  # 30% chance per update
                self.spread_rumor_to_random_planet(rumor)
                
    def spread_rumor_to_random_planet(self, rumor):
        """Spread a rumor to a random planet via word-of-mouth"""
        unvisited_planets = [p for p in self.planets if p.name not in rumor['visited_planets']]
        if unvisited_planets:
            destination = random.choice(unvisited_planets)
            rumor['visited_planets'].add(destination.name)
            rumor['spread_count'] += 1
            
            # Add as local news with degraded accuracy
            news = {
                'content': rumor['content'],
                'source': f"Traveler from {random.choice(list(rumor['visited_planets']))}",
                'timestamp': time.time(),
                'reliability': rumor['accuracy']
            }
            destination.add_news(news)
            
            print(f"💬 Rumor spread to {destination.name} via word-of-mouth")
            
    def update(self):
        """Update the communication system"""
        current_time = time.time()
        
        # Deliver letters that have arrived
        for ship in self.letter_ships[:]:
            if current_time >= ship['arrival_time']:
                ship['destination'].receive_letter(ship['letter'])
                self.letter_ships.remove(ship)
                
        # Spread rumors
        self.spread_rumors()
        
    def show_status(self):
        """Show system status"""
        print(f"\n📡 COMMUNICATION SYSTEM STATUS:")
        print(f"Letter Ships in Transit: {len(self.letter_ships)}")
        print(f"Active Rumors: {len(self.rumors)}")
        
        # Show planets with information
        planets_with_mail = sum(1 for p in self.planets if p.mail_received)
        planets_with_news = sum(1 for p in self.planets if p.local_news)
        print(f"Planets with Mail: {planets_with_mail}/{len(self.planets)}")
        print(f"Planets with News: {planets_with_news}/{len(self.planets)}")

def run_physical_communication_demo():
    """Run the physical communication demonstration"""
    print("📡 PHYSICAL COMMUNICATION SYSTEM DEMONSTRATION")
    print("=" * 60)
    print("🎯 Authentic Pirates!-style communication: No instant messages!")
    print("📨 All communication via physical letters and word-of-mouth")
    print()
    
    demo = PhysicalCommunicationDemo()
    
    print("🌍 INITIAL GALAXY STATE:")
    factions = defaultdict(list)
    for planet in demo.planets:
        factions[planet.faction].append(planet.name)
    
    for faction, planets in factions.items():
        print(f"  {faction}: {', '.join(planets)}")
    print()
    
    # Demonstrate war declaration
    print("⚔️ PHASE 1: WAR DECLARATION")
    print("-" * 30)
    demo.declare_war(
        "Terran Federation", 
        "Mars Republic",
        "Mars Republic has violated territorial agreements and attacked our trade convoys."
    )
    print()
    
    # Simulate some time passing while letters travel
    print("⏰ PHASE 2: LETTER DELIVERY (waiting for courier ships...)")
    print("-" * 30)
    for i in range(8):  # 8 seconds of simulation
        time.sleep(1)
        demo.update()
        if i == 3:
            print("📰 Meanwhile, rumors begin to spread via word-of-mouth...")
            
    print()
    
    # Send some diplomatic letters
    print("🤝 PHASE 3: DIPLOMATIC COMMUNICATIONS")
    print("-" * 30)
    terra_prime = demo.planets[0]  # Terra Prime
    europa_station = demo.planets[2]  # Europa Station
    
    demo.send_letter(
        sender_planet=terra_prime,
        recipient_planet=europa_station,
        letter_type="DIPLOMATIC_LETTER",
        subject="Alliance Proposal",
        content="In light of recent Martian aggression, we propose a mutual defense pact.",
        sender_faction="Terran Federation",
        recipient_faction="Jupiter Consortium"
    )
    
    # Simulate some pirate warnings
    ceres_outpost = demo.planets[3]  # Ceres Outpost
    demo.send_letter(
        sender_planet=ceres_outpost,
        recipient_planet=europa_station,
        letter_type="PIRATE_WARNING",
        subject="PIRATE ALERT",
        content="Pirates attacked our mining convoy in the asteroid belt. Recommend escort ships for all cargo runs.",
        sender_faction="independent",
        recipient_faction="Jupiter Consortium"
    )
    
    # More time for delivery
    print("⏰ Waiting for diplomatic letters to arrive...")
    for i in range(5):
        time.sleep(1)
        demo.update()
    print()
    
    # Show information propagation
    print("📊 PHASE 4: INFORMATION PROPAGATION ANALYSIS")
    print("-" * 30)
    demo.show_status()
    print()
    
    # Simulate player visiting planets
    print("🚀 PHASE 5: PLAYER EXPLORATION")
    print("-" * 30)
    print("Player visits planets and learns local information...")
    
    # Visit some planets
    for planet in demo.planets[:4]:  # Visit first 4 planets
        planet.player_visits()
        print()
        
    # Show final state
    print("📈 FINAL COMMUNICATION ANALYSIS:")
    print("-" * 30)
    demo.show_status()
    
    if demo.rumors:
        print("\n💬 ACTIVE RUMORS:")
        for rumor in demo.rumors:
            spread_info = f"spread to {len(rumor['visited_planets'])} planets"
            accuracy_info = f"{rumor['accuracy']:.0%} accurate"
            age_info = f"{rumor['age']:.1f}s old"
            print(f"   • {rumor['content']} ({spread_info}, {accuracy_info}, {age_info})")
    
    print("\n✅ PHYSICAL COMMUNICATION FEATURES DEMONSTRATED:")
    print("🔹 War declarations require physical letter delivery to each planet")
    print("🔹 Letters have realistic travel times based on distance")
    print("🔹 News spreads through word-of-mouth via traders/travelers")
    print("🔹 Information accuracy degrades as rumors spread")
    print("🔹 Planets only know what they've been told directly")
    print("🔹 Player learns local information when visiting planets")
    print("🔹 No instant communication - everything is physical!")

if __name__ == "__main__":
    run_physical_communication_demo()