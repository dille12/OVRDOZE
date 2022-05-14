import unittest
# what the what? from run import *
class TestRun(unittest.TestCase):
    
    def test_lobby_host(self):
        pass
    def test_start_mp_game(self):
            pass


    def test_host_game(self) :
            pass

    def test_start_multiplayer_client(self):
        pass

    def test_join_game(self):
        pass

    def test_main_menu(self):
        pass

    def test_quit(self):
        pass

    def test_start_sp(self):
        pass

    def test_start_mp(self):
        pass

    def test_settings(self):
        pass

    def test_kill_server(self):
        pass

    def test_sp_lob(self):
            pass

    def test_Glitch(self):
        return
        glitch=Glitch();
        def test_tick():
            self.assertNoLogs(glitch.tick())

    def test_Button(self):
        return
        button = Button([854,100], "Singleplayer", "single_player_lobby", None)
        def test_tick():
            self.assertNoLogs(button.tick())