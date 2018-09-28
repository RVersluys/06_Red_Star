import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, text, fontsize, color, persistance, pos, size = (250,100)):
        pygame.sprite.Sprite.__init__(self)

        self.persistance = persistance
        self.font = pygame.font.Font(pygame.font.match_font("Xolonium"), fontsize)
        self.textSurf = self.font.render(text, 1, color)

        self.image = pygame.Surface(size)
        self.image.set_colorkey((0,0,0))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [size[0]/2 - W/2, size[1]/2 - H/2])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.ticks = 0

    def update(self):
        self.ticks += 1
        if self.persistance[0] < self.ticks:
            if self.ticks >= self.persistance[0] + self.persistance[1]:
                self.kill
            alpha = int((self.persistance[1] - (self.ticks - self.persistance[0])) / self.persistance[1] * 255)
            self.image.set_alpha(alpha)
