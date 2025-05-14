from CollitionState import CollitionState
import pygame

class EntityCollider:
    def __init__(self, entity):
        self.entity = entity

    def check_horizontal_collision(self, target_rect):
        if not self.entity.rect.colliderect(target_rect):
            return

        if self.entity.velocity_x > 0:
            # Moving right, hit wall on right
            self.entity.rect.right = target_rect.left
            self.entity.velocity_x = 0
            self.entity.wall_dir = "right"
            if self.entity.falling and not self.entity.on_ground:
                        if not self.entity.wallslide:
                            self.entity.pending_wallslide = True
                            self.entity.velocity_y = 0
                            self.entity.wallslide_start_x = self.entity.rect.centerx
        elif self.entity.velocity_x < 0:
            # Moving left, hit wall on left
            self.entity.rect.left = target_rect.right
            self.entity.velocity_x = 0
            self.entity.wall_dir = "left"
            if self.entity.falling and not self.entity.on_ground:
                        if not self.entity.wallslide:
                            self.entity.pending_wallslide = True
                            self.entity.velocity_y = 0
                            self.entity.wallslide_start_x = self.entity.rect.centerx

    def check_vertical_collision(self, target_rect):
        if not self.entity.rect.colliderect(target_rect):
            return

        if self.entity.velocity_y > 0:
            # Falling, landed on top of platform
            self.entity.rect.bottom = target_rect.top
            self.entity.velocity_y = 0
            self.entity.on_ground = True
            self.entity.jumping = False
            self.entity.wall_dir = None
            self.entity.wallslide = False
            self.entity.stomp = False

        elif self.entity.velocity_y < 0:
            # Jumping, hit head on ceiling
            self.entity.rect.top = target_rect.bottom
            self.entity.velocity_y = 0
            self.entity.wall_dir = None