import pygame
import sys
import random

#Game area
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 20
SPEED = 10

#Colour
BLACK = (0,0,0)
GREEN = (0,255,0)
DARK_GREY = (40,40,40)

#Make a score record
score_list = []

#Build a class
class Snake():
    def __init__(self):
        #Coordinate
        self.body = [
            (WIDTH // 2, HEIGHT // 2),
            (WIDTH // 2 - GRID_SIZE, HEIGHT // 2),
            (WIDTH // 2 - GRID_SIZE * 2, HEIGHT // 2)
        ]
        #The default direction is to move to the right
        self.dx = GRID_SIZE
        self.dy = 0
        self.alive = True

    #control the direction (UP, DOWN, LEFT, RIGHT)
    def change_direction(self, direction):
        if direction == "UP" and self.dy == 0:
            self.dx = 0
            self.dy = -GRID_SIZE
        elif direction == "DOWN" and self.dy == 0:
            self.dx = 0
            self.dy = GRID_SIZE
        elif direction == "LEFT" and self.dx == 0:
            self.dx = -GRID_SIZE
            self.dy = 0
        elif direction == "RIGHT" and self.dx == 0:
            self.dx = GRID_SIZE
            self.dy = 0

    #start to move snake
    def move(self, food_pos):
        #original coordinate and add the variable for each coordinate of x and y
        head_x, head_y = self.body[0]
        new_head = (head_x + self.dx, head_y + self.dy)
        #wall collision detect
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            self.alive = False
            return False
        #eat food
        if new_head == food_pos:
            self.body.insert(0, new_head)
            return True
        else:
            self.body.insert(0, new_head)
            self.body.pop()
            return False
            
    #start draw the snake in the screen
    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    #after gameover, the game will reset
    def reset(self):
        self.body = [
            (WIDTH // 2, HEIGHT // 2),
            (WIDTH // 2 - GRID_SIZE, HEIGHT // 2),
            (WIDTH // 2 - GRID_SIZE * 2, HEIGHT // 2)
        ]

        self.dx = GRID_SIZE
        self.dy = 0
        self.alive = True


#A food class
class Food():
    def __init__(self):
        self.generate()

    #Generate food randomly
    def generate(self):
        self.x = random.randint(1, (WIDTH // GRID_SIZE) - 2) * GRID_SIZE
        self.y = random.randint(1, (HEIGHT // GRID_SIZE) - 2) * GRID_SIZE
        self.position = (self.x, self.y)

    #draw the food in the screen
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, GRID_SIZE, GRID_SIZE))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MY SNAKE")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 80)
score_list_font = pygame.font.Font(None, 36)

my_snake = Snake()
food = Food()

#game main system
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Detect the keyborad event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                    my_snake.reset()
                    food = Food()

            elif my_snake.alive:
                if event.key == pygame.K_UP:
                    my_snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    my_snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    my_snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    my_snake.change_direction("RIGHT")

    if my_snake.alive:
        ate = my_snake.move(food.position)
        if ate:
            food = Food()

    #Make a grid
    screen.fill(BLACK)
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, DARK_GREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, DARK_GREY, (0, y), (WIDTH, y))
    
    #Make a "GAMEOVE", restart notice, and the highest score in the screen
    if my_snake.alive:
        food.draw(screen)
        my_snake.draw(screen)
    else:
        score_list.append(len(my_snake.body)-3)
        #Highest score
        score_list_text = score_list_font.render(f'Highest score: {max(score_list)}', True, (200, 200, 200))
        score_list_rect = score_list_text.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(score_list_text, score_list_rect)
        #GAMEOVER
        game_over_text = game_over_font.render("GAMEOVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(game_over_text, text_rect)
        #Restart notice
        hint_text = font.render("Press R to Restart", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(hint_text, hint_rect)

    #The score during the game
    score_text = font.render(f'Score: {len(my_snake.body)-3}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(SPEED)
