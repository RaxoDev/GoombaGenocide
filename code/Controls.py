import pygame

class Controls:
    def __init__(self, mario):
        self.mario = mario  # Reference to the Mario instance
        self.jump_initiated = False  # Flag to track if jump was triggered (to avoid holding the key)
        self.stomp_initiated = False  # Flag to manage stomp input similarly

    def handle_inputs(self, keys):
        """Handles Mario's movement inputs"""

        # === Horizontal movement logic ===
        target_speed = 0  # Target speed to transition toward
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            # Move right, using sprint speed if sprinting
            target_speed = self.mario.sprint_speed if self.mario.sprinting else self.mario.speed
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            # Move left, using sprint speed if sprinting
            target_speed = -self.mario.sprint_speed if self.mario.sprinting else -self.mario.speed

        if keys[pygame.K_RIGHT]:
            self.is_moving_right = True
            self.is_moving_left = False
        elif keys[pygame.K_LEFT]:
            self.is_moving_right = False
            self.is_moving_left = True
        else:
            self.is_moving_right = False
            self.is_moving_left = False

        # === Smooth velocity blending ===
        blend_rate = 0.1  # Controls acceleration smoothness
        self.mario.velocity_x += (target_speed - self.mario.velocity_x) * blend_rate

        # === Deceleration if no keys pressed ===
        if target_speed == 0 and abs(self.mario.velocity_x) > 0.1:
            self.mario.velocity_x *= 0.9  # Slowly reduce speed
        elif abs(self.mario.velocity_x) < 0.1:
            self.mario.velocity_x = 0  # Stop entirely if very slow

        # === Crouching ===
        if keys[pygame.K_DOWN]:
            self.mario.startCrouch()
        else:
            self.mario.stopCrouch()

        # === Sprinting only works when not crouching ===
        self.mario.sprinting = keys[pygame.K_LSHIFT] and not self.mario.crouch

        # === Wallslide behavior control ===
        if self.mario.wallslide:
            # Cancel wallslide if pressing away from wall direction
            if (keys[pygame.K_RIGHT]) and (self.mario.wall_dir == "left"):
                self.mario.wallslide = False
            if (keys[pygame.K_LEFT]) and (self.mario.wall_dir == "right"):
                self.mario.wallslide = False
            if not (keys[pygame.K_LEFT]) and (self.mario.wall_dir == "left"):
                self.mario.wallslide = False
            if not (keys[pygame.K_RIGHT]) and (self.mario.wall_dir == "right"):
                self.mario.wallslide = False

        # === Wallslide state input checks ===
        self.mario.pressLeft = (keys[pygame.K_LEFT]) and (self.mario.wall_dir == "left")
        self.mario.pressRight = (keys[pygame.K_RIGHT]) and (self.mario.wall_dir == "right")

        # === Jumping ===
        if keys[pygame.K_SPACE]:
            if self.mario.on_ground and not self.jump_initiated:
                # Jump from ground
                self.mario.jump()
                self.jump_initiated = True

            elif self.mario.wallslide and not self.jump_initiated:
                # Wall jump
                self.mario.wall_jump()
                self.jump_initiated = True

            elif self.mario.jumping and self.mario.jump_button_held:
                self.mario.jump_update()
        else:
            if self.jump_initiated:
                self.mario.stop_jump()
            self.jump_initiated = False


        # === Stomping mechanic ===
        if keys[pygame.K_DOWN]: 
            if not self.stomp_initiated:
                self.mario.stomping()  # Force fast downward velocity
                self.stomp_initiated = True
        else:
            self.stomp_initiated = False

    def update(self):
        pass
