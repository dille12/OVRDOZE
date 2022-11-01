import random

class MP_Object:
    def __init__(self, app):
        while True:
            self.id = random.randint(0, 4294967296)
            self.app = app
            if self.id not in self.app.nwobjects:
                self.app.nwobjects[self.id] = self
                break

        print("Identification Successful")
