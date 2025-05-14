import pygame
import pytmx
from Platforms import Platform
from Mario import Mario

class Level:
    def __init__(self, map_file):
        self.tmx_data = pytmx.load_pygame(map_file)
        self.platforms = self.load_platforms()
        
    def get_spawn_point(self):
        # Calculates spawn point using map dimensions
        x = 7 * self.tmx_data.tilewidth
        y = (self.tmx_data.height - 8) * self.tmx_data.tileheight
        return x, y

    def load_platforms(self):
        platforms = []
        
        # Look for the "Collision" layer (assuming it contains collision tiles)
        collision_layer = self.tmx_data.get_layer_by_name("Collisions")
        if collision_layer:
            for x, y, gid in collision_layer:
                tile = self.tmx_data.get_tile_image_by_gid(gid)
                if tile:  # Check if tile exists
                    # Assuming each tile is a platform
                    platform = Platform(x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight, 
                                        self.tmx_data.tilewidth, self.tmx_data.tileheight, "platform")
                    platforms.append(platform)

        return platforms

    def draw_map(self, screen, camera):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, camera.apply(pygame.Rect(
                                x * self.tmx_data.tilewidth,
                                y * self.tmx_data.tileheight,
                                self.tmx_data.tilewidth,
                                self.tmx_data.tileheight
                            )))
                    

