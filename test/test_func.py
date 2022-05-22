import unittest
from func import *

class TestFunc(unittest.TestCase):
    def test_load_animation(self):
        pass
    def test_debug_render(self):
        pass
    def test_print_s(self):
        pass
    def test_colorize(self):
        pass
    def test_BezierInterpolation(self):
        pass
    def test_rgb_render(self):
        pass
    def test_get_dist_points(self):
        pass
    def test_render_cool(self):
        pass
    def test_check_for_render(self):
        pass
    def test_get_angle(self):
        p1 = [10.0,25.0]
        p2 = [10.0,10.0]
        points = []
        a1=[
            -59.0362435,
            -48.4903349,
            -173.6584497,
            -148.2879728,
            -120.9532548,
            -93.3987254,
            -66.3546114,
            -44.1048636,
            -178.8824011,
            -155.8496017,
        ]
        a2=[
            -59.0362435,
            -48.4903349,
            -173.6584497,
            -148.2879728,
            -120.9532548,
            -93.3987254,
            -66.3546114,
            -44.1048636,
            -178.8824011,
            -155.8496017,

        ]
        for i in range(10):
            points.append([math.cos(i)*25.0,math.sin(i)*25.0])

        print(points)
        for i,p in enumerate(points):
            r1 = round(get_angle(p1,p),7)
            r2 = round(get_angle(p2,p),7)
            p_simple = [round(p[0],2),round(p[1],2)]
            print("r1 ",p1,"=>",p_simple,"==",round(r1,2));
            print("r2 ",p2,"=>",p_simple,"==",round(r2,2));
            self.assertAlmostEqual(r1,a1[i])
            self.assertEqual(r1,a2[i])

    def test_minus(self):
        pass


    def test_pick_random_from_list(self):
        pass
    def test_pick_random_from_dict(self):
        pass
    def test_minus_list(self):
        pass
    def test_list_play(self):
        pass
    def test_load_image(self):
        pass
    def test_draw_pos(self):
        pass
    def test_get_closest_value(self):
        pass
    def test_get_closest_point(self):
        pass
    def test_player_movement2(self):
        pass
    def test_player_movement(self):
        pass
    def test_render_player(self):
        pass
    def test_rot_center(self):
        pass

    def test_camera_aling(self):
        pass
    def test_keypress_manager(self):
        pass
    def test_weapon_fire(self):
        pass
    def test_get_point_from_list(self):
        pass
    def test_calc_route(self):
        pass
    def test_draw_HUD(self):
        pass

