#!/usr/bin/env python3
"""
ILK Space Game - Headless Mode
A headless version of the space game that runs economic simulations and tests
without requiring graphics or GUI components.
"""

import os
import sys
import logging
import traceback
import time
import signal

# Setup logging
verbose = os.environ.get('GAME_VERBOSE', '0') == '1'
logging.basicConfig(
    level=logging.DEBUG if verbose else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('space_game_headless.log', mode='w')
    ]
)
logger = logging.getLogger(__name__)

logger.info("=== ILK SPACE GAME - HEADLESS MODE ===")

# Import the headless test framework
try:
    from headless_game_test import GameStabilityTester
    logger.info("Headless game components loaded successfully")
except ImportError as e:
    logger.error(f"Failed to import headless components: {e}")
    print("❌ HEADLESS MODE INITIALIZATION FAILED")
    print("Could not import required headless game components.")
    print("Please ensure all files are present and dependencies are installed.")
    sys.exit(1)

class HeadlessGameRunner:
    """Main class for running the game in headless mode"""
    
    def __init__(self):
        self.running = False
        self.tester = GameStabilityTester()
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
        
    def run_stability_tests(self):
        """Run comprehensive stability tests"""
        logger.info("Starting comprehensive stability tests...")
        
        try:
            success = self.tester.run_all_tests()
            
            if success:
                logger.info("All stability tests passed successfully!")
                print("\n✅ GAME STABILITY VERIFIED")
                print("🎮 The enhanced Pirates! space game is stable and ready!")
                return 0
            else:
                logger.error("Some stability tests failed")
                print("\n❌ STABILITY ISSUES DETECTED")
                print("🔧 Please review the test results above")
                return 1
                
        except Exception as e:
            logger.error(f"Error during stability testing: {e}")
            logger.error(traceback.format_exc())
            print(f"\n💥 STABILITY TEST CRASHED: {e}")
            return 1
    
    def run_economic_simulation(self, days=30):
        """Run extended economic simulation"""
        logger.info(f"Starting {days}-day economic simulation...")
        
        try:
            # Import and use the economic components from the test framework
            from headless_game_test import MarketSystem, PlayerWallet
            
            market = MarketSystem()
            wallet = PlayerWallet(10000)
            
            # Create a variety of test planets
            planet_types = ["agricultural", "industrial", "mining", "tech", "luxury"]
            test_planets = []
            
            for i, planet_type in enumerate(planet_types):
                planet_name = f"TestPlanet_{planet_type}_{i+1}"
                market.generate_market_for_planet(planet_name, planet_type)
                test_planets.append(planet_name)
                logger.info(f"Created {planet_type} planet: {planet_name}")
            
            # Track economic metrics over time
            daily_metrics = []
            
            print(f"\n🏭 ECONOMIC SIMULATION - {days} DAYS")
            print("=" * 50)
            
            for day in range(1, days + 1):
                # Daily market update
                market.daily_economic_update()
                
                # Collect metrics
                total_stockpiles = 0
                planet_count = len(market.planet_economies)
                
                for planet_name, economy in market.planet_economies.items():
                    total_stockpiles += sum(economy.stockpiles.values())
                
                avg_stockpile = total_stockpiles / planet_count if planet_count > 0 else 0
                
                daily_metrics.append({
                    'day': day,
                    'total_stockpiles': total_stockpiles,
                    'avg_stockpile': avg_stockpile,
                    'planet_count': planet_count
                })
                
                # Progress reporting
                if day % 10 == 0 or day == days:
                    print(f"Day {day:3d}: Avg stockpile per planet: {avg_stockpile:.1f}")
                    
                # Check for runaway scenarios
                if avg_stockpile > 100000:  # Unrealistic stockpile growth
                    logger.warning(f"Day {day}: Potential runaway growth detected (avg: {avg_stockpile:.1f})")
                elif avg_stockpile < 10:  # Economic collapse
                    logger.warning(f"Day {day}: Potential economic collapse detected (avg: {avg_stockpile:.1f})")
            
            # Analyze results
            print("\n📊 SIMULATION RESULTS:")
            print("-" * 30)
            
            initial_avg = daily_metrics[0]['avg_stockpile']
            final_avg = daily_metrics[-1]['avg_stockpile']
            
            growth_rate = ((final_avg - initial_avg) / initial_avg) * 100 if initial_avg > 0 else 0
            
            print(f"Initial average stockpile: {initial_avg:.1f}")
            print(f"Final average stockpile: {final_avg:.1f}")
            print(f"Growth rate: {growth_rate:+.2f}%")
            
            # Stability assessment
            if abs(growth_rate) < 50:  # Less than 50% change is considered stable
                print("✅ Economic system appears stable")
                stability_result = True
            else:
                print("⚠️ Economic system shows significant instability")
                stability_result = False
                
            # Show planet details
            print(f"\n🌍 PLANET SUMMARY ({len(test_planets)} planets):")
            for planet_name in test_planets:
                economy = market.planet_economies[planet_name]
                total = sum(economy.stockpiles.values())
                print(f"  {planet_name}: {total:.0f} total stockpiles")
            
            logger.info(f"Economic simulation completed. Stable: {stability_result}")
            return 0 if stability_result else 1
            
        except Exception as e:
            logger.error(f"Error during economic simulation: {e}")
            logger.error(traceback.format_exc())
            print(f"\n💥 ECONOMIC SIMULATION CRASHED: {e}")
            return 1
    
    def run_interactive_mode(self):
        """Run interactive headless mode"""
        logger.info("Starting interactive headless mode...")
        print("\n🎮 INTERACTIVE HEADLESS MODE")
        print("Type 'help' for commands, 'quit' to exit")
        
        self.running = True
        
        while self.running:
            try:
                command = input("\nHeadless> ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    break
                elif command == 'help':
                    self.show_help()
                elif command == 'test':
                    self.run_stability_tests()
                elif command.startswith('sim'):
                    # Parse simulation days
                    parts = command.split()
                    days = 30
                    if len(parts) > 1:
                        try:
                            days = int(parts[1])
                        except ValueError:
                            print("Invalid number of days, using default (30)")
                    self.run_economic_simulation(days)
                elif command == 'status':
                    self.show_system_status()
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nReceived interrupt signal")
                break
            except EOFError:
                print("\nReceived EOF")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"Error: {e}")
        
        print("👋 Goodbye!")
        return 0
    
    def show_help(self):
        """Show available commands"""
        print("\n📚 AVAILABLE COMMANDS:")
        print("  help          - Show this help message")
        print("  test          - Run stability tests")
        print("  sim [days]    - Run economic simulation (default 30 days)")
        print("  status        - Show system status")
        print("  quit / exit   - Exit the program")
    
    def show_system_status(self):
        """Show current system status"""
        print("\n🔧 SYSTEM STATUS:")
        print(f"  Logging level: {'DEBUG' if verbose else 'INFO'}")
        print(f"  Log file: space_game_headless.log")
        print(f"  Process ID: {os.getpid()}")
        print(f"  Python version: {sys.version}")

def main():
    """Main entry point"""
    runner = HeadlessGameRunner()
    
    # Check for command line arguments
    test_mode = os.environ.get('GAME_TEST_MODE', '0') == '1'
    
    if test_mode:
        # Run stability tests
        return runner.run_stability_tests()
    elif len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            return runner.run_stability_tests()
        elif sys.argv[1] == 'sim':
            days = 30
            if len(sys.argv) > 2:
                try:
                    days = int(sys.argv[2])
                except ValueError:
                    print("Invalid number of days, using default (30)")
            return runner.run_economic_simulation(days)
        elif sys.argv[1] == 'interactive':
            return runner.run_interactive_mode()
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("Available commands: test, sim [days], interactive")
            return 1
    else:
        # Default to interactive mode
        return runner.run_interactive_mode()

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        print(f"💥 FATAL ERROR: {e}")
        sys.exit(1)