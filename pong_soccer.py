import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-3, 3])
        self.max_speed = 8
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Bounce off top and bottom walls
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y
            
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)
        
    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-3, 3])

class Player:
    def __init__(self, x, y, width, height, color, controls):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 6
        self.controls = controls  # Dictionary with 'up' and 'down' keys
        
    def update(self, keys):
        if keys[self.controls['up']] and self.y > 0:
            self.y -= self.speed
        if keys[self.controls['down']] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
            
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Goal:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height), 3)

class PongSoccer:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("3-Player Pong Soccer")
        self.clock = pygame.time.Clock()
        
        # Create players
        # Player 1 (Left goalkeeper) - Red
        self.player1 = Player(30, SCREEN_HEIGHT//2 - 50, 15, 100, RED, 
                             {'up': pygame.K_w, 'down': pygame.K_s})
        
        # Player 2 (Blue field player) - Now positioned in front of the right goal
        self.player2 = Player(SCREEN_WIDTH - 100, SCREEN_HEIGHT//2 - 40, 15, 80, BLUE,
                             {'up': pygame.K_UP, 'down': pygame.K_DOWN})
        
        # Player 3 (Right goalkeeper) - Green
        self.player3 = Player(SCREEN_WIDTH - 45, SCREEN_HEIGHT//2 - 50, 15, 100, GREEN,
                             {'up': pygame.K_i, 'down': pygame.K_k})
        
        # Create ball
        self.ball = Ball(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        
        # Create goals
        self.left_goal = Goal(0, SCREEN_HEIGHT//2 - 75, 10, 150)
        self.right_goal = Goal(SCREEN_WIDTH - 10, SCREEN_HEIGHT//2 - 75, 10, 150)
        
        # Score
        self.left_score = 0
        self.right_score = 0
        self.font = pygame.font.Font(None, 74)
        
    def check_ball_paddle_collision(self, player):
        ball_rect = pygame.Rect(self.ball.x - self.ball.radius, 
                               self.ball.y - self.ball.radius,
                               self.ball.radius * 2, 
                               self.ball.radius * 2)
        
        if ball_rect.colliderect(player.get_rect()):
            # Calculate collision point relative to paddle center
            collision_point = (self.ball.y - (player.y + player.height/2)) / (player.height/2)
            
            # Reverse horizontal direction and add spin based on collision point
            self.ball.speed_x = -self.ball.speed_x
            self.ball.speed_y += collision_point * 3
            
            # Limit ball speed
            if abs(self.ball.speed_y) > self.ball.max_speed:
                self.ball.speed_y = self.ball.max_speed if self.ball.speed_y > 0 else -self.ball.max_speed
                
    def check_goal(self):
        # Left goal (Player 3 scores)
        if (self.ball.x - self.ball.radius <= 10 and 
            self.left_goal.y <= self.ball.y <= self.left_goal.y + self.left_goal.height):
            self.right_score += 1
            self.ball.reset()
            return True
            
        # Right goal (Player 1 scores)  
        if (self.ball.x + self.ball.radius >= SCREEN_WIDTH - 10 and
            self.right_goal.y <= self.ball.y <= self.right_goal.y + self.right_goal.height):
            self.left_score += 1
            self.ball.reset()
            return True
            
        # Ball out of bounds (reset)
        if self.ball.x < 0 or self.ball.x > SCREEN_WIDTH:
            self.ball.reset()
            return True
            
        return False
        
    def draw_field(self):
        # Draw field background
        self.screen.fill(GREEN)
        
        # Draw center line
        pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT), 3)
        
        # Draw center circle
        pygame.draw.circle(self.screen, WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 50, 3)
        
        # Draw goals
        self.left_goal.draw(self.screen)
        self.right_goal.draw(self.screen)
        
    def draw_ui(self):
        # Draw scores
        left_text = self.font.render(str(self.left_score), True, WHITE)
        right_text = self.font.render(str(self.right_score), True, WHITE)
        
        self.screen.blit(left_text, (SCREEN_WIDTH//4, 50))
        self.screen.blit(right_text, (3*SCREEN_WIDTH//4, 50))
        
        # Draw player labels
        small_font = pygame.font.Font(None, 36)
        p1_label = small_font.render("P1 (W/S)", True, RED)
        p2_label = small_font.render("P2 (↑/↓)", True, BLUE)
        p3_label = small_font.render("P3 (I/K)", True, GREEN)
        
        self.screen.blit(p1_label, (10, 10))
        self.screen.blit(p2_label, (SCREEN_WIDTH - 200, 10))
        self.screen.blit(p3_label, (SCREEN_WIDTH - 100, 10))
        
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        # Reset game
                        self.left_score = 0
                        self.right_score = 0
                        self.ball.reset()
            
            # Get pressed keys
            keys = pygame.key.get_pressed()
            
            # Update players
            self.player1.update(keys)
            self.player2.update(keys)
            self.player3.update(keys)
            
            # Update ball
            self.ball.update()
            
            # Check collisions
            self.check_ball_paddle_collision(self.player1)
            self.check_ball_paddle_collision(self.player2)
            self.check_ball_paddle_collision(self.player3)
            
            # Check for goals
            self.check_goal()
            
            # Draw everything
            self.draw_field()
            
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            self.player3.draw(self.screen)
            
            self.ball.draw(self.screen)
            
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PongSoccer()
    game.run()
