from PIL import Image
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_IMAGE = os.path.join(BASE_DIR, "data", "glaster_blaster.jpg")
OUTPUT_MEM = os.path.join(BASE_DIR, "data", "glaster_blaster.mem")

WIDTH = 30
HEIGHT = 40

# Load image
img = Image.open(INPUT_IMAGE).convert("L")  # convert to grayscale
img = img.resize((WIDTH, HEIGHT))          # ensure correct size

# Get pixel data
pixels = np.array(img, dtype=np.uint8).flatten()

pixels = [63 if p >= 140 else 0 for p in pixels]

# Write to .mem as hex
with open(OUTPUT_MEM, "w") as f:
    for p in pixels:
        f.write(f"{p:02X}\n")

print("Done →", OUTPUT_MEM)
