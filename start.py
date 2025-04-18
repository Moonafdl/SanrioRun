import pygame
import os
import csv

pygame.init()

# Screen setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sanrio Run')

# Frame rate
clock = pygame.time.Clock()
FPS = 60

# Game variables
GRAVITY = 0.75
moving_left = False
moving_right = False
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 1

# Load images 
# Store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'image/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# Colors
PINK = (255, 192, 203)
WHITE = (255, 255, 255)

# Function to draw background
def draw_bg():
    screen.fill(PINK)
    pygame.draw.rect(screen, WHITE, pygame.Rect(0, 640, SCREEN_WIDTH, 80))


class Cinna(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = False  # Start on the ground
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # Load walk1.png to walk8.png
        for i in range(1, 9):
            img = pygame.image.load(f'image/char/Walk/walk{i}.png').convert_alpha()

            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        # Handle horizontal movement
        if moving_left:
            dx = -self.speed
            self.flip = False
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = True
            self.direction = 1

        # Handle jumping
        if self.jump and not self.in_air:
            self.vel_y = -11  # Jump strength
            self.jump = False
            self.in_air = True

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10  # Prevent falling too fast

        dy += self.vel_y

        # Prevent falling below ground level
        if self.rect.bottom + dy > 640:
            dy = 640 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        if moving_left or moving_right:
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                if self.frame_index >= len(self.animation_list):
                    self.frame_index = 0
                self.image = self.animation_list[self.frame_index]
        else:
            self.frame_index = 0
            self.image = self.animation_list[self.frame_index]

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        # Iterate through each value in level data file 
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(decoration)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:    # cretae player     
                        player = Cinna('player', 200, 600, 1.65, 5)
                    elif tile == 16: #Create enemy
                        enemy = Cinna('player', 200, 600, 1.65, 5)
                    # elif tile == 19: # create health box
                    elif tile == 20:    # create exit 
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(decoration)

        return player

    def draw(self):
        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
                    

# Create empty tile list 
world_data = []
for row in range(ROWS):
    r = [-1] * COLS 
    world_data.append(r)

# Load in level data and create world
with open(f'level{level}_data.csv', newline = '') as csvfile:
    reader =  csv.reader(csvfile, delimiter = ',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
player = world.process_data(world_data)

# Game loop
run = True
while run:
    clock.tick(FPS)

    # Update Backgroup
    draw_bg()

    # draw world map
    world.draw()

    player.update_animation()
    player.move(moving_left, moving_right)
    player.draw()

    # update and draw groups 
    decoration_group.update()
    water_group.update()
    exit_group.update()
    decoration_group.draw(screen)
    water_group.draw(screen)
    exit_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:  
                if not player.in_air:  # Check if the player is on the ground
                    player.jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()
