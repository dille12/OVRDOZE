# Work in progress - very basic app class shell:
# goal: support passing obj instances between modules,
# move funcs out of RUN.property
# - Contrib: Velas2
from game_objects.maps import get_maps
import utilities.get_preferences
from networking.server import Server
from networking.chat import Chat
from networking.datagatherer import DataGatherer
import os
import core.game as game
from core.values import *
import core.func as func
import ast
import pygame
from core.classes import kill_count_render
from weapons.armory import upgradeMap
import pickle
import utilities.highscores as highscores

terminal3 = pygame.font.Font(fp("texture/terminal.ttf"), 50)
terminal2 = pygame.font.Font(fp("texture/terminal.ttf"), 30)
terminal1 = pygame.font.Font(fp("texture/terminal.ttf"), 10)



class App:
    def __init__(self, pygame):
        self.pygame = pygame
        try:
            self.server = Server(self)
        except:
            print("Could not create a server!")
        self.ip = None


        self.loadProgression()


        self.preferences()
        self.chat = Chat(self)
        self.data_collector = DataGatherer(self)
        print(self.res)
        pygame.init()
        pygame.font.init()
        self.path_cache = {}
        self.path_times = {"calc" : [0, 0], "cache" : [0, 0], "max" : 0}
        self.route = None
        self.player_team = placeholder
        self.net = None
        self.endless = True
        self.server_tick_rate = GameTick(1)

        pygame.joystick.init()
        self.joysticks = {}
        self.detectJoysticks = False

        self.players = []
        self.nwobjects = {}
        self.selected_map = 0
        self.multiplayer = True
        self.ping = [0]
        self.loading = False

        self.divisions = 10

        self.soldier_cache = {}

        self.zombiegroup = pygame.sprite.Group()
        self.unitstatuses = []
        self.screen_glitch = 1
        self.pos_sent = False
        self.levels = ["Requiem", "Manufactory", "Liberation", "Contamination"]
        self.day = -1
        self.phase = 0

        self.start_game_with_mp = []
        self.menu_animations = []

        self.vignetteCounter = 0
        self.bloodCounter = 0

        self.weaponInvToggle = False

        self.dontIncreaseDay = False

        self.reloadOnQuit = False

        self.weaponChangeTick = GameTick(30, oneshot=True)

        self.jamTick = GameTick(5)

        self.musicDisplayTick = GameTick(180, oneshot=True)
        self.weaponSwitchTick = GameTick(10, oneshot=True, nonMutable = True)

        self.jamIm = False

        self.enemies_within_range = 0

        self.casings = []

        self.fPressTick = GameTick(15, oneshot=True)
        self.f_press_cont_monitor = False

        self.vibrateTick = GameTick(5, nonMutable=True)
        self.vibratePos = pygame.math.Vector2()
        self.vibrateTargetPos = pygame.math.Vector2()
        self.vibrateVel = pygame.math.Vector2()

        self.ovrdozeGT = GameTick(45, oneshot=True)
        self.ovrdozeGT.value = self.ovrdozeGT.max_value

        self.kills = 0
        self.multi_kill = 0
        self.multi_kill_tick = GameTick(45, oneshot=True)
        self.killedThisTick = False

        self.upgradeBlink = GameTick(40)
        self.notificationBlink = GameTick(40)
        self.bosses = 0
        self.bossTick = GameTick(120, oneshot=True)
        self.bossTick.value = self.bossTick.max_value

        self.y_pos_abs = 0
        self.y_pos = 0
        self.max_y_pos = 0

        self.shop_quit = False
        print("APP INITTED")
        self.loadProgression()
        self.upgradeWeapon = None
        self.lockedLevels = []

        highscores.write_default_highscore()
        highscores.checkHighscores(self)
        self.inLoadLoop = False
        self.tutorialIndex = 0

        self.inIntense = 0

        

    def checkLevelProgression(self):

        self.levelProgression = {"Manufactory" : [5, "NORMAL", "Requiem"], "Liberation" : [10, "NORMAL", "Manufactory"], "Contamination" : [10, "NORMAL", "Liberation"],
                            "Downtown" : [15, "NORMAL", "Contamination"],}

        for x in self.maps_dict:
            map = self.maps_dict[x]["map"]
            if map.name in self.levelProgression:

                minRounds, diff, reqMap = self.levelProgression[map.name]

                if self.highscore[reqMap][diff][0] < minRounds:
                    self.lockedLevels.append(x)

        print("Locked levels:", self.lockedLevels)



    def saveProgression(self):
        path = utilities.get_preferences.get_path("ovrdoze_data/data.pkl")
        with open(path, 'wb') as file:
            # Save the data to the file
            pickle.dump({"money" : self.money, "ownedGuns" : self.ownedGuns, "ownedUpgrades" : self.ownedUpgrades, "weaponKills" : self.weaponKills, 
                         "startingPistol" : self.startingPistol}, file) 

    def loadProgression(self):
        path = utilities.get_preferences.get_path("ovrdoze_data/data.pkl")

        if not os.path.exists(path):
            print("No progression")
            self.money = 0
            self.ownedGuns = ["M1911"]
            self.ownedUpgrades = {"M1911" : []}
            self.weaponKills = {"M1911" : 0}
            self.startingPistol = "M1911"
            self.saveProgression()
            return

        # Open the file in binary read mode
        with open(path, 'rb') as file:
            # Load the data from the file
            loaded_data = pickle.load(file)

        self.money = loaded_data["money"]
        self.ownedGuns = loaded_data["ownedGuns"]
        self.ownedUpgrades = loaded_data["ownedUpgrades"]
        self.weaponKills = loaded_data["weaponKills"]
        self.startingPistol = loaded_data["startingPistol"]
        print("Progression loaded")

    def introScreen(self, screen, clock):

        if IS.introPlayed and not self.reloadOnQuit:
            return

        seq = func.load_animation("anim/vs", 1, 60, alpha=255, intro = False, loadCompressed=True, size = [854,480])
        introSound.play()
        for x in range(len(seq) + 60):
            screen.fill([0,0,0])
            clock.tick(45)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if x < len(seq):
                screen.blit(seq[x], [0,0])

            pygame.display.update()

        IS.introPlayed = True

    def tutorial(self):

        a = terminal3.render(f"{self.tutorialIndex+1}/{len(tutorialTexts)}", False, [255,255,255])
        screen.blit(a, [size[0]/2 - a.get_width()/2, 20])

        a = terminal3.render(f"{tutorialTitles[self.tutorialIndex]}", False, [255,255,255])
        screen.blit(a, [size[0]/2 - a.get_width()/2, 80])



        text = tutorialTexts[self.tutorialIndex]

        t = splitText(text, maxLength=35)
        y_pos = 150
        for x in t:
            a = terminal2.render(x, False, [255,255,255])
            screen.blit(a, [size[0]/2 - a.get_width()/2, y_pos])
            y_pos += 40




    def inspectUpgrades(self, button_unlock, mouse_pos, mouse_single_tick, glitch, button_back_from_upgrades, button_setstartingpistol):

        text = terminal2.render(f"Money : {self.money}$", False, [255, 255, 255])
        screen.blit(text, [20, 150])

        text = terminal2.render(self.upgradeWeapon.name, False, [255, 255, 255])
        screen.blit(text, [40 + self.upgradeWeapon.image_non_alpha.get_size()[0]/2 - text.get_size()[0]/2, 20])
        screen.blit(self.upgradeWeapon.image_non_alpha, [40, 60])

        text = terminal2.render(f"Kills: {self.weaponKills[self.upgradeWeapon.name]}", False, [255, 255, 255])
        screen.blit(text, [40 + self.upgradeWeapon.image_non_alpha.get_size()[0]/2 - text.get_size()[0]/2, 120])

        fulfilled = False
        req = [100, 250, 500]
        if len(self.ownedUpgrades[self.upgradeWeapon.name]) < 3:
            amount = req[len(self.ownedUpgrades[self.upgradeWeapon.name])]
            fulfilled = amount <= self.weaponKills[self.upgradeWeapon.name]
        if fulfilled:

            if self.money < amount*5:
                button_unlock.locked = True
                button_unlock.tooltip = f"Price of unlocking this upgrade is {amount*5}$"
            else:
                button_unlock.locked = False
                button_unlock.tooltip = "Unlock this upgrade"
        elif len(self.ownedUpgrades[self.upgradeWeapon.name]) < 3:
            button_unlock.locked = True
            button_unlock.tooltip = f"You have to reach {amount} kills with this weapon to unlock this upgrade."

        buttonPos = [300, 50 + 60 * min(2, (len(self.ownedUpgrades[self.upgradeWeapon.name])))]

        if len(self.ownedUpgrades[self.upgradeWeapon.name]) < 3:

            text = terminal1.render(f"Required kills: {amount}", False, [255, 255, 255])
            screen.blit(text, [buttonPos[0], buttonPos[1] + 60])
            text = terminal1.render(f"Price: {amount*5}$", False, [255, 255, 255])
            screen.blit(text, [buttonPos[0], buttonPos[1] + 75])

        if len(self.ownedUpgrades[self.upgradeWeapon.name]) < 3:
            button_unlock.pos = buttonPos
            button_unlock.tick(screen, mouse_pos, mouse_single_tick, glitch, arg = self)

        y_pos = 60

        nonActive = False


        for x in self.upgradeWeapon.availableUpgrades:

            unlocked = x in self.ownedUpgrades[self.upgradeWeapon.name]
            color = [255, 255, 255]
            if not unlocked and nonActive:
                color = [100, 100, 100]
            elif not unlocked:
                nonActive = True
            
            text = terminal2.render(x if unlocked else "?", False, color)
            p = [500 - text.get_size()[0]/2, y_pos]
            screen.blit(text, p)
            if unlocked:
                self.toolTip(p, mouse_pos, text, upgradeMap[x]["Desc"])
                screen.blit(upgradeIcons[x.replace(" ", "").lower()][0], [510 + text.get_size()[0]/2, y_pos+5])
            
            y_pos += 60


        if self.upgradeWeapon.name in PISTOLS:

            if self.startingPistol == self.upgradeWeapon.name:
                button_setstartingpistol.locked = True
                button_setstartingpistol.tooltip="Already your starting pistol."
                
            else:
                button_setstartingpistol.locked = False
                button_setstartingpistol.tooltip="Set this gun as your starting pistol. The starting pistol will have infinite ammo."

            button_setstartingpistol.tick(screen, mouse_pos, mouse_single_tick, glitch, arg = [self, self.upgradeWeapon.name])

        button_back_from_upgrades.tick(screen, mouse_pos, mouse_single_tick, glitch, arg = self)
        

        

    def toolTip(self, pos, mouse_pos, surf, text):
        if surf.get_rect().collidepoint([mouse_pos[0] - pos[0], mouse_pos[1] - pos[1]]):
            t = splitText(text, maxLength=25)
            renderedText = []
            maxPos = [0,0]
            for x in t:
                renderedText.append(terminal1.render(x, False, [255,255,255]))
                maxPos[0] = max(maxPos[0], renderedText[-1].get_size()[0])
                maxPos[1] = max(maxPos[1], renderedText[-1].get_size()[1])


            s = pygame.Surface([maxPos[0], len(t) * maxPos[1]], pygame.SRCALPHA, 32).convert_alpha()
            s.fill((0, 0, 0, 150))
        
            y = 0
            for x in renderedText:
                s.blit(x, [0, y])
                y += maxPos[1]
            
            self.toolTipSurf = s



    def send_data(self, line):
        if not self.multiplayer:
            return
        self.data_collector.data.append(line)

    def start_mp_list(self, list):
        self.start_game_with_mp = list

    def damage_dummy(self, name, damage):
        if name == self.name:
            self.player_actor_ref.force_player_damage(damage)
        else:
            self.multiplayer_actors.force_player_damage(damage)

    def append_player(self, name):
        changed = False
        if name not in self.players:
            self.players.append(name)
            changed = True
        if changed:
            self.send_data(f"self.game_ref.append_player('{self.name}')")


    def collect_data(self):
        #self.chat.tick()
        if not self.net:
            return


        try:
            self.data_collector.tick()
        except Exception as e:
            print(e)

    def update_fps(self):
        if self.fps == "60":
            self.clocktick = 60
        elif self.fps == "144":
            self.clocktick = 144
        elif self.fps == "Unlimited":
            self.clocktick = 240

    def set_map(self, id):
        self.selected_map = id
        self.map_tick = 5
        menu_click2.play()

    def clear_compiled_navmeshes(self):
        for map in self.maps:
            if os.path.isfile(map.compiled_file):
                os.remove(map.compiled_file)



    def preferences(self):
        (
            self.name,
            self.draw_los,
            self.dev,
            self.fs,
            self.ultraviolence,
            self.last_ip,
            self.fps,
            self.vsync,
            self.res,
            self.volume,
            self.music,
            self.MULT_ACKNOWLEDGEMENT,
        ) = utilities.get_preferences.pref()

        #self.name = "Client" + str(random.randint(1,9999))

    def write_prefs(self):
        utilities.get_preferences.write_prefs(
            self.name, self.draw_los, self.dev, self.fs, self.ultraviolence, self.ip, self.fps, self.vsync, self.res, self.volume, self.music, self.MULT_ACKNOWLEDGEMENT
        )

        self.saveProgression()


    def threaded_player_info_gathering(self):
        self.threading = True

        reply = self.net.send(self.name)

        if "STARTGAME" in reply.split("/"):
            print("Client reveived start order")
            self.start_multiplayer_client(None)
            return

        for x in reply.split("/"):
            y = x.split("-")
            if y[0] == "" or y[0] in self.get_names() or len(y) == 1:
                continue

            print("Player connected:", y[0])

            team = Player(ast.literal_eval(y[1]), y[0], y[2])

            self.game_ref.connected_players.append(team)
            if y[0] == self.name_box.text and self.game_ref.player_team == placeholder:
                print("Assigning to player team")
                self.game_ref.player_team = team

        self.threading = False





    def update_screen(self, return_screen = False):

        if return_screen:
            return pygame.display.get_surface(), 1

        if self.vsync:
            vs = 1
        else:
            vs = 0

        if self.fs:
            screen = pygame.display.set_mode(size, pygame.SCALED | pygame.FULLSCREEN, vsync=vs)
            mouse_conversion = 1
        else:
            print("Setting to windowed")
            screen = pygame.display.set_mode(size, vsync=vs)
            mouse_conversion = 1

        print("Screen update done")

        self.screen_copy = screen

        return screen, mouse_conversion




    def lobby_host(self, thread, ip):
        print("SERVER STARTING")
        self.server.server_run()

    def getMaps(self):
        maps_dict = {}

        self.maps = get_maps(self)
        i = 0
        for map_1 in self.maps:

            map_surf = map_1.__dict__["background"]
            x, y = map_surf.get_rect().size
            scale_factor = (200*(size[0]/854)) / x
            img = self.pygame.transform.scale(
                map_surf, (x * scale_factor, y * scale_factor)
            )

            if map_1.name == "Overworld":
                self.overworld = map_1
            else:
                maps_dict[i] = {"map": map_1, "image": img}
                i += 1

        self.maps_dict = maps_dict
        return maps_dict

    def start_sp(self, arg):
        print("SP")
        # get_preferences.write_prefs(name, draw_los, dev, ultraviolence, ip)
        app, name, arg, draw_los, dev, skip_intervals, map = arg

        game.main(
            app,
            self_name=name,
            difficulty=arg,
            draw_los=draw_los,
            dev_tools=dev,
            skip_intervals=skip_intervals,
            map=map,
        )

    def launch_multiplier_server(self, arg):
        print("LAUNCHING!")
        reply = self.net.send(f"PACKET\nself.game_ref.start_mp_list([{self.players}, {self.selected_map}])\nEND#")
        self.start_multiplayer_client(self.players, self.selected_map)



    def start_multiplayer_client(self, players, selected_map):
        self.write_prefs()
        game.main(
            self,
            multiplayer=True,
            net=self.net,
            players=players,
            self_name=self.name,
            map=self.maps_dict[selected_map]["map"],
        )
