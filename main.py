# -*- coding: utf-8 -*-


import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random



pygame.init()
ventana = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Naves')


sonido_Bala = pygame.mixer.Sound('resources/sound/bullet.wav')
enemigo_muerto = pygame.mixer.Sound('resources/sound/enemigo_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
sonido_Bala.set_volume(0.3)
enemigo_muerto.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


Fondo = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

Aimg = 'resources/image/shoot.png'
imagen_nave = pygame.image.load(Aimg)


Jugador_rect = []
Jugador_rect.append(pygame.Rect(0, 99, 102, 126))        
Jugador_rect.append(pygame.Rect(165, 360, 102, 126))
Jugador_rect.append(pygame.Rect(165, 234, 102, 126))     
Jugador_rect.append(pygame.Rect(330, 624, 102, 126))
Jugador_rect.append(pygame.Rect(330, 498, 102, 126))
Jugador_rect.append(pygame.Rect(432, 624, 102, 126))
Jugador_pos = [200, 600]
Jugador = Jugador(imagen_nave, Jugador_rect, Jugador_pos)


Bala_rect = pygame.Rect(1004, 987, 9, 21)
Bala_img = imagen_nave.subsurface(Bala_rect)


enemigo_rect = pygame.Rect(534, 612, 57, 43)
enemigo_img = imagen_nave.subsurface(enemigo_rect)


enemigo_down_imgs = []
enemigo_down_imgs.append(imagen_nave.subsurface(pygame.Rect(267, 347, 57, 43)))
enemigo_down_imgs.append(imagen_nave.subsurface(pygame.Rect(873, 697, 57, 43)))
enemigo_down_imgs.append(imagen_nave.subsurface(pygame.Rect(267, 296, 57, 43)))
enemigo_down_imgs.append(imagen_nave.subsurface(pygame.Rect(930, 697, 57, 43)))

enemigos = pygame.sprite.Group()
enemies_down = pygame.sprite.Group()

shoot_frequency = 0
enemy_frequency = 0

Jugador_down_index = 16

puntaje = 0

clock = pygame.time.Clock()

running = True

while running:
    
    clock.tick(60)

    
    if not Jugador.is_hit:
        if shoot_frequency % 15 == 0:
            sonido_Bala.play()
            Jugador.shoot(Bala_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

   
    if enemy_frequency % 50 == 0:
        enemigo_pos = [random.randint(0, SCREEN_WIDTH - enemigo_rect.width), 0]
        enemigo = Enemigo(enemigo_img, enemigo_down_imgs, enemigo_pos)
        enemigos.add(enemigo)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    
    for bullet in Jugador.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            Jugador.bullets.remove(bullet)

    
    for enemy in enemigos:
        enemy.move()
        
        if pygame.sprite.collide_circle(enemy, Jugador):
            enemies_down.add(enemy)
            enemigos.remove(enemy)
            Jugador.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemigos.remove(enemy)

    
    enemigos_down = pygame.sprite.groupcollide(enemigos, Jugador.bullets, 1, 1)
    for enemy_down in enemigos_down:
        enemies_down.add(enemy_down)

    
    ventana.fill(0)
    ventana.blit(Fondo, (0, 0))

    
    if not Jugador.is_hit:
        ventana.blit(Jugador.image[Jugador.img_index], Jugador.rect)
        
        Jugador.img_index = shoot_frequency // 8
    else:
        Jugador.img_index = Jugador_down_index // 8
        ventana.blit(Jugador.image[Jugador.img_index], Jugador.rect)
        Jugador_down_index += 1
        if Jugador_down_index > 47:
            running = False

    
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemigo_muerto.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            puntaje += 1000
            continue
        ventana.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    
    Jugador.bullets.draw(ventana)
    enemigos.draw(ventana)

    
    puntaje_font = pygame.font.Font(None, 36)
    puntaje_text = puntaje_font.render(str(puntaje), True, (128, 128, 128))
    text_rect = puntaje_text.get_rect()
    text_rect.topleft = [10, 10]
    ventana.blit(puntaje_text, text_rect)

    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    
    key_pressed = pygame.key.get_pressed()
    
    if not Jugador.is_hit:
        if key_pressed[K_w] or key_pressed[K_UP]:
            Jugador.arriba()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            Jugador.abajo()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            Jugador.izquierda()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            Jugador.derecha()


font = pygame.font.Font(None, 48)
text = font.render('puntaje: '+ str(puntaje), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = ventana.get_rect().centerx
text_rect.centery = ventana.get_rect().centery + 24
ventana.blit(game_over, (0, 0))
ventana.blit(text, text_rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
