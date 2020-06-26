import pygame, sys, math, random

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

scWidth = 800
scHeight = 600
screen = pygame.display.set_mode((scWidth, scHeight))

run = True

class Lander(object):
    def __init__(self, parent_surface, x, y, width, height):
        self.x = x
        self.y = y
        self.parent = parent_surface
        self.width = width
        self.height = height
        self.color = (212, 212, 212)
        self.flame_color = (255, 0, 0)
        self.vel_x = 0
        self.vel_y = 0
        self.thrust = 0
        self.rotate = 90
        self.gas = 100
        self.left = False
        self.right = False
        self.thrust_on = False
        self.offset_x = 12
        self.offset_y = 12
        self.gravity = .08

    def rot_center(self):
        """rotate an image while keeping its center and size"""
        orig_rect = self.parent.get_rect()
        rot_image = pygame.transform.rotate(self.parent, self.rotate - 90)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def movement(self):
        if self.rotate >= 360 or self.rotate <= -360:
            self.rotate = 0
        if self.thrust > 0:
            self.thrust = 0
        if self.thrust < -10:
            self.thrust = -10
        x = -1 * (math.cos(math.radians(self.rotate)) * self.thrust)
        y = (math.sin(math.radians(self.rotate)) * self.thrust)
        #print(f"X = {x}, Y = {y}, ANG = {self.rotate}, THRUST = {self.thrust}")
        #print("-----------------")
        self.x += self.vel_x + x
        self.vel_y += self.gravity + y + self.thrust
        self.y += self.vel_y

    def draw_console(self, screen):
        #gas gauge
        pygame.draw.rect(screen, (255, 0, 0), (scWidth - 120, 15, 100, 20))
        pygame.draw.rect(screen, (0, 255, 0), (scWidth - 120, 15, self.gas, 20))

        #thrust gauge
        pygame.draw.rect(screen, (190, 190, 190), (scWidth - 30, 150, 10, 100))
        pygame.draw.rect(screen, (150, 190, 190), (scWidth - 40, 250 + (self.thrust * 1000), 30, 10))

        #Lateral Veolcity
        #Vertial Velocity
        #Distance to Ground

    def draw(self, screen):
        self.movement()

        xy1 = (self.offset_x + 8, self.offset_y + self.height)
        xy2 = (self.offset_x + self.width - 8, self.offset_y + self.height)
        xy3 = ((self.offset_x + self.width/2), self.offset_y + self.height - 1 - (self.thrust*100) )

        pygame.draw.rect(self.parent, self.color, (self.offset_x, self.offset_y, self.width, self.height)) #lander drawing
        pygame.draw.polygon(self.parent, self.flame_color, [xy1, xy2, xy3] )
        new_parent = self.rot_center() #pygame.transform.rotate(self.parent, self.rotate - 90)
        screen.blit(new_parent, (self.x, self.y))

class DisplayTextObject(object):
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.color = (0, 0, 0)

    def draw(self):
        text_object = pygame.font.SysFont('Arial', 16)
        text_object = text_object.render(self.text, True, self.color)
        screen.blit(text_object, (self.x, self.y))

class World(object):
    def __init__(self, width, height, obstacles):
        self.width = width #whole field
        self.height = height #whole field
        self.ground_height = 75
        self.obstacles = obstacles
        self.bg_color = (0,0,0)
        self.color1 = (230, 225, 235)
        self.color2 = (215, 225, 230)
        self.color3 = (200, 200, 200)
        #self.goal = [(x, y), (x, y)] #Needs further defining

    def clr_slct(self):
        clr_list = (self.color1, self.color2, self.color3)
        randNum = random.randint(0,3)
        return clr_list[randNum]

    def draw(self, screen):
        #draw ground
        pygame.draw.rect(screen, self.color1, (0, self.height - self.ground_height, self.width, self.ground_height))
        pass

surface = pygame.Surface((56, 56)) #parent surface for lander
surface.fill((255, 255, 255))
lander = Lander(surface, 100, 100, 32, 32)

#levels
level1 = World(800, 600, 0)

def text_objects():
    sampleText = DisplayTextObject(scWidth - 40, 280, str(lander.thrust * -100))
    sampleText.draw()


def redrawGameWindow():
    screen.fill((255,255,255))
    level1.draw(screen)
    lander.draw(screen)
    lander.draw_console(screen)
    text_objects()
    pygame.display.update()


while run:
    clock.tick(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    keys = pygame.key.get_pressed()

    lander.gas -= abs(lander.thrust/15)

    mouse = pygame.mouse.get_pressed() # (True, False, False)
    pos = pygame.mouse.get_pos()

    box = (100, 100, 100, 50)
    #      x     y   width height
    # if pos[0] >= box[0] and pos[14] <= box[0] + box[2]:
    #     if [pos[1] >= box[1] and pos[1] <= (pos[1] + box[3]):
    #         if mouse[0]:
    #             print("Big Fart")


    if keys[pygame.K_LEFT]:
        lander.vel_x -= .01
        lander.left = True
        lander.gas -= .02
    if keys[pygame.K_RIGHT]:
        lander.vel_x += .01
        lander.right = True
        lander.gas -= .02
    if keys[pygame.K_UP]:
        lander.thrust -= .0012
        lander.thrust_on: True
    if keys[pygame.K_DOWN]:
        if lander.thrust < 0:
            lander.thrust += .0012
    if keys[pygame.K_a]:
        lander.rotate += .8
        lander.gas -=.01
    if keys[pygame.K_d]:
        lander.rotate -= .8
        lander.gas -=.01
    if lander.thrust <= -10:
        lander.thrust = -10
    else:
        lander.thrust_on = False
    redrawGameWindow()
