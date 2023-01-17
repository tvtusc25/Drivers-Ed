import pygame
import math

# Initialize Pygame
pygame.init()

# Set the size of the window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Set the title of the window
pygame.display.set_caption("DriversEd")

class Background:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("2lanestreet.png")
        self.rect = self.image.get_rect()

class Car:
    def __init__(self, x, y):
        #initial speed, coords, image, friction, drag
        self.x = x
        self.y = y
        self.speed = 0
        self.angle = 90
        self.friction = 0.05
        self.original_image = pygame.image.load("car.png")
        self.turn_left_image = pygame.image.load("car_light_left.png")
        self.turn_right_image = pygame.image.load("car_light_right.png")
        self.image = self.original_image.copy()
        self.current_image = self.image
        self.rect = self.image.get_rect()

    def update(self):
        #friction
        if self.speed > 0:
            self.speed -= self.friction
        elif self.speed < 0:
            self.speed += self.friction
        self.speed = max(min(self.speed,6),-6)
        #rotation
        self.y += math.sin(math.radians(self.angle)) * (self.speed)
        self.x -= math.cos(math.radians(self.angle)) * (self.speed)
        self.image = pygame.transform.rotate(self.current_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def handle_keys(self):
        #key presses and acceleration/rotation
        keys = pygame.key.get_pressed()
        if self.speed > 0.1 or self.speed < -0.1:
            if keys[pygame.K_LEFT]:
                self.angle += 2.5
            if keys[pygame.K_RIGHT]:
                self.angle -= 2.5
        if keys[pygame.K_UP]:
            self.speed -= 0.2
        if keys[pygame.K_DOWN]:
            self.speed += 0.2
        if keys[pygame.K_w]:
            self.current_image = self.original_image
            self.image = pygame.transform.rotate(self.current_image, self.angle)
            self.rect = self.image.get_rect(center=(self.x, self.y))
        if keys[pygame.K_q]:
            self.current_image = self.turn_left_image
            self.image = pygame.transform.rotate(self.current_image, self.angle)
            self.rect = self.image.get_rect(center=(self.x, self.y))
        if keys[pygame.K_e]:
            self.current_image = self.turn_right_image
            self.image = pygame.transform.rotate(self.turn_right_image, self.angle)
            self.rect = self.image.get_rect(center=(self.x, self.y))

player_car = Car(500, 500)
background = Background(500, 500)

running = True
clock = pygame.time.Clock()

while running:
    #set max frame rate to 60 fps
    clock.tick(60)
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((0, 255, 0))
    screen.blit(background.image, background.rect)

    screen.blit(player_car.image, player_car.rect)
    player_car.handle_keys()
    player_car.update()
    
    pygame.display.flip()

pygame.quit()
