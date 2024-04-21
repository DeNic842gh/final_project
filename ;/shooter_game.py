# Імпорти
from pygame import *
from random import randint
from time import time as timer
import os

# Шрифт
font.init()
font1 = font.SysFont("Impact", 80)
font2 = font.SysFont("Impact", 36)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

# Музика
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# Картинкі
img_back = "fort.png"
img_bullet = "bullets2.png"
img_hero = "recket2.png"
img_enemy = "ufo1.png"
img_asteroid = "aste1.jpg"

# Змінні
score = 0
goal = 30
lost = 0
max_lost = 3
health = 3
workdir = os.getcwd()


class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(os.path.join(workdir, player_image)), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_DOWN] and self.rect.y > 5:
            self.rect.y+= self.speed
        if keys[K_UP] and self.rect.y < win_width - 80:
            self.rect.y-= self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


class Asteroid(GameSprite):

    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0


class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 20)

asteroids = sprite.Group()
monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

for i in range(1, 3):
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()

finish = False
run = True
rel_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background, (0, 0))

        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 2:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (win_width / 2 - 200, win_height - 100))
            else:
                num_fire = 0
                rel_time - False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            health -= 1

        if sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, asteroids, True)
            asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)
            health -= 1

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if lost >= max_lost or health == 0:
            finish = True
            window.blit(lose, (200, 200))

        display.update()
    time.delay(60)