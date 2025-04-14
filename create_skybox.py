#!/usr/bin/env python3

import os
import numpy as np
from PIL import Image

# Create assets/textures directory if it doesn't exist
os.makedirs('assets/textures', exist_ok=True)

# Function to create a starry sky texture
def create_starry_sky(width, height, num_stars=1000):
    # Create a black background
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Add stars (white pixels)
    for _ in range(num_stars):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        brightness = np.random.randint(200, 256)
        img[y, x] = [brightness, brightness, brightness]
    
    # Add some larger stars
    for _ in range(50):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        size = np.random.randint(1, 3)
        brightness = np.random.randint(200, 256)
        
        for dx in range(-size, size+1):
            for dy in range(-size, size+1):
                if 0 <= x+dx < width and 0 <= y+dy < height:
                    # Create a small star with a gradient
                    distance = np.sqrt(dx**2 + dy**2)
                    if distance <= size:
                        factor = 1 - (distance / size)
                        img[y+dy, x+dx] = [brightness*factor, brightness*factor, brightness*factor]
    
    return Image.fromarray(img)

# Create the six faces of the skybox
faces = ['right', 'left', 'top', 'bottom', 'front', 'back']
for face in faces:
    # Create a starry sky texture for each face
    img = create_starry_sky(1024, 1024)
    
    # Save the texture
    img.save(f'assets/textures/skybox_{face}.png')

print("Skybox textures created successfully!") 