import func
from values import *

terminal = pygame.font.Font(fp("texture/terminal.ttf"), 20)
terminal2 = pygame.font.Font(fp("texture/terminal.ttf"), 30)
terminal3 = pygame.font.Font(fp("texture/terminal.ttf"), 10)


class weapon_button:
    def __init__(self, weapon, slot):
        self.weapon = weapon
        self.slot = slot
        self.active = False

    def tick(self, app, screen, y_pos, mouse_pos, click):
        visible = True
        if self.slot < y_pos - 0.5 or self.slot > y_pos + 2.5:
            visible = False

        def_pos = [20, 100 + (self.slot - y_pos) * 100]
        owned = False
        if self.weapon.name in app.ownedGuns:
            owned = True

        if visible:

            


            if 20 < mouse_pos[0] < 320 and def_pos[1] < mouse_pos[1] < def_pos[1] + 67:
                
                if owned:
                    screen.blit(self.weapon.image_non_alpha, def_pos)
                else:
                    func.blit_glitch(screen, self.weapon.image_red, def_pos, glitch = 5)

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
                if owned:
                    screen.blit(self.weapon.image_non_alpha, def_pos)
                else:
                    func.blit_glitch(screen, self.weapon.image_red, def_pos, glitch = 5)
            else:
                if owned:
                    screen.blit(self.weapon.image, def_pos)
                else:
                    func.blit_glitch(screen, self.weapon.image_red, def_pos, glitch = 5)

            if owned:

                if self.active:
                    iIm = 1
                else:
                    iIm = 0

                for i, x in enumerate(app.ownedUpgrades[self.weapon.name]):
                    y_pos = 2 + i*21
                    x_pos = 178
                    screen.blit(upgradeIcons[x.replace(" ", "").lower()][iIm], [def_pos[0] + x_pos, def_pos[1] + y_pos])


            if self.active:
                pygame.draw.rect(
                    screen,
                    [255, 155, 155],
                    [def_pos[0] - 3, def_pos[1] - 3, 206, 73],
                    3,
                )
                color = [255, 0, 0]

        if self.active and owned:
            text = terminal2.render(self.weapon.name, False, [255, 255, 255])
            screen.blit(text, [size[0] / 3, 60])

            text = terminal.render(f"Ammo : {self.weapon.ammo}", False, [255, 255, 255])
            screen.blit(text, [size[0] / 3, 90])

            text = terminal.render(
                f"Ammo capacity : {self.weapon._clip_size} + 1", False, [255, 255, 255]
            )
            screen.blit(text, [size[0] / 3, 110])

            if self.weapon.semi_auto:
                text = terminal.render(
                    f"Firemode : Semi-Automatic", False, [255, 255, 255]
                )
                screen.blit(text, [size[0] / 3, 130])
            elif self.weapon.burst:
                text = terminal.render(
                    f"Firemode : {self.weapon.burst_bullets} round burstfire, RPM : {self.weapon._bullet_per_min}",
                    False,
                    [255, 255, 255],
                )
                screen.blit(text, [size[0] / 3, 130])

            else:
                text = terminal.render(
                    f"Firemode : Fully Automatic, RPM : {self.weapon._bullet_per_min}",
                    False,
                    [255, 255, 255],
                )
                screen.blit(text, [size[0] / 3, 130])

            if self.weapon.rocket_launcher:
                text = terminal.render(
                    f"Exploding projectiles", False, [255, 255, 255]
                )
                screen.blit(text, [size[0] / 3, 150])


            elif self.weapon.piercing_bullets > 1:

                text = terminal.render(
                    f"Armor piercing bullets", False, [255, 255, 255]
                )
                screen.blit(text, [size[0] / 3, 150])

            else:

                text = terminal.render(f"Nonpiercing bullets", False, [255, 255, 255])
                screen.blit(text, [size[0] / 3, 150])
            if self.weapon._shotgun:
                text = terminal.render(
                    f"Damage per shot : {self.weapon._damage} x {self.weapon._bullets_at_once} pellets",
                    False,
                    [255, 255, 255],
                )
            else:
                text = terminal.render(
                    f"Damage per shot : {self.weapon._damage}", False, [255, 255, 255]
                )
            screen.blit(text, [size[0] / 3, 170])

            text = terminal.render(
                f"Reload time : {round(self.weapon._reload_rate/60,1)}s",
                False,
                [255, 255, 255],
            )
            screen.blit(text, [size[0] / 3, 190])

            if self.weapon._spread < 2:
                text = terminal.render(f"Accuracy : Great", False, [0, 255, 0])
                screen.blit(text, [size[0] / 3, 240])

            elif self.weapon._spread < 4:
                text = terminal.render(f"Accuracy : Good", False, [255, 255, 0])
                screen.blit(text, [size[0] / 3, 240])

            elif self.weapon._spread < 6:
                text = terminal.render(f"Accuracy : Normal", False, [255, 153, 0])
                screen.blit(text, [size[0] / 3, 240])

            else:
                text = terminal.render(f"Accuracy : Bad", False, [255, 0, 0])
                screen.blit(text, [size[0] / 3, 240])

            if self.weapon.spread_per_bullet < 2:
                text = terminal.render(f"Recoil : Low", False, [0, 255, 0])
                screen.blit(text, [size[0] / 3, 260])

            elif self.weapon.spread_per_bullet < 3:
                text = terminal.render(f"Recoil : High", False, [255, 255, 0])
                screen.blit(text, [size[0] / 3, 260])

            elif self.weapon.spread_per_bullet < 4:
                text = terminal.render(f"Recoil : Very high", False, [255, 153, 0])
                screen.blit(text, [size[0] / 3, 260])

            else:
                text = terminal.render(f"Recoil : Extremely High", False, [255, 0, 0])
                screen.blit(text, [size[0] / 3, 260])

            if self.weapon._spread_recovery < 0.93:
                text = terminal.render(f"Recoil recovery : Great", False, [0, 255, 0])
                screen.blit(text, [size[0] / 3, 280])

            elif self.weapon._spread_recovery < 0.945:
                text = terminal.render(f"Recoil recovery : Good", False, [255, 255, 0])
                screen.blit(text, [size[0] / 3, 280])

            elif self.weapon._spread_recovery < 0.96:
                text = terminal.render(
                    f"Recoil recovery : Normal", False, [255, 153, 0]
                )
                screen.blit(text, [size[0] / 3, 280])

            else:
                text = terminal.render(f"Recoil recovery : Bad", False, [255, 0, 0])
                screen.blit(text, [size[0] / 3, 280])

            if self.weapon.handling > 0.8:
                text = terminal.render(f"Handling : Great", False, [0, 255, 0])
                screen.blit(text, [size[0] / 3, 300])

            elif self.weapon.handling > 0.6:
                text = terminal.render(f"Handling : Good", False, [255, 255, 0])
                screen.blit(text, [size[0] / 3, 300])

            elif self.weapon.handling > 0.4:
                text = terminal.render(f"Handling : Normal", False, [255, 153, 0])
                screen.blit(text, [size[0] / 3, 300])

            else:
                text = terminal.render(f"Handling : Bad", False, [255, 0, 0])
                screen.blit(text, [size[0] / 3, 300])

            if self.weapon.view > 0.03:
                text = terminal.render(f"Visibility : Great", False, [0, 255, 0])
                screen.blit(text, [size[0] / 3, 320])

            elif self.weapon.view > 0.02:
                text = terminal.render(f"Visibility : Good", False, [255, 255, 0])
                screen.blit(text, [size[0] / 3, 320])

            elif self.weapon.view > 0.01:
                text = terminal.render(f"Visibility : Normal", False, [255, 153, 0])
                screen.blit(text, [size[0] / 3, 320])

            else:
                text = terminal.render(f"Visibility : Bad", False, [255, 0, 0])
                screen.blit(text, [size[0] / 3, 320])

        

        else:
            color = [255, 255, 255]

        if self.active:

            if not owned:

                priceColor = [100, 255, 100] if self.weapon.price <= app.money else [255,0,0]

                text = terminal2.render(
                    f"PRICE : {self.weapon.price}$", False, priceColor
                )

            elif self.weapon.name in app.ownedUpgrades:
                text = terminal2.render(
                    f"UPGRADES : {len(app.ownedUpgrades[self.weapon.name])}/{len(self.weapon.availableUpgrades)}", False, [255,255,255]
                )

            screen.blit(text, [size[0] / 3, 350])
            
            text = terminal2.render(self.weapon.name if owned else "UNKNOWN", False, [255, 255, 255])
            screen.blit(text, [size[0] / 3, 60])

        if visible and owned:

            text = terminal.render(self.weapon.name, False, color)
            screen.blit(text, def_pos)

        elif visible:
            if self.weapon.price <= app.money:
                if app.upgradeBlink.value < app.upgradeBlink.max_value/2:
                    screen.blit(buyIcon, [20, def_pos[1] + 47])

        if owned:
            req = [100, 250, 500]
            fulfilled = False
            if self.weapon.name in app.ownedUpgrades and self.weapon.name in app.weaponKills:
                if len(app.ownedUpgrades[self.weapon.name]) != 3:
                    amount = req[len(app.ownedUpgrades[self.weapon.name])]
                    fulfilled = amount <= app.weaponKills[self.weapon.name]

                if fulfilled:
                    if app.upgradeBlink.value < app.upgradeBlink.max_value/2:
                        screen.blit(upgradeIcon, [20, def_pos[1] + 47])

        self.owned = owned


