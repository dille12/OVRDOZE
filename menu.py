class Menu:
    def __init__(
        self,
        buttons=None,
        background=None,
        checkboxes=None,
        clock=None,
        screen=None,
        terminal1=None,
        terminal2=None,
        particle_list=None,
    ):
        self.particle_list = particle_list
        self.buttons_displayed = []
        self.check_boxs_displayed = []
        self.background = background
        self.terminal1 = terminal1
        self.terminal2 = terminal2
        self.cb_a = checkboxes
        self.b_a = buttons
        self.screen = screen
        self.menu_state = "start"
        self.clock = clock

    def update(self, state):
        self._update_menu(state)

        # python has no switch - but would this be a good use for match? (I hear it's faster)
        if self.menu_state == "start":
            self.start_menu(state)
        elif self.menu_state == "settings":
            self.settings_menu(state)
        elif self.menu_state == "mp_start":
            self.multiplayer_start_menu(state)
        elif self.menu_state == "upnp_menu":
            self.upnp_menu(state)
        elif self.menu_state == "single_player_lobby":
            self.single_player_lobby_menu(state)
        elif self.menu_state == "lobby":
            self.lobby_menu(state)
        elif self.menu_state == "mp_menu":
            self.mp_menu(state)

    def _update_basic_state(self, state):
        ##
        ##here goes the basic menu state updates regardless of screen
        ##
        for x in self.particle_list:
            x.tick(self.screen, [0, 0])

        # make mouse_pos current mouse pos
        state["mouse_pos"] = state["get_mouse_pos"]()

    def start_menu(self, state):
        pass

    def settings_menu(self, state):
        pass

    def multiplayer_start_menu(self, state):
        pass

    def upnp_menu(self, state):
        pass

    def single_player_lobby_menu(self, state):
        pass

    def lobby_menu(self, state):
        pass

    def multiplayer_menu(self, state):
        pass

    def get_state(self, state):
        return self.menu_state
