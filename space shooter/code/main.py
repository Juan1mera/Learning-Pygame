import pygame
from os.path import join
from random import randint, uniform

# Inicio General
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
runnig = True
clock = pygame.time.Clock()

# Images
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
explosion_framse = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
laser_sound.set_volume(0.2)

explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
explosion_sound.set_volume(0.1)


game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_music.set_volume(0.1)

gameover = False
current_time = 0
puntation = 0
life = 3
start_time = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.origianl_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
        # join se usa para no tener problemas si es macos o windows para no tener problemas con "/" o "\"
        self.image = self.origianl_surf
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        #Cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldowb_duration = 200



        # Mask

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldowb_duration:
                self.can_shoot = True

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        # Hace que la velocidad se igual siempre aunque vaya dos teclas esten presionadas
        # player_direction = player_direction.normalize() if player_direction else player_direction
        
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites, laser_sprites), laser_surf, self.rect.midtop )
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()  
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))  
class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom <= 0:
            self.kill()
class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.origianl_surf = surf
        self.image = self.origianl_surf
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.life = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation_speed = randint(20, 150)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.life:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.origianl_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)
class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)
    
    def update(self, dt):
        self.frame_index += 20 *dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def collisions():

    global gameover
    all_sprites.update(dt)
    collision_sprites = pygame.sprite.spritecollide(player, meteor_srpites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        for meteor in collision_sprites:
            collision_pos = meteor.rect.center
            AnimatedExplosion(explosion_framse, collision_pos, all_sprites)
            explosion_sound.play()
        global life 
        life -= 1
        if life <= 0:
            gameover = True

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_srpites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_framse, laser.rect.midtop, all_sprites)
            explosion_sound.play()
            global puntation
            puntation += 1


def display_score():
    global current_time
    if playing:
        # Calcula el tiempo transcurrido desde que se inició el juego
        current_time = (pygame.time.get_ticks() - start_time) // 1000  # Tiempo en segundos
    else:
        current_time = 0  # Al reiniciar, muestra 0

    text_surf = font.render(str(current_time), True, '#cbd1f5')
    text_rect = text_surf.get_rect(midbottom=(40, 80))
    window.blit(text_surf, text_rect)
    pygame.draw.rect(window, "#cbd1f5", text_rect.inflate(20, 20).move(0, -5), 5, 10)
def display_puntation():
    global puntation
    text_surf = font.render(str(puntation), True, '#cbd1f5')
    text_rect = text_surf.get_rect(midbottom=(40, 240))
    window.blit(text_surf, text_rect)
    pygame.draw.rect(window, "#cbd1f5", text_rect.inflate(20, 20).move(0, -5), 5, 10)

def display_life():
    global life 
    text_surf = font.render(str(life), True, '#cbd1f5')
    text_rect = text_surf.get_rect(midbottom=(40, 160))
    window.blit(text_surf, text_rect)
    pygame.draw.rect(window, "#cbd1f5", text_rect.inflate(20, 20).move(0, -5), 5, 10)
def display_text():
    current_time = pygame.time.get_ticks()
    
    if (current_time // 500) % 2 == 0:
        text_surf = font.render("Press Enter to Start", True, '#cbd1f5')
        text_rect = text_surf.get_rect(midtop=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
        window.blit(text_surf, text_rect)
        pygame.draw.rect(window, "#cbd1f5", text_rect.inflate(20, 20).move(0, -5), 5, 10)
def gameover_text():
    current_time = pygame.time.get_ticks()
    
    if (current_time // 500) % 2 == 0:
        text_surf = font.render("Game Over, Press Enter to Restart", True, '#cbd1f5')
        text_rect = text_surf.get_rect(midtop=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
        window.blit(text_surf, text_rect)
        pygame.draw.rect(window, "#cbd1f5", text_rect.inflate(20, 20).move(0, -5), 5, 10)
def next_leve_text():
    current_time = pygame.time.get_ticks()
    
    if (current_time // 500) % 2 == 0:
        text_surf = font.render("Next Level", True, '#cbd1f5')
        text_rect = text_surf.get_rect(midtop=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 160))
        window.blit(text_surf, text_rect)
        pygame.draw.rect(window, "#cbd1f5", text_rect.inflate(20, 20).move(0, -5), 5, 10)





# surfaces
surf = pygame.Surface((100, 200))
surf.fill('red')

# Sprites
all_sprites = pygame.sprite.Group()
meteor_srpites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()


for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# Customs Events
number_asteroids = 500
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, number_asteroids)

playing = False
game_music.play(loops=-1)
second_level =  False
while runnig:

    number_asteroids -= 1
    pygame.mouse.set_visible(False)
    dt = clock.tick() / 1000 # fps
    window.fill('#1b1d29')
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            runnig = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN: 
                playing = True
                gameover = False
                life = 3
                puntation = 0
                current_time = 0
                start_time = pygame.time.get_ticks()


        if e.type == meteor_event and playing and gameover == False:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor((all_sprites, meteor_srpites), meteor_surf, (x, y))

    if puntation >= 10:
        second_level = True
        playing = False
    
    if second_level:
        next_leve_text()

    # Colisiones
    display_score()
    display_puntation()
    display_life()
    if playing == False:
        display_text()
    if gameover:
        gameover_text()


    collisions()
    all_sprites.draw(window)

    pygame.display.update()



pygame.quit()