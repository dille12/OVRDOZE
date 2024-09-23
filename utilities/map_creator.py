import sys
import pygame
import math
import random
import core.func as func
import core.level as level
import tkinter as tk
from tkinter import filedialog
from hud_elements.button import Button
from _thread import *
from core.values import *
import ast
import core.los as los
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import hud_elements.hud_elements as hud_elements
import utilities.get_preferences as get_preferences
import shutil

class Wall_Rect:
    def __init__(self, rect):
        self.rect = rect
        self.clicks = 0

    def get_rect(self, camera_pos, zoom_scalar):
        return (self.rect.x - camera_pos[0]) * zoom_scalar, (self.rect.y - camera_pos[1]) * zoom_scalar, self.rect.w * zoom_scalar, self.rect.h * zoom_scalar


class Map_Editor:
    def __init__(self):
        self.screen = pygame.display.set_mode((1366,768))
        self.clock = pygame.time.Clock()
        self.clicked = False
        self.button_import = Button([160,30], "IMPORT IMAGE", self.import_file, None, None)
        self.button_new_map = Button([160,120], "NEW MAP", self.new_map, None, None, locked=True)
        self.camera_pos = [0,0]
        self.level_images = []
        self.zoom = 0
        self.terminal = pygame.font.Font(fp("texture/terminal.ttf"), 20)
        self.file = ""
        self.textbox_x = hud_elements.text_box((20, 120), "10")
        self.textbox_y = hud_elements.text_box((20, 80), "10")
        self.textbox_size_x = hud_elements.text_box((20, 160), "2000")
        self.textbox_size_y = hud_elements.text_box((20, 200), "2000")
        self.mode = "None"
        self.walltool = Button([160,200], "RECT TOOL", self.set_mode, "RECTS", None)
        self.navtool = Button([160,260], "NAVPOINTS", self.set_mode, "NAV", None)
        self.viewwalls = Button([160,320], "VIEW WALLS", self.set_mode, "WALLS", None)
        self.walls = []

        self.exportNameT = hud_elements.text_box((20, 630), "MyLevel")

        self.exportButton = Button([160,700], "EXPORT LEVEL", self.exportLevel, None, None)
        self.level = None
        self.print_walls_button = Button([160,400], "PRINT RECTS", self.print_walls, None, None)
        self.rects = []
        self.draw_rect = None
        self.cancel_tick = False
        self.navmesh = {}
        self.nav_points = []
        self.coverage = 0
        self.covered_points = []
        self.tile_textures = {}
        self.level_editor_stage = None
        self.map_size = [0,0]
        self.active_texture = None
        self.load_textures()

    def get_navpoint_coverage(self):
        coverage = 0
        self.covered_points = []
        for x in self.level.nav_mesh_available_spots:
            for y in self.nav_points:
                if los.check_los_jit(np.array(x),np.array(y),self.level.numpy_array_wall_los,self.level.numpy_array_wall_no_los):
                    coverage += 1
                    self.covered_points.append(x)
                    break

        print(coverage)
        print(len(self.level.nav_mesh_available_spots))

        return coverage/len(self.level.nav_mesh_available_spots)

    def load_textures(self):
        mypath = os.path.abspath(os.getcwd()) + "/assets/map_creator_textures/"
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for x in onlyfiles:
            self.tile_textures[x] = pygame.image.load(mypath + x)

    def new_map(self,arg):
        self.level_editor_stage = "NEW"
        self.update_surface()


    def build_nav_mesh(self):
        NAV_MESH = []
        for line in self.nav_points:
            ref_point = {"point": line, "connected": []}
            NAV_MESH.append(ref_point)

        self.navmesh = self.level.generate_navmesh(NAV_MESH, self.level, loading_screen = False)
        self.coverage = self.get_navpoint_coverage()

    def exportLevel(self, arg):

        print(os.getcwd())

        levelFolder = os.getcwd() + "/ovrdoze_data/levels"

        if not os.path.exists(levelFolder):
            os.mkdir(levelFolder)

        pLevel = levelFolder + f"/{self.exportNameT.text}"
        if not os.path.exists(pLevel):
            os.mkdir(pLevel)

        print("Folder located")
        print(pLevel)
        with open(pLevel + f"/navmesh.txt", "w") as f:
            f.write(str(self.nav_points))

        with open(pLevel + f"/walls.txt", "w") as f:
            f.write(str(self.rects))

        source_path = self.file

        tempIm = pygame.image.load(source_path)

        destination_path = pLevel + "/map.png"

        pygame.image.save(tempIm, destination_path)
        
        print("data stored!")
        

    def print_walls(self,arg):
        #self.print_nav(None)
        self.cancel_tick = True
        i = "["
        for r in self.rects:
            x,y,w,h = r
            i += f"[ {int(x)}, {int(y)}, {int(w)}, {int(h)} ],\n"

        i += "]"
        print(i)
        return i

    def print_nav(self, arg):
        print("\n"*2, "NAVMESH:\n\n\n")
        for x in self.nav_points:
            print(f"[{round(x[0]/(1920/854))}, {round(x[1]/(1920/854))}]")
        print("\n"*5)

    def draw_level_walls(self):
        for wall in self.walls:
            p1, p2 = wall.get_points()

            pygame.draw.line(self.screen, [255,0,0], self.zoom_pos(p1), self.zoom_pos(p2), 3)

    def build_level(self, arg):
        #pols = self.print_walls(None)
        pols = self.rects
        if not pols:
            return
        if pols:
            self.level = level.Map(None, "test", None, None, [0,0], 1, self.map_size, POLYGONS = pols, mult2 = 1, mult = 1)
            self.walls = self.level.generate_wall_structure2()

        self.level.compile_navmesh(1)
        self.level.generate_numpy_wall_points()


    def edit_nav_mesh(self):
        self.draw_level_walls()
        if not self.level:
            return
        for x in self.level.nav_mesh_available_spots:
            pygame.draw.circle(self.screen, [0,255,0] if x in self.covered_points else [255,0,0], self.zoom_pos(x), 2)

        mouse_real_pos = (self.mouse_pos[0] / self.zoom_scalar() + self.camera_pos[0]) / 1, (self.mouse_pos[1] / self.zoom_scalar() + self.camera_pos[1]) / 1

        for x in self.navmesh:

            for y in x["connected"]:
                pygame.draw.line(self.screen, [255,0,0], self.zoom_pos(x["point"]), self.zoom_pos(y), 3)

            if func.get_dist_points(self.mouse_pos, self.zoom_pos(x["point"])) < 25:
                pygame.draw.circle(self.screen, [255,255,100], self.zoom_pos(x["point"]), 7)
                if self.mouse_single_tick:
                    self.nav_points.remove(x["point"])
                    self.mouse_single_tick = False
                    self.build_nav_mesh()
                    break

            else:
                pygame.draw.circle(self.screen, [100,255,0], self.zoom_pos(x["point"]), 5)

        if self.mouse_single_tick and not self.blockClick:
            self.nav_points.append(mouse_real_pos)
            self.build_nav_mesh()


        text = self.terminal.render(f"NAVMESH COVERAGE: {self.coverage*100:.1f}%", False, [255,255,255])
        self.screen.blit(text, (0,500))




    def zoom_tick(self, amount):
        zoom_Start = self.zoom
        if amount == 1 and self.zoom < 9:
            self.zoom += 1
        elif amount == -1 and self.zoom > 0:
            self.zoom -= 1

        if self.zoom != zoom_Start:
            screen_size_start = [self.mouse_pos[0] * (5/4) ** zoom_Start, self.mouse_pos[1] * (5/4) ** zoom_Start]
            screen_size = [self.mouse_pos[0] * (5/4) ** self.zoom, self.mouse_pos[1] * (5/4) ** self.zoom]


            # self.camera_pos_target[0] += screen_size_start[0] - screen_size[0]
            # self.camera_pos_target[1] += screen_size_start[1] - screen_size[1]
            self.camera_pos[0] += screen_size_start[0] - screen_size[0]
            self.camera_pos[1] += screen_size_start[1] - screen_size[1]

    def import_file(self, arg):

        #path = os.path.dirname(os.path.realpath(__file__))

        root = tk.Tk()
        root.withdraw()



        file_path = filedialog.askopenfilename()

        #os.chdir(path)



        self.file = file_path
        self.level_images.clear()
        if file_path:
            temp = pygame.image.load(file_path).convert()
            self.process_zoom(temp)

        print("import complete")
        self.level_editor_stage = "EDIT"

    def process_zoom(self, temp):
        self.level_images.clear()
        self.map_size = list(temp.get_size())
        for i in range(10):
            exp = (4/5) ** i
            size = temp.get_size()
            image = pygame.transform.scale(
                temp.copy(), [size[0] * exp, size[1]* exp]
            )
            self.level_images.append(image)
            print([size[0] * exp, size[1]* exp])

    def zoom_scalar(self):
        return (4/5) ** self.zoom

    def zoom_pos(self, pos):
        return [(pos[0] - self.camera_pos[0]) * self.zoom_scalar(), (pos[1] - self.camera_pos[1]) * self.zoom_scalar()]

    def update_surface(self):
        self.level_raw = pygame.Surface(self.map_size)
        self.process_zoom(self.level_raw)
        print("Surface updated")

    def set_mode(self, mode):
        self.cancel_tick = True

        self.build_level(None)

        if self.mode == mode:
            self.mode = "None"
        else:
            self.mode = mode

        if self.mode == "NAV":
            for x in self.level_images:
                x.set_alpha(50)
        else:
            for x in self.level_images:
                x.set_alpha(255)


    def wall_draw(self):

        mouse_real_pos = (self.mouse_pos[0] / self.zoom_scalar() + self.camera_pos[0]) / 1, (self.mouse_pos[1] / self.zoom_scalar() + self.camera_pos[1]) / 1



        #pos = self.zoom_pos(func.minus(list(self.mouse_pos), self.camera_pos, op = "+"))
        # pos[0] -= pos[0]%self.x_divisions
        # pos[1] -= pos[1]%self.x_divisions

        x = mouse_real_pos[0]//(self.map_size[0]/self.x_divisions)
        y = mouse_real_pos[1]//(self.map_size[1]/self.y_divisions)

        xConstraint = 0 <= x <= self.x_divisions
        yConstraint = 0 <= y <= self.y_divisions

        if self.blockClick:
            xConstraint = False

        pos = [x * self.map_size[0]/self.x_divisions * 1, y * self.map_size[1]/self.y_divisions * 1]

        if xConstraint and yConstraint:
            pygame.draw.circle(self.screen, [255,255,0], self.zoom_pos(pos), 10)

        for r in self.rects:
            x,y,w,h = r

            draw_rect = pygame.Rect((x-self.camera_pos[0]) * self.zoom_scalar(), (y-self.camera_pos[1]) * self.zoom_scalar(), w * self.zoom_scalar(), h * self.zoom_scalar())
            if draw_rect.collidepoint(self.mouse_pos) and self.mouse_single_tick and not self.draw_rect and xConstraint and yConstraint:
                self.draw_rect = (x,y)
                self.rects.remove(r)
                menu_click2.play()
                self.mouse_single_tick = False
                break
            pygame.draw.rect(self.screen, [150,0,20], draw_rect, 4)

        if self.mouse_single_tick and not self.draw_rect and xConstraint and yConstraint:
            self.draw_rect = pos
            self.mouse_single_tick = False
            menu_click2.play()


        if self.draw_rect:

            d_p = self.zoom_pos(self.draw_rect)

            pygame.draw.circle(self.screen, [255,0,0], d_p, 10)

            d_p_2 = self.zoom_pos(pos)
            rect = [d_p[0], d_p[1], d_p_2[0] - d_p[0], d_p_2[1] - d_p[1]]

            if rect[2] < 0:
                rect[0] += rect[2]
                rect[2] = -rect[2]

            if rect[3] < 0:
                rect[1] += rect[3]
                rect[3] = -rect[3]


            pygame.draw.rect(self.screen, [255,0,255], rect, 3)

            if self.mouse_single_tick and xConstraint and yConstraint:
                menu_click2.play()
                if round(rect[2]) == 0 or round(rect[3]) == 0:
                    self.draw_rect = None
                else:

                    rect2 = (rect[0] / self.zoom_scalar() + self.camera_pos[0], rect[1] / self.zoom_scalar() + self.camera_pos[1], rect[2] / self.zoom_scalar(), rect[3] / self.zoom_scalar())

                    self.rects.append(rect2)
                    self.draw_rect = None

    def tick_creator(self):
        self.screen.blit(self.level_images[self.zoom], self.zoom_pos((0,0)))
        map_size_delta = self.map_size.copy()
        mouse_real_pos = (self.mouse_pos[0] / self.zoom_scalar() + self.camera_pos[0]) / 1, (self.mouse_pos[1] / self.zoom_scalar() + self.camera_pos[1]) / 1
        text = self.terminal.render(f"Subdivisions:", False, [255,255,255])
        self.screen.blit(text, (20,80))
        self.textbox_x.tick(self.screen, self.mouse_single_tick, self.mouse_pos, self.events)
        self.textbox_size_x.tick(self.screen, self.mouse_single_tick, self.mouse_pos, self.events)
        self.textbox_size_y.tick(self.screen, self.mouse_single_tick, self.mouse_pos, self.events)
        
        if True:
            if self.textbox_size_x.text.isdigit():
                self.map_size[0] = int(self.textbox_size_x.text)
            else:
                self.map_size[0] = 1000
            if self.textbox_size_y.text.isdigit():
                self.map_size[1] = int(self.textbox_size_y.text)
            else:
                self.map_size[1] = 1000

            if map_size_delta != self.map_size:
                self.update_surface()


            if self.textbox_x.text.isdigit():
                self.x_divisions = int(self.textbox_x.text)
            else:
                self.x_divisions = 25

            for x in range(self.x_divisions+1):

                x_pos = x * self.map_size[0]/self.x_divisions * 1
                y_pos = self.map_size[1] * 1

                pygame.draw.line(self.screen, [100,100,100], self.zoom_pos((x_pos,0)), self.zoom_pos((x_pos,y_pos)))

            #self.textbox_y.tick(self.screen, self.mouse_single_tick, self.mouse_pos, )

            if self.textbox_x.text.isdigit():
                self.y_divisions = int(self.textbox_x.text)
            else:
                self.y_divisions = 25

            for y in range(self.y_divisions+1):

                y_pos = y * self.map_size[1]/self.y_divisions * 1

                x_pos = self.map_size[0] * 1

                pygame.draw.line(self.screen, [100,100,100], self.zoom_pos((0,y_pos)), self.zoom_pos((x_pos,y_pos)))
        y_pos = 80
        for x in self.tile_textures:
            text = self.terminal.render(x, False, [255,255,255] if x != self.active_texture else [255,100,100])
            pos = (1366 - 10 - text.get_size()[0], y_pos)
            text_rect = text.get_rect()
            text_rect.x, text_rect.y  = pos
            if text_rect.collidepoint(self.mouse_pos):
                text = self.terminal.render(x, False, [255,0,0])
                if self.mouse_single_tick:
                    menu_click2.play()
                    if self.active_texture == x:
                        self.active_texture = None
                    else:
                        self.active_texture = x

            self.screen.blit(text, pos)
            y_pos += 30

        x = mouse_real_pos[0]//(self.map_size[0]/self.x_divisions)
        y = mouse_real_pos[1]//(self.map_size[1]/self.y_divisions)

        pos = [x * self.map_size[0]/self.x_divisions * 1, y * self.map_size[1]/self.y_divisions * 1]
        zpos = self.zoom_pos(pos)
        if 0 <= x < self.x_divisions and  0 <= y < self.x_divisions:

            tile_size = (self.map_size[0]/self.x_divisions * self.zoom_scalar(), self.map_size[1]/self.y_divisions * self.zoom_scalar())
            if self.active_texture:
                texture = pygame.transform.scale(self.tile_textures[self.active_texture], (self.map_size[0]/self.x_divisions * self.zoom_scalar(), self.map_size[1]/self.y_divisions * self.zoom_scalar())).convert()
                self.screen.blit(texture, zpos)
                if self.mouse_single_tick:
                    texture = pygame.transform.scale(self.tile_textures[self.active_texture], (self.map_size[0]/self.x_divisions, self.map_size[1]/self.y_divisions)).convert()
                    self.level_raw.blit(texture, pos)
                    menu_click2.play()
                    self.process_zoom(self.level_raw)



    def tick_editor(self):
        self.blockClick = False
        for x in [self.walltool, self.viewwalls, self.navtool, self.exportButton, self.print_walls_button]:
            if x.targeted:
                self.blockClick = True
                break



        if self.level_images:
            self.screen.blit(self.level_images[self.zoom], self.zoom_pos((0,0)))

            if self.mode == "RECTS":
                a = self.textbox_x.active
                text = self.terminal.render(f"Subdivisions:", False, [255,255,255])
                self.screen.blit(text, (20,50))
                self.textbox_x.tick(self.screen, self.mouse_single_tick, self.mouse_pos, self.events)
                self.textbox_y.tick(self.screen, self.mouse_single_tick, self.mouse_pos, self.events)
                if a != self.textbox_x.active:
                    self.mouse_single_tick = False

                if self.textbox_x.text.isdigit():
                    self.x_divisions = int(self.textbox_x.text)
                else:
                    self.x_divisions = 25

                for x in range(self.x_divisions):

                    x_pos = x * self.map_size[0]/self.x_divisions * 1
                    y_pos = self.map_size[1] * 1

                    pygame.draw.line(self.screen, [100,100,100], self.zoom_pos((x_pos,0)), self.zoom_pos((x_pos,y_pos)))

                #self.textbox_y.tick(self.screen, self.mouse_single_tick, self.mouse_pos, )

                if self.textbox_y.text.isdigit():
                    self.y_divisions = int(self.textbox_y.text)
                else:
                    self.y_divisions = 25

                for y in range(self.y_divisions):

                    y_pos = y * self.map_size[1]/self.y_divisions * 1

                    x_pos = self.map_size[0] * 1

                    pygame.draw.line(self.screen, [100,100,100], self.zoom_pos((0,y_pos)), self.zoom_pos((x_pos,y_pos)))

            #for y in range(self.y_divisions):

        

        if self.cancel_tick:
            self.cancel_tick = False
            self.mouse_single_tick = False

        if self.mode == "RECTS":
            self.wall_draw()

        elif self.mode == "WALLS":
            self.draw_level_walls()

        elif self.mode == "NAV":
            self.edit_nav_mesh()



        if self.file:
            text = self.terminal.render(self.file, False, [255,255,255])
            self.screen.blit(text, (0,0))

            text = self.terminal.render("MODE:" + self.mode, False, [255,255,255])
            self.screen.blit(text, (0,350))

        self.walltool.tick(self.screen, self.mouse_pos, self.mouse_single_tick, None)
        self.navtool.tick(self.screen, self.mouse_pos, self.mouse_single_tick, None)
        self.viewwalls.tick(self.screen, self.mouse_pos, self.mouse_single_tick, None)
        self.print_walls_button.tick(self.screen, self.mouse_pos, self.mouse_single_tick, None)

        self.exportNameT.tick(self.screen, self.mouse_single_tick, self.mouse_pos, self.events)

        self.exportButton.tick(self.screen, self.mouse_pos, self.mouse_single_tick, None)

    def tick(self):
        self.clock.tick(60)

        self.mouse_single_tick = False
        if pygame.mouse.get_pressed()[0] and self.clicked == False:
            self.mouse_single_tick = True
            self.clicked = True
        elif pygame.mouse.get_pressed()[0] == False:
            self.clicked = False

        x,y = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[1]:
            self.camera_pos[0] -= x * (5/4)**self.zoom
            self.camera_pos[1] -= y * (5/4)**self.zoom
        self.mouse_pos = pygame.mouse.get_pos()

        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.zoom_tick(-1)
                elif event.button == 5:
                    self.zoom_tick(1)
            if event.type == pygame.QUIT:
                sys.exit()

        self.screen.fill((100,0,0))

        if not self.level_editor_stage:
            self.button_new_map.tick(self.screen, self.mouse_pos, self.mouse_single_tick, None)
            self.button_import.tick(self.screen, self.mouse_pos, self.mouse_single_tick, None)
        elif self.level_editor_stage == "EDIT":
            self.tick_editor()
        else:
            self.tick_creator()



        pygame.display.update()

def launch():
    me = Map_Editor()
    while 1:
        me.tick()


if __name__ == '__main__':
    launch()
