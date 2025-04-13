from pygame import *
from random import *
from time import time as timer

mixer.init()
mixer.music.load('space (1).ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire (1).ogg')

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (255, 0, 0))
font2 = font.Font(None, 36)

img_back = "background.jpg" #фон гри
img_hero = "банка помідорів.png" #гравець
img_bullet = "помідор-removebg-preview.png"
img_enemy = "шахед.png" #ворог
img_ast = "asteroid (1).png"

score = 0
lost = 0
max_lost = 3
goal = 10
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, w, h, player_speed): #конструктор
        sprite.Sprite.__init__(self)
        self.image = transform.scale(
            image.load(player_image), (w, h))
        self.speed = player_speed

        #крдинати спавну
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    #завантаження гравця
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed # швидкість падіння
        global lost #глобальна змінна підрахунку пропущених кораблів
        if self.rect.y > win_height: # якщо коробль знизу
            self.rect.x = randint(80, win_width - 80) # рандомна поява x
            self.rect.y = 0 
            lost = lost + 1 # збільшуємо lost

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group() #група спрайтів 
for i in range (1, 6):
    monster = Enemy(img_enemy, randint(
        80, win_width - 80), -40, 80, 50, randint(1, 5)) # створюємо рандомно ворога
    monsters.add(monster) # додаємо в групу

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()

finish = False
run = True # прапорець скидається кнопкою закриття вікна
rel_time = False
num_fire = 0

while run:
    print(life)
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN: 
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0)) # фон

        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255)) # текст рахунку
        window.blit(text, (10, 20)) # відображення тексту

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update() # оновлення гравця
        monsters.update() # оновлення списку воррогів 
        asteroids.update()
        bullets.update()

        ship.reset() # відображення гравця
        monsters.draw(window) # відображення
        asteroids.draw(window)
        bullets.draw(window)

        if rel_time:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('А все, жди тепер, нічого було багато шмалять ...', 1, (150, 0, 0))
                window.blit(reload, (100, 460))

            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        #if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
        #    finish = True
        #    window.blit(lose, (200, 200))

        '''
        #можливий програш: пропустили занадто багато чи герой зіткнувся з ворогом чи встероїдом
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            finish = True # програли, ставимо тло і більше не керуємо спрайтами.
            window.blit(lose, (200, 200))'''

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True #програли, ставим фон і більше не упровляєм спрайтами
            window.blit(lose, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))


        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update() # оновлення вікна
    time.delay(50) # затримка 50 мс