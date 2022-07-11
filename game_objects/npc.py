from game_objects.game_object import Game_Object
import classtest
from values import *
import los
import func
import classes
class NPC(Game_Object):
    def __init__(self, pos, angle, player_inventory, name, image, potrait):
        self.pos = pos
        self.image = pygame.transform.scale( pygame.image.load("texture/" + image),[round(119/multiplier),round(119/multiplier)]).convert_alpha()

        self.image, rect= func.rot_center(self.image, angle, self.pos[0], self.pos[1])
        rect = self.image.get_rect().center
        self.pos = [self.pos[0] - rect[0], self.pos[1] - rect[1]]

        self.potrait = pygame.image.load("texture/" + potrait)

        self.interactable = classes.Interactable(self.pos, player_inventory, name = name, type = "NPC", image = "placeholder_npc.png")


    def tick(self, screen, player_actor, camera_pos, map):
        self.temppos = func.minus_list(self.pos,camera_pos)

        if True:

            screen.blit(self.image, self.temppos)

        self.interactable.tick(screen, player_actor.pos, camera_pos)
