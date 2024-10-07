import pygame
import random

pygame.init()
width = 800
height = 600
font = pygame.font.SysFont(None,30)
space_img = pygame.image.load('./player.png')
enemy_img = pygame.image.load('./enemy.png')
playerWidth = 100
playerHeight = 90
enemyWidth = 60
enemyHeight = 50
playerSpeed = 3
enemySpeed = 3
bulletSpeed = 20
WHITE = (255,255,255)
BLACK = (0,0,0)
spaceImg = pygame.transform.rotate(pygame.transform.scale(space_img, (playerWidth,playerHeight)), -90)
enemyImg = pygame.transform.rotate(pygame.transform.scale(enemy_img, (enemyWidth,enemyHeight)), 90)
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Shooter")

def drawPlayer(x,y):
    win.blit(spaceImg, (x,y))

def drawEnemy(x,y):
    win.blit(enemyImg, (x,y))

def drawBullet(x,y):
    pygame.draw.rect(win, WHITE, [x,y,10,3])

def scoreD(score):
    text = font.render(f"Score : {str(score)}", True, WHITE)
    win.blit(text,(10,10))

def main():
    playerX = (width - playerWidth) / 4
    playerY = (height - playerHeight) / 2
    bulletX = 0
    bulletY = 0
    score = 0
    life = 3
    bullet_state = "ready"
    enemies = []
    spawnTime = 0
    enemySpawnD = 300
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and playerY - playerSpeed > 0:
            playerY -= playerSpeed
        if keys[pygame.K_DOWN] and playerY < height - playerHeight:
            playerY += playerSpeed
        if keys[pygame.K_LEFT] and playerX - playerSpeed > 0:
            playerX -= playerSpeed
        if keys[pygame.K_RIGHT] and playerX < width / 2 - playerWidth:
            playerX += playerSpeed
        if keys[pygame.K_LSHIFT] and bullet_state == "ready":
            bullet_state = "fire"
            bulletX = playerX + playerWidth
            bulletY = playerY + playerWidth / 2
        win.fill(BLACK)
        pygame.draw.rect(win,WHITE,[width//2-4,0,20,height])
        drawPlayer(playerX,playerY)
        for enemy in enemies:
            drawEnemy(enemy["x"],enemy["y"])
            if enemy["move_direction"] == "down":
                if enemy["y"] < height - enemyHeight:
                    enemy["y"] += enemySpeed
                else:
                    enemy["move_direction"] = "up"
            elif enemy["move_direction"] == "up":
                if enemy["y"] > 0:
                    enemy["y"] -= enemySpeed
                else:
                    enemy["move_direction"] = "down"
            
            if enemy["bullet_state"] == "ready":
                enemy["bullet_state"] = "fire"
                enemy["bulletX"] = enemy["x"] - 10
                enemy["bulletY"] = enemy["y"] + enemyHeight / 2
            
            if enemy["bullet_state"] == "fire":
                drawBullet(enemy["bulletX"],enemy["bulletY"])
                enemy["bulletX"] -=  bulletSpeed
                if enemy["bulletX"] <= playerX + playerWidth and enemy["bulletX"] >= playerX and enemy["bulletY"] >= playerY and enemy["bulletY"] <= playerY + playerHeight:
                    life -= 1
                    enemy["bullet_state"] = "ready"
                    if life == 0:
                        run = False
                    else:
                        playerX = (width - playerWidth) / 4
                        playerY = (height - playerHeight) / 2
        if bullet_state == "fire":
            drawBullet(bulletX,bulletY)
            bulletX += bulletSpeed
            enemy["bullet_state"] = "ready"

            for enemy in enemies:
                if bulletX >= enemy["x"] and bulletX <= enemy["x"] + enemyWidth and bulletY >= enemy["y"] and bulletY <= enemy["y"] + enemyHeight:
                    score += 1
                    bullet_state = "ready"
                    enemies.remove(enemy)
            if bulletX >= width:
                bullet_state = "ready"
        
        scoreD(score)
        lifeT = font.render(f"Life : {str(life)}", True, WHITE)
        win.blit(lifeT, (10,40))
        def spawnEnemy():
            enemyX = (width - enemyWidth) * 3 / 4
            enemyY = random.randint(0,height-enemyHeight)
            enemy_move_direction = "down" if random.randint(0,1) == 0 else "up"
            enemies.append({"x":enemyX,"y":enemyY,"move_direction":enemy_move_direction,"bullet_state":"ready","bulletX":0,"bulletY":0})
        spawnTime += 2
        if spawnTime >= enemySpawnD:
            spawnTime = 0
            spawnEnemy()
        pygame.display.update()
        pygame.time.Clock().tick(60)
    pygame.quit()
    quit()

main()