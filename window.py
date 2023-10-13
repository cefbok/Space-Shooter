import pygame, sys
from random import randint

def laser_update(laser_list, speed = 400):
    for rect in laser_list:
        rect.y -= speed * dt
        if rect.bottom < 0:
            laser_list.remove(rect)

def score():
    score_text = f'Score: {pygame.time.get_ticks() // 1000}'
    text_surface = font.render(score_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center = (window_w / 2, window_h / 4))
    display_surface.blit(text_surface, (text_rect))
    pygame.draw.rect(display_surface, 'white', text_rect.inflate(100, 20), width= 5, border_radius=2)

def laser_timer(can_shoot, duration = 500):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True
    return can_shoot

def meteor_update(meteor_list, speed = 300):
    for rect in meteor_list:
        rect.y += speed * dt
        if rect.top > window_h:
            meteor_list.remove(rect)

# game init
pygame.init()
window_w, window_h = 1280,720
display_surface = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Space Invader")
clock = pygame.time.Clock()

# bg import
bg_space = pygame.image.load("./graphics/background.png").convert()

# Ship import 
space_ship = pygame.image.load("./graphics/ship.png").convert_alpha()
ship_rect = space_ship.get_rect(center = (window_w / 2, window_h / 2))

# text import
font = pygame.font.Font("./graphics/subatomic.ttf", 50)

# laser Import
laser_surf = pygame.image.load("./graphics/laser.png").convert_alpha()
laser_list = []

# Meteor Import
meteor_surf = pygame.image.load("./graphics/meteor.png").convert_alpha()
meteor_list = []

# laser timer
can_shoot = True
shoot_time = None

# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 800)

# sound
laser_sound = pygame.mixer.Sound('./sounds/laser.ogg')
explosion_sound = pygame.mixer.Sound('./sounds/explosion.wav')
bg_music = pygame.mixer.Sound('./sounds/music.wav')
pygame.mixer.Sound.set_volume(bg_music, 0.1)
pygame.mixer.Sound.set_volume(laser_sound, 0.5)
pygame.mixer.Sound.set_volume(explosion_sound, 0.7)
bg_music.play(loops = -1)

# keeps the game running
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # laser
        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
            laser_list.append(laser_rect)

            # timer
            can_shoot = False
            shoot_time = pygame.time.get_ticks()

            # laser sound
            laser_sound.play()

        if event.type == meteor_timer:
            x_pos = randint(-100, window_w + 100)
            y_pos = randint(-100, -50)
            meteor_rect = meteor_surf.get_rect(center = (x_pos,y_pos))
            meteor_list.append(meteor_rect)

    # fps limit
    dt = clock.tick() / 1000

    # mouse input
    ship_rect.center = pygame.mouse.get_pos()

    # update
    laser_update(laser_list)
    meteor_update(meteor_list)
    can_shoot = laser_timer(can_shoot, 300)

    # collisions
    for meteor in meteor_list:
        meteor_rect = meteor[0]
        if ship_rect.colliderect(meteor):
            pygame.quit()
            sys.exit()
    
    # laser x meteor
    for laser in laser_list:
        for meteor in meteor_list:
            if laser_rect.colliderect(meteor):
                meteor_list.remove(meteor)
                laser_list.remove(laser)
                explosion_sound.play()
    
    # drawing
    display_surface.fill((0, 0, 0))
    display_surface.blit(bg_space,(0,0))
    display_surface.blit(space_ship,(ship_rect))
    score()
    for rect in laser_list:
        display_surface.blit(laser_surf, rect)

    for rect in meteor_list:
        display_surface.blit(meteor_surf, rect)

    #frame / update diplay surface
    pygame.display.update()