import os
import pygame
import random
import time
 
 
class Settings:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    FPS = 60
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")
 
 
class Moving:
    def __init__(self, image_file, x, y, speedx, speedy, scale_size):
        image_path = os.path.join(Settings.IMAGE_PATH, image_file)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file '{image_file}' not found at {Settings.IMAGE_PATH}")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, scale_size)  
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speedx = speedx
        self.speedy = speedy
 
    def update(self):
        self.rect = self.rect.move(self.speedx, self.speedy)        
        if self.rect.left < 0 or self.rect.right > Settings.WINDOW_WIDTH:
            self.speedx *= -1
        if self.rect.top < 0 or self.rect.bottom > Settings.WINDOW_HEIGHT:
            self.speedy *= -1
 
    def draw(self, screen):
        screen.blit(self.image, self.rect)
 
 
def create_ball():
    x = random.randint(0, 100)  
    y = random.randint(0, 100)  
    speedx = random.choice([-3, -2, 2, 3])  
    speedy = random.choice([-3, -2, 2, 3])  
    return Moving("ball.png", x, y, speedx, speedy, (50, 50))  
 
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Moving Objects Example")
    clock = pygame.time.Clock()
 
    background_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "background2.jpg")).convert()
    background_image = pygame.transform.scale(background_image, (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
 
 
    obstacles = [
        Moving("bird01.png", 250, 50, 0, 0, (50, 50)),
        Moving("car01.png", 600, 200, 0, 0, (70, 40)),      
        Moving("regenschirm01.png", 400, 300, 0, 0, (80, 60)),  
        Moving("Ballon.png", 700, 100, 0, 0, (60, 60)),  
        Moving("stone01.png", 200, 200, 0, 0, (60, 50)),  
    ]
 
    balls = []
    last_ball_time = time.time()
 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
 
        if time.time() - last_ball_time > 2:  
            balls.append(create_ball())  
            last_ball_time = time.time()  
 
       
        for ball in balls[:]:
            ball.update()
 
            for obstacle in obstacles[:]:  
                if ball.rect.colliderect(obstacle.rect):
                    balls.remove(ball)  
                    obstacles.remove(obstacle)  
                    break  
 
        screen.blit(background_image, (0, 0))
        for obj in obstacles:
            obj.draw(screen)
        for ball in balls:
            ball.draw(screen)
 
        pygame.display.flip()
        clock.tick(Settings.FPS)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()