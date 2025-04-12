class Cinna(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
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

        if moving_left:
            dx = -self.speed
            self.flip = False  # Flip the sprite when moving left
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = True  # Don't flip the sprite when moving right
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

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

# Player
player = Cinna('player', 200, 600, 0.5, 5)  # Reduce scale to 0.5


# Game loop
run = True
while run:
    clock.tick(FPS)
    draw_bg()

    player.update_animation()
    player.move(moving_left, moving_right)
    player.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                player.jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()