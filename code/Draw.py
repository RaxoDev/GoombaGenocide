class Draw:
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera

    def draw_mario(self, mario):
        adjusted_rect = self.camera.apply(mario.rect)
        mario.draw(self.screen, adjusted_rect)

    def draw_platforms(self, platforms):
        for platform in platforms:
            platform.draw(self.screen, self.camera)
            
    #def draw_goombas(self, goombas)

    
    def draw_All(self,mario, platforms ): # när vi lägger in mer saker att "rita" lägger i till dem här i denna funktion
        self.draw_mario(mario)
        self.draw_platforms(platforms)
        #så tex när goombas kommer så lägger vi till här
            # self.draw_goombas(goombas)