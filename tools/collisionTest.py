import numpy as np
import random
import time
class Entity:
    def __init__(self, x, y):
        self.pos = [x, y]

def update_positions(entities):
    positions = np.array([entity.pos for entity in entities], dtype = np.float64)
    pairwise_distances = np.linalg.norm(positions[:, np.newaxis] - positions, axis=-1)
    # Set a repulsion factor
    repulsion_factor = 0.1

    # Calculate repulsion forces based on distances
    repulsion_forces = repulsion_factor / (pairwise_distances + 1e-6)

    
    # Update positions based on repulsion forces
    for i in range(len(entities)):

        repulsion_forces[i,i] = 0

        # Exclude the entity itself when calculating repulsion forces
        repulsion_directions = (positions[i] - positions)
        repulsion_directions /= (pairwise_distances[i, :] + 1e-6)[:, np.newaxis]

        entityRepulsion = np.repeat(repulsion_forces[i, :][:, np.newaxis], 2, axis=1)
        
        repulsion_force = np.sum(entityRepulsion * repulsion_directions, axis=0)
        entities[i].pos += repulsion_force


entities = []

for x in range(50):
    entities.append(Entity(random.uniform(-5,5), random.uniform(-5,5)))

# Update positions based on repulsion forces


# Print the updated positions
for x in range(100):
    t = time.perf_counter()
    update_positions(entities)

    print(entities[0].pos)
