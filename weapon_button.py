import func
from values import *
terminal = pygame.font.Font('texture/terminal.ttf', 20)
terminal2 = pygame.font.Font('texture/terminal.ttf', 30)
terminal3 = pygame.font.Font('texture/terminal.ttf', 10)

class weapon_button:
    def __init__(self, weapon, slot):
        self.weapon = weapon
        self.slot = slot
        self.active = False

    def tick(self, screen, y_pos, mouse_pos, click):
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
                        self.active = True

                        for x in ruperts_shop_selections:
                            if x.weapon != self.weapon:
                                x.active = False


            elif self.active:
                screen.blit(self.weapon.image_non_alpha, def_pos)
            else:
                screen.blit(self.weapon.image, def_pos)

            if self.active:
                pygame.draw.rect(screen, [255,155,155], [def_pos[0]-3, def_pos[1]-3, 206, 73],3)
                color = [255,0,0]

        if self.active:
            text = terminal2.render(self.weapon.name, False, [255,255,255])
            screen.blit(text, [size[0]/3, 60])

            text = terminal.render(f"Ammo : {self.weapon.ammo}", False, [255,255,255])
            screen.blit(text, [size[0]/3, 90])

            text = terminal.render(f"Ammo capacity : {self.weapon._clip_size} + 1", False, [255,255,255])
            screen.blit(text, [size[0]/3, 110])

            if self.weapon.semi_auto:
                text = terminal.render(f"Firemode : Semi-Automatic", False, [255,255,255])
                screen.blit(text, [size[0]/3, 130])
            elif self.weapon.burst:
                text = terminal.render(f"Firemode : {self.weapon.burst_bullets} round burstfire, RPM : {self.weapon._bullet_per_min}", False, [255,255,255])
                screen.blit(text, [size[0]/3, 130])

            else:
                text = terminal.render(f"Firemode : Fully Automatic, RPM : {self.weapon._bullet_per_min}", False, [255,255,255])
                screen.blit(text, [size[0]/3, 130])

            if self.weapon.piercing_bullets:

                text = terminal.render(f"Armor piercing bullets", False, [255,255,255])
                screen.blit(text, [size[0]/3, 150])

            else:

                text = terminal.render(f"Nonpiercing bullets", False, [255,255,255])
                screen.blit(text, [size[0]/3, 150])
            if self.weapon._shotgun:
                text = terminal.render(f"Damage per shot : {self.weapon._damage} x {self.weapon._bullets_at_once} pellets", False, [255,255,255])
            else:
                text = terminal.render(f"Damage per shot : {self.weapon._damage}", False, [255,255,255])
            screen.blit(text, [size[0]/3, 170])

            text = terminal.render(f"Reload time : {round(self.weapon._reload_rate/60,1)}s", False, [255,255,255])
            screen.blit(text, [size[0]/3, 190])

            if self.weapon._spread < 2:
                text = terminal.render(f"Accuracy : Great", False, [0,255,0])
                screen.blit(text, [size[0]/3, 240])

            elif self.weapon._spread < 4:
                text = terminal.render(f"Accuracy : Good", False, [255,255,0])
                screen.blit(text, [size[0]/3, 240])

            elif self.weapon._spread < 6:
                text = terminal.render(f"Accuracy : Normal", False, [255,153,0])
                screen.blit(text, [size[0]/3, 240])

            else:
                text = terminal.render(f"Accuracy : Bad", False, [255,0,0])
                screen.blit(text, [size[0]/3, 240])


            if self.weapon.spread_per_bullet < 2:
                text = terminal.render(f"Recoil : Low", False, [0,255,0])
                screen.blit(text, [size[0]/3, 260])

            elif self.weapon.spread_per_bullet < 3:
                text = terminal.render(f"Recoil : High", False, [255,255,0])
                screen.blit(text, [size[0]/3, 260])

            elif self.weapon.spread_per_bullet < 4:
                text = terminal.render(f"Recoil : Very high", False, [255,153,0])
                screen.blit(text, [size[0]/3, 260])

            else:
                text = terminal.render(f"Recoil : Extremely High", False, [255,0,0])
                screen.blit(text, [size[0]/3, 260])

            if self.weapon._spread_recovery < 0.93:
                text = terminal.render(f"Recoil recovery : Great", False, [0,255,0])
                screen.blit(text, [size[0]/3, 280])

            elif self.weapon._spread_recovery < 0.945:
                text = terminal.render(f"Recoil recovery : Good", False, [255,255,0])
                screen.blit(text, [size[0]/3, 280])

            elif self.weapon._spread_recovery < 0.96:
                text = terminal.render(f"Recoil recovery : Normal", False, [255,153,0])
                screen.blit(text, [size[0]/3, 280])

            else:
                text = terminal.render(f"Recoil recovery : Bad", False, [255,0,0])
                screen.blit(text, [size[0]/3, 280])

            if self.weapon.handling > 0.8:
                text = terminal.render(f"Handling : Great", False, [0,255,0])
                screen.blit(text, [size[0]/3, 300])

            elif self.weapon.handling > 0.6:
                text = terminal.render(f"Handling : Good", False, [255,255,0])
                screen.blit(text, [size[0]/3, 300])

            elif self.weapon.handling > 0.4:
                text = terminal.render(f"Handling : Normal", False, [255,153,0])
                screen.blit(text, [size[0]/3, 300])

            else:
                text = terminal.render(f"Handling : Bad", False, [255,0,0])
                screen.blit(text, [size[0]/3, 300])


            if self.weapon.view > 0.03:
                text = terminal.render(f"Visibility : Great", False, [0,255,0])
                screen.blit(text, [size[0]/3, 320])

            elif self.weapon.view > 0.02:
                text = terminal.render(f"Visibility : Good", False, [255,255,0])
                screen.blit(text, [size[0]/3, 320])

            elif self.weapon.view > 0.01:
                text = terminal.render(f"Visibility : Normal", False, [255,153,0])
                screen.blit(text, [size[0]/3, 320])

            else:
                text = terminal.render(f"Visibility : Bad", False, [255,0,0])
                screen.blit(text, [size[0]/3, 320])

            text = terminal2.render(f"PRICE : {self.weapon.price}$", False, [255,255,255])
            screen.blit(text, [size[0]/3, 350])














        else:
            color = [255,255,255]

        if visible:

            text = terminal.render(self.weapon.name, False, color)
            screen.blit(text, def_pos)

        self.owned = owned

        if owned and visible:

            text = terminal2.render("OWNED", False, [255,0,0])
            screen.blit(text, func.minus_list(func.minus(def_pos, [100,34]), text.get_rect().center))
