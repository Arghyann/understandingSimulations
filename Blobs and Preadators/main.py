from environment import Environment
from graph import Graph
from predator import Predator
from blob import Blob
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Array that will store numbers per frame of entities for analyzing graph
blob_number_per_frame = []
predator_number_per_frame = []

# Constants
maxPredators = 50
maxBlobs = 20
maxFrames = 200

# Simulation Environment
env = Environment(50)

# Selecting random frames for the predators to spawn
predFrames = [random.randint(0, maxFrames) for _ in range(maxPredators)]
predFrames.sort()
# Selecting random frames for the blobs to spawn
blobFrames = [random.randint(0, maxFrames) for _ in range(maxBlobs)]
blobFrames.sort()

# Create the plot
fig, ax = plt.subplots()
im = ax.imshow(env.space, animated=True)

# Create text element to display mitosis count outside of the plot
mitosis_text_outside = plt.text(0.5, 1.05, '', color='blue', fontsize=12, ha='center', transform=fig.transFigure)

def update(frame):
    # Generating 5 blobs at random frames
    if frame in blobFrames:
        for _ in range(5):
            tempForGender = random.choice([True, False])
            Blob(tempForGender, 5, env)
    # Blob movement in each frame
    for blob in env.blobs:
        blob.age += 0.2
        blob.movement()

    # Predator generating in random frames
    if frame in predFrames:
        tempForGender = random.choice([True, False])
        Predator(tempForGender, 5, env)

    # Predator movement in each frame
    for predator in env.predators:
        predator.age += 0.2
        predator.movement()

    # Generate food every 10 frames
    if frame % 10 == 0 and frame != 0:
        env.add_food([], 5, 10)

    # Update the plot
    im.set_array(env.space)
    blob_number_per_frame.append(len(env.blobs))
    predator_number_per_frame.append(len(env.predators))
    
    # Update text element with mitosis count
    mitosis_text_outside.set_text(f'Mitosis: {env.mitosisCount}')
    
    # Return a list of artists to be updated in the animation
    return [im, mitosis_text_outside]

# Plot the animation
ani = animation.FuncAnimation(fig, update, frames=maxFrames, interval=100, blit=True)  # Actually animates all the frames

# Display the plot
plt.show()

# Plot the graph for analyzing the number of entities
plt.plot(blob_number_per_frame, label='Blobs')
plt.plot(predator_number_per_frame, label='Predators')
plt.xlabel('Frame')
plt.ylabel('Number of entities')
plt.legend()
plt.show()
