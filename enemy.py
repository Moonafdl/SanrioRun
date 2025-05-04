import pygame
import os

class Enemy(pygame.sprite.Sprite):
    """
    A patrolling enemy that walks back and forth between two x-bounds
    and flips its sprite when changing direction.
    """
    def __init__(self, x, y, left_bound, right_bound, frames, speed=2, anim_cooldown=150):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = speed
        self.direction = 1  # 1 → right, -1 → left
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.anim_cooldown = anim_cooldown

    def update(self):
        # Move horizontally
        self.rect.x += self.speed * self.direction
        # Reverse at patrol bounds
        if self.rect.x < self.left_bound or self.rect.x > self.right_bound:
            self.direction *= -1

        # Animate walk cycle
        now = pygame.time.get_ticks()
        if now - self.update_time > self.anim_cooldown:
            self.update_time = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        # Flip image when moving left
        flip_h = (self.direction == -1)
        self.image = pygame.transform.flip(self.frames[self.frame_index], flip_h, False)

class EnemyManager:
    """
    Manages loading enemy assets, spawning, updating, drawing, and collision checks.
    """
    def __init__(self, sprite_path, scale=0.3):
        # Load walk animation frames once
        self.frames = []
        for i in range(1, 9):
            img = pygame.image.load(os.path.join(sprite_path, f"ppwalk{i}.png")).convert_alpha()
            w, h = img.get_size()
            self.frames.append(pygame.transform.scale(img, (int(w*scale), int(h*scale))))

        self.enemy_group = pygame.sprite.Group()

    def spawn(self, x, y, left_bound, right_bound, speed=2):
        """
        Create an Enemy at (x, y) patrolling between left_bound and right_bound.
        """
        enemy = Enemy(x, y, left_bound, right_bound, self.frames, speed)
        self.enemy_group.add(enemy)
        return enemy

    def reset(self):
        """
        Remove all existing enemies.
        """
        self.enemy_group.empty()

    def update(self):
        """
        Update all enemies in the group.
        """
        self.enemy_group.update()

    def draw(self, screen, scroll_x):
        """
        Draw all enemies offset by the camera scroll.
        """
        for enemy in self.enemy_group:
            screen.blit(enemy.image, (enemy.rect.x - scroll_x, enemy.rect.y))

    def check_collision(self, player):
        """
        Returns True if the player collides with any enemy.
        """
        return pygame.sprite.spritecollideany(player, self.enemy_group)
