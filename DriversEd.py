import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set the size of the window
screen = pygame.display.set_mode((950, 750))

# Set the title of the window
pygame.display.set_caption("DriversEd")

#game music
soundObj = pygame.mixer.Sound("song1.mp3")
soundObj.play()

# set timer
FONT = pygame.font.SysFont("Sans", 30)
TEXT_COLOR = (0, 0, 0)
start_time = pygame.time.get_ticks()

class game_start:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("title.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

class start_button:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("start_button.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

class Grass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("grass.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

class Instruction:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("diagram.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

class Intersection:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("FinalIntersection.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
class Sign:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("stop_sign.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

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
        if keys[pygame.K_1]:
            game_over()
            
#start screen
start = game_start(500,375)
#start button
startButton = start_button(500,500)
# vertical intersection
intersection = Intersection(490, 350)
# horizontal interesection
intersection1 = Intersection(39, 774)
intersection1.image = pygame.transform.rotate(intersection1.image, 90)
#stop sign that player's car approaches
sign = Sign(530, 425)
# stop sign to right of player
sign2 = Sign(530, 320)
sign2.image = pygame.transform.rotate(sign2.image, 90)
# stop sign opposite of player
sign3 = Sign(420, 300)
sign3.image = pygame.transform.rotate(sign3.image, 180)
# stop sign to left of player
sign4 = Sign(400, 430)
sign4.image = pygame.transform.rotate(sign4.image, 270)

clock = pygame.time.Clock()
num = random.randint(0,2)

screen.blit(start.image, start.rect)
screen.blit(startButton.image, startButton.rect)
pygame.display.flip()

def first_level():
    player_car = Car(503, 710)
    while True:
        clock.tick(50)
        pygame.event.pump()
        screen.fill((0, 255, 0))
        screen.blit(intersection.image, intersection.rect)
        screen.blit(intersection1.image, intersection1.rect)
        instructions(num)
        screen.blit(player_car.image, player_car.rect)
        player_car.handle_keys()
        player_car.update()
                
        screen.blit(sign.image, sign.rect)
        screen.blit(sign2.image, sign2.rect)
        screen.blit(sign3.image, sign3.rect)
        screen.blit(sign4.image, sign4.rect)
        # checks if player crosses a certain point on map, can be used to translate to level two
        # num is a random number that refers to the instructions function that generates which way the user should go 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if player_car.rect.left < 50 and num == 0:
            print("leftworks")
        elif player_car.rect.left > 850 and num == 1:
            print("rightworks")
        elif player_car.rect.top < 0 and num == 2:
            print("straightworks")
        elif start_time:
            time_since_enter = (pygame.time.get_ticks() - start_time) / 1000
            message = 'Timer: ' + str(time_since_enter) + ' seconds'
            screen.blit(FONT.render(message, True, TEXT_COLOR), (20, 20))
        pygame.display.flip()
        

def instructions(num):
    message = ["Make a left turn", "Make a right turn", "Go straight"]
    screen.blit(FONT.render(message[num], True, "black"), (20, 50))
    diagram = Instruction(120, 165)
    screen.blit(diagram.image, diagram.rect)

def game_over():
    grey_list = ['grey1', 'grey2', 'grey3', 'grey4', 'grey5', 'grey6', 'grey7', 'grey8', 'grey9', 'grey10',
          'grey11', 'grey12', 'grey13', 'grey14', 'grey15', 'grey16', 'grey17', 'grey18', 'grey19',
          'grey20', 'grey21', 'grey22', 'grey23', 'grey24', 'grey25', 'grey26', 'grey27', 'grey28',
          'grey29', 'grey30', 'grey31', 'grey32', 'grey33', 'grey34', 'grey35', 'grey36', 'grey37',
          'grey38', 'grey39', 'grey40', 'grey42', 'grey43', 'grey44', 'grey45', 'grey46', 'grey47',
          'grey48', 'grey49', 'grey50', 'grey51', 'grey52', 'grey53', 'grey54', 'grey55', 'grey56',
          'grey57', 'grey58', 'grey59', 'grey60', 'grey61', 'grey62', 'grey63', 'grey64', 'grey65',
          'grey66', 'grey67', 'grey68', 'grey69', 'grey70', 'grey71', 'grey72', 'grey73', 'grey74',
          'grey75', 'grey76', 'grey77', 'grey78', 'grey79', 'grey80', 'grey81', 'grey82', 'grey83',
          'grey84', 'grey85', 'grey86', 'grey87', 'grey88', 'grey89', 'grey90', 'grey91', 'grey92',
          'grey93', 'grey94', 'grey95', 'grey97', 'grey98', 'grey99']
    for i in range(95, -1, -1):
        pygame.draw.rect(screen, grey_list[i], pygame.Rect(0,0, screen.get_size()[0], screen.get_size()[1]))
        pygame.display.flip()
        pygame.time.delay(10)
    level = 0
    message = ('GAME OVER: Level {} passed'.format(level))
    running = True
    screen.blit(FONT.render(message, True, "white"), (300, 375))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                first_level()
        pygame.display.flip()

running = True
while running:
    #set max frame rate to 70 fps
    clock.tick(50)
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if startButton.rect.collidepoint(mouse_pos):
                first_level() 

pygame.quit()
