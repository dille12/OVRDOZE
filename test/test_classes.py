import unittest
from classes import *


class TestClasses(unittest.TestCase):
    def test_player_hit_detection(self):
        pass


class TestItem(unittest.TestCase):
    def test_copy(self):
        pass

    def test_get_name(self):
        pass

    def test_sound(self):
        pass

    def test_render(self):
        pass


class TestInventory(unittest.TestCase):
    def test_set_inventory(self):
        pass

    def test_drop_inventory(self):
        pass

    def test_toggle_inv(self):
        pass

    def test_set_search(self):
        pass

    def test_try_deleting_self(self):
        pass

    def test_get_amount_of_type(self):
        pass

    def test_append_to_inv(self):
        pass

    def test_remove_amount(self):
        pass

    def test_get_inv(self):
        pass

    def test_draw_contents(self):
        pass

    def test_draw_inventory(self):
        pass


class TestInteractable(unittest.TestCase):
    def test_tick_prompt(self):
        pass

    def test_prompt_dist(self):
        pass

    def test_get_name(self):
        pass

    def test_tick(self):
        pass

    def test_interact(self):
        pass

    def test_get_pos(self):
        pass

    def test_kill_bp(self):
        pass


class TestButtonPrompt(unittest.TestCase):
    def tick(self):
        pass


class testKillCountRender(unittest.TestCase):
    def tick(self):
        pass


class Particle(unittest.TestCase):
    def test_tick(self):
        pass


class TestPlayer(unittest.TestCase):
    def test_set_pos(self):
        pass

    def test_set_angle(self):
        pass

    def test_set_aim_at(self):
        pass

    def test_get_angle(self):
        pass

    def test_get_pos(self):
        pass

    def test_get_hp(self):
        pass

    def test_get_sanity_change(self):
        pass

    def test_set_sanity(self):
        pass

    def test_set_hp(self):
        pass


class TestWall(unittest.TestCase):
    def test_get_center(self):
        pass

    def test_get_points(self):
        pass
