import pygame
from os.path import join
from random import randint, uniform
import math

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
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

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
        self.original_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300
        self.angle = 0  # Ángulo inicial
        self.rotation_speed = 180  # Grados por segundo

        # Cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 200

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def handle_wrap_around(self):
        if self.rect.top < -80:
            self.rect.bottom = WINDOW_HEIGHT
        elif self.rect.bottom > WINDOW_HEIGHT + 80:
            self.rect.top = -60

        if self.rect.left < -80:
            self.rect.right = WINDOW_WIDTH
        elif self.rect.right > WINDOW_WIDTH + 80:
            self.rect.left = -60

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Rotar a la izquierda o derecha
        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed * dt
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed * dt

        # Normalizar el ángulo
        self.angle %= 360

        # Crear la imagen rotada
        self.image = pygame.transform.rotozoom(self.original_surf, -self.angle, 1)
        self.rect = self.image.get_frect(center=self.rect.center)

        # Movimiento hacia adelante en la dirección del ángulo
        if keys[pygame.K_UP]:
            radians = math.radians(self.angle)
            self.direction.x = math.sin(radians)
            self.direction.y = -math.cos(radians)

            self.rect.center += self.direction * self.speed * dt

        # Teletransporte en los bordes
        self.handle_wrap_around()

        # Disparo
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites, laser_sprites), laser_surf, self.rect.center, self.angle)
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
    def __init__(self, groups, surf, pos, angle):
        super().__init__(groups)

        # Rotar el láser según el ángulo de la nave
        self.original_image = surf
        self.image = pygame.transform.rotozoom(self.original_image, -angle, 1)
        self.rect = self.image.get_frect(center=pos)

        # Calcular la dirección del láser basada en el ángulo
        radians = math.radians(angle)
        self.direction = pygame.Vector2(math.sin(radians), -math.cos(radians))

        # Ajustar la posición de salida del láser
        offset = pygame.Vector2(self.direction.x * 30, self.direction.y * 30)
        self.rect.center += offset

        self.speed = 800

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if (self.rect.bottom <= 0 or self.rect.top >= WINDOW_HEIGHT or
                self.rect.right <= 0 or self.rect.left >= WINDOW_WIDTH):
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos, scale=1):
        super().__init__(groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.life = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(500, 600)
        self.rotation_speed = randint(50, 200)
        self.rotation = 0
        self.scale = scale

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.life:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, self.scale)
        self.rect = self.image.get_frect(center=self.rect.center)


class MeteorMini(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos, scale=1):
        super().__init__(groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.life = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(500, 600)
        self.rotation_speed = randint(50, 200)
        self.rotation = 0
        self.scale = scale

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.life:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, self.scale)
        self.rect = self.image.get_frect(center=self.rect.center)


class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()


# Sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
mini_meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()


# Funciones
def display_score():
    global current_time
    if playing:
        current_time = (pygame.time.get_ticks() - start_time) // 1000
    else:
        current_time = 0

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


def collisions():
    global gameover, life, puntation

    # Actualizar todos los sprites
    all_sprites.update(dt)

    # Colisiones del jugador con meteoritos grandes
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        for meteor in collision_sprites:
            collision_pos = meteor.rect.center
            AnimatedExplosion(explosion_frames, collision_pos, all_sprites)
            explosion_sound.play()
        life -= 1
        if life <= 0:
            gameover = True
    # COlisiones del jugador con meteoritos pequeños
    collision_sprites = pygame.sprite.spritecollide(player, mini_meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        for meteor in collision_sprites:
            collision_pos = meteor.rect.center
            AnimatedExplosion(explosion_frames, collision_pos, all_sprites)
            explosion_sound.play()
        life -= 1
        if life <= 0:
            gameover = True

    # Colisiones de los láseres con meteoritos grandes
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()  # Destruir el láser al colisionar
            for meteor in collided_sprites:
                # Generar explosión en la posición de colisión
                collision_pos = meteor.rect.center
                AnimatedExplosion(explosion_frames, collision_pos, all_sprites)

                # Crear dos meteoritos pequeños desde la posición de colisión
                MeteorMini((all_sprites, mini_meteor_sprites), meteor_surf, collision_pos, scale=0.7)
                MeteorMini((all_sprites, mini_meteor_sprites), meteor_surf, collision_pos, scale=0.7)

                explosion_sound.play()

            puntation += 1

    # Colisiones de los láseres con meteoritos pequeños
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, mini_meteor_sprites, True)
        if collided_sprites:
            laser.kill()  # Destruir el láser
            for mini_meteor in collided_sprites:
                collision_pos = mini_meteor.rect.center
                AnimatedExplosion(explosion_frames, collision_pos, all_sprites)
                explosion_sound.play()

            puntation += 1


# surfaces
surf = pygame.Surface((100, 200))
surf.fill('red')

for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# Customs Events
number_asteroids = 900
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, number_asteroids)

playing = False
game_music.play(loops=-1)
second_level = False
first_level = True

while runnig:
    number_asteroids -= 10
    pygame.mouse.set_visible(False)
    dt = clock.tick() / 1000  # fps
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

        # Level 1
        if e.type == meteor_event and playing and not gameover and first_level:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor((all_sprites, meteor_sprites), meteor_surf, (x, y))

        # Level 2
        if e.type == meteor_event and playing and not gameover and second_level:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            MeteorMini((all_sprites, mini_meteor_sprites), meteor_surf, (x, y), scale=0.5)

    if puntation >= 10:
        second_level = True
        playing = False
        first_level = False

    if second_level and not playing:
        next_leve_text()

    # Colisiones
    display_score()
    display_puntation()
    display_life()
    if not playing:
        display_text()
    if gameover:
        gameover_text()

    collisions()
    all_sprites.draw(window)

    pygame.display.update()

pygame.quit()
