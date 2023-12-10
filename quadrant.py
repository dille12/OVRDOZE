import numpy as np
import los
class Quadrant:
    def __init__(self, app, map, x, y):
        self.app = app
        self.map = map
        self.x = x
        self.y = y
        self.enemies = []
        self.bullets = []
        self.fires = []

        div = self.app.divisions

        self.x_range = [map.size_converted[0] * x/div, map.size_converted[0] * (x+1)/div]
        self.y_range = [map.size_converted[1] * y/div, map.size_converted[1] * (y+1)/div]

    def checkIfIn(self, pos):
        return self.x_range[0] <= pos[0] <= self.x_range[1] and self.y_range[0] <= pos[1] <= self.y_range[1]
    
    def update_positions(self, entities, player_actor):
        positions = np.array([entity.pos for entity in entities if entity.visible], dtype = np.float64)
        if positions.shape[0] <= 1:
            return
        pairwise_distances = np.linalg.norm(positions[:, np.newaxis] - positions, axis=-1)
        # Set a repulsion factor
        repulsion_factor = 10

        # Calculate repulsion forces based on distances
        repulsion_forces = repulsion_factor / (pairwise_distances + 1e-6)


        
        # Update positions based on repulsion forces
        for i in range(positions.shape[0]):

            repulsion_forces[i,i] = 0

            # Exclude the entity itself when calculating repulsion forces
            repulsion_directions = (positions[i] - positions)
            repulsion_directions /= (pairwise_distances[i, :] + 1e-6)[:, np.newaxis]

            entityRepulsion = np.repeat(repulsion_forces[i, :][:, np.newaxis], 2, axis=1)
            
            repulsion_force = np.sum(entityRepulsion * repulsion_directions, axis=0)
            p = entities[i].pos + repulsion_force
            entities[i].pos = p.tolist()

    def collisionCheck(self, player_actor):
        self.update_positions(self.enemies, player_actor)
    

            