import pygame, sys
from random import randint, uniform

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups) # init the parent class
        self.image = pygame.image.load("./graphics/ship.png").convert_alpha()
        self.rect = self.image.get_rect(center = (window_w / 2, window_h / 2))
        self.mask = pygame.mask.from_surface(self.image)

        # timer
        self.can_shoot = True
        self.shoot_time = None

        # sound
        self.laser_sound = pygame.mixer.Sound("./sounds/laser.ogg")
        pygame.mixer.Sound.set_volume(self.laser_sound, 0.5)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 400:
                self.can_shoot = True

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def shoot_laser(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            Laser(self.rect.midtop, laser_group)
            self.laser_sound.play()
    
    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, False, pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()

    def update(self):
        self.input_position()
        self.shoot_laser()
        self.laser_timer()
        self.meteor_collision()

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)
        
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600
        
        self.explosion_sound = pygame.mixer.Sound('./sounds/explosion.wav')
        pygame.mixer.Sound.set_volume(self.explosion_sound, 0.3)

    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
            self.kill()
            self.explosion_sound.play()


    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if self.rect.bottom < 0:
            self.kill()
        self.meteor_collision()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        meteor_surf = pygame.image.load("./graphics/meteor.png").convert_alpha()
        meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5, 1.5)
        self.meteor_scaled = pygame.transform.scale(meteor_surf, meteor_size)
        self.image = self.meteor_scaled
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 600)

        # rotation
        self.rotation = 0
        self.rotation_speed = randint(30, 60)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(self.meteor_scaled, self.rotation, 1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        if self.rect.bottom > window_h:
            self.kill()
        self.rotate()
        
class Score:
    def __init__(self):
        self.font = pygame.font.Font("./graphics/subatomic.ttf", 50)
    
    def display(self):
        score_text = f'Score: {pygame.time.get_ticks() // 1000}'
        text_surf = self.font.render(score_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(topright = (window_w - 40, window_h / 20))
        display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            display_surface, 
            (255,255,255), 
            text_rect.inflate(30, 30), 
            width=5, border_radius=5)

# setup
pygame.init()
window_w, window_h = 1280, 720
display_surface = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()

# bg
bg_surf =  pygame.image.load("./graphics/background.png").convert()

# sprite group
ship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# sprite creation
ship = Ship(ship_group)

# timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 400)

# score
score = Score()

# bg music
bg_music = pygame.mixer.Sound('./sounds/music.wav')
pygame.mixer.Sound.set_volume(bg_music, 0.1)
bg_music.play()

# game loop
while True:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == meteor_timer:
            meteor_y = randint(-150, -50)
            meteor_x = randint(-100, window_w + 100)
            Meteor((meteor_x, meteor_y), groups = meteor_group)


    
    # delta time
    dt = clock.tick() / 1000

    # update
    ship_group.update()
    laser_group.update()
    meteor_group.update()

    # bg
    display_surface.blit(bg_surf, (0,0))

    score.display()

    #graphics
    ship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)

    # draw / update the frame
    pygame.display.update()