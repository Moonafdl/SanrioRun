import pygame, json, hashlib, os, csv, sys

# ——— Colors ———
BG_LOGIN      = (255, 240, 245)   # pastel pink
BG_GAME       = (255, 228, 233)
WHITE         = (255, 255, 255)
PINK          = (255, 105, 180)
DARK_PINK     = (219, 112, 147)
INPUT_BG      = (255, 255, 255)
INPUT_BORDER  = (255, 182, 193)
BUTTON_BG     = (255, 182, 193)
BUTTON_HOVER  = (255, 105, 180)
TEXT_COLOR    = (180, 30, 75)

# ——— Helper: draw rounded rect ———
def draw_rounded_rect(surf, rect, color, radius=12):
    pygame.draw.rect(surf, color, rect, border_radius=radius)

# ——— Input Box & Login System ———
class InputBox:
    def __init__(self, x, y, w, h, is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.is_password = is_password
        self.text = ''
        self.font = pygame.font.SysFont('Arial', 28)
        self.active = False


    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(e.pos)
        if e.type == pygame.KEYDOWN and self.active:
            if e.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += e.unicode

    def draw(self, screen, label):
        # label
        lbl = self.font.render(label, True, PINK)
        screen.blit(lbl, (self.rect.x, self.rect.y - 30))
        # box background
        draw_rounded_rect(screen, self.rect, INPUT_BG, 8)
        pygame.draw.rect(screen, INPUT_BORDER, self.rect, 2, border_radius=8)
        # text
        disp = '*' * len(self.text) if self.is_password else self.text
        txt_surf = self.font.render(disp, True, TEXT_COLOR)
        y_off = (self.rect.h - txt_surf.get_height()) // 2
        screen.blit(txt_surf, (self.rect.x + 10, self.rect.y + y_off))

class LoginSystem:
    def __init__(self, sw, sh):
        self.file = "user_data.json"
        self.sw, self.sh = sw, sh
        self.title_font = pygame.font.SysFont('Arial', 64, bold=True)
        self.btn_font   = pygame.font.SysFont('Arial', 32, bold=True)
        midx = sw // 2
        # input boxes
        self.user_box = InputBox(midx - 200, sh//2 - 40, 400, 50)
        self.pass_box = InputBox(midx - 200, sh//2 + 40, 400, 50, is_password=True)
        # buttons
        self.login_btn    = pygame.Rect(midx - 200, sh//2 + 120, 180, 60)
        self.register_btn = pygame.Rect(midx + 20,  sh//2 + 120, 180, 60)

    def _load(self):
        if not os.path.exists(self.file):
            with open(self.file,'w') as f: f.write('{}')
            return {}
        try:
            return json.load(open(self.file))
        except:
            os.rename(self.file, self.file + '.bak')
            with open(self.file,'w') as f: f.write('{}')
            return {}

    def _save(self, data):
        json.dump(data, open(self.file,'w'))

    def _hash(self, pwd):
        return hashlib.sha256(pwd.encode()).hexdigest()

    def register(self, u, p):
        data = self._load()
        if u in data: return False
        data[u] = self._hash(p)
        self._save(data)
        return True

    def auth(self, u, p):
        data = self._load()
        return u in data and data[u] == self._hash(p)

    def show_message(self, screen, msg, color):
        surf = self.btn_font.render(msg, True, color)
        rect = surf.get_rect(center=(self.sw//2, self.sh//2 + 200))
        screen.blit(surf, rect)
        pygame.display.flip()
        pygame.time.delay(1500)

    def handle_event(self, e):
        self.user_box.handle_event(e)
        self.pass_box.handle_event(e)
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.login_btn.collidepoint(e.pos):
                u, p = self.user_box.text, self.pass_box.text
                data = self._load()
                if u not in data:
                    return False, "User does not exist"
                if data[u] != self._hash(p):
                    return False, "Incorrect password"
                return True, u
            if self.register_btn.collidepoint(e.pos):
                u, p = self.user_box.text, self.pass_box.text
                if not u or not p:
                    return False, "Enter username & password"
                if self.register(u, p):
                    return False, "Registered successfully"
                return False, "Username taken"
        return None, None

    def draw(self, screen):
        screen.fill(BG_LOGIN)
        # title with shadow
        txt = "Sanrio Run"
        shadow = self.title_font.render(txt, True, DARK_PINK)
        main   = self.title_font.render(txt, True, WHITE)
        x = (self.sw - main.get_width()) // 2
        screen.blit(shadow, (x + 3, 80 + 3))
        screen.blit(main,   (x, 80))
        # inputs
        self.user_box.draw(screen, "Username")
        self.pass_box.draw(screen, "Password")
        # buttons
        mx, my = pygame.mouse.get_pos()
        for rect, label in ((self.login_btn, "Login"), (self.register_btn, "Register")):
            col = BUTTON_HOVER if rect.collidepoint((mx, my)) else BUTTON_BG
            draw_rounded_rect(screen, rect, col, 12)
            surf = self.btn_font.render(label, True, WHITE)
            screen.blit(surf, surf.get_rect(center=rect.center))

# ——— Death Screen ———
def death_screen():
    btn = pygame.Rect(0, 0, 300, 70)
    btn.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)
    font = pygame.font.SysFont('Arial', 48, bold=True)
    btn_font = pygame.font.SysFont('Arial', 32, bold=True)
    while True:
        mx, my = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(e.pos):
                return
            if e.type == pygame.KEYDOWN:
                return
        # dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        # message
        msg = font.render("You have died", True, WHITE)
        screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80)))
        # button
        col = BUTTON_HOVER if btn.collidepoint((mx, my)) else BUTTON_BG
        draw_rounded_rect(screen, btn, col, 12)
        t = btn_font.render("Try Again", True, WHITE)
        screen.blit(t, t.get_rect(center=btn.center))
        pygame.display.update()
        clock.tick(60)

# ——— Pause Menu ———
def pause_menu():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 192, 203, 180))
    resume_btn = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 40, 300, 50)
    exit_btn   = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 30, 300, 50)
    title_f = pygame.font.SysFont('Arial', 72, bold=True)
    btn_f   = pygame.font.SysFont('Arial', 36, bold=True)
    while True:
        mx, my = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if resume_btn.collidepoint(e.pos): return 'resume'
                if exit_btn.collidepoint(e.pos):   return 'exit'
        screen.blit(overlay, (0, 0))
        # heading
        txt = "Paused"
        shadow = title_f.render(txt, True, DARK_PINK)
        main   = title_f.render(txt, True, WHITE)
        screen.blit(shadow, shadow.get_rect(center=(SCREEN_WIDTH//2+2, SCREEN_HEIGHT//2-120+2)))
        screen.blit(main,   main.get_rect(center=(SCREEN_WIDTH//2,   SCREEN_HEIGHT//2-120)))
        # resume
        col = BUTTON_HOVER if resume_btn.collidepoint((mx,my)) else BUTTON_BG
        draw_rounded_rect(screen, resume_btn, col, 12)
        rtxt = btn_f.render("Resume", True, WHITE)
        screen.blit(rtxt, rtxt.get_rect(center=resume_btn.center))
        # exit
        col2 = BUTTON_HOVER if exit_btn.collidepoint((mx,my)) else BUTTON_BG
        draw_rounded_rect(screen, exit_btn, col2, 12)
        etxt = btn_f.render("Exit Game", True, WHITE)
        screen.blit(etxt, etxt.get_rect(center=exit_btn.center))
        pygame.display.update()
        clock.tick(60)

# ——— Save/Load Game State ———
# will be set per-user after login
SAVE_FILE = None

def save_state():
    state = {
        'player_x': player.rect.x,
        'player_y': player.rect.y,
        'screen_scroll': screen_scroll
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(state, f)

def load_state():
    if not SAVE_FILE or not os.path.exists(SAVE_FILE):
        return False
    try:
        st = json.load(open(SAVE_FILE))
        player.rect.x = st['player_x']
        player.rect.y = st['player_y']
        return st['screen_scroll']
    except:
        return False

# ——— Reset Level & Draw Background ———
enemy_group = pygame.sprite.Group()

def find_ground_y(x_pos, world):
    """Find the Y coordinate of the top solid tile at x_pos"""
    for y in range(ROWS):
        for x in range(COLS):
            if x * TILE_SIZE <= x_pos < (x + 1) * TILE_SIZE:
                t = world.data[y][x]
                if 0 <= t <= 8:
                    return y * TILE_SIZE
    return SCREEN_HEIGHT - TILE_SIZE  # fallback ground level


def reset_level():
    global world, player, screen_scroll, bg_scroll
    water_group.empty(); decoration_group.empty(); exit_group.empty(); enemy_group.empty()
    data = [[-1] * COLS for _ in range(ROWS)]
    with open('level1_data.csv', newline='') as f:
        for y, row in enumerate(csv.reader(f)):
            for x, v in enumerate(row):
                data[y][x] = int(v)
    world = World()
    player = world.process_data(data)

    screen_scroll = bg_scroll = 0.0

def draw_health_bar(surface, x, y, current, max_health):
    bar_width = 200
    bar_height = 20
    fill_width = (current / max_health) * bar_width

    fill_rect = pygame.Rect(x, y, fill_width, bar_height)
    border_rect = pygame.Rect(x, y, bar_width, bar_height)

    pygame.draw.rect(surface, PINK, fill_rect)
    pygame.draw.rect(surface, INPUT_BORDER, border_rect, 3)

def draw_bg(s):
    screen.fill(BG_GAME)
    pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - TILE_SIZE, SCREEN_WIDTH, TILE_SIZE))
    w = sky_img.get_width()
    for i in range((SCREEN_WIDTH // w) + 4):
        screen.blit(sky_img,      (i * w - int(s * 0.5), 0))
        screen.blit(mountain_img, (i * w - int(s * 0.6),
                                    SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img,    (i * w - int(s * 0.7),
                                    SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img,    (i * w - int(s * 0.8),
                                    SCREEN_HEIGHT - pine2_img.get_height()))

# ——— Player & World Classes ———
class Cinna(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed, self.vel_y = 5, 0
        self.jump, self.in_air = False, True
        self.jumps, self.flip   = 0, False
        self.health = 3
        self.last_hit_time = 0
        self.max_health = 3

        self.pushback_x = 0
        self.frames = []
        for i in range(1, 9):
            p = os.path.join('image/char/Walk', f'walk{i}.png')
            im = pygame.image.load(p).convert_alpha()
            w, h = im.get_size()
            self.frames.append(pygame.transform.scale(im, (int(w*0.3), int(h*0.3))))
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.frames[0]
        self.rect  = self.image.get_rect(
            topleft=(x, y - (self.image.get_height() - TILE_SIZE))
        )

    def update_animation(self, moving):
        cooldown = 100
        if moving and pygame.time.get_ticks() - self.update_time > cooldown:
            self.update_time   = pygame.time.get_ticks()
            self.frame_index  = (self.frame_index + 1) % len(self.frames)
        if not moving:
            self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def move(self, left, right, world):
        dx = dy = 0
        if left:  dx, self.flip = -self.speed, False
        if right: dx, self.flip =  self.speed, True

        dx += self.pushback_x  # ← Add pushback to movement
        self.pushback_x *= 0.8  # Gradually reduce pushback (friction)

        if abs(self.pushback_x) < 0.5:
            self.pushback_x = 0

        if self.jump and self.jumps < MAX_JUMPS:
            self.vel_y, self.jump, self.jumps, self.in_air = -11, False, self.jumps+1, True
        self.vel_y = min(self.vel_y + GRAVITY, 10)
        dy = self.vel_y
        for img, rc in world.obstacles:
            new = pygame.Rect(self.rect.x+dx, self.rect.y, self.rect.width, self.rect.height)
            if rc.colliderect(new) and rc.top < self.rect.bottom - 5:
                dx = 0
            if rc.colliderect(self.rect.x, self.rect.y+dy, self.rect.width, self.rect.height):
                if self.vel_y < 0:
                    dy, self.vel_y = rc.bottom - self.rect.top, 0
                else:
                    dy, self.vel_y, self.in_air, self.jumps = rc.top - self.rect.bottom, 0, False, 0
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, si):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x - si, self.rect.y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        for i in range(1, 9):
            path = os.path.join('image/char/Enemy', f'ppwalk{i}.png')
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            scaled = pygame.transform.scale(img, (int(w * 0.2), int(h * 0.2)))
            self.frames.append(scaled)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.speed = 2
        self.update_time = pygame.time.get_ticks()
        self.move_range = 150
        self.start_x = x

    def die(self):
        self.kill()  


    def update(self):
        self.rect.y += 5  # basic gravity

        # Check for ground
        on_ground = False
        for img, tile in world.obstacles:
            if tile.colliderect(self.rect.x, self.rect.bottom, self.rect.width, 1):
                on_ground = True
                self.rect.bottom = tile.top
                break

        if not on_ground:
            return

        # Edge detection: check one pixel ahead
        edge_check_x = self.rect.midbottom[0] + (self.direction * self.rect.width // 2)
        edge_check_rect = pygame.Rect(edge_check_x, self.rect.bottom + 1, 2, 2)
        grounded_ahead = any(tile.colliderect(edge_check_rect) for _, tile in world.obstacles)

        if not grounded_ahead:
            self.direction *= -1  # turn around at edge

        # Move horizontally
        self.rect.x += self.direction * self.speed
        if abs(self.rect.x - self.start_x) > self.move_range:
            self.direction *= -1

        # Animate
        if pygame.time.get_ticks() - self.update_time > 100:
            self.update_time = pygame.time.get_ticks()
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

    def draw(self, scroll_x):
        img = pygame.transform.flip(self.image, self.direction > 0, False)
        screen.blit(img, (self.rect.x - scroll_x, self.rect.y))

class World:
    def __init__(self):
        self.health = 3
        self.last_hit_time = 0
        self.obstacles = []

    def process_data(self, data):
        self.data = data
        player = None
        for y, row in enumerate(data):
            for x, t in enumerate(row):
                if t < 0:
                    continue
                if t == 30:
                    ground_y = find_ground_y(x * TILE_SIZE, self)
                    enemy = Enemy(x * TILE_SIZE, ground_y)
                    enemy_group.add(enemy)
                    continue  # skip loading image for this tile
                if t >= len(img_list):
                    continue  # ignore unknown tiles

                im = img_list[t]
                rc = im.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
                if 0 <= t <= 8:
                    self.obstacles.append((im, rc))
                elif 9 <= t <= 10:
                    spr = pygame.sprite.Sprite(); spr.image, spr.rect = im, rc; water_group.add(spr)
                elif 11 <= t <= 14:
                    spr = pygame.sprite.Sprite(); spr.image, spr.rect = im, rc; decoration_group.add(spr)
                elif t == 15:
                    player = Cinna(rc.x, rc.y)
                elif t == 20:
                    spr = pygame.sprite.Sprite(); spr.image, spr.rect = im, rc; exit_group.add(spr)
        return player


    def draw(self, si):
        for im, rc in self.obstacles:
            screen.blit(im, (rc.x - si, rc.y))

# ——— Pygame Init & Asset Loading ———
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen   = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock    = pygame.time.Clock()
FPS      = 60

# Movement
moving_left = moving_right = False

# World
GRAVITY     = 0.75
ROWS, COLS  = 16, 150
TILE_SIZE   = SCREEN_HEIGHT // ROWS
TILE_TYPES  = 21
MAX_JUMPS   = 2
WORLD_WIDTH = COLS * TILE_SIZE

# Load images
sky_img      = pygame.image.load('image/Background/sky_cloud.png').convert_alpha()
mountain_img = pygame.image.load('image/Background/mountain.png').convert_alpha()
pine1_img    = pygame.image.load('image/Background/pine1.png').convert_alpha()
pine2_img    = pygame.image.load('image/Background/pine2.png').convert_alpha()

img_list = []
for i in range(TILE_TYPES):
    im = pygame.image.load(f'image/tile/{i}.png').convert_alpha()
    img_list.append(pygame.transform.scale(im, (TILE_SIZE, TILE_SIZE)))

water_group      = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
exit_group       = pygame.sprite.Group()

# ——— 1) Login Loop ———
login = LoginSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
logged_in = False
current_user = None
while not logged_in:
    clock.tick(FPS)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        res, msg = login.handle_event(e)
        if res is True:
            logged_in = True
            current_user = msg
            SAVE_FILE = f"{current_user}_save_data.json"
        elif res is False:
            login.show_message(screen, msg, PINK)
    login.draw(screen)
    pygame.display.update()

# ——— 2) Start / Resume Game ———
reset_level()
ss = load_state()
if ss is not False:
    screen_scroll = bg_scroll = ss

running = True
while running:
    clock.tick(FPS)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a: moving_left  = True
            if e.key == pygame.K_d: moving_right = True
            if e.key == pygame.K_SPACE and player.jumps < MAX_JUMPS:
                player.jump = True
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_a: moving_left  = False
            if e.key == pygame.K_d: moving_right = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            mx, my = e.pos
            if mx > SCREEN_WIDTH - 50 and my < 50:
                choice = pause_menu()
                if choice == 'exit':
                    save_state()
                    running = False
                    break

    if not running:
        break

    player.move(moving_left, moving_right, world)

    died = (player.rect.top > SCREEN_HEIGHT or
            any(player.rect.colliderect(w.rect) for w in water_group))
    if died:
        pygame.event.clear()
        death_screen()
        reset_level()
        # reset movement so you don’t keep sliding
        moving_left = moving_right = False
        continue


    # camera
    screen_scroll = player.rect.centerx - SCREEN_WIDTH//2
    screen_scroll = max(0, min(screen_scroll, WORLD_WIDTH - SCREEN_WIDTH))
    scroll_int    = int(screen_scroll)
    bg_scroll     = screen_scroll

    # draw scene
    draw_bg(bg_scroll)
    world.draw(scroll_int)

    # menu icon
    pygame.draw.rect(screen, DARK_PINK, (SCREEN_WIDTH-40,10,30,30), 2, border_radius=4)
    pygame.draw.line(screen, DARK_PINK, (SCREEN_WIDTH-35,17), (SCREEN_WIDTH-15,17), 3)
    pygame.draw.line(screen, DARK_PINK, (SCREEN_WIDTH-35,25), (SCREEN_WIDTH-15,25), 3)
    pygame.draw.line(screen, DARK_PINK, (SCREEN_WIDTH-35,33), (SCREEN_WIDTH-15,33), 3)

    for grp in (water_group, decoration_group, exit_group):
        for spr in grp:
            screen.blit(spr.image, (spr.rect.x - scroll_int, spr.rect.y))
    enemy_group.update()
    for enemy in enemy_group:
        enemy.draw(scroll_int)

    hit_cooldown = 1000  # milliseconds
    now = pygame.time.get_ticks()

    for enemy in enemy_group:
        enemy_hitbox = enemy.rect.inflate(-20, -10)

        if player.rect.colliderect(enemy_hitbox):
            is_stomping = (
                player.vel_y > 0 and
                player.rect.bottom - enemy.rect.top < 20 and
                player.rect.centery < enemy.rect.centery
            )
            if is_stomping:
                enemy.die()
                player.vel_y = -12
            else:
                if now - player.last_hit_time > hit_cooldown:
                    player.health -= 1
                    player.last_hit_time = now
                    print(f"Player hit! Health = {player.health}")

                    if player.rect.centerx < enemy.rect.centerx:
                        player.pushback_x = -20
                    else:
                        player.pushback_x = 20
                    player.vel_y = -6

                    if player.health <= 0:
                        pygame.event.clear()
                        death_screen()
                        reset_level()
                        moving_left = moving_right = False
                        break

    player.update_animation(moving_left or moving_right)
    player.draw(scroll_int)

    draw_health_bar(screen, 20, 20, player.health, player.max_health)

    pygame.display.update()

pygame.quit()
