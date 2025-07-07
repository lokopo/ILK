#!/usr/bin/env python3

import os
import sys
import subprocess
import venv
import argparse
import logging

def setup_logging(verbose=False):
    """Setup logging with proper formatting and levels."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('game_launch.log', mode='w')
        ]
    )
    return logging.getLogger(__name__)

def check_environment():
    """Check if we're in a headless environment."""
    headless_indicators = [
        'DISPLAY' not in os.environ,
        'SSH_CONNECTION' in os.environ,
        'SSH_CLIENT' in os.environ,
        os.environ.get('TERM', '').lower() in ['screen', 'tmux', 'linux'],
        not os.path.exists('/dev/tty'),
    ]
    
    headless_score = sum(headless_indicators)
    
    # Check for common headless system indicators
    try:
        with open('/proc/version', 'r') as f:
            version = f.read().lower()
            if 'microsoft' in version or 'wsl' in version:
                headless_score += 1
    except:
        pass
    
    return headless_score >= 2

def setup_venv(logger):
    """Setup virtual environment with better error handling."""
    try:
        if not os.path.exists("venv"):
            logger.info("Creating virtual environment...")
            venv.create("venv", with_pip=True)
            logger.info("Virtual environment created successfully")
        else:
            logger.info("Virtual environment already exists")
        
        # Determine the pip path based on the OS
        if sys.platform == "win32":
            pip_path = os.path.join("venv", "Scripts", "pip")
            python_path = os.path.join("venv", "Scripts", "python")
        else:
            pip_path = os.path.join("venv", "bin", "pip")
            python_path = os.path.join("venv", "bin", "python")
        
        # Check if pip exists
        if not os.path.exists(pip_path):
            logger.error(f"pip not found at {pip_path}")
            return None
            
        # Install requirements
        logger.info("Installing requirements...")
        result = subprocess.run([pip_path, "install", "-r", "requirements.txt"], 
                                capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"Failed to install requirements: {result.stderr}")
            return None
        else:
            logger.info("Requirements installed successfully")
            
        return python_path
        
    except Exception as e:
        logger.error(f"Error setting up virtual environment: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='ILK Space Game Launcher',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_me.py                    # Normal GUI mode
  python run_me.py --headless         # Headless mode (no graphics)
  python run_me.py --test             # Run stability tests
  python run_me.py --headless --test  # Run headless tests
  python run_me.py --verbose          # Enable verbose logging
        """
    )
    
    parser.add_argument('--headless', action='store_true', 
                        help='Run in headless mode (no graphics)')
    parser.add_argument('--test', action='store_true', 
                        help='Run stability tests instead of the game')
    parser.add_argument('--verbose', '-v', action='store_true', 
                        help='Enable verbose logging')
    parser.add_argument('--force-gui', action='store_true', 
                        help='Force GUI mode even in headless environment')
    parser.add_argument('--diagnostics', action='store_true', 
                        help='Run system diagnostics')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.verbose)
    
    logger.info("=== ILK Space Game Launcher Starting ===")
    logger.info(f"Python: {sys.version}")
    logger.info(f"Platform: {sys.platform}")
    logger.info(f"Arguments: {args}")
    
    # Check environment
    is_headless_env = check_environment()
    logger.info(f"Headless environment detected: {is_headless_env}")
    
    # Determine run mode
    if args.headless or (is_headless_env and not args.force_gui):
        run_mode = "headless"
    else:
        run_mode = "gui"
    
    logger.info(f"Selected run mode: {run_mode}")
    
    # Setup virtual environment
    python_path = setup_venv(logger)
    if not python_path:
        logger.error("Failed to setup virtual environment")
        return 1
    
    # Run diagnostics if requested
    if args.diagnostics:
        logger.info("Running system diagnostics...")
        try:
            result = subprocess.run([python_path, "-c", 
                "import sys; print('Python OK'); import pygame; print('Pygame OK'); import numpy; print('NumPy OK')"],
                capture_output=True, text=True)
            logger.info(f"Diagnostics result: {result.stdout}")
            if result.stderr:
                logger.warning(f"Diagnostics warnings: {result.stderr}")
        except Exception as e:
            logger.error(f"Diagnostics failed: {e}")
    
    # Choose what to run
    if args.test:
        if run_mode == "headless":
            logger.info("Starting headless stability tests...")
            script_name = "space_game_headless.py"
            script_args = ["test"]
        else:
            logger.info("Starting GUI tests...")
            script_name = "space_game.py"
            script_args = []
            os.environ['GAME_TEST_MODE'] = '1'
    else:
        if run_mode == "headless":
            logger.info("Starting headless game mode...")
            script_name = "space_game_headless.py"
            script_args = ["interactive"]
        else:
            logger.info("Starting GUI game mode...")
            script_name = "space_game.py"
            script_args = []
    
    # Set environment variables for the game
    os.environ['GAME_VERBOSE'] = '1' if args.verbose else '0'
    
    try:
        # Run the game
        logger.info(f"Launching {script_name} with args: {script_args}")
        cmd = [python_path, script_name] + script_args
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        if result.returncode == 0:
            logger.info("Game completed successfully")
            return 0
        else:
            logger.error(f"Game exited with code {result.returncode}")
            return result.returncode
            
    except KeyboardInterrupt:
        logger.info("Game interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Error running game: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 