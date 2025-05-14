import pygame

class Camera:
    def __init__(self, width, height, level_height):
        self.camera_rect = pygame.Rect(0, 1700, width, height)  # Camera's viewport
        self.width = width
        self.height = height
        self.level_height = level_height  # Set this to the total level height (world height)
        self.camera_limit = True

    def apply(self, target_rect):
        """Apply the camera's offset to Mario or any target object."""
        return target_rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def apply_platform(self, target_rect):
        """Apply the camera's offset to platforms (background objects)."""
        return target_rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def update(self, target):
        """Update the camera position to follow Mario vertically after he falls below a threshold."""
        mario_center_y = target.rect.centery
        camera_speed = 0.1

        first_lock = 1456      # Camera bottom stays here until Mario goes lower
        second_lock = 640

        # If Mario is below the lock threshold, let the camera follow him
        target_y = mario_center_y - self.height // 2
        self.camera_rect.y += (target_y - self.camera_rect.y) * camera_speed

        
        
        if mario_center_y > second_lock:
            if mario_center_y > first_lock:
                if self.camera_rect.top < first_lock:
                    self.camera_rect.top = first_lock
            elif self.camera_rect.bottom > first_lock:
                self.camera_rect.bottom = first_lock
            elif self.camera_rect.top < second_lock:
                self.camera_rect.top = second_lock

        else:
            if self.camera_rect.bottom > second_lock:
                self.camera_rect.bottom = second_lock
        
        if self.camera_rect.bottom > 2272:
            self.camera_rect.bottom = 2271
        
            

        # Clamp the camera within level bounds
        if self.camera_rect.y < 0:
            self.camera_rect.y = 0
        elif self.camera_rect.y > self.level_height - self.height:
            self.camera_rect.y = self.level_height - self.height