from npcs.soldier import Soldier
from values import *
class Patrol:
    def __init__(
            self,
            app,
            pos,
            interactables,
            target_actor,
            NAV_MESH,
            walls_filtered,
            map,
        ):
        self.app = app
        self.pos = pos
        self.interactables = interactables
        self.target_actor = target_actor
        self.NAV_MESH = NAV_MESH
        self.walls = walls_filtered
        self.map = map

        self.troops = []

        self.patrol_leader = None


        for i in range(random.randint(2,3)):

            soldier = Soldier(
                app,
                map.get_random_point(walls_filtered, p_pos=self.target_actor.pos.copy(), max_dist = 300, max_dist_point = self.pos),
                interactables,
                target_actor,
                NAV_MESH,
                walls_filtered,
                map,
            )

            soldier.patrol = self

            self.troops.append(soldier)

            enemy_list.append(soldier)

        self.check_leader()



    def check_leader(self):
        if self.troops:
            self.patrol_leader = self.troops[0]
