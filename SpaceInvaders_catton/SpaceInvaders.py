import pygame
import random 
# variables
WINDOW = pygame.display.set_mode((600, 600))
pygame.display.set_caption('SpaceInvaders by Catton')
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0) 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)                                                                                             
MYCOLOR = (18, 52, 86)
pygame.font.init()


GAME_FONT = pygame.font.SysFont('comicsans', 30)
ENEMYPOS = [295, 320, 365] 
BULLETS = [] # this stores pygame.Rect
ENEMIES = [] # this stores pygame.Rect
ENEMYBULLETS = []
# C:\Users\evync\OneDrive\Music\Pictures\UFO.png
SPACESHIP_ORIGINAL = pygame.image.load('UFO.jpg')
SPACESHIP = pygame.transform.scale(SPACESHIP_ORIGINAL, (70, 70)) 


ENEMY_ORIGINAL = pygame.image.load('UFO.jpg')
ENEMY = pygame.transform.scale(ENEMY_ORIGINAL, (40, 40)) 

ENEMY_HIT = pygame.USEREVENT + 1 
PLAYER_HIT = pygame.USEREVENT + 2

def makeEnemies():
    ENEMIES.append(pygame.Rect((275, 70, 40, 40)))
    ENEMIES.append(pygame.Rect((320, 70, 40, 40)))
    ENEMIES.append(pygame.Rect((365, 70, 40, 40)))


def enemiesControl(direction):
    
    for enemy in ENEMIES:
        enemy.x += direction
        
        if direction == 2:
            
            b = ENEMYPOS[0]
            b += 2/3
            ENEMYPOS.remove(ENEMYPOS[0])
            ENEMYPOS.insert(0, b)

            a = ENEMYPOS[1]
            a += 2/3
            ENEMYPOS.remove(ENEMYPOS[1])
            ENEMYPOS.insert(1, a)

            c = ENEMYPOS[2]
            c += 2/3
            ENEMYPOS.remove(ENEMYPOS[2])
            ENEMYPOS.insert(2, c)

        if direction == -2: 
            b = ENEMYPOS[0]
            b += -2/3
            ENEMYPOS.remove(ENEMYPOS[0])
            ENEMYPOS.insert(0, b)

            a = ENEMYPOS[1]
            a += -2/3
            ENEMYPOS.remove(ENEMYPOS[1])
            ENEMYPOS.insert(1, a)

            c = ENEMYPOS[2]
            c += -2/3
            ENEMYPOS.remove(ENEMYPOS[2])
            ENEMYPOS.insert(2, c)

        if enemy.left <= 0:
            direction = 2

        if enemy.right > WINDOW.get_width():
            direction = -2

        

        pygame.draw.rect(WINDOW, BLUE, enemy)
   
        WINDOW.blit(ENEMY, (enemy))
    return direction


def playerControl(PLAYER):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and PLAYER.x < WINDOW.get_width() - PLAYER.width:
        PLAYER.x += 7

    if keys[pygame.K_LEFT] and PLAYER.x > 0:
        PLAYER.x -= 7 

    WINDOW.blit(SPACESHIP, (PLAYER.x, PLAYER.y))
    #pygame.draw.rect(WINDOW, RED, PLAYER)

def bulletControl():
    for bullet in BULLETS:
        bullet.y -= 15
        for enemy in ENEMIES:
            if bullet.colliderect(enemy):  
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                ENEMIES.remove(enemy)
                BULLETS.remove(bullet )
        pygame.draw.rect(WINDOW, WHITE, bullet)

def enemyBulletControl(PLAYER): 
    for bullet in ENEMYBULLETS:
        bullet.y += 15
        
        if bullet.colliderect(PLAYER):  
            ENEMYBULLETS.remove(bullet)  
            pygame.event.post(pygame.event.Event(PLAYER_HIT))
        pygame.draw.rect(WINDOW, WHITE, bullet)


def game():
    PLAYER = pygame.Rect(WINDOW.get_width() // 2 - 50 // 2, 530, 70, 70)
    # game loop, this loop runs as long as you want your game to run
    clock = pygame.time.Clock() # slows the loop down

     # made once
    makeEnemies()
    direction = -2 

    score = 0
    score_text = GAME_FONT.render('Score: ' + str(score), 1, RED)

    running = True
    
    while running:
        clock.tick(30) # 60 FPS

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
            # print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    BULLETS.append(pygame.Rect(PLAYER.x + 35, 530, 5, 10))
            v = random.randint(0, 10)
            if v == 1:
                x = random.randint(ENEMYPOS[0]// 1, ENEMYPOS[2]// 1)
                ENEMYBULLETS.append(pygame.Rect(x, 90, 5, 10))
            
                   
            if event.type == ENEMY_HIT: 
                score += 1  
            if event.type == PLAYER_HIT: 
                score -= 1 


        WINDOW.fill(MYCOLOR)
        # all items you want to see on the window go here
        score_text = GAME_FONT.render('Score: ' + str(score), 1, RED)
        WINDOW.blit(score_text, (10, 10))

        if score >= 3: 
            you_win = GAME_FONT.render('YOU WIN', 1, RED)
            WINDOW.blit(you_win, (225, 250))
        if score <= -4: 
            you_loose = GAME_FONT.render('YOU LOOSE', 1, RED)
            WINDOW.blit(you_loose, (225, 250))
            
        if event.type == PLAYER_HIT: 
            you_loose = GAME_FONT.render('YOU LOOSE', 1, RED)
            WINDOW.blit(you_loose, (225, 250))

        
        playerControl(PLAYER) # runs lots of times
        bulletControl()
        enemyBulletControl(PLAYER)
        direction = enemiesControl(direction)
        enemyBulletControl(PLAYER)
        # the following line is the last in of code in while loop
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    game()
    pygame.quit()
