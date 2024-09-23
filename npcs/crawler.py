import pygame
from pygame.math import Vector2 as v2
import math
import random
import core.func as func
from _thread import start_new_thread
import core.los as los
import numpy as np
from core.values import *
import core.classes as classes

def smoothRotationFactor(angleVel, gainFactor, diff):
    dir = 1 if diff > 0 else -1
    decelarationTicks = abs(angleVel/gainFactor)
    distanceDecelerating = angleVel*decelarationTicks-0.5*dir*gainFactor*decelarationTicks**2
    acceleratingMod = 1 if distanceDecelerating < diff else -1
    return acceleratingMod
def angleDiff(angle, target_angle):
    return (target_angle - angle + 180) % 360 - 180
def angleBetweenVectors(v1, v2):
    return 90 + v1.angle_to(v2-v1)

class Crawler:
    def __init__(self, app, pos, map, NAV_MESH, walls, target):
        self.app = app
        self.pos = v2(pos)  # Position of the body (torso)
        self.current_route_idx = 0
        self.vel = v2([0,0])
        self.pullingHand = None
        self.map = map
        self.navmesh_ref = NAV_MESH.copy()
        self.target = target
        self.walls = walls
        self.target_pos = self.pos.copy()
        self.spottedPlayer = True
        self.class_type = "CRAWLER"
        self.route = []
        self.route_tick = 0
        self.calculating = False
        self.killed = False
        self.hp = 10000
        self.stuckTick = 0
        self.size = 125
        self.app.bosses += 1
        self.app.bossTick.value = 0

        self.attack_speed = 10
        self.attack_tick = 0
        self.damage = 5

        self.quadrantType = 1
        self.quadrant = 0

        class Hand:
            def __init__(self, pos, parent, offset, name = 1):
                self.pos = pos
                self.pulling = False
                self.opposingH = None
                self.parent = parent
                self.moving = False
                self.endPos = None
                self.name = f"Hand{name}"
                self.offset = offset

                self.vel = v2([0,0])
                self.shoulder = self.parent.pos.copy()

            def getNextPoint(self, p):
                d = p.distance_to(self.parent.next_route_point)

                if d == 0:
                    p += [1,1]


                direction_to_next = (self.parent.next_route_point - p).normalize()
                angle = direction_to_next.angle_to([0, 0])
                offset = self.offset.rotate(90 - angle)

                self.endPos = p + direction_to_next * 80 + offset

                # Initialize variables to find the closest point
                closest_point = None
                closest_distance = float('inf')

                # Iterate through the grab spots to find the closest valid point
                for point in self.parent.map.crawlerGrabSpots:
                    # Calculate the distance to the current point
                    distance = self.endPos.distance_to(point)

                    if self.opposingH.endPos:
                        p = self.opposingH.endPos
                    else:
                        p = self.parent.pos

                    # Check line of sight
                    if (los.check_los_jit(np.array(p), np.array(point), self.parent.map.numpy_array_wall_los) and
                         los.check_los_jit(np.array(self.pos), np.array(point), self.parent.map.numpy_array_wall_los) and
                         los.check_los_jit(np.array(self.opposingH.pos), np.array(point), self.parent.map.numpy_array_wall_los)):
                        # Update closest point if this one is closer
                        if distance < closest_distance:
                            closest_distance = distance
                            closest_point = point

                # If a valid point was found, return it; otherwise return None or handle accordingly
                if closest_point is not None:
                    self.endPos = closest_point
                else:
                    print("No point found")
                    pass


            def tick(self):

                MOVEMENTMOD = self.parent.MOVEMENTMOD

                ACCELERATION = 2 * MOVEMENTMOD
                DRAGACCELERATION = 1 * MOVEMENTMOD
                
                REACHMOD = 1.05
                  
                if self.endPos:

                    if not self.pulling:

                        self.vel[0] += ACCELERATION * smoothRotationFactor(self.vel[0], ACCELERATION, self.endPos[0] - self.pos[0])
                        self.vel[1] += ACCELERATION * smoothRotationFactor(self.vel[1], ACCELERATION, self.endPos[1] - self.pos[1])


                        self.pos += self.vel

                        dToShoulder = self.pos.distance_to(self.shoulder)
                        clamped = False
                        if dToShoulder > (self.parent.upper_arm_length + self.parent.forearm_length) * REACHMOD:
                            dir = (self.pos - self.shoulder).normalize()
                            self.pos = self.shoulder + dir * (self.parent.upper_arm_length + self.parent.forearm_length) * REACHMOD
                            clamped = True

                        self.parent.pullingHand = self

                        d = self.pos.distance_to(self.endPos)
                        if (d < 10 or clamped) and not self.opposingH.pulling and self.parent.needToPull:
                            self.moving = False
                            self.pulling = True
                            direction_to_next = (self.parent.pos - self.parent.next_route_point).normalize()
                            d = self.parent.pos.distance_to(self.pos)
                            self.endPos = self.parent.pos - direction_to_next * d
                            self.opposingH.getNextPoint(self.endPos)
                            self.vel = v2([0,0])
                            func.list_play(crawlerFootSteps)
                            

                    else:

                        self.parent.vel[0] += DRAGACCELERATION * smoothRotationFactor(self.vel[0], ACCELERATION, self.endPos[0] - self.parent.pos[0])
                        self.parent.vel[1] += DRAGACCELERATION * smoothRotationFactor(self.vel[1], ACCELERATION, self.endPos[1] - self.parent.pos[1])

                        #self.parent.pos = self.parent.pos * 0.87 + self.endPos * 0.13
                        d = self.parent.pos.distance_to(self.endPos)
                        d2 = self.pos.distance_to(self.shoulder)
                        if d < 25 or d2 > (self.parent.upper_arm_length + self.parent.forearm_length) * REACHMOD**2:
                            self.pulling = False
                            self.endPos = None
                            self.moving = True




        self.angle = 0
        self.angleVel = 0
        self.anglePointTo = 0
        
                        
        
        # Initial hand positions relative to the body
        self.hand1 = Hand(self.pos + v2(25, 25), self, v2(60, 0), name=1)
        self.hand2 = Hand(self.pos + v2(-25, 25), self, v2(-60, 0), name=2)
        self.hand1.opposingH = self.hand2
        self.hand2.opposingH = self.hand1
        
        
        # Length of arm segments (upper arm and forearm)
        self.upper_arm_length = 60
        self.forearm_length = 60
        
        # Initial state of hands
        self.moving_hand = False  # Alternates between 1 and 2 to indicate which hand moves
        self.pulling = False

        self.handEndPos = []

    def checkRoute(self):
        l = self.pos
        e = False
        for x in self.route:
            if not los.check_los_jit(np.array(l), np.array(x), self.map.numpy_array_wall_los):
                print("ROUTE ERROR", x, l, "not connected")
                e = True
                break
            l = x

        if e:
            d2 = 10000
            for x in self.navmesh_ref:
                d = func.get_dist_points(self.pos, x["point"])
                if d < d2:
                    target = x["point"]
                    d2 = d
            self.route = [target]
            print("Corrected route")
        
        


    def search_route(self):
        self.calculating = True
        print("Started route calc")

        wanderPos = random.choice(self.navmesh_ref)["point"]

        self.route, self.cached_route = func.calc_route(
            self.pos, wanderPos, self.navmesh_ref, [self.map.numpy_array_wall_los, self.map.numpy_array_wall_no_los], cache = self.app
        )

        self.route_tick = 60
        

        self.checkRoute()

        print("Ended")
        self.calculating = False

    def set_hp(self, hp, reduce=False):
        if reduce:
            self.hp -= hp
        else:
            self.hp = hp
    def get_hp(self):
        return self.hp

    def get_route_to_target(self):

        if (
            self.route_tick == 0
            and not self.calculating
        ):
            start_new_thread(self.search_route, ())



    def kill_actor(
        self,
        camera_pos,
        list,
        draw_blood_parts,
        player_actor,
        silent=False,
        zevent=False,
        firedFrom = None,
    ):
        
        self.quadrant.enemies.remove(self)
        list.remove(self)
        self.app.bosses -= 1


        if not silent:

            player_actor.money += self.app.payOut
            money_tick.value = 0

            self.app.multi_kill += 1
            self.app.multi_kill_tick.value = 0
            self.app.kills += 1
            self.app.killedThisTick = True

            if firedFrom:
                self.app.weaponKills[firedFrom] += 1

            func.list_play(death_sounds)
            func.list_play(kill_sounds)
  


            for i in range(15):
                particle_list.append(
                    classes.Particle(
                        func.minus(self.pos, camera_pos),
                        type="blood_particle",
                        magnitude=2,
                        screen=draw_blood_parts,
                    )
                )

                # particle_list.append(
                #     classes.Particle(
                #         func.minus(self.pos, camera_pos),
                #         type="flying_blood",
                #         magnitude=1,
                #         screen=screen,
                #     )
                # )

        self.killed = True



    def ik_solver2(self, hand, shoulderPos, handTypeRight = True):


        shoulderToHandVector = hand.pos - shoulderPos  # Vector from shoulder to hand

        # Use atan2 to get the angle in degrees
        shoulderToHandAngle = math.degrees(math.atan2(shoulderToHandVector.y, shoulderToHandVector.x))

        distance = shoulderPos.distance_to(hand.pos)

        distance = min(distance, self.upper_arm_length + self.forearm_length)
        distance = max(distance, 0)

        C = math.acos((self.upper_arm_length**2 + self.forearm_length**2 - distance**2)/(2*self.upper_arm_length*self.forearm_length))
        C = math.degrees(C)

        if handTypeRight:
            elbowAngle = 180 + 2*shoulderToHandAngle - C
        else:
            elbowAngle = -180 + C + 2*shoulderToHandAngle

        # Convert the elbowAngle to radians for pygame
        elbowAngleRadians = math.radians(elbowAngle)

        # Create a vector from the shoulder, angled at elbowAngle, with length self.upper_arm_length
        upper_arm_vector = pygame.math.Vector2(
            self.upper_arm_length * math.cos(elbowAngleRadians/2),
            self.upper_arm_length * math.sin(elbowAngleRadians/2)
        )

        # Now, you have the vector for the upper arm direction

        return shoulderPos + upper_arm_vector


    def ik_solver(self, hand_pos, body_pos, is_left_hand=True):
        """
        Solves inverse kinematics for the elbow position with clamping to avoid unnatural bending.
        hand_pos: Position of the hand (end effector).
        body_pos: Position of the torso (shoulder joint).
        is_left_hand: Boolean to check if it's the left hand (True) or right hand (False).
        Returns: Position of the elbow.
        """
        direction = hand_pos - body_pos
        dist = direction.length()

        # Clamp the distance to avoid overextension
        dist = min(dist, self.upper_arm_length + self.forearm_length)
        
        # Law of cosines to find the angle for the upper arm
        try:
            cos_angle = (self.upper_arm_length**2 + dist**2 - self.forearm_length**2) / (2 * self.upper_arm_length * dist)
            cos_angle = max(-1, min(1, cos_angle))  # Clamp between -1 and 1 to avoid domain errors
            angle = math.acos(cos_angle)
        except ValueError:
            # Handle any math domain errors
            angle = 0
        
        # Get direction of the elbow from the shoulder to the hand
        direction = direction.normalize()

        # Rotate the vector by the angle to get the elbow's direction
        if is_left_hand:
            elbow_direction = direction.rotate_rad(angle)  # Left hand rotates in the opposite direction
        else:
            elbow_direction = direction.rotate_rad(-angle)  # Right hand rotates normally

        # Calculate the elbow position
        elbow_pos = body_pos + elbow_direction * self.upper_arm_length

        # **Constraint check**: Ensure the elbow bends in the correct direction by calculating dot product
        # between the direction of the forearm and the desired target direction.
        hand_to_elbow = elbow_pos - hand_pos
        body_to_hand = hand_pos - body_pos

        # Dot product to check if the elbow is in the wrong direction
        if hand_to_elbow.dot(body_to_hand) < 0:
            # The elbow is in the wrong direction, mirror the elbow
            if is_left_hand:
                elbow_pos = body_pos + direction.rotate_rad(-angle) * self.upper_arm_length
            else:
                elbow_pos = body_pos + direction.rotate_rad(angle) * self.upper_arm_length

        return elbow_pos


    def playSound(self, sound):
        dir = (self.pos[0] - self.target.pos[0])/500
        inputChannels = [1,1]


        if dir > 0:
            inputChannels[0] = min(1-abs(dir), 1)
        else:
            inputChannels[1] = min(1-abs(dir), 1)

        c = pygame.mixer.find_channel(force = True)
        c.set_volume(inputChannels[0], inputChannels[1])
        c.play(random.choice(sound).sound)
    

    def move_hand(self):
        """
        Move hand towards the target position by a certain grabbing distance.
        """
        pass

    def check_if_alive(self):
        if self.killed or self not in enemy_list:
            return False
        else:
            return True

    
    def getHand(self):
        return self.hand1 if self.moving_hand else self.hand2
    
    def hit_detection(
        self, camera_pos, pos, lastpos, damage, enemy_list, map_render, player_actor, firedFrom
    ):



        points_1 = [
            [self.pos[0], self.pos[1] - self.size * 2.5],
            [self.pos[0], self.pos[1] + self.size * 2.5],
        ]
        points_2 = [
            [self.pos[0] - self.size * 2.5, self.pos[1]],
            [self.pos[0] + self.size * 2.5, self.pos[1]],
        ]

        if los.intersect(pos, lastpos, points_1[0], points_1[1]) or los.intersect(
            pos, lastpos, points_2[0], points_2[1]
        ):


            self.hp -= damage
            if self.hp < 0:
                self.kill_actor(camera_pos, enemy_list, map_render, player_actor, firedFrom=firedFrom)
                

            else:
                func.list_play(hit_sounds)

            return True
        return False
    
    def knockback(self, amount, angle, daemon_bullet=False):

        return


    def move(self, map_boundaries, map_render):
        """
        This method handles the crawling movement where the hands alternate grabbing and pulling the body.
        """
        #if self.current_route_idx >= len(self.route):
        #    self.route.append((random.randint(0,800), random.randint(0,600)))

        self.visible = los.check_los_jit(self.target.np_pos, np.array(self.pos), self.map.numpy_array_wall_los)
        next_route_point = None
        if self.visible:
            next_route_point = v2(self.target.pos)
            self.route = []
            self.target_pos = next_route_point
            if self.app.wave:
                self.MOVEMENTMOD = timedelta.mod(0.3)
            else:
                self.MOVEMENTMOD = timedelta.mod(0.35)

            if not self.spottedPlayer:
                func.list_play(crawlerAttack)
            self.spottedPlayer = True

            if los.get_dist_points(self.pos, self.target_pos) < 50:
                if self.attack_tick <= 0 and self.target.hp > 0:
                    self.attack_tick = self.attack_speed
                    self.target.hp -= self.damage
                    func.list_play(pl_hit)
                    self.app.screen_glitch = 5
                    try:
                        self.target.knockback(
                            self.damage, math.radians(90 + self.target_angle)
                        )
                    except:
                        pass
                    for i in range(3):
                        particle_list.append(
                            classes.Particle(
                                func.minus(self.target.pos, camera_pos),
                                type="blood_particle",
                                magnitude=0.5,
                                screen=map_render,
                            )
                        )


        else:
            self.spottedPlayer = False
            self.MOVEMENTMOD = timedelta.mod(0.15)
            if (self.pos - self.target_pos).length() < 30:
                if self.route != []:

                    self.target_pos = self.route[0]
                    self.route.remove(self.route[0])


                else:
                    self.get_route_to_target()
            else:
                next_route_point = self.target_pos


        if not next_route_point:
            next_route_point = self.pos.copy()

        
        
        self.needToPull = True
        # Update route point if reached
        if (self.pos - next_route_point).length() < 30:
            self.needToPull = False
        
        self.next_route_point = self.target_pos
        
        

        if not self.handEndPos:

            #self.moving_hand = not self.moving_hand

            #p = self.getHandPos()

            #direction_to_next = (next_route_point - p).normalize()

            #self.handEndPos = direction_to_next * 45
            pass

            
        #self.move_hand()

        if not self.hand1.endPos and not self.hand2.endPos:
            self.hand1.getNextPoint(self.pos)
            print("Resetted Hand Pos")






        if self.pullingHand:
            midpoint = self.next_route_point
            #midpoint = self.pullingHand.endPos
            #midpoint = (self.hand1.pos + self.hand2.pos) / 2
        else:
            midpoint = self.pos + [10,0]

        self.anglePointTo = v2([0,0]).angle_to(self.pos - midpoint) + 180  # Add 180 to face the opposite direction (toward the hands)
        ACC = 0.25 * self.MOVEMENTMOD
        self.angleVel += ACC * smoothRotationFactor(self.angleVel, ACC, diff = angleDiff(self.angle, self.anglePointTo))
        self.angle += self.angleVel

        #self.pos = (self.hand1 + self.hand2) / 2
        self.hand1.tick()
        self.hand2.tick()
        self.pos += self.vel
        self.vel *= 0.9
        checkColl = False

        if checkColl:

            collision_types, coll_pos = self.map.checkcollision(
                    self.pos,
                    self.vel,
                    30,
                    map_boundaries,
                )
            self.pos = v2(coll_pos)
            stuck = False
            for x in collision_types:
                if collision_types[x]:
                    stuck = True
                    self.stuckTick += 1
                    break
            if not stuck and self.stuckTick > 0:
                self.stuckTick -= 0.5
            
            if stuck and self.stuckTick > 10:
                self.hand1.endPos = None
                self.hand2.endPos = None
                self.stuckTick = 0


    def get_pos(self):
        return self.pos

    def render(self, screen, camera_pos):
                
        #pygame.draw.circle(self.app.screen, (255, 255, 0), target, 2)  # Draw body

        # ARM
        target = self.pos + self.shoulder1 #POS
        armAngle = v2([0,0]).angle_to(self.pos + self.shoulder1 - self.elbow1)
        anchorPixel = v2([30, 0])

        im = pygame.transform.rotate(crawlerArm, 300 - armAngle)

        p = target - v2(im.get_size())/2 - anchorPixel.rotate(armAngle)  - camera_pos
        if not self.LineRender:
            screen.blit(im, p)

        # HAND
        target = self.elbow1 #POS
        handAngle = v2([0,0]).angle_to(self.elbow1 - self.hand1.pos)
        anchorPixel = v2([30, 0])

        im = pygame.transform.rotate(crawlerHand, 300 - handAngle)

        p = target - v2(im.get_size())/2 - anchorPixel.rotate(handAngle)  - camera_pos

        if not self.LineRender:
            screen.blit(im, p)


        # ARM
        target = self.pos + self.shoulder2 #POS
        armAngle = v2([0,0]).angle_to(self.pos + self.shoulder2 - self.elbow2)
        anchorPixel = v2([30, 0])

        im = pygame.transform.flip(crawlerArm, True, False)

        im = pygame.transform.rotate(im, 234 - armAngle)

        p = target - v2(im.get_size())/2 - anchorPixel.rotate(armAngle) - camera_pos

        if not self.LineRender:
            screen.blit(im, p)

        # HAND
        target = self.elbow2 #POS
        handAngle = v2([0,0]).angle_to(self.elbow2 - self.hand2.pos)
        anchorPixel = v2([30, 0])

        im = pygame.transform.flip(crawlerHand, True, False)
        im = pygame.transform.rotate(im, 234 - handAngle)

        p = target - v2(im.get_size())/2 - anchorPixel.rotate(handAngle) - camera_pos

        if not self.LineRender:
            screen.blit(im, p)


        im = pygame.transform.rotate(crawlerBody, 270-self.angle)
        screen.blit(im, self.pos - v2(im.get_size())/2 - camera_pos)


        

    def tick(self, screen,
                    map_boundaries,
                    player_actor,
                    camera_pos,
                    map,
                    walls,
                    NAV_MESH,
                    map_render,
                    phase=None,
                    wall_points=None):
        # Call the move function to update the position and hands

        if not self.quadrant:
            map.setToQuadrant(self, self.pos)

        if not self.quadrant.checkIfIn(self.pos):
            self.quadrant.enemies.remove(self)
            map.setToQuadrant(self, self.pos)

        for melee_hit in melee_list:
            angle_to_melee = 360 - math.degrees(
                math.atan2(
                    self.pos[1] - melee_hit["pos"][1], self.pos[0] - melee_hit["pos"][0]
                )
            )
            if (
                los.get_dist_points(melee_hit["pos"], self.pos)
                < melee_hit["strike_range"]
                and los.get_angle_diff(abs(angle_to_melee), melee_hit["angle"])
                < melee_hit["arc"] / 2
            ):
                melee_hit_sound.stop()
                melee_hit_sound.play()
                self.hp -= melee_hit["damage"]

        if self.attack_tick > 0:
            self.attack_tick -= timedelta.mod(1)

        self.move(map_boundaries, map_render)

        if self.route_tick != 0:
            self.route_tick -= 1
        

        self.shoulder1 = v2([0,1]).rotate(self.angle) * 30
        self.shoulder2 = v2([0,1]).rotate(self.angle) * (-30)

        self.hand1.shoulder = self.pos + self.shoulder1
        self.hand2.shoulder = self.pos + self.shoulder2
        
        # Calculate the elbows using inverse kinematics
        #self.elbow1 = self.ik_solver(self.hand1.pos, self.pos+self.shoulder1, is_left_hand=False)
        #self.elbow2 = self.ik_solver(self.hand2.pos, self.pos+self.shoulder2, is_left_hand=True)

        self.elbow1 = self.ik_solver2(self.hand1, self.pos+self.shoulder1)
        self.elbow2 = self.ik_solver2(self.hand2, self.pos+self.shoulder2, handTypeRight=False)

        self.hand1.elbow = self.elbow1 
        self.hand2.elbow = self.elbow2 

        self.LineRender = False

        self.render(screen, camera_pos)
        
        # Draw the crawler (for debugging and visualization)
        #pygame.draw.circle(self.app.screen, (255, 0, 0), self.pos, 10)  # Draw body

        angler = v2([1,0]).rotate(self.angle) * 30

        if phase == 6:
            last_x = self.pos
            for x in [self.target_pos] + self.route:
                pygame.draw.line(screen, (255, 255, 255), v2(x) - camera_pos, v2(last_x) - camera_pos, 2)
                last_x = x

        #pygame.draw.line(self.app.screen, (255, 0, 0), self.pos, self.pos+angler, 1)  # Upper arm 1
        if self.LineRender:
            pygame.draw.circle(self.app.screen, (255, 255, 0), self.hand1.pos, 5)  # Draw hand 1
            pygame.draw.circle(self.app.screen, (0, 255, 0), self.hand2.pos, 5)  # Draw hand 2
            pygame.draw.circle(self.app.screen, (0, 0, 255), self.elbow1, 5)  # Draw elbow 1
            pygame.draw.circle(self.app.screen, (0, 0, 255), self.elbow2, 5)  # Draw elbow 2


            
            
            # Draw arms (lines between shoulder, elbow, and hand)
            pygame.draw.line(self.app.screen, (255, 255, 255), self.pos + self.shoulder1, self.elbow1, 2)  # Upper arm 1
            pygame.draw.line(self.app.screen, (255, 255, 255), self.elbow1, self.hand1.pos, 2)  # Forearm 1
            pygame.draw.line(self.app.screen, (255, 255, 255), self.pos + self.shoulder2, self.elbow2, 2)  # Upper arm 2
            pygame.draw.line(self.app.screen, (255, 255, 255), self.elbow2, self.hand2.pos, 2)  # Forearm 2



if __name__ == "__main__":

    # Create two vectors
    vector1 = pygame.math.Vector2(1, 0)  # Example: a unit vector along the x-axis
    vector2 = pygame.math.Vector2(0, 1)  # Example: a unit vector along the y-axis

    # Calculate the angle from vector1 to vector2
    angle = angleBetweenVectors(vector1, vector2)


    pygame.init()
    
    # Set up the display
    screen_width, screen_height = 1600, 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Crawler Test")

    # Create an app-like object to pass the screen into the crawler (you can modify this as needed)
    class App:
        def __init__(self, screen):
            self.screen = screen
            

    # Define the app and route
    app = App(screen)
    route = [(100, 300), (300, 300), (500, 500), (700, 300)]  # A simple route for the crawler

    # Initialize the Crawler
    crawler = Crawler(app, (100, 300), route)


    # Main game loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a background color (black)
        screen.fill((0, 0, 0))

        # Update and draw the crawler
        crawler.tick()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
