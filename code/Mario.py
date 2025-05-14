import pygame
from EntityCollider import EntityCollider
import time

class Mario:
    def __init__(self, x, y):
        # Mario's hitbox/position rectangle
        self.rect = pygame.Rect(x, y, 16, 32)
        # self.color = (255, 0, 0)
        spritesheet = pygame.image.load("../assets/mariosprite.png").convert_alpha()  # Mario image
       # Extract the correct region (259, 1, 16, 32)
        # Extract the different sprites for movement
        self.sprite_right_1 = pygame.Surface((16, 32), pygame.SRCALPHA)
        self.sprite_right_2 = pygame.Surface((16, 32), pygame.SRCALPHA)
        self.sprite_left_1 = pygame.Surface((16, 32), pygame.SRCALPHA)
        self.sprite_left_2 = pygame.Surface((16, 32), pygame.SRCALPHA)
        
        # Extract images from spritesheet (right-facing: 9, 10) (left-facing: 1, 2)
        sprite_rect_right_1 = pygame.Rect(328, 0, 16, 32)  # Right-facing first frame
        sprite_rect_right_2 = pygame.Rect(368, 0, 16, 32)  # Right-facing second frame
        sprite_rect_left_1 = pygame.Rect(8, 0, 16, 32)     # Left-facing first frame
        sprite_rect_left_2 = pygame.Rect(48, 0, 16, 32)    # Left-facing second frame

        # Blit the individual sprites from the spritesheet
        self.sprite_right_1.blit(spritesheet, (0, 0), sprite_rect_right_1)
        self.sprite_right_2.blit(spritesheet, (0, 0), sprite_rect_right_2)
        self.sprite_left_1.blit(spritesheet, (0, 0), sprite_rect_left_1)
        self.sprite_left_2.blit(spritesheet, (0, 0), sprite_rect_left_2)

         # Now define the idle sprites
        self.sprite_idle_right = pygame.Surface((16, 32), pygame.SRCALPHA)
        self.sprite_idle_left = pygame.Surface((16, 32), pygame.SRCALPHA)

        sprite_rect_idle_right = pygame.Rect(206, 0, 16, 32)  # Right-facing idle frame (x=206)
        sprite_rect_idle_left = pygame.Rect(166, 0, 16, 32)   # Left-facing idle frame (x=166)

        # Blit the idle sprites
        self.sprite_idle_right.blit(spritesheet, (0, 0), sprite_rect_idle_right)
        self.sprite_idle_left.blit(spritesheet, (0, 0), sprite_rect_idle_left)


        # Initial setup
        self.image = self.sprite_idle_right  # Default image (right-facing)
        self.facing_left = False  # Initially facing right

        # Timer to control sprite switching
        self.last_switch_time = time.time()
        self.sprite_interval = 0.35  # Interval to switch sprites (0.5 seconds)

        
        # Initially Mario faces right
        self.facing_left = True

        self.left_limit = 0
        self.right_limit= 368

        # === Movement Attributes ===
        self.velocity_x = 0                 # Horizontal velocity
        self.velocity_y = 0                 # Vertical velocity
        self.speed = 2                      # Walking speed
        self.sprint_speed = 3.5               # Sprinting speed
        self.friction = 0.4                 # Not used in this code but might be for deceleration
        self.jump_force = -8               # Standard jump force
        self.max_jump_force = -22           # Max charged jump force
        self.jump_charge_rate = -3          # Rate at which jump is "charged" when holding the button
        self.max_fall_speed = 16            # Terminal velocity when stomping
        self.gravity = 1                    # Downward force applied each frame
        self.stomp_speed = 16               # Fast downward speed when stomping
        self.jump_force_wall = -8          # Jump force for wall jump
        self.wall_jump_push = 0             # Horizontal force applied when wall jumping
        self.wall_jump_locked = False       # Prevents direction change immediately after wall jump
        self.wall_jump_lock_dir = None      # Direction lock after wall jump
        self.wall_jump_lock_timer = 0       # Timer for how long lock lasts
        self.wall_jump_lock_duration = 15   # Duration of the wall jump lock in frames
        self.wall_dir = None                # Wall side ("left" or "right") for wall slide / wall jump
        self.is_wall_jump = False
        
        # === State Flags ===
        self.small = False                  # Is Mario small (affects crouching)
        self.running = False                # Currently running
        self.sprinting = False              # Currently sprinting
        self.jumping = False                # Currently jumping
        self.falling = False                # Currently falling
        self.crouch = False                 # Currently crouching
        self.stomp = False                  # Currently stomping
        self.on_ground = False              # Is Mario touching the ground
        self.jump_button_held = False       # Is the jump button held down
        self.jump_time = 0                  # Time jump button has been held
        self.wallslide_grace_duration = 10
        self.wallslide_grace_timer = 0
        self.pending_wallslide = False

        # === Wall Contact Flags ===
        self.pressRight = False             # Right input while falling (used in wall logic)
        self.pressLeft = False              # Left input while falling (used in wall logic)
        self.wallslide = False              # Is currently wall sliding
        self.wallslide_start_x = 0          # Is the x position  of mario when the wallslide started

        # === Size Constants ===
        self.big_height = 32                # Height when big
        self.small_height = 16              # Height when crouching

    def apply_gravity(self, platforms):
        self.on_ground = False  # Reset on_ground status before checking for collisions
        
        # Apply gravity to vertical velocity
        self.velocity_y += self.gravity  # Add gravity to vertical velocity
        if not self.wallslide:
            if self.stomp:
                if self.velocity_y > self.max_fall_speed:
                    self.velocity_y = self.max_fall_speed  # Limit falling speed
            else:
                if self.velocity_y > 13:
                    self.velocity_y = 13
        else:
            if self.velocity_y > 3:
                self.velocity_y = 3
                if abs(self.wallslide_start_x - self.rect.centerx) > 1:
                    self.wallslide = False

        # Check for collision with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                # If Mario is falling and collides with a platform
                self.on_ground = True
                self.velocity_y = 0  # Stop vertical movement when on the ground
                self.rect.bottom = platform.rect.top  # Position Mario on top of the platform
                break  # Exit the loop once a collision is detected
        else:
            # If no collision was detected, Mario is still falling
            self.falling = self.velocity_y > 0

    def update(self, platforms, collider, controls):
        # Debugging print to track state each frame
        if controls.is_moving_right:
            self.facing_left = False
            self.animate_right()  # Animate right if moving
        elif controls.is_moving_left:
            self.facing_left = True
            self.animate_left()  # Animate left if moving
        else:
            self.standing_still()  # Ensure we stand still if no input

        # Flip the sprite based on facing direction
        if self.facing_left:
            self.image = self.sprite_left_1 if self.image == self.sprite_left_1 else self.sprite_left_2
        else:
            self.image = self.sprite_right_1 if self.image == self.sprite_right_1 else self.sprite_right_2
                
        self.apply_gravity(platforms) 
        # Handle direction lock after wall jump
        if self.wall_jump_locked:
            self.wall_jump_lock_timer -= 1
            if self.wall_jump_lock_timer <= 0:
                self.wall_jump_locked = False  # Unlock after timer expires

        # === Grace logic for wallslide ===
        if self.pending_wallslide:
            pressing_toward_wall = (
                (self.wall_dir == "left" and self.pressLeft) or
                (self.wall_dir == "right" and self.pressRight)
            )

            if self.wallslide_grace_timer == 0:
                self.wallslide_grace_timer = self.wallslide_grace_duration

            if not pressing_toward_wall:
                # If player moved away from the wall, cancel the grace period and stop sliding
                self.pending_wallslide = False
                self.wallslide = False
                self.wallslide_grace_timer = 0  # Reset grace timer
            else:
                # If player is still pressing toward the wall, decrease the grace timer
                self.wallslide_grace_timer -= 1
                self.velocity_y = 0  # Mario is "stuck" during grace period
                if self.wallslide_grace_timer <= 0:
                    # After grace period, start wall sliding if still pressing toward the wall
                    self.wallslide = True
                    self.pending_wallslide = False

        # Apply horizontal velocity push after wall jump
        if self.wall_jump_locked:
            self.velocity_x = self.wall_jump_push

        # Apply velocity to Mario's position
        # Separate horizontal movement
        self.rect.y += self.velocity_y
        for platform in platforms:
            collider.check_vertical_collision(platform.rect)
        
        mario_x_pos = self.rect.x + self.velocity_x
        if not (mario_x_pos < self.left_limit or mario_x_pos > self.right_limit):
            self.rect.x += self.velocity_x
            for platform in platforms:
                collider.check_horizontal_collision(platform.rect)




    def animate_left(self):
        if not self.facing_left:
            return  # If Mario is not facing left, don't animate left

        # Switch sprite every 0.5 seconds while moving left
        if time.time() - self.last_switch_time > self.sprite_interval:
            self.last_switch_time = time.time()  # Reset the timer
            if self.image == self.sprite_left_1:
                self.image = self.sprite_left_2
            else:
                self.image = self.sprite_left_1

    def animate_right(self):
        if self.facing_left:
            return  # If Mario is facing left, don't animate right

        # Switch sprite every 0.5 seconds while moving right
        if time.time() - self.last_switch_time > self.sprite_interval:
            self.last_switch_time = time.time()  # Reset the timer
            if self.image == self.sprite_right_1:
                self.image = self.sprite_right_2
            else:
                self.image = self.sprite_right_1

    def standing_still(self):
         # When standing still, use the last direction and switch to the idle animation
        if self.facing_left:
            self.image = self.sprite_idle_left  # Idle sprite for left-facing
        else:
            self.image = self.sprite_idle_right  # Idle sprite for right-facing

    def wall_jump(self):
        if self.wallslide and not self.on_ground:
        # Initiate wall jump only if we're not already jumping
            self.is_wall_jump = True
            self.jumping = True
            self.on_ground = False
            self.jump_button_held = True

            self.jump_time = 0
            self.velocity_y = self.jump_force_wall  # Vertical part of wall jump

            # Apply a smooth horizontal push depending on wall side
            if self.wall_dir == "left":
                self.wall_jump_push = 6  # More gradual push to the right
                self.wall_jump_locked = True
                self.wall_jump_lock_dir = "left"
            elif self.wall_dir == "right":
                self.wall_jump_push = -6  # More gradual push to the left
                self.wall_jump_locked = True
                self.wall_jump_lock_dir = "right"

            # Set timer for direction lock after wall jump
            self.wall_jump_lock_timer = self.wall_jump_lock_duration
            self.wallslide = False  # Stop wall sliding after jump

    def jump(self):
        if self.on_ground:
            # Start with base jump force
            self.velocity_y = self.jump_force
            self.on_ground = False
            self.is_wall_jump = False
            self.jumping = True
            self.jump_button_held = True
            self.jump_time = 0  # Reset jump hold timer

    def jump_update(self):
        # Only charge jump if button is held and we haven't reached max force
        if self.jump_button_held and self.jump_time % 3 and self.jump_time < 10 and not self.is_wall_jump:  # Only while moving upward
            self.velocity_y += self.jump_charge_rate * 0.5  # Slower charge rate


            
            # Clamp to max jump force
            if self.velocity_y < self.max_jump_force:
                self.velocity_y = self.max_jump_force
        self.jump_time += 1

    def stop_jump(self):
        # When jump button is released
        self.jump_button_held = False

    def startCrouch(self):
        pass

    def stopCrouch(self):
        pass

    def stomping(self):
        pass

    def draw(self, screen, adjusted_rect):
        screen.blit(self.image, adjusted_rect)
