import random
from core.values import *

class MP_Object:
    def __init__(self):
        self.app = ID_container
        if "id" in self.__dict__:
            if self.id != -1:
                self.app.nwobjects[self.id] = self
                return

        while True:
            self.id = random.randint(0, 4294967296)

            if self.id not in self.app.nwobjects:
                self.app.nwobjects[self.id] = self
                break


    def kill_id(self):
        if self.id in self.app.nwobjects:
            del self.app.nwobjects[self.id]
