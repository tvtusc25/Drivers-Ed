import pygame
import math

# Initialize Pygame
pygame.init()

# Set the size of the window
screen = pygame.display.set_mode((950, 750))

#Game Over Messages
game_over_mess = ["Failure to Stop", "Failure to Follow Instructions", "Failure to Maintain Lane", "Failure to Use Turn Signal"]
game_over_code = 0

# Set the title of the window
pygame.display.set_caption("Driver's Ed")

#game music
soundObj = pygame.mixer.Sound("song1.mp3")
soundObj.play()

# set font
FONT = pygame.font.SysFont("Arial", 20)
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
        
class Red_Zone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("fail.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
class Stop_Zone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("stop.png")
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
            
def instructions(num):
    message = ["Stop, Turn-Signal, and Make a Left Turn", "Stop, Turn-Signal, and Make a Right Turn", "Stop and Go Straight"]
    screen.blit(FONT.render(message[num], True, "black"), (20, 50))
    diagram = Instruction(120, 650)
    screen.blit(diagram.image, diagram.rect)

def start_screen():
    while True:
        screen.blit(start.image, start.rect)
        screen.blit(startButton.image, startButton.rect)
        pygame.display.flip()
        clock.tick(50)
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if startButton.rect.collidepoint(pygame.mouse.get_pos()):
                startButton.image = pygame.image.load("start_button2.png")
            else:
                startButton.image = pygame.image.load("start_button.png")
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if startButton.rect.collidepoint(mouse_pos):
                    first_level()

def game_over(code, level):
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
    message = ('GAME OVER: Level {} Failed'.format(level))
    screen.blit(FONT.render(message, True, "white"), (375, 375))
    reason = game_over_mess[code]
    screen.blit(FONT.render(reason, True, "white"), (375, 400))
    pygame.display.flip()
    pygame.time.delay(1000)
    start_screen()

def win(time):
    green_list = ['green4', 'green3', 'green2', 'green1']
    for i in range(4):
        pygame.draw.rect(screen, green_list[i], pygame.Rect(0,0, screen.get_size()[0], screen.get_size()[1]))
        pygame.display.flip()
        pygame.time.delay(10)
    message = ('PASSED: In {} Seconds'.format(time))
    screen.blit(FONT.render(message, True, "white"), (375, 375))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()

def first_level():
    #stop/zone flag
    stopped = False
    in_zone = False
    player_car = Car(503, 710)
    while True:
        #frame rate is 50
        clock.tick(50)
        pygame.event.pump()
        #blit fail zones
        screen.blit(stop.image, stop.rect)
        screen.blit(fail1.image, fail1.rect)
        screen.blit(fail2.image, fail2.rect)
        screen.blit(fail3.image, fail3.rect)
        screen.blit(fail4.image, fail4.rect)
        screen.fill((0, 255, 0))
        #blit intersections
        screen.blit(intersection.image, intersection.rect)
        screen.blit(intersection1.image, intersection1.rect)
        #go straight instruction
        instructions(2)
        #blit car and update
        screen.blit(player_car.image, player_car.rect)
        player_car.handle_keys()
        player_car.update()
        #blit sign
        screen.blit(sign.image, sign.rect)
        # checks if player crosses a certain point on map, can be used to translate to level two
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            if player_car.speed > 0.1 or player_car.speed < -0.1:
                if keys[pygame.K_LEFT]:
                    if player_car.current_image != player_car.turn_left_image:
                        game_over(3,1)
                if keys[pygame.K_RIGHT]:
                    if player_car.current_image != player_car.turn_right_image:
                        game_over(3,1)
        #road direction win/lose
        if player_car.rect.top < 0:
            second_level()
        elif player_car.rect.left > 850:
            game_over(1, 1)
        elif player_car.rect.left < 50:
            game_over(1, 1)
        #collisions
        if player_car.rect.colliderect(fail1.rect) or player_car.rect.colliderect(fail2.rect) or player_car.rect.colliderect(fail3.rect) or player_car.rect.colliderect(fail4.rect):
            game_over(2, 1)
        # check if car is in zone
        if player_car.rect.colliderect(stop.rect) and not in_zone:
            in_zone = True
        # check if car has left zone without stopping
        elif not player_car.rect.colliderect(stop.rect) and in_zone and not stopped:
            # car has left zone without stopping, game over
            game_over(0, 1)
        if not stopped:
            if player_car.rect.colliderect(stop.rect):
                if player_car.speed < 0.1 and player_car.speed > -0.1:
                    stopped = True
        if start_time:
            time_since_enter = (pygame.time.get_ticks() - start_time) / 1000
            message = 'Timer: ' + str(time_since_enter) + ' seconds'
            screen.blit(FONT.render(message, True, TEXT_COLOR), (20, 20))
        pygame.display.flip()

def second_level():
    #stop/zone flag
    stopped = False
    in_zone = False
    player_car = Car(503, 710)
    while True:
        clock.tick(50)
        pygame.event.pump()
        #blit fail zones
        screen.blit(stop.image, stop.rect)
        screen.blit(fail1.image, fail1.rect)
        screen.blit(fail2.image, fail2.rect)
        screen.blit(fail3.image, fail3.rect)
        screen.blit(fail4.image, fail4.rect)
        screen.fill((0, 255, 0))
        screen.blit(intersection.image, intersection.rect)
        screen.blit(intersection1.image, intersection1.rect)
        instructions(0)
        screen.blit(player_car.image, player_car.rect)
        player_car.handle_keys()
        player_car.update()
        screen.blit(sign.image, sign.rect)
        # checks if player crosses a certain point on map, can be used to translate to level two
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            if player_car.speed > 0.1 or player_car.speed < -0.1:
                if keys[pygame.K_LEFT]:
                    if player_car.current_image != player_car.turn_left_image:
                        game_over(3,2)
                if keys[pygame.K_RIGHT]:
                    if player_car.current_image != player_car.turn_right_image:
                        game_over(3,2)
        if player_car.rect.left < 50:
            third_level()
        elif player_car.rect.left > 850:
            game_over(1, 2)
        elif player_car.rect.top < 0:
            game_over(1, 2)
        if player_car.rect.colliderect(fail1.rect) or player_car.rect.colliderect(fail2.rect) or player_car.rect.colliderect(fail3.rect) or player_car.rect.colliderect(fail4.rect):
            game_over(2, 2)
        # check if car is in zone
        if player_car.rect.colliderect(stop.rect) and not in_zone:
            in_zone = True
        # check if car has left zone without stopping
        elif not player_car.rect.colliderect(stop.rect) and in_zone and not stopped:
            # car has left zone without stopping, game over
            game_over(0, 2)
        if not stopped:
            if player_car.rect.colliderect(stop.rect):
                if player_car.speed < 0.1 and player_car.speed > -0.1:
                    stopped = True
        if start_time:
            time_since_enter = (pygame.time.get_ticks() - start_time) / 1000
            message = 'Timer: ' + str(time_since_enter) + ' seconds'
            screen.blit(FONT.render(message, True, TEXT_COLOR), (20, 20))
        pygame.display.flip()
        
def third_level():
    #stop/zone flag
    stopped = False
    in_zone = False
    player_car = Car(503, 710)
    time = 0
    while True:
        clock.tick(50)
        pygame.event.pump()
        #blit fail zones
        screen.blit(stop.image, stop.rect)
        screen.blit(fail1.image, fail1.rect)
        screen.blit(fail2.image, fail2.rect)
        screen.blit(fail3.image, fail3.rect)
        screen.blit(fail4.image, fail4.rect)
        screen.fill((0, 255, 0))
        screen.blit(intersection.image, intersection.rect)
        screen.blit(intersection1.image, intersection1.rect)
        instructions(1)
        screen.blit(player_car.image, player_car.rect)
        player_car.handle_keys()
        player_car.update()
        screen.blit(sign.image, sign.rect)
        # checks if player crosses a certain point on map, can be used to translate to level two
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            if player_car.speed > 0.1 or player_car.speed < -0.1:
                if keys[pygame.K_LEFT]:
                    if player_car.current_image != player_car.turn_left_image:
                        game_over(3,3)
                if keys[pygame.K_RIGHT]:
                    if player_car.current_image != player_car.turn_right_image:
                        game_over(3,3)
        if player_car.rect.left > 850:
            win(time)
        elif player_car.rect.left < 50:
            game_over(1, 3)
        elif player_car.rect.top < 0:
            game_over(1, 3)
        if player_car.rect.colliderect(fail1.rect) or player_car.rect.colliderect(fail2.rect) or player_car.rect.colliderect(fail3.rect) or player_car.rect.colliderect(fail4.rect):
            game_over(2, 3)
        # check if car is in zone
        if player_car.rect.colliderect(stop.rect) and not in_zone:
            in_zone = True
        # check if car has left zone without stopping
        elif not player_car.rect.colliderect(stop.rect) and in_zone and not stopped:
            # car has left zone without stopping, game over
            game_over(0, 3)
        if not stopped:
            if player_car.rect.colliderect(stop.rect):
                if player_car.speed < 0.1 and player_car.speed > -0.1:
                    stopped = True
        if start_time:
            time_since_enter = (pygame.time.get_ticks() - start_time) / 1000
            message = 'Timer: ' + str(time_since_enter) + ' seconds'
            time = time_since_enter
            screen.blit(FONT.render(message, True, TEXT_COLOR), (20, 20))
        pygame.display.flip()
        
#start screen
start = game_start(475,375)
#start button
startButton = start_button(475,450)
# vertical intersection
intersection = Intersection(490, 350)
# horizontal interesection
intersection1 = Intersection(39, 774)
intersection1.image = pygame.transform.rotate(intersection1.image, 90)
#fail zones
fail1 = Red_Zone(190,110)
fail2 = Red_Zone(800,110)
fail3 = Red_Zone(160,580)
fail4 = Red_Zone(820,580)
#stop sign and zone that player's car approaches
sign = Sign(530, 425)
stop = Stop_Zone(500,500)
#clock
clock = pygame.time.Clock()
#start game screen
start_screen()
#quit sequence
pygame.quit()
