import pygame
import sys
import random

pygame.init()

# Screen
screen_width = 412
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball game")

def game_loop():
    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    skyblue = (135, 206, 235)
    red = (255, 0, 0)
    green = (0,255,0)
    gray = (128, 128, 128)

    # Images
    spikes_img = pygame.image.load('gallery/Spikes.png')
    spikes_img_down = pygame.transform.rotate(spikes_img, 180)
    ball_img = pygame.image.load('gallery/ball.png')

    def draw_text(text, color, size, x, y):
        font = pygame.font.Font('gallery/minecraft.otf', size)
        display_text = font.render(text, True, color)
        screen.blit(display_text, (x,y))

    def game_over():
        ball.upspeed = 0
        ball.gravity = 0
        ball.speed = 0

        with open('gallery/Hiscore.txt', 'w') as f:
            f.write(str(hiscore))
            
        draw_text("Game Over!", red, 25, 130, 220)
        draw_text("Press enter to play again", red, 20, 80, 260)

        if keys[pygame.K_RETURN]:
            game_loop()

    # Importing Hiscore
    with open('gallery/Hiscore.txt', 'r') as f:
        hiscore = f.read()

    class Platform():
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            self.hitbox = (self.x, self.y, self.width, self.height)

        def draw(self):
            pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height))
            self.hitbox = (self.x, self.y, self.width, self.height)
            # pygame.draw.rect(screen, green, self.hitbox, 2)

        def move(self):
            self.y -= ball.upspeed

    class Player():
        def __init__(self):
            self.x = 200
            self.y = 100
            self.width = 20
            self.height = 20
            self.speed = 8
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            self.gravity = 6
            self.moving = True
            self.upspeed = 6
            # self.stop = False

        def draw(self):
            screen.blit(ball_img, (self.x, self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)
            # pygame.draw.rect(screen, green, self.hitbox, 2)

        def move(self):
            if keys[pygame.K_LEFT]:
                self.x -= self.speed

            if keys[pygame.K_RIGHT]:
                self.x += self.speed

        
            self.y += self.gravity

        def stop(self):
            self.gravity = 0
            self.y -= self.upspeed
            
    # Some more Global Variables
    clock = pygame.time.Clock()
    fps = 30
    platform1_count = 0
    platform2_count = 0
    platform3_count = 0
    platforms = []
    keys = pygame.key.get_pressed()
    ball = Player()
    score = 0
    over = False

    # Gameloop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Generating Platform No. 1 at some distance
        platform1_count += 1
        if platform1_count > random.randint(40,80):
            platforms.append(Platform(30, screen_height + random.randint(90, 150), 80, 10))
            platform1_count = 0

        # Generating Platform No. 2 at some distance
        platform2_count += 1
        if platform2_count > random.randint(40,90):
            platforms.append(Platform(160, screen_height, 80, 10))
            platform2_count = 0

        # Generating Platform No. 3 at some distance
        platform3_count += 1
        if platform3_count > random.randint(40,70):
            platforms.append(Platform(screen_width - 70 - 40, screen_height + random.randint(100, 200), 80, 10))
            platform3_count = 0

        # Making Boundaries
        if ball.x <= 0:
            ball.x = 0

        if ball.x >= screen_width - ball.width:
            ball.x = screen_width - ball.width

        # if ball.y >= screen_height - ball.height:
        #     ball.y = screen_height - ball.height

        # Making ball rest on the Platform
        for platform in platforms:
            if ball.hitbox[0] + ball.hitbox[3] > platform.hitbox[0] and ball.hitbox[0] < platform.hitbox[0] + platform.hitbox[2]:
                if ball.hitbox[1] + ball.hitbox[3] >= platform.hitbox[1] and ball.hitbox[1] + ball.hitbox[3] <= platform.hitbox[1] + platform.hitbox[3]:
                    # print(244)
                    ball.stop()

                    if not ball.stop():
                        ball.gravity = 6

        # Collison of ball width spikes 
        if ball.y <= 25+32:
            ball.y = 25+25
            over = True

        if ball.y >= screen_height-ball.height-32:
            ball.y = screen_height-ball.height-32
            over = True

        # Increasing Score
        if not over:
            score += 1

        # Increasing Hiscore
        if score > int(hiscore):
            hiscore = score

        # Background Color
        screen.fill(skyblue)

        # Displaying and Moving Platform
        for platform in platforms:
            platform.draw()
            platform.move()

        # Displaying Spikes image    
        screen.blit(spikes_img, (0, 25))
        screen.blit(spikes_img_down, (0, screen_height-32))

        # Displaying and Moving Ball image
        ball.draw()
        keys = pygame.key.get_pressed()
        ball.move()

        # Displaying Score and Hiscore
        pygame.draw.rect(screen, gray, (0, 0, screen_width, 25))
        draw_text("Score : "+str(score)+"  Hiscore : "+str(hiscore), white, 20, 20, 5)

        # game over and restart
        if over:
            game_over()

        # Frame Rates
        clock.tick(fps)

        # Updating Everything
        pygame.display.update()

game_loop()