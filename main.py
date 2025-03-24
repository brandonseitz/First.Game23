import pygame
import random

p = pygame
WIDTH = 600
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
RED = (255, 5, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (238, 130, 238)
ORANGE = (255, 165, 0)

running = True
new_game = True
game_over = False

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def newmob():
    rock = Mob("r",2,3)
    mobs.add(rock)
    all_sprites.add(rock)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.height = 20
        self.width = 20
         # self.image = pygame.Surface((self.height,self.width))
        # self.image.fill(ORANGE)
        self.image = pygame.image.load("All Game Art/bullet.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        # set up move
        self.speedx = 0
        self.speedy = 10

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.top <= 0:
            self.kill()
class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.height = 20
        self.width = 10
        self.image = pygame.Surface((self.height,self.width))
        self.image.fill(ORANGE)
        self.type = random.choice(['health','gun'])
        # self.image = pygame.image.load("All Game Art/shield_bronze.png")
        # if self.type == 'gun':
        #     self.image = pygame.image.load("All Game Art/bolt_gold.png")
        # self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.center = center
        # set up move
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy

class Mob(pygame.sprite.Sprite):
    def __init__(self,r,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.height = 48
        self.width = 60
        self.meteor_list = []
        #self.load_images()
        #rocks = random.choice(self.meteor_img)
        #self.image = rocks
        # self.image = pygame.Surface((self.width,self.height))
        #self.image.fill(RED)
        # self.pick = random.choice(self.meteor_list)
        # self.image = self.pick
        self.image = pygame.image.load("All Game Art/ufo.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        #rectangle
        self.rect  = self.image.get_rect()
        #location on screen
        self.rect.x = random.randrange(0, WIDTH - self.width)
        self.rect.centery = random.randrange(-200, -100)
        # set up move
        self.speedx = 0
        self.speedy = random.randrange(3, 5)

    def load_images(self):
        for i in range(1, 4):
            filename = "All Game Art/meteor{}.png".format(i)
            img = pygame.image.load(filename)
            self.images.append(img)

    def update(self):
        if self.rect.top >= HEIGHT:
            self.rect.centerx = random.randrange(0, WIDTH - self.width)
            self.rect.centery = random.randrange(-200, -100)
            self.speedy = random.randrange(5, 20)
        self.rect.y += self.speedy


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.height = 38
        self.width = 60
        self.create_mob = False
        # self.image = pygame.Surface((self.height,self.width))
        # self.image.fill(BLUE)
        self.image = pygame.image.load("All Game Art/ship5.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        # set up move
        self.speedx = 0
        self.speedy = 3
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.score = 0
        self.lives = 3
        self.health = 100
        self.spawn = True
        self.mob_count=0
        self.power = 1
        self.power_time = pygame.time.get_ticks()

        self.mini_img = p.transform.scale(self.image, (20,20))

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            b = Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(b)
            bullets.add(b)
        if self.power>= 2:
            b1 = Bullet(self.rect.left, self.rect.top)
            b2 = Bullet(self.rect.right, self.rect.top)
            all_sprites.add(b1)
            bullets.add(b1)
            all_sprites.add(b2)
            bullets.add(b2)


    def update(self):
        if self.power>=2 and pygame.time.get_ticks() - self.power_time>5000:
            self.power -=1
            self.power_time=pygame.time.get_ticks()
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        # self.rect.y += self.speedy

def start_screen():
    screen.fill(BLACK)
    draw_text(screen, "WELCOME", 64, WIDTH // 2, HEIGHT // 2.5, RED)
    draw_text(screen, "Press SPACE to Start", 32, WIDTH // 2, (HEIGHT // 2.5) - 20, RED)
    draw_text(screen, "Press Q to Quit", 32, WIDTH // 2, (HEIGHT // 2.5) + 55, RED)
    p.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in p.event.get():
            k = p.key.get_pressed()
            if event.type == p.QUIT:
                p.quit()
            if event.type == p.KEYDOWN:
                if k[p.K_SPACE]:
                    waiting = False
                if k[p.K_q]:
                    p.quit()
# initialize pygame and create window
pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Game")
clock = pygame.time.Clock()

start_screen()

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
mobs = pygame.sprite.Group()
r="r"
l="l"
n="n"

ship = Player()
all_sprites.add(ship)

background_img = pygame.image.load("All Game Art/backgroundSpace_01.1.png")

background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
background_rect = background_img.get_rect()

for i in range(8):
    rock = Mob("r",2, 3)
    mobs.add(rock)
    all_sprites.add(rock)


now = pygame.time.get_ticks()
delay = 400



# Game loop

last_spawn = pygame.time.get_ticks()
delay = 2000
while running:
    if new_game:
        new_game = False
        count = 0
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        if game_over:
            if event.type == p.KEYDOWN:
                if event.key == p.K_SPACE:
                    ship.lives = 3
                    ship.health = 100
                    ship.score = 0
                    all_sprites.empty()
                    mobs.empty()
                    bullets.empty()
                    all_sprites.add(ship)
                    game_over = False
                    new_game = True
                elif event.key == p.K_q:
                    pass
    if game_over:
        screen.fill(BLACK)
        draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 2.5, RED)
        draw_text(screen, "Press SPACE to Restart", 32, WIDTH // 2, (HEIGHT // 2.5) - 20, RED)
        draw_text(screen, "Press Q to Quit", 32, WIDTH // 2, (HEIGHT // 2.5) + 55, RED)
        p.display.flip()
    else:
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        hit_player = pygame.sprite.spritecollide(ship, mobs, True)
        hit_mob = pygame.sprite.groupcollide(bullets, mobs, True, True)
        hit_power = pygame.sprite.spritecollide(ship, powers, True)

        if hit_player:
            # damage to player(ship)
            ship.health -= 25
            newmob()
        if ship.health <= 0:
            ship.health = 100
            ship.lives -= 1
        if ship.lives <= 0:
            game_over = True
        if hit_mob:
            for hit in hit_mob:
                pow = Power(hit.rect.center)
                all_sprites.add(pow)
                powers.add(pow)
            ship.score += 1
            newmob()
        if ship.spawn == True:
                x = random.randrange(100,WIDTH-ship.width-40)
                y = random.randrange(100,300)
                m = Mob(r,x,y)
                all_sprites.add(m)
                mobs.add(m)
                m1 = Mob(l,x,y)
                all_sprites.add(m1)
                mobs.add(m1)
                ship.spawn = False
        # if ship.spawn:
        if ship.create_mob == True:
            m2 = Mob(n,x,y)
            all_sprites.add(m2)
            mobs.add(m2)
            ship.create_mob = False

            ship.mob_count +=1
        if ship.mob_count <3:
            now = pygame.time.get_ticks()
            if now - last_spawn > delay:
                ship.spawn = True
                last_spawn = now

        if hit_power:
            for pow in hit_power:
                ran = random.choice(pow.type)
                if ran == 'gun':
                    pass
                elif ran == 'health':
                    pass

        # update
        all_sprites.update()
        # Draw / render
        # screen.fill(GREEN)
        screen.blit(background_img, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, str(ship.score), 32, WIDTH // 2, 10, WHITE)
        #draw_text(screen, str(ship.lives), 32, 3 * WIDTH // 4, 10, WHITE)
        #draw_text(screen, str(ship.health), 32, WIDTH // 4, 10, WHITE)
        draw_shield_bar(screen, 5, 5, ship.health)
        draw_lives(screen, WIDTH - 100, 5, ship.lives, ship.mini_img)

        # *after* drawing everything, flip the display
        pygame.display.flip()

pygame.quit()