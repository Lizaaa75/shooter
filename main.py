from pygame import *
from random import *

mixer.init()
mixer.music.load('space (1).ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire (1).ogg')

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (255, 0, 0))
font2 = font.Font(None, 36)

img_back = "galaxy (1).jpg" #фон гри
img_hero = "rocket (1).png" #гравець
img_bullet = "bullet (1).png"
img_enemy = "ufo (1).png" #ворог

score = 0
lost = 0
max_lost = 3
goal = 10

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

bullets = sprite.Group()

finish = False
run = True # прапорець скидається кнопкою закриття вікна

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN: 
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0, 0)) # фон

        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255)) # текст рахунку
        window.blit(text, (10, 20)) # відображення тексту

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update() # оновлення гравця
        monsters.update() # оновлення списку воррогів 
        bullets.update()

        ship.reset() # відображення гравця
        monsters.draw(window) # відображення
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update() # оновлення вікна
    time.delay(50) # затримка 50 мс