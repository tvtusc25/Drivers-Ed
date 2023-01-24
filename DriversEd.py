import pygame
import math

# Initialize Pygame
pygame.init()

# Set the size of the window
screen = pygame.display.set_mode((950, 750))

#Game Over Messages
game_over_mess = ["Failure to Stop", "Failure to Follow Instructions", "Failure to Maintain Lane", "Failure to Use Turn Signal", "You Crashed"]
game_over_code = 0

# Set the title of the window
pygame.display.set_caption("Driver's Ed")

#game music
soundObj = pygame.mixer.Sound("song1.mp3")
soundObj.set_volume(0.1)
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

class Instruction:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("diagram.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
class Background:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("background.png")
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
        self.turnSound = pygame.mixer.Sound("turnsignal.mp3")
        self.startSound = pygame.mixer.Sound("carstarting.mp3")
        

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    self.current_image = self.turn_left_image
                    self.image = pygame.transform.rotate(self.current_image, self.angle)
                    self.rect = self.image.get_rect(center=(self.x, self.y))
                    self.turnSound.play()
                if event.key == pygame.K_e:
                    self.current_image = self.turn_right_image
                    self.image = pygame.transform.rotate(self.turn_right_image, self.angle)
                    self.rect = self.image.get_rect(center=(self.x, self.y))
                    self.turnSound.set_volume(1)
                    self.turnSound.play()
                if event.key == pygame.K_UP:
                    self.startSound.set_volume(0.1)
                    self.startSound.play()
class AIcar:
    def __init__(self, speed, waypoints, imgAngle, loop = False):
        self.original_image = pygame.image.load("car.png")
        self.turn_left_image = pygame.image.load("car_light_left.png")
        self.turn_right_image = pygame.image.load("car_light_right.png")
        self.image = self.original_image.copy()
        self.current_image = self.image
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.current_image, imgAngle)
        self.loop = loop
        self.counter = 0
        #SUBJECT TO CHANGE - could be a constant across all AICars
        self.speed = speed
        self.waypoints = waypoints
        self.next_point = 0
        self.current = pygame.math.Vector2(self.waypoints[0])
        self.rect.center = self.current
        #Sets end point if exists on list
        self.tindex = 1
        if self.tindex < len(self.waypoints) - 1:
            self.target = pygame.math.Vector2(self.waypoints[self.tindex])
            self.moving = True
        else:
            self.target = self.current
            self.moving = False

    def move(self):
        if self.moving:
            distance = self.current.distance_to(self.target)
            if distance > self.speed:
                self.current = self.current+(self.target-self.current).normalize()*self.speed
                self.rect.center = self.current
            else:
                #Moves car to target and get new target from waypoints
                self.current = self.target
                self.rect.center = self.current
                #Set next end point if exists on list
                self.tindex += 1
                if self.tindex < len(self.waypoints):
                    self.target = pygame.math.Vector2(self.waypoints[self.tindex])
                else:
                    if self.loop:
                        self.tindex = 0
                    else:
                        self.moving = False

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
        pygame.time.delay(20)
    message = ('GAME OVER: Level {} Failed'.format(level))
    screen.blit(FONT.render(message, True, "white"), (375, 375))
    reason = game_over_mess[code]
    screen.blit(FONT.render(reason, True, "white"), (375, 400))
    pygame.display.flip()
    pygame.time.delay(3000)
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
        #blit background
        screen.blit(background.image, background.rect)
        #go straight instruction
        instructions(2)
        #blit car and update
        player_car.handle_keys()
        player_car.update()
        screen.blit(player_car.image, player_car.rect)
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
    waypoints = [(-100, 385), (400, 385), (1100, 385)]
    aiCar = AIcar(2, waypoints, 0, False)
    while True:
        clock.tick(50)
        pygame.event.pump()
        #blit fail zones
        screen.blit(stop.image, stop.rect)
        screen.blit(fail1.image, fail1.rect)
        screen.blit(fail2.image, fail2.rect)
        screen.blit(fail3.image, fail3.rect)
        screen.blit(fail4.image, fail4.rect)
        #blit background
        screen.blit(background.image, background.rect)
        screen.blit(aiCar.image, aiCar.rect)
        instructions(0)
        pauseTime = 10
        if((330 > aiCar.current[0] or aiCar.current[0] > 360) or aiCar.counter >= pauseTime):
            aiCar.move()
        if(330 <= aiCar.current[0] and aiCar.current[0] <= 360 and aiCar.counter < pauseTime):
            aiCar.counter += 1
            aiCar.waypoints.append((355,385))
        if(aiCar.counter == pauseTime - 1):
            aiCar.waypoints = [(400,385), (1100, 385), (1200, 385)]
        player_car.handle_keys()
        player_car.update()
        screen.blit(player_car.image, player_car.rect)
        # checks if player crosses a certain point on map, can be used to translate to level two
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
        if player_car.rect.colliderect(aiCar.rect):
            game_over(4, 2)
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
        screen.blit(background.image, background.rect)
        instructions(1)
        player_car.handle_keys()
        player_car.update()
        screen.blit(player_car.image, player_car.rect)
        # checks if player crosses a certain point on map, can be used to translate to level two
        keys = pygame.key.get_pressed()
        if player_car.speed > 0.1 or player_car.speed < -0.1:
            if keys[pygame.K_LEFT]:
                if player_car.current_image != player_car.turn_left_image:
                    game_over(3,1)
            if keys[pygame.K_RIGHT]:
                if player_car.current_image != player_car.turn_right_image:
                    game_over(3,1)
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
            screen.blit(FONT.render(message, True, "black"), (20, 20))
        pygame.display.flip()
 
#start screen
start = game_start(475,375)
#start button
startButton = start_button(475,450)
#background
background = Background(475,375)
#fail zones
fail1 = Red_Zone(190,110)
fail2 = Red_Zone(800,110)
fail3 = Red_Zone(160,580)
fail4 = Red_Zone(820,580)
#stop zone
stop = Stop_Zone(500,500)
#clock
clock = pygame.time.Clock()
#start game screen
start_screen()
#quit sequence
pygame.quit()
