#!/usr/bin/env python3

import os
import sys
import subprocess
import venv

def setup_venv():
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        venv.create("venv", with_pip=True)
        
        # Determine the pip path based on the OS
        if sys.platform == "win32":
            pip_path = os.path.join("venv", "Scripts", "pip")
        else:
            pip_path = os.path.join("venv", "bin", "pip")
            
        # Install requirements
        print("Installing requirements...")
        subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    
    # Determine the python path based on the OS
    if sys.platform == "win32":
        python_path = os.path.join("venv", "Scripts", "python")
    else:
        python_path = os.path.join("venv", "bin", "python")
    
    return python_path

def main():
    python_path = setup_venv()
    print("Starting game...")
    subprocess.run([python_path, "space_game.py"])

if __name__ == "__main__":
    main() 