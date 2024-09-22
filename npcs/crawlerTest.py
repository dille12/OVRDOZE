import pygame
import math

def ik_solver2(self, hand, shoulderPos, handTypeRight=True):
    # Vector from shoulder to hand
    shoulderToHandVector = hand - shoulderPos
    shoulderToHandAngle = math.degrees(math.atan2(shoulderToHandVector.y, shoulderToHandVector.x))  # Angle between shoulder and hand
    distance = shoulderPos.distance_to(hand)

    # Clamp distance to ensure it's within valid range
    distance = min(distance, self.upper_arm_length + self.forearm_length)
    distance = max(distance, 0)

    # Calculate elbow angle (C) using the law of cosines
    C = math.acos((self.upper_arm_length**2 + self.forearm_length**2 - distance**2) / 
                  (2 * self.upper_arm_length * self.forearm_length))
    C_degrees = math.degrees(C)

    # Calculate angle for upper arm
    # The elbow angle should bend in the opposite direction, so subtract C_degrees
    elbowAngle = shoulderToHandAngle - C_degrees

    # Convert elbow angle to radians
    elbowAngleRadians = math.radians(elbowAngle)

    # Create a vector from the shoulder towards the elbow at the calculated angle
    upper_arm_vector = pygame.math.Vector2(
        self.upper_arm_length * math.cos(elbowAngleRadians),
        self.upper_arm_length * math.sin(elbowAngleRadians)
    )

    # Find the position of the elbow by adding the upper arm vector to the shoulder position
    elbowPos = shoulderPos + upper_arm_vector

    return elbowPos

# Example usage
shoulder = pygame.math.Vector2(100, 100)
hand = pygame.math.Vector2(150, 50)

# Dummy function to calculate the angle between two vectors
def angleBetweenVectors(vec1, vec2):
    return vec1.angle_to(vec2)

# Call the solver function
upper_arm_length = 60
forearm_length = 55

class Arm:
    def __init__(self, upper_arm_length, forearm_length):
        self.upper_arm_length = upper_arm_length
        self.forearm_length = forearm_length

    def ik_solver2(self, hand, shoulderPos, handTypeRight=True):
        return ik_solver2(self, hand, shoulderPos, handTypeRight)

arm = Arm(upper_arm_length, forearm_length)
elbowPos = arm.ik_solver2(hand, shoulder)

print(elbowPos)
