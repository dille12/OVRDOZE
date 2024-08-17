import random
class SyncAgent:
    def __init__(self):
        self.id = random.randint(0, 255)
        self._values = self.__dict__.copy()
    
    def _tick(self):
        packets = []
        for x in self._values.keys():

            if x in ["_values"]:
                continue

            if self.__dict__[x] != self._values[x]:
                packets.append([x, str(self.__dict__[x])])
        self._values = self.__dict__.copy()
        
    

if __name__ == "__main__":
    agent = SyncAgent()
    agent._tick()
    agent.shit = 2
    agent._tick()