import pygame
import json
import hashlib
import os

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class InputBox:
    def __init__(self, x, y, w, h, text='', is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.is_password = is_password
        self.visible_text = text if not is_password else '*' * len(text)
        self.active = False
        
        # Initialize font only if pygame is initialized
        if pygame.get_init():
            self.font = pygame.font.SysFont('Arial', 32)
            self.txt_surface = self.font.render(self.visible_text, True, self.color)
        else:
            # Fallback if pygame isn't initialized (shouldn't happen in normal use)
            self.font = None
            self.txt_surface = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = LIGHT_BLUE if self.active else BLACK
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.visible_text = self.text if not self.is_password else '*' * len(self.text)
                else:
                    self.text += event.unicode
                    self.visible_text = self.text if not self.is_password else '*' * len(self.text)
                
                if self.font:  # Only render if font is available
                    self.txt_surface = self.font.render(self.visible_text, True, self.color)
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        if self.txt_surface:
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        label = "Password:" if self.is_password else "Username:"
        if pygame.font.get_init():
            label_surface = pygame.font.SysFont('Arial', 24).render(label, True, BLACK)
            screen.blit(label_surface, (self.rect.x, self.rect.y - 30))

class LoginSystem:
    def __init__(self, screen_width, screen_height):
        self.USER_DATA_FILE = "user_data.json"
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize fonts only if pygame is initialized
        if pygame.font.get_init():
            self.font = pygame.font.SysFont('Arial', 32)
            self.small_font = pygame.font.SysFont('Arial', 24)
        else:
            self.font = None
            self.small_font = None
            
        self.username_box = InputBox(screen_width//2 - 150, screen_height//2 - 50, 300, 50)
        self.password_box = InputBox(screen_width//2 - 150, screen_height//2 + 50, 300, 50, is_password=True)
        self.login_button = pygame.Rect(screen_width//2 - 150, screen_height//2 + 150, 140, 50)
        self.register_button = pygame.Rect(screen_width//2 + 10, screen_height//2 + 150, 140, 50)
        self.message = ""
        self.message_color = BLACK
        self.message_time = 0
    
    def update(self):
        if self.message and pygame.time.get_ticks() - self.message_time > 2000:
            self.message = ""

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_user_data(self):
        if os.path.exists(self.USER_DATA_FILE):
            with open(self.USER_DATA_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_user_data(self, data):
        with open(self.USER_DATA_FILE, 'w') as f:
            json.dump(data, f)

    def register_user(self, username, password):
        user_data = self.load_user_data()
        if username in user_data:
            return False
        hashed_password = self.hash_password(password)
        user_data[username] = hashed_password
        self.save_user_data(user_data)
        return True

    def authenticate_user(self, username, password):
        user_data = self.load_user_data()
        if username not in user_data:
            return False
        hashed_password = self.hash_password(password)
        return user_data[username] == hashed_password

    def show_message(self, screen, message, color, duration=2000):
        message_surface = self.font.render(message, True, color)
        message_rect = message_surface.get_rect(center=(self.screen_width//2, self.screen_height//2 + 100))
        screen.blit(message_surface, message_rect)
        pygame.display.flip()
        pygame.time.delay(duration)

    def draw(self, screen):
        screen.fill(PINK)
        
        # Draw title
        title = self.font.render("Sanrio Run Login", True, BLACK)
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 100))
        
        # Draw input boxes
        self.username_box.draw(screen)
        self.password_box.draw(screen)
        
        # Draw buttons
        pygame.draw.rect(screen, GREEN, self.login_button)
        pygame.draw.rect(screen, LIGHT_BLUE, self.register_button)
        
        login_text = self.small_font.render("Login", True, BLACK)
        register_text = self.small_font.render("Register", True, BLACK)
        
        screen.blit(login_text, (self.login_button.x + self.login_button.width//2 - login_text.get_width()//2, 
                                self.login_button.y + self.login_button.height//2 - login_text.get_height()//2))
        screen.blit(register_text, (self.register_button.x + self.register_button.width//2 - register_text.get_width()//2, 
                                  self.register_button.y + self.register_button.height//2 - register_text.get_height()//2))

    def handle_events(self, event):
        self.username_box.handle_event(event)
        self.password_box.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.login_button.collidepoint(event.pos):
                if self.authenticate_user(self.username_box.text, self.password_box.text):
                    return True, self.username_box.text
                else:
                    return False, "Invalid username or password"
            elif self.register_button.collidepoint(event.pos):
                if not self.username_box.text or not self.password_box.text:
                    return False, "Username and password required"
                elif self.register_user(self.username_box.text, self.password_box.text):
                    return False, "Registration successful!"
                else:
                    return False, "Username already exists"
        return None, None