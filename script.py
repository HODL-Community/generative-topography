import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from noise import pnoise2
import random
from multiprocessing import Pool
import os
import json

def generate_noise(args):
    i, width, scale, octaves, persistence, lacunarity, base = args
    row = np.zeros(width)
    for j in range(width):
        row[j] = pnoise2(i*scale, j*scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=2048, repeaty=2048, base=base) * 2
    return row

def generate_color_map(scale, seed):
    random.seed(seed)
    base = random.randint(0, 100)
    color_count = 256
    color_sequence = []
    r, g, b = random.random(), random.random(), random.random()  # Starting color
    for i in range(color_count):
        t = i / (color_count - 1)  # Normalized index
        x, y = t * scale, t * scale  # Coordinate scaling
        r = np.clip(r + pnoise2(x, y, base=base) * 0.1, 0, 1)  # Adding noise and ensuring values stay in [0, 1]
        g = np.clip(g + pnoise2(x + 100, y, base=base) * 0.1, 0, 1)  # Adding noise and ensuring values stay in [0, 1]
        b = np.clip(b + pnoise2(x, y + 100, base=base) * 0.1, 0, 1)  # Adding noise and ensuring values stay in [0, 1]
        color_sequence.append((r, g, b))
    return mcolors.LinearSegmentedColormap.from_list('custom', color_sequence)



def generate_topographic_map(width, height, scale=None, octaves=6, persistence=0.65, lacunarity=2.0, seed=4567567):
    random.seed(seed)
    if scale is None:
        scale = random.uniform(0.000003, 0.0001)
    base = random.randint(0, 100)
    with Pool() as pool:
        world = np.array(pool.map(generate_noise, [(i, width, scale, octaves, persistence, lacunarity, base) for i in range(height)]))
    return world

def render_topographic_map(world, colormap, filename='topographic_map.png'):
    fig, ax = plt.subplots()
    contour_levels = random.randint(20, 100)  # Random number of contour levels
    contour = ax.contour(world, levels=contour_levels, colors='black', linewidths=0.2, linestyles='solid')
    ax.imshow(world, cmap=colormap, extent=contour.extent)
    ax.axis('off')  # This line removes the axes for a cleaner look.
    plt.savefig(filename, dpi=1200, bbox_inches='tight')
    plt.close(fig)  # Close the figure to free up resources

def main():
    image_count = int(input("Enter the number of images to generate: "))
    width, height = 4000, 4000  # Image dimensions

    # Create directories to store the generated images and JSON files
    os.makedirs("generated_images", exist_ok=True)
    os.makedirs("generated_json", exist_ok=True)

    for i in range(image_count):
        print(f"Generating image {i + 1} of {image_count}...")

        # Random seeds for color and height
        color_seed, height_seed = random.randint(0, 1000000), random.randint(0, 1000000)
        scale = random.uniform(0.000003, 0.0001)
        contour_levels = random.randint(20, 100)

        # Generate the topographic map and color map
        topographic_map = generate_topographic_map(width, height, scale=scale, seed=height_seed)
        colormap = generate_color_map(10.0, seed=color_seed)

        # Render the topographic map and save it to a file
        image_filename = f"generated_images/{i + 1}.png"
        render_topographic_map(topographic_map, colormap, image_filename)
        print(f"Image {i + 1} saved as {image_filename}")

        # Generate and save JSON file
        json_filename = f"generated_json/{i + 1}.json"
        json_data = {
            "name": f"Topo-Generative Dreams #{i + 1}",
            "description": "A generative art collection by @SnapsNoCaps displaying the beauty of TOPOGRAPHY & perlin noise.",
            "image": f"{i + 1}.png",
            "attributes": [
                {"trait_type": "Perlin Seed", "value": height_seed},
                {"trait_type": "Colour Seed", "value": color_seed},
                {"trait_type": "scale", "value": scale},
                {"trait_type": "Contour Levels", "value": contour_levels}
            ],
        }
        with open(json_filename, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"JSON for image {i + 1} saved as {json_filename}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
