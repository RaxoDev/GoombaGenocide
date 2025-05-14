import pygame

class CollitionState:
    def __init__(self, is_colliding = False, is_top = False, is_bot = False, is_right = False, is_left = False):
        # Flag indicating whether a collision has occurred
        self.is_colliding = is_colliding

        # Flags to indicate the side(s) of the collision
        self.is_top = is_top    # True if the entity hit something from below (e.g. bumping head on block)
        self.is_bot = is_bot    # True if the entity landed on top of something
        self.is_right = is_right  # True if collision occurred on the right side
        self.is_left = is_left    # True if collision occurred on the left side

    def __repr__(self):
        # Custom string representation for debugging/logging purposes
        return f"<CollisionState Colliding={self.is_colliding}, Top={self.is_top}, Bottom={self.is_bot}, Left={self.is_left}, Right={self.is_right}>"

