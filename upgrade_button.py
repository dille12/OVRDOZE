import func
from values import *
from armory import upgradeMap, statMap

terminal = pygame.font.Font("texture/terminal.ttf", 20)
terminal2 = pygame.font.Font("texture/terminal.ttf", 30)
terminal3 = pygame.font.Font("texture/terminal.ttf", 10)


class upgradeButton:
    def __init__(self, weapon, slot):
        self.weapon = weapon
        self.slot = slot
        self.active = False
        self.upgradeI = 0
        self.owned = False

    def tick(self, screen, y_pos, mouse_pos, click, player_actor):
        visible = True
        if self.slot < y_pos - 0.5 or self.slot > y_pos + 2.5:
            visible = False

        def_pos = [20, 100 + (self.slot - y_pos) * 100]
        owned = False
        for x in player_weapons:
            if x.name == self.weapon.name:

                owned = True
                break

        if visible:

            if 20 < mouse_pos[0] < 320 and def_pos[1] < mouse_pos[1] < def_pos[1] + 67:

                screen.blit(self.weapon.image_non_alpha, def_pos)

                if click:
                    menu_click.play()
                    if self.active:
                        self.active = False
                    else:

                        for x in player_actor.upgradeButtons:
                            x.active = False
                        self.active = True

            elif self.active:
                screen.blit(self.weapon.image_non_alpha, def_pos)
            else:
                screen.blit(self.weapon.image, def_pos)

            if self.active:
                pygame.draw.rect(
                    screen,
                    [255, 155, 155],
                    [def_pos[0] - 3, def_pos[1] - 3, 206, 73],
                    3,
                )
                color = [255, 0, 0]

                

                LRect = pygame.Rect([350,120], arrowLeft.get_size())
                RRect = pygame.Rect([600,120], arrowRight.get_size())

                if LRect.collidepoint(mouse_pos):
                    screen.blit(arrowLeftRed, [350,120])
                    if click:
                        self.upgradeI -= 1
                        menu_click.play()
                else:
                    screen.blit(arrowLeft, [350,120])

                if RRect.collidepoint(mouse_pos):
                    screen.blit(arrowRightRed, [600,120])
                    if click:
                        self.upgradeI += 1
                        menu_click.play()
                else:
                    screen.blit(arrowRight, [600,120])

                if self.upgradeI < 0:
                    self.upgradeI = len(self.weapon.availableUpgrades) - 1
                if self.upgradeI > len(self.weapon.availableUpgrades) - 1:
                    self.upgradeI = 0

                t = terminal.render(self.weapon.availableUpgrades[self.upgradeI], False, [255,255,255])

                screen.blit(t, [487 - t.get_size()[0]/2, 120])

                t = terminal.render(f"{self.upgradeI + 1}/{len(self.weapon.availableUpgrades)}", False, [155,155,155])

                screen.blit(t, [620, 120])

                u = self.weapon.availableUpgrades[self.upgradeI]

                if u in upgradeMap and self.upgradeI not in self.weapon.activatedUpgrades:
                    t = terminal.render(upgradeMap[u]["Desc"], False, [155,155,155])

                    screen.blit(t, [350, 150])

                    stat = upgradeMap[u]["stat"]

                    if upgradeMap[u]["stat"] in statMap:
                        v = statMap[stat]
                        t = terminal.render(f"Stat: {v}", False, [155,155,155])
                    else:
                        v = stat
                        t = terminal.render(f"Stat: {v}", False, [155,155,155])
                    screen.blit(t, [350, 180])

                    if "set" in upgradeMap[u]:
                        v = upgradeMap[u]["set"]
                        t = terminal.render(f"Value: {self.weapon.__dict__[stat]} ] {v}", False, [155,155,155])
                        

                    if "addval" in upgradeMap[u]:
                        v = upgradeMap[u]["addval"]

                        t = terminal.render(f"Value: {self.weapon.__dict__[stat]} ] {self.weapon.__dict__[stat] + v}", False, [155,155,155])

                    if "multval" in upgradeMap[u]:
                        v = upgradeMap[u]["multval"]

                        t = terminal.render(f"Value: {self.weapon.__dict__[stat]} ] {self.weapon.__dict__[stat] * v}", False, [155,155,155])

                    screen.blit(t, [350, 210])
                else:
                    t = terminal.render("Upgrade already owned.", False, [155,155,155])
                    screen.blit(t, [350, 180])

                         
                




        if self.active:
            text = terminal2.render(self.weapon.name, False, [255, 255, 255])
            screen.blit(text, [size[0] / 3, 60])


        else:
            color = [255, 255, 255]

        if visible:

            text = terminal.render(self.weapon.name, False, color)
            screen.blit(text, def_pos)

     