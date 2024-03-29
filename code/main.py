import pygame,sys
from settings import *
from level import Level


class Game:
    def __init__(self):

        #general setup 
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.SCALED)
        pygame.display.set_caption("Fighter")
        self.clock = pygame.time.Clock()
        self.level = Level() 
        self.music = pygame.mixer.Sound("audio/main.mp3")
        self.music.set_volume(0.2)
        self.music.play()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 

            

            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()