import pygame
from pygame import *
from random import randint
from time import time as timer


mixer.init()
mixer.music.load('zm.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
start_time = timer()

font.init()
font1 = font.SysFont("Impact", 36)
font2 = font.SysFont("Impact", 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))


img_back = "back.png"
img_hero = "player.png"
img_enemy = "zombie.png"
img_ast = "asteroid.png"
#img_heart0 = "hearbeat.png"
#img_heart1 = "hearbear_1.png"
#img_heart2 = "hearbear_2.png"
#img_heart3 = "hearbeat_3.png"

score = 0
lost = 0
#goal = 100
max_lost = 3
#life = 3
md = 1
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, sixe_y , sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(size_x, sixe_y))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        self.max_life = 3
        self.life = 3
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 100:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet("bullets.png", self.rect.centerx, self.rect.top, 1, 20, -15)
        bullets.add(bullet)

    #def heal(self):
    #    if self.life < self.max_life:
    #        self.life += 1
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width - 80)
            self.rect.y = 0

#class MedKit(GameSprite):
#    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
#        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
#
#    def update(self):
#        self.rect.y += self.speed
#        if self.rect.y > win_height:
#            self.rect.x = randint(80, win_width - 80)
#            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

player = Player(img_hero, 10, win_height - 100, 80, 100, 10)

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(1, 15):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 81, 81, randint(1, 3))
    monsters.add(monster)
#heart0 = GameSprite(img_heart0, randint(0, win_width - 0), 40, 100, 100,randint(0, 0))
#heart1 = GameSprite(img_heart1, randint(0, win_width - 0), 40, 100, 100,randint(0, 0))
#heart2 = GameSprite(img_heart2, randint(0, win_width - 0), 40, 100, 100,randint(0, 0))
#heart3 = GameSprite(img_heart3, randint(0, win_width - 0), 40, 100, 100,randint(0, 0))
#heart = GameSprite("hearbeat.png", randint(0, win_width - 0), 40, 100, 100,randint(0, 0))


run = True
finish = False
clock = time.Clock()
FPS = 30
rel_time = False
num_fire = 0

#medkits = sprite.Group()
#medkit = MedKit("med.png", randint(80, win_width - 80), 0, 40, 40, randint(1, 3))
#medkits.add(medkit)
#life = 3
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and not finish:
            if e.key == K_SPACE:
                if num_fire < 30 and not rel_time:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()
                elif num_fire >= 30 and not rel_time:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))
        player.update()
        #heart.reset()
        monsters.update()
        bullets.update()
        #heart.update()
        player.reset()
        #heart.reset()
        #heart0.rect.x = 10
        #heart0.rect.y = 100
        #heart.rect.x = 10
        #heart.rect.y = 100
        #heart1.rect.x = 10
        #heart1.rect.y = 100
        #heart2.rect.x = 10
        #heart2.rect.y = 100
       #if int(life) == 2:
       #    window.blit(background, (0, 0))
       #    player.update()
       #    heart1.reset()
       #    monsters.update()
       #    bullets.update()
       #    heart1.update()
       #    player.reset()
       #    heart1.reset()
       #    medkit.reset()
       #if int(life) == 2:
       #    window.blit(background, (0, 0))
       #    player.update()
       #    heart2.reset()
       #    monsters.update()
       #    bullets.update()
       #    heart2.update()
       #    player.reset()
       #    heart2.reset()
       #    medkit.reset()
       #if int(life) == 2:
       #    heart = heart3
       #else:
       #    heart = heart3
        monsters.draw(window)
        bullets.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 2:
                reload = font2.render('Перезарядка..', 1, (150, 0, 0))
                window.blit(reload, (win_width/2-200, win_height-100))
            else:
                num_fire = 0
                rel_time = False


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 81, 81, randint(1, 3))
            monsters.add(monster)


        #if pygame.sprite.collide_rect(player, medkit):
        #    life += 1
        #    medkit.rect.y = -40
        #    if life == 3:
        #        heart = heart0
        #    if life == 2:
        #        heart = heart1


        if sprite.spritecollide(player, monsters, False):
            sprite.spritecollide(player, monsters, True)

            #life = life -1

        current_time = timer()
        if current_time - start_time >= 60:
            finish = True

       #if life == 0 or lost >= max_lost:
       #    heart = img_heart3
       #    finish = True
       #    window.blit(lose, (200, 200))


        #if score >= ##goal:
        #    finish = True
        #    window.blit(win, (200, 200))

        text = font1.render("Рахунок: " + str(score),1, (255,255,255))
        window.blit(text,(10, 20))

        elapsed_time = current_time - start_time
        remaining_time = max(0, 60 - elapsed_time)
        time_text = font1.render("Час: " + str(int(remaining_time)), 1, (255, 255, 255))
        window.blit(time_text, (10, 50))

        #text_life = font1.render(str(life), 1, (0, 150, 0))
        #window.blit(text_life, (650, 10))

        display.update()
    clock.tick(FPS)
