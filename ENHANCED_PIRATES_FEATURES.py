# Enhanced Pirates! Features for 3D Space Game
# ===============================================

from ursina import *
import random
import math
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
import time

# ===== FLEET MANAGEMENT SYSTEM =====

class ShipClass(Enum):
    FIGHTER = "FIGHTER"           # Fast, light combat
    CORVETTE = "CORVETTE"         # Small multi-role
    FRIGATE = "FRIGATE"           # Medium warship
    DESTROYER = "DESTROYER"       # Heavy combat
    CRUISER = "CRUISER"           # Large multi-role
    BATTLESHIP = "BATTLESHIP"     # Massive warship
    CARRIER = "CARRIER"           # Fighter carrier
    FREIGHTER = "FREIGHTER"       # Cargo hauler
    TRANSPORT = "TRANSPORT"       # Passenger/crew
    MINING_BARGE = "MINING_BARGE" # Resource extraction

@dataclass
class ShipStats:
    max_health: int
    armor: int
    shield_strength: int
    speed: float
    maneuverability: float
    cargo_capacity: int
    crew_capacity: int
    fuel_capacity: int
    weapon_hardpoints: int
    base_cost: int

class CapturedShip:
    def __init__(self, ship_class, name=None, condition=1.0):
        self.ship_class = ship_class
        self.name = name or f"{ship_class.value}-{random.randint(100, 999)}"
        self.condition = condition  # 0.0 to 1.0
        self.stats = self.get_base_stats()
        self.current_health = int(self.stats.max_health * condition)
        self.assigned_crew = []
        self.position = Vec3(0, 0, 0)
        self.role = "patrol"  # patrol, escort, mining, trading
        self.cargo = {}
        self.fuel = self.stats.fuel_capacity * condition
        
    def get_base_stats(self):
        """Get base stats for ship class"""
        ship_stats = {
            ShipClass.FIGHTER: ShipStats(100, 5, 50, 150, 0.9, 10, 2, 80, 2, 50000),
            ShipClass.CORVETTE: ShipStats(200, 15, 100, 120, 0.8, 50, 5, 150, 4, 120000),
            ShipClass.FRIGATE: ShipStats(500, 30, 200, 100, 0.6, 100, 15, 300, 6, 300000),
            ShipClass.DESTROYER: ShipStats(800, 50, 300, 80, 0.5, 150, 25, 500, 8, 600000),
            ShipClass.CRUISER: ShipStats(1200, 75, 500, 70, 0.4, 300, 50, 800, 10, 1200000),
            ShipClass.BATTLESHIP: ShipStats(2000, 120, 800, 50, 0.3, 200, 80, 1200, 15, 2500000),
            ShipClass.CARRIER: ShipStats(1500, 60, 400, 60, 0.3, 500, 100, 1000, 5, 2000000),
            ShipClass.FREIGHTER: ShipStats(400, 20, 100, 70, 0.4, 1000, 10, 600, 2, 400000),
            ShipClass.TRANSPORT: ShipStats(300, 15, 80, 80, 0.5, 200, 50, 400, 1, 250000),
            ShipClass.MINING_BARGE: ShipStats(600, 40, 150, 40, 0.2, 800, 20, 800, 3, 800000)
        }
        return ship_stats.get(self.ship_class, ship_stats[ShipClass.CORVETTE])
    
    def get_effective_stats(self):
        """Get stats modified by condition and crew"""
        base = self.stats
        condition_mod = self.condition
        crew_mod = min(1.2, len(self.assigned_crew) / (base.crew_capacity * 0.5))
        
        return {
            'health': int(base.max_health * condition_mod),
            'speed': base.speed * condition_mod * crew_mod,
            'cargo': int(base.cargo_capacity * condition_mod),
            'combat_rating': (base.armor + base.shield_strength) * condition_mod * crew_mod
        }
    
    def can_perform_role(self, role):
        """Check if ship can perform specific role"""
        role_requirements = {
            'combat': [ShipClass.FIGHTER, ShipClass.CORVETTE, ShipClass.FRIGATE, ShipClass.DESTROYER, ShipClass.BATTLESHIP],
            'trading': [ShipClass.FREIGHTER, ShipClass.TRANSPORT, ShipClass.CORVETTE],
            'mining': [ShipClass.MINING_BARGE, ShipClass.FREIGHTER],
            'escort': [ShipClass.FIGHTER, ShipClass.CORVETTE, ShipClass.FRIGATE, ShipClass.DESTROYER],
            'patrol': [ShipClass.FIGHTER, ShipClass.CORVETTE, ShipClass.FRIGATE]
        }
        return self.ship_class in role_requirements.get(role, [])

class FleetManager:
    def __init__(self):
        self.flagship = None  # Player's main ship
        self.fleet = []  # List of CapturedShip objects
        self.max_fleet_size = 8
        self.fleet_reputation = 0  # Reputation as a fleet commander
        
    def add_ship(self, ship):
        """Add captured ship to fleet"""
        if len(self.fleet) < self.max_fleet_size:
            self.fleet.append(ship)
            return True
        return False
    
    def remove_ship(self, ship_index):
        """Remove ship from fleet (sell or abandon)"""
        if 0 <= ship_index < len(self.fleet):
            ship = self.fleet.pop(ship_index)
            return ship
        return None
    
    def assign_crew_to_ship(self, ship_index, crew_members):
        """Assign crew to specific ship"""
        if 0 <= ship_index < len(self.fleet):
            ship = self.fleet[ship_index]
            if len(crew_members) <= ship.stats.crew_capacity:
                ship.assigned_crew = crew_members
                return True
        return False
    
    def set_ship_role(self, ship_index, role):
        """Set role for fleet ship"""
        if 0 <= ship_index < len(self.fleet):
            ship = self.fleet[ship_index]
            if ship.can_perform_role(role):
                ship.role = role
                return True
        return False
    
    def get_fleet_combat_strength(self):
        """Calculate total fleet combat power"""
        total_strength = 0
        for ship in self.fleet:
            if ship.role in ['combat', 'escort', 'patrol']:
                stats = ship.get_effective_stats()
                total_strength += stats['combat_rating']
        return total_strength
    
    def get_fleet_cargo_capacity(self):
        """Calculate total fleet cargo capacity"""
        total_cargo = 0
        for ship in self.fleet:
            if ship.role in ['trading', 'mining']:
                stats = ship.get_effective_stats()
                total_cargo += stats['cargo']
        return total_cargo
    
    def update_fleet_positions(self, flagship_pos):
        """Update fleet ship positions in formation"""
        for i, ship in enumerate(self.fleet):
            # Formation positioning around flagship
            angle = (i / len(self.fleet)) * 2 * math.pi
            distance = 20 + (i % 3) * 10
            offset_x = math.cos(angle) * distance
            offset_z = math.sin(angle) * distance
            ship.position = flagship_pos + Vec3(offset_x, 0, offset_z)

# ===== PERSONAL COMBAT & DUELING SYSTEM =====

class CombatStance(Enum):
    AGGRESSIVE = "AGGRESSIVE"
    DEFENSIVE = "DEFENSIVE"
    BALANCED = "BALANCED"

class WeaponType(Enum):
    PLASMA_SWORD = "PLASMA_SWORD"     # High damage, slow
    LASER_RAPIER = "LASER_RAPIER"     # Fast, precise
    ENERGY_CUTLASS = "ENERGY_CUTLASS" # Balanced
    STUN_BATON = "STUN_BATON"         # Non-lethal

@dataclass
class PersonalWeapon:
    weapon_type: WeaponType
    damage: int
    speed: float
    accuracy: float
    range: float
    special_ability: str

class PersonalCombatSystem:
    def __init__(self):
        self.player_health = 100
        self.player_max_health = 100
        self.player_skill = 5  # 1-10 skill level
        self.player_weapon = WeaponType.ENERGY_CUTLASS
        self.combat_active = False
        self.opponent = None
        self.combat_timer = 0
        
        # Combat UI elements
        self.combat_ui = Entity(parent=camera.ui, enabled=False)
        self.health_bar = Entity(parent=self.combat_ui, model='cube', color=color.red, 
                                scale=(0.3, 0.05, 1), position=(-0.3, 0.4, 0))
        self.opponent_health_bar = Entity(parent=self.combat_ui, model='cube', color=color.orange, 
                                         scale=(0.3, 0.05, 1), position=(0.3, 0.4, 0))
        
    def start_duel(self, opponent_name, opponent_skill=5):
        """Initiate personal combat"""
        self.combat_active = True
        self.opponent = {
            'name': opponent_name,
            'health': 100,
            'max_health': 100,
            'skill': opponent_skill,
            'stance': CombatStance.BALANCED
        }
        self.combat_timer = 0
        self.combat_ui.enabled = True
        print(f"⚔️ Engaging in personal combat with {opponent_name}!")
        
    def update_combat(self, dt):
        """Update combat system"""
        if not self.combat_active:
            return
            
        self.combat_timer += dt
        
        # Auto-combat resolution (can be expanded to real-time input)
        if self.combat_timer > 0.5:  # Combat tick every 0.5 seconds
            self.resolve_combat_round()
            self.combat_timer = 0
            
        # Update health bars
        player_health_ratio = self.player_health / self.player_max_health
        opponent_health_ratio = self.opponent['health'] / self.opponent['max_health']
        
        self.health_bar.scale_x = 0.3 * player_health_ratio
        self.opponent_health_bar.scale_x = 0.3 * opponent_health_ratio
        
        # Check for combat end
        if self.player_health <= 0:
            self.end_combat(False)
        elif self.opponent['health'] <= 0:
            self.end_combat(True)
            
    def resolve_combat_round(self):
        """Resolve one round of combat"""
        # Player attack
        player_attack = random.randint(1, 20) + self.player_skill
        opponent_defense = random.randint(1, 20) + self.opponent['skill']
        
        if player_attack > opponent_defense:
            damage = random.randint(5, 15) + self.player_skill
            self.opponent['health'] -= damage
            print(f"You hit for {damage} damage!")
            
        # Opponent attack
        opponent_attack = random.randint(1, 20) + self.opponent['skill']
        player_defense = random.randint(1, 20) + self.player_skill
        
        if opponent_attack > player_defense:
            damage = random.randint(5, 15) + self.opponent['skill']
            self.player_health -= damage
            print(f"{self.opponent['name']} hits you for {damage} damage!")
            
    def end_combat(self, player_won):
        """End combat and apply results"""
        self.combat_active = False
        self.combat_ui.enabled = False
        
        if player_won:
            print(f"🏆 Victory! You defeated {self.opponent['name']}!")
            self.player_skill += 0.1  # Skill improvement
            return "victory"
        else:
            print(f"💀 Defeat! {self.opponent['name']} bested you in combat!")
            self.player_health = 1  # Don't actually die, just injured
            return "defeat"

# ===== TREASURE HUNTING & EXPLORATION =====

class TreasureType(Enum):
    ANCIENT_ARTIFACT = "ANCIENT_ARTIFACT"
    ALIEN_TECHNOLOGY = "ALIEN_TECHNOLOGY"
    SHIP_WRECKAGE = "SHIP_WRECKAGE"
    DATA_CACHE = "DATA_CACHE"
    MINERAL_DEPOSIT = "MINERAL_DEPOSIT"
    LOST_CARGO = "LOST_CARGO"

@dataclass
class TreasureSite:
    position: Vec3
    treasure_type: TreasureType
    difficulty: int  # 1-5
    discovered: bool
    map_available: bool
    estimated_value: int
    description: str
    guardian_strength: int  # Combat difficulty if guarded

class TreasureMap:
    def __init__(self, treasure_site, quality=1.0):
        self.treasure_site = treasure_site
        self.quality = quality  # 0.0-1.0, affects accuracy
        self.cryptic_clues = self.generate_clues()
        
    def generate_clues(self):
        """Generate cryptic location clues"""
        clues = [
            "Near the crimson giant's third moon",
            "Where two asteroid fields intersect",
            "In the shadow of the dead star",
            "Beyond the nebula's edge",
            "Where ancient battles were fought"
        ]
        return random.choice(clues)

class TreasureHuntingSystem:
    def __init__(self):
        self.treasure_sites = []
        self.treasure_maps = []
        self.player_discovered = set()
        self.scanning_range = 10.0
        
        self.generate_treasure_sites()
        
    def generate_treasure_sites(self):
        """Generate random treasure sites throughout space"""
        for _ in range(20):  # 20 treasure sites
            site = TreasureSite(
                position=Vec3(random.randint(-500, 500), 0, random.randint(-500, 500)),
                treasure_type=random.choice(list(TreasureType)),
                difficulty=random.randint(1, 5),
                discovered=False,
                map_available=random.choice([True, False]),
                estimated_value=random.randint(5000, 100000),
                description="",
                guardian_strength=random.randint(0, 3)
            )
            self.treasure_sites.append(site)
            
    def scan_for_treasures(self, player_position):
        """Scan for nearby treasure sites"""
        found_treasures = []
        for site in self.treasure_sites:
            distance = (site.position - player_position).length()
            if distance <= self.scanning_range and not site.discovered:
                # Scanning success based on equipment and skill
                scan_success = random.random() < 0.3  # 30% base chance
                if scan_success:
                    found_treasures.append(site)
                    print(f"📡 Sensor anomaly detected! Possible treasure site at coordinates {site.position}")
                    
        return found_treasures
    
    def excavate_treasure(self, site, player_skill=5):
        """Attempt to excavate treasure from site"""
        if site.discovered:
            return None
            
        # Excavation difficulty check
        excavation_roll = random.randint(1, 20) + player_skill
        difficulty_threshold = 10 + (site.difficulty * 2)
        
        if excavation_roll >= difficulty_threshold:
            site.discovered = True
            treasure_value = site.estimated_value * random.uniform(0.8, 1.2)
            
            rewards = {
                'credits': int(treasure_value),
                'artifacts': 1 if site.treasure_type == TreasureType.ANCIENT_ARTIFACT else 0,
                'technology': 1 if site.treasure_type == TreasureType.ALIEN_TECHNOLOGY else 0,
                'reputation': site.difficulty
            }
            
            print(f"💎 Treasure excavated! Found {site.treasure_type.value} worth {rewards['credits']} credits!")
            return rewards
        else:
            print(f"❌ Excavation failed. The site remains undisturbed.")
            return None

# ===== ORBITAL BOMBARDMENT & PLANETARY ASSAULT =====

class PlanetaryDefense(Enum):
    NONE = "NONE"
    LIGHT = "LIGHT"
    MODERATE = "MODERATE"
    HEAVY = "HEAVY"
    FORTRESS = "FORTRESS"

class AssaultType(Enum):
    ORBITAL_BOMBARDMENT = "ORBITAL_BOMBARDMENT"
    GROUND_ASSAULT = "GROUND_ASSAULT"
    BLOCKADE = "BLOCKADE"
    SURGICAL_STRIKE = "SURGICAL_STRIKE"

@dataclass
class PlanetaryTarget:
    name: str
    defense_level: PlanetaryDefense
    population: int
    military_strength: int
    economic_value: int
    faction_allegiance: str
    shield_generators: int
    orbital_platforms: int

class OrbitalCombatSystem:
    def __init__(self):
        self.bombardment_active = False
        self.target_planet = None
        self.assault_progress = 0.0
        self.civilian_casualties = 0
        self.military_casualties = 0
        
    def initiate_orbital_assault(self, planet_name, assault_type, fleet_strength):
        """Begin orbital assault on planet"""
        # Get planet defense info
        target = self.get_planetary_target(planet_name)
        
        print(f"🚀 Initiating {assault_type.value} on {planet_name}")
        print(f"Target defenses: {target.defense_level.value}")
        print(f"Fleet strength: {fleet_strength}")
        
        # Calculate assault outcome
        success_chance = self.calculate_assault_success(target, fleet_strength, assault_type)
        
        if random.random() < success_chance:
            return self.execute_successful_assault(target, assault_type, fleet_strength)
        else:
            return self.execute_failed_assault(target, assault_type, fleet_strength)
    
    def get_planetary_target(self, planet_name):
        """Get planetary defense information"""
        # This would integrate with your existing planet system
        return PlanetaryTarget(
            name=planet_name,
            defense_level=random.choice(list(PlanetaryDefense)),
            population=random.randint(100000, 10000000),
            military_strength=random.randint(10, 100),
            economic_value=random.randint(50000, 1000000),
            faction_allegiance="unknown",
            shield_generators=random.randint(0, 5),
            orbital_platforms=random.randint(0, 10)
        )
    
    def calculate_assault_success(self, target, fleet_strength, assault_type):
        """Calculate probability of assault success"""
        base_chance = 0.5
        
        # Fleet strength modifier
        strength_modifier = min(0.4, fleet_strength / 1000)
        
        # Defense modifier
        defense_modifiers = {
            PlanetaryDefense.NONE: 0.3,
            PlanetaryDefense.LIGHT: 0.1,
            PlanetaryDefense.MODERATE: -0.1,
            PlanetaryDefense.HEAVY: -0.2,
            PlanetaryDefense.FORTRESS: -0.3
        }
        defense_modifier = defense_modifiers[target.defense_level]
        
        # Assault type modifier
        type_modifiers = {
            AssaultType.ORBITAL_BOMBARDMENT: 0.2,  # Easier from orbit
            AssaultType.GROUND_ASSAULT: -0.1,      # Harder ground combat
            AssaultType.BLOCKADE: 0.1,             # Siege warfare
            AssaultType.SURGICAL_STRIKE: -0.2      # Precise but difficult
        }
        type_modifier = type_modifiers[assault_type]
        
        final_chance = base_chance + strength_modifier + defense_modifier + type_modifier
        return max(0.1, min(0.9, final_chance))
    
    def execute_successful_assault(self, target, assault_type, fleet_strength):
        """Handle successful assault outcomes"""
        results = {
            'success': True,
            'credits_gained': 0,
            'reputation_change': {},
            'casualties': 0,
            'description': ""
        }
        
        if assault_type == AssaultType.ORBITAL_BOMBARDMENT:
            # High civilian casualties, major economic damage
            results['credits_gained'] = target.economic_value * 0.3
            results['casualties'] = target.population * 0.1
            results['description'] = f"Orbital bombardment devastated {target.name}. Massive casualties."
            results['reputation_change'] = {'all_factions': -20}  # War crime
            
        elif assault_type == AssaultType.SURGICAL_STRIKE:
            # Low casualties, precise objectives
            results['credits_gained'] = target.economic_value * 0.1
            results['casualties'] = target.population * 0.001
            results['description'] = f"Surgical strike on {target.name} achieved objectives with minimal casualties."
            results['reputation_change'] = {target.faction_allegiance: -10}
            
        elif assault_type == AssaultType.BLOCKADE:
            # Economic pressure, gradual effect
            results['credits_gained'] = target.economic_value * 0.05
            results['casualties'] = 0
            results['description'] = f"Blockade of {target.name} is disrupting their economy."
            results['reputation_change'] = {target.faction_allegiance: -5}
            
        return results
    
    def execute_failed_assault(self, target, assault_type, fleet_strength):
        """Handle failed assault outcomes"""
        results = {
            'success': False,
            'fleet_losses': random.randint(10, 30),
            'reputation_change': {target.faction_allegiance: -15},
            'description': f"Assault on {target.name} failed. Fleet took heavy losses."
        }
        return results

# ===== CHARACTER DEVELOPMENT & AGING =====

class PersonalSkill(Enum):
    PILOTING = "PILOTING"
    COMBAT = "COMBAT"
    LEADERSHIP = "LEADERSHIP"
    ENGINEERING = "ENGINEERING"
    TRADING = "TRADING"
    DIPLOMACY = "DIPLOMACY"

class CharacterDevelopment:
    def __init__(self):
        self.age = 25  # Starting age
        self.skills = {skill: random.randint(3, 7) for skill in PersonalSkill}
        self.experience_points = {skill: 0 for skill in PersonalSkill}
        self.legendary_achievements = []
        self.years_active = 0
        self.retirement_forced = False
        
        # Age-related decline
        self.peak_age = 40
        self.decline_age = 55
        self.mandatory_retirement_age = 70
        
    def advance_time(self, days):
        """Age character and apply experience"""
        years_passed = days / 365.0
        self.years_active += years_passed
        old_age = self.age
        self.age += years_passed
        
        # Check for age milestones
        if int(old_age) != int(self.age):
            self.handle_aging()
            
    def handle_aging(self):
        """Handle age-related effects"""
        print(f"🎂 Another year passes. You are now {int(self.age)} years old.")
        
        if self.age > self.decline_age:
            # Age-related skill decline
            decline_chance = (self.age - self.decline_age) / 20.0
            for skill in PersonalSkill:
                if random.random() < decline_chance:
                    self.skills[skill] = max(1, self.skills[skill] - 0.5)
                    print(f"📉 Age is taking its toll. {skill.value} skill has declined.")
                    
        if self.age >= self.mandatory_retirement_age:
            self.retirement_forced = True
            print(f"⏰ Time catches up with everyone. Mandatory retirement at age {int(self.age)}.")
            
    def gain_experience(self, skill_type, amount):
        """Gain experience in a skill"""
        if skill_type in self.experience_points:
            self.experience_points[skill_type] += amount
            
            # Check for skill improvement
            required_exp = self.skills[skill_type] * 100
            if self.experience_points[skill_type] >= required_exp:
                self.skills[skill_type] += 0.5
                self.experience_points[skill_type] = 0
                print(f"📈 {skill_type.value} skill improved to {self.skills[skill_type]:.1f}!")
                
    def get_skill_modifier(self, skill_type):
        """Get skill modifier for various actions"""
        base_skill = self.skills.get(skill_type, 5)
        
        # Age modifier
        if self.age < self.peak_age:
            age_mod = 1.0 + (self.peak_age - self.age) * 0.01  # Young bonus
        elif self.age > self.decline_age:
            age_mod = 1.0 - (self.age - self.decline_age) * 0.02  # Age penalty
        else:
            age_mod = 1.1  # Peak performance
            
        return base_skill * age_mod
    
    def earn_achievement(self, achievement_name, description):
        """Earn legendary achievement"""
        achievement = {
            'name': achievement_name,
            'description': description,
            'year_earned': int(self.years_active),
            'age_earned': int(self.age)
        }
        self.legendary_achievements.append(achievement)
        print(f"🏆 LEGENDARY ACHIEVEMENT: {achievement_name}")
        print(f"   {description}")

# ===== DYNAMIC WORLD EVENTS =====

class WorldEventType(Enum):
    GALACTIC_WAR = "GALACTIC_WAR"
    ECONOMIC_CRASH = "ECONOMIC_CRASH"
    TECHNOLOGICAL_BREAKTHROUGH = "TECHNOLOGICAL_BREAKTHROUGH"
    ALIEN_INVASION = "ALIEN_INVASION"
    PLAGUE_OUTBREAK = "PLAGUE_OUTBREAK"
    RESOURCE_SHORTAGE = "RESOURCE_SHORTAGE"
    POLITICAL_REVOLUTION = "POLITICAL_REVOLUTION"

@dataclass
class WorldEvent:
    event_type: WorldEventType
    affected_regions: List[str]
    duration_days: float
    intensity: float  # 0.0 to 1.0
    economic_impact: Dict[str, float]
    political_impact: Dict[str, int]
    description: str
    start_time: float

class DynamicWorldEvents:
    def __init__(self):
        self.active_events = []
        self.event_history = []
        self.last_major_event = 0
        
    def update(self, current_time):
        """Update world events"""
        # Remove expired events
        self.active_events = [event for event in self.active_events 
                             if current_time - event.start_time < event.duration_days]
        
        # Check for new major events
        if current_time - self.last_major_event > 30 and random.random() < 0.05:  # 5% chance monthly
            self.trigger_major_event(current_time)
            
    def trigger_major_event(self, current_time):
        """Trigger a major world-changing event"""
        event_type = random.choice(list(WorldEventType))
        
        if event_type == WorldEventType.GALACTIC_WAR:
            event = WorldEvent(
                event_type=event_type,
                affected_regions=["Core Worlds", "Outer Rim", "Border Systems"],
                duration_days=random.randint(180, 730),  # 6 months to 2 years
                intensity=random.uniform(0.6, 1.0),
                economic_impact={"weapons": 2.0, "medicine": 1.5, "luxury_goods": 0.5},
                political_impact={"reputation_decay": 2, "faction_tensions": 10},
                description="Galaxy-spanning conflict erupts between major factions!",
                start_time=current_time
            )
        elif event_type == WorldEventType.TECHNOLOGICAL_BREAKTHROUGH:
            event = WorldEvent(
                event_type=event_type,
                affected_regions=["Tech Worlds", "Research Stations"],
                duration_days=random.randint(90, 365),
                intensity=random.uniform(0.4, 0.8),
                economic_impact={"technology": 0.7, "medicine": 0.8},
                political_impact={"tech_faction_bonus": 15},
                description="Revolutionary technology discovered! Markets shifting rapidly.",
                start_time=current_time
            )
        # Add more event types...
        
        self.active_events.append(event)
        self.last_major_event = current_time
        print(f"🌍 MAJOR WORLD EVENT: {event.description}")
        
        return event

# ===== ENHANCED SHIP BOARDING SYSTEM =====

class BoardingAction(Enum):
    BREACH_AND_CLEAR = "BREACH_AND_CLEAR"
    STEALTH_INFILTRATION = "STEALTH_INFILTRATION"
    NEGOTIATED_SURRENDER = "NEGOTIATED_SURRENDER"
    DEVASTATING_ASSAULT = "DEVASTATING_ASSAULT"

class ShipBoardingSystem:
    def __init__(self):
        self.boarding_active = False
        self.target_ship = None
        self.boarding_progress = 0.0
        
    def initiate_boarding(self, target_ship_type, target_crew_count, boarding_action):
        """Start ship boarding sequence"""
        self.boarding_active = True
        self.target_ship = {
            'type': target_ship_type,
            'crew_count': target_crew_count,
            'resistance': random.randint(1, 10),
            'cargo_value': random.randint(10000, 100000)
        }
        
        print(f"🚀 Initiating boarding action: {boarding_action.value}")
        return self.resolve_boarding(boarding_action)
    
    def resolve_boarding(self, action):
        """Resolve boarding attempt"""
        player_skill = 7  # This would come from character system
        crew_bonus = 3   # This would come from crew system
        
        success_chances = {
            BoardingAction.BREACH_AND_CLEAR: 0.7,
            BoardingAction.STEALTH_INFILTRATION: 0.5,
            BoardingAction.NEGOTIATED_SURRENDER: 0.4,
            BoardingAction.DEVASTATING_ASSAULT: 0.8
        }
        
        base_chance = success_chances[action]
        skill_modifier = (player_skill + crew_bonus) / 20.0
        resistance_modifier = -self.target_ship['resistance'] / 20.0
        
        final_chance = base_chance + skill_modifier + resistance_modifier
        
        if random.random() < final_chance:
            return self.successful_boarding(action)
        else:
            return self.failed_boarding(action)
    
    def successful_boarding(self, action):
        """Handle successful boarding"""
        results = {
            'success': True,
            'cargo_captured': 0,
            'crew_casualties': 0,
            'ship_condition': 1.0,
            'reputation_impact': 0
        }
        
        if action == BoardingAction.DEVASTATING_ASSAULT:
            results['cargo_captured'] = self.target_ship['cargo_value'] * 0.6
            results['crew_casualties'] = self.target_ship['crew_count'] * 0.8
            results['ship_condition'] = 0.3  # Heavily damaged
            results['reputation_impact'] = -5  # Brutal reputation
            
        elif action == BoardingAction.STEALTH_INFILTRATION:
            results['cargo_captured'] = self.target_ship['cargo_value'] * 0.8
            results['crew_casualties'] = self.target_ship['crew_count'] * 0.1
            results['ship_condition'] = 0.9  # Minimal damage
            results['reputation_impact'] = 2  # Skillful reputation
            
        elif action == BoardingAction.NEGOTIATED_SURRENDER:
            results['cargo_captured'] = self.target_ship['cargo_value'] * 0.4
            results['crew_casualties'] = 0
            results['ship_condition'] = 1.0  # No damage
            results['reputation_impact'] = 5  # Honorable reputation
            
        print(f"✅ Boarding successful! Captured {results['cargo_captured']} credits worth of cargo.")
        print(f"Ship condition: {results['ship_condition']*100:.0f}%")
        
        # Offer to capture the ship
        if results['ship_condition'] > 0.5:
            print(f"💡 Ship is in good condition. Add to fleet? (Implementation needed)")
            
        self.boarding_active = False
        return results
    
    def failed_boarding(self, action):
        """Handle failed boarding"""
        results = {
            'success': False,
            'crew_losses': random.randint(1, 5),
            'ship_damage': random.uniform(0.1, 0.3),
            'target_escaped': True
        }
        
        print(f"❌ Boarding failed! Lost {results['crew_losses']} crew members.")
        print(f"Your ship took {results['ship_damage']*100:.0f}% damage.")
        
        self.boarding_active = False
        return results

# ===== INTEGRATION CLASS =====

class EnhancedPiratesFeatures:
    """Main class integrating all enhanced Pirates! features"""
    
    def __init__(self):
        self.fleet_manager = FleetManager()
        self.personal_combat = PersonalCombatSystem()
        self.treasure_hunting = TreasureHuntingSystem()
        self.orbital_combat = OrbitalCombatSystem()
        self.character_development = CharacterDevelopment()
        self.world_events = DynamicWorldEvents()
        self.ship_boarding = ShipBoardingSystem()
        
        print("🚀 Enhanced Pirates! features initialized!")
        print("💫 New systems available:")
        print("   - Fleet Management (Multiple ships)")
        print("   - Personal Combat & Dueling")
        print("   - Treasure Hunting & Exploration")
        print("   - Orbital Bombardment & Planetary Assault")
        print("   - Character Development & Aging")
        print("   - Dynamic World Events")
        print("   - Enhanced Ship Boarding")
    
    def update(self, dt, player_position, current_time):
        """Update all enhanced systems"""
        # Update personal combat
        self.personal_combat.update_combat(dt)
        
        # Update character aging
        self.character_development.advance_time(dt / 86400)  # Convert seconds to days
        
        # Update world events
        self.world_events.update(current_time / 86400)  # Convert to days
        
        # Update fleet positions
        if self.fleet_manager.fleet:
            self.fleet_manager.update_fleet_positions(player_position)
            
        # Scan for treasures
        if random.random() < 0.01:  # 1% chance per update
            treasures = self.treasure_hunting.scan_for_treasures(player_position)
    
    def get_available_commands(self):
        """Return available enhanced commands"""
        commands = {
            'V': 'Fleet Management',
            'X': 'Personal Combat Training',
            'Z': 'Treasure Scanner',
            'O': 'Orbital Operations',
            'P': 'Character Profile',
            'CTRL+B': 'Boarding Action'
        }
        return commands

# Initialize the enhanced features
# This would be integrated into your main game initialization
# enhanced_features = EnhancedPiratesFeatures()