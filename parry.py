import pygame
import sys
import random

FPS = 60
MAX_WIDTH = 500
MAX_HEIGHT = 750

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))

background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (MAX_WIDTH, MAX_HEIGHT))
player_image = pygame.image.load("miya.png").convert_alpha()
enemy_image = pygame.image.load("Dong.png").convert_alpha()
bonus_image = pygame.image.load("melon.png").convert_alpha()  # 보너스 아이템 이미지
bonus_image = pygame.transform.scale(bonus_image, (40, 40))

font = pygame.font.Font(None, 36)

def show_message(messages):
    screen.blit(background, (0, 0))
    y_offset = MAX_HEIGHT // 2 - 40
    max_width = 0
    text_surfaces = []
    
    for message in messages:
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(MAX_WIDTH // 2, y_offset))
        text_surfaces.append((text, text_rect))
        max_width = max(max_width, text_rect.width)
        y_offset += 40  
    
    box_width = max_width + 20
    box_height = len(messages) * 40 + 20
    box_rect = pygame.Rect((MAX_WIDTH // 2 - box_width // 2, MAX_HEIGHT // 2 - box_height // 2 + 20), (box_width, box_height))
    pygame.draw.rect(screen, (255, 255, 255), box_rect)  
    pygame.draw.rect(screen, (0, 0, 0), box_rect, 2)  
    
    for text, text_rect in text_surfaces:
        screen.blit(text, text_rect)
    
    pygame.display.update()
    
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                waiting_for_input = False

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.image = pygame.transform.scale(player_image, (60, 60))
        
    def draw(self):
        return screen.blit(self.image, (self.x, self.y))
    
    def move(self, pressed_keys):
        if pressed_keys[pygame.K_RIGHT] and self.x < MAX_WIDTH - 40:
            self.x += self.speed
        if pressed_keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed

class Enemy():
    def __init__(self):
        self.x = random.randrange(0, MAX_WIDTH - 40)
        self.y = 50
        self.speed = random.randrange(10, 20)
        self.image = pygame.transform.scale(enemy_image, (45, 45))
        
    def draw(self):
        return screen.blit(self.image, (self.x, self.y))
        
    def move(self, score):
        self.y += self.speed
        if self.y >= MAX_HEIGHT:
            self.y = 50
            self.x = random.randrange(0, MAX_WIDTH - 40)
            self.speed = random.randrange(7, 15) + (score // 500)

class BonusItem():
    def __init__(self):
        self.x = random.randrange(0, MAX_WIDTH - 30)
        self.y = -30
        self.speed = 5
        self.image = bonus_image
        
    def draw(self):
        return screen.blit(self.image, (self.x, self.y))
    
    def move(self):
        self.y += self.speed
        if self.y >= MAX_HEIGHT:
            self.y = -30
            self.x = random.randrange(0, MAX_WIDTH - 30)

def main():
    show_message(["","Press any arrow key to START!" , "Dodge the POOP Eat melon for BONUS"])
    
    while True:
        player = Player(MAX_WIDTH // 2, MAX_HEIGHT - 60)
        enemies = [Enemy()]
        bonus_item = BonusItem()
        score = 0
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            clock.tick(FPS)
            screen.blit(background, (0, 0))
            
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))
            
            pressed_keys = pygame.key.get_pressed()
            player.move(pressed_keys)
            player_rect = player.draw()
            
            if score >= 700 and len(enemies) == 1:
                enemies.append(Enemy())
            
            for enemy in enemies:
                enemy_rect = enemy.draw()
                enemy.move(score)
                if player_rect.colliderect(enemy_rect):
                    show_message(["!Game Over!", f"Your score: {score}", "Press any key to restart", "ESC to exit."])
                    running = False
            
            bonus_rect = bonus_item.draw()
            bonus_item.move()
            
            if player_rect.colliderect(bonus_rect):
                score += 100
                bonus_item.y = -30
                bonus_item.x = random.randrange(0, MAX_WIDTH - 30)
            
            score += 1
            pygame.display.update()

if __name__ == '__main__':
    main()