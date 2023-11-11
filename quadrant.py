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
    

            