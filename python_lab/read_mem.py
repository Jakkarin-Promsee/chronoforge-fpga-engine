from PIL import Image
import numpy as np
import os
import re

WIDTH = 30
HEIGHT = 40

# Read file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE_DIR, "output", "test.mem")

with open(path, "r") as f:
    text = f.read()

# Extract only valid hex bytes
data = re.findall(r"\b[0-9A-Fa-f]{2}\b", text)

print("Found bytes:", len(data))  # should be 2400

pixels = [int(x, 16) for x in data]

print(pixels)

# Reshape
img_array = np.array(pixels, dtype=np.uint8).reshape((HEIGHT, WIDTH))

# Save
img = Image.fromarray(img_array, mode='L')
img.save("output.png")
img.show()
