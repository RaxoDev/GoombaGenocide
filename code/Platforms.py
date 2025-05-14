import pygame

class Platform:
    def  __init__(self, x, y, width, height, platform_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = platform_type
        self.color = self.get_color_by_type(platform_type)

    def get_color_by_type(self, platform_type):
        if platform_type == "ground":
            return (139, 69, 19)
        elif platform_type == "lava":
            return (0, 0, 0)
        elif platform_type == "bounce":
            return (0, 0, 0)
        else:
            return (100, 100, 100)  # default/unknown
    
    def draw(self, screen, camera):
        adjusted_rect = camera.apply_platform(self.rect)
        pygame.draw.rect(screen, self.color, adjusted_rect)