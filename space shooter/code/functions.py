import pygame
from clases import AnimatedExplosion

puntation = 0
life = 3

def collisions(player, all_sprites, meteor_srpites, laser_sprites, explosion_framse, explosion_sound):
    global life, puntation
    all_sprites.update()
    collision_sprites = pygame.sprite.spritecollide(player, meteor_srpites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        for meteor in collision_sprites:
            collision_pos = meteor.rect.center
            AnimatedExplosion(explosion_framse, collision_pos, all_sprites)
            explosion_sound.play()
        life -= 1
        if life <= 0:
            return False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_srpites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_framse, laser.rect.midtop, all_sprites)
            explosion_sound.play()
            puntation += 1
    return True

def display_score(window, font):
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, '#cbd1f5')
    text_rect = text_surf.get_rect(midbottom=(40, 80))
    window.blit(text_surf, text_rect)
    pygame.draw.rect(window, "#cbd1f5", text_rect.inflate(20, 20).move(0, -5), 5, 10)

def display_puntation(window, font):
    global puntation
    text_surf = font.render(str(puntation), True, '#cbd1f5')
    text_rect = text_surf.get_rect(midbottom=(40, 240))
    window.blit(text_surf, text_rect)
    pygame.draw.rect(window, "#cbd1f5", text_rect.inflate(20, 20).move(0, -5), 5, 10)

def display_life(window, font, life):
    text_surf = font.render(str(life), True, '#cbd1f5')
    text_rect = text_surf.get_rect(midbottom=(40, 160))
    window.blit(text_surf, text_rect)
    pygame.draw.rect(window, "#cbd1f5", text_rect.inflate(20, 20).move(0, -5), 5, 10)
