from core.values import *

class storyTeller:
    def __init__(self, app, player_inventory):
        self.app = app
        self.player_inventory = player_inventory
        self.playerPerformanceTick = GameTick(15)
        self.playerPerformanceLowHealth = 0
        self.playerPerformanceHighHealth = 100
        self.playerPerformace = 1
        self.gunDropped = False
        self.drugMaxAmounts = {
            "Heroin" : 2,
            "Cocaine" : 3,
            "Diazepam" : 8,
        }
        self.ammoShot = {
            "45 ACP" : 0,
            "9MM" : 0,
            "50 CAL" : 0, 
            "12 GAUGE" : 0, 
            "7.62x39MM" : 0, 
            "5.56x45MM NATO" : 0, 
            "Energy Cell" : 0
        }

    def getGunDropRate(self):
        d = 0.01 * min([((4 - 3 * self.playerPerformace) ** 5), 100]) if not self.gunDropped else 0
        return d
    
    def checkGun(self, gun):
        for x in player_weapons:
            if gun.name == x.name:
                return False
            
        if gun.ammo == "INF" and random.uniform(0, 1) > 0.1:
            return False
            

        return True
    
    def getAmountInWorld(self, item):
        ammoAmountInWorld = self.player_inventory.get_amount_of_type(item.name)
        for x in interactables:
                if x.type == "item" and x.item.name == item.name:
                    ammoAmountInWorld += x.amount
        return ammoAmountInWorld
    

    def ammoUpdate(self, type):
        if type in self.ammoShot:
            self.ammoShot[type] += 0.04
            self.ammoShot[type] = min([1, self.ammoShot[type]])
            
        for i in self.ammoShot:
            self.ammoShot[i] *= (0.995 ** max([1, 4-len(player_weapons)]))


    def getChanceToDropAmmo(self, type):
        return random.uniform(0, 1) > self.ammoShot[type]
        

    def determineItemDropping(self, item, amount):
        if item.name in ["45 ACP", "9MM", "50 CAL", "12 GAUGE", "7.62x39MM", "5.56x45MM NATO", "Energy Cell", "HE Grenade", "Molotov"]:

            ammoAmountInWorld = self.getAmountInWorld(item)

            if item.name == "5.56x45MM NATO" and self.playerPerformace > 0.8:
                return False
            
            if item.name in self.ammoShot:
                if not self.getChanceToDropAmmo(item.name):
                    return False
            

            if ammoAmountInWorld + amount > item.max_stack:
                print("Skipping ammo drop:", item.name, amount, "Amount of ammo in world:", ammoAmountInWorld)
                return False
            
        elif item.name in ["Diazepam", "Cocaine", "Heroin"]:
            if random.uniform(0, self.app.player_actor_ref.sanity/100) < 1 - self.playerPerformace:
                if self.getAmountInWorld(item) + amount <= self.drugMaxAmounts[item.name]:
                    return True
            else:
                print("Not dropping drug")
                return False
            
        elif item.name in ["Sentry Turret", "Moving Turret"]:

            if item.name == "Sentry Turret":
                inWorld = len(turret_list)
            else:
                inWorld = len(turret_bro)

            if random.uniform(0.95, 1.02) > self.playerPerformace and self.getAmountInWorld(item) + inWorld + amount <= item.max_stack:
                return True
            else:
                print("NOT DROPPING", item)
                return False
            
        else:
            if random.uniform(0.95, 1.02) > self.playerPerformace and self.getAmountInWorld(item) + amount <= item.max_stack:
                return True
            else:
                return False



        return True

