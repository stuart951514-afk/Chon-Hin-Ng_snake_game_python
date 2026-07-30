import pygame #Game engine: window, graphics, events, and clock
import sys #System exit: terminates the program safely
import random #Random generation: spawns food at random grid positions

#1. Game Constants (UPPERCASE)

# Window dimensions
WIDTH = 600
HEIGHT = 600

# Grid cell size (snake and food are 20x20 pixels)
GRID_SIZE = 20

# Game speed (higher value = faster movement)
SPEED = 10

# RGB Color definitions
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREY = (40, 40, 40)
WHITE = (255, 255, 255)
LIGHT_GREY = (200, 200, 200)

#2. Global Variables
# Stores all scores from each game session (used to calculate highest score)
score_list = []

#3. Snake Class
class Snake():
    """Manages the snake's body, movement, direction, and rendering."""
    
    def __init__(self):
        """Initialise the snake with 3 segments, starting direction: right."""
        # Body: list of (x, y) tuples. Index 0 is the head.
        self.body = [
            (WIDTH // 2, HEIGHT // 2),                      # Head (300, 300)
            (WIDTH // 2 - GRID_SIZE, HEIGHT // 2),          # Body (280, 300)
            (WIDTH // 2 - GRID_SIZE * 2, HEIGHT // 2)       # Tail (260, 300)
        ]
        
        # Direction vectors: dx for horizontal, dy for vertical
        # Initial direction: moving right (dx = +20 per frame)
        self.dx = GRID_SIZE
        self.dy = 0
        
        # Alive status: True = alive, False = dead
        self.alive = True

    def change_direction(self, direction):
        """
        Change the snake's direction based on keyboard input.
        Prevents the snake from reversing into itself.
        Parameter direction: "UP", "DOWN", "LEFT", or "RIGHT".
        """
        # Move up: only allowed if not currently moving vertically (dy == 0)
        if direction == "UP" and self.dy == 0:
            self.dx = 0
            self.dy = -GRID_SIZE   # y decreases = upward on screen
        # Move down: only if not moving vertically
        elif direction == "DOWN" and self.dy == 0:
            self.dx = 0
            self.dy = GRID_SIZE    # y increases = downward on screen
        # Move left: only if not moving horizontally (dx == 0)
        elif direction == "LEFT" and self.dx == 0:
            self.dx = -GRID_SIZE   # x decreases = left
            self.dy = 0
        # Move right: only if not moving horizontally
        elif direction == "RIGHT" and self.dx == 0:
            self.dx = GRID_SIZE    # x increases = right
            self.dy = 0

    def move(self, food_pos):
        """
        Core movement logic executed every frame.
        Parameter food_pos: current (x, y) coordinates of the food.
        Returns: True if food was eaten, False otherwise.
        """
        # 1. Get current head coordinates
        head_x, head_y = self.body[0]
        
        # 2. Calculate new head position based on current direction
        new_head = (head_x + self.dx, head_y + self.dy)

        # 3. Wall collision detection: if new head is outside the window, snake dies
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT):
            self.alive = False
            return False   # Food not eaten

        # 4. Check if the snake ate the food (head overlaps food position)
        if new_head == food_pos:
            # Food eaten: insert new head, do NOT remove tail (snake grows)
            self.body.insert(0, new_head)
            return True    # Food eaten successfully
        else:
            # Normal movement: insert new head, remove tail (length stays constant)
            self.body.insert(0, new_head)
            self.body.pop()
            return False   # No food eaten

    def draw(self, screen):
        """
        Draw every segment of the snake on the screen.
        Parameter screen: the Pygame display surface (window).
        """
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    def reset(self):
        """
        Reset the snake to its initial state (used when pressing 'R' to restart).
        """
        self.body = [
            (WIDTH // 2, HEIGHT // 2),
            (WIDTH // 2 - GRID_SIZE, HEIGHT // 2),
            (WIDTH // 2 - GRID_SIZE * 2, HEIGHT // 2)
        ]
        self.dx = GRID_SIZE
        self.dy = 0
        self.alive = True


#4. Food Class
class Food():
    """Manages random food generation and rendering."""
    
    def __init__(self):
        """Automatically generate the first food position on creation."""
        self.generate()

    def generate(self):
        """
        Generate a random food position on the grid.
        Avoids the very edges to prevent visual clipping.
        """
        # Range: 1 to (number_of_cells - 2) to keep food away from borders
        self.x = random.randint(1, (WIDTH // GRID_SIZE) - 2) * GRID_SIZE
        self.y = random.randint(1, (HEIGHT // GRID_SIZE) - 2) * GRID_SIZE
        self.position = (self.x, self.y)

    def draw(self, screen):
        """Draw the food as a red rectangle on the screen."""
        pygame.draw.rect(screen, RED, (self.x, self.y, GRID_SIZE, GRID_SIZE))


#5. Pygame Initialisation
pygame.init()                           # Start the Pygame engine
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
pygame.display.set_caption("MY SNAKE")  # Set window title
clock = pygame.time.Clock()             # Create a clock object for frame rate control

#6. Font Setup (for rendering text)
font = pygame.font.Font(None, 36)       # Regular font for score
game_over_font = pygame.font.Font(None, 80)  # Large font for "GAMEOVER"
score_list_font = pygame.font.Font(None, 36) # Medium font for highest score

#7. Create Game Objects
my_snake = Snake()   # Instantiate the snake
food = Food()        # Instantiate the first food

#8. Main Game Loop
while True:
    #8a. Event Handling (user input and system events)
    for event in pygame.event.get():
        # If user clicks the window's close button, exit the program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle keyboard events
        if event.type == pygame.KEYDOWN:
            # Press 'R' to restart the game (whether dead or alive)
            if event.key == pygame.K_r:
                my_snake.reset()   # Reset snake to initial state
                food = Food()      # Generate a new food
                # Note: score_list is NOT cleared to preserve highest score

            # Direction keys only work if the snake is alive
            elif my_snake.alive:
                if event.key == pygame.K_UP:
                    my_snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    my_snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    my_snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    my_snake.change_direction("RIGHT")

    #8b. Update Game Logic
    if my_snake.alive:
        # Move the snake and check if it ate the food
        ate = my_snake.move(food.position)
        if ate:
            # If food was eaten, generate a new food
            food = Food()

    #8c. Render Everything (drawing on the screen)
    # Fill the background with black
    screen.fill(BLACK)

    # Draw light grey grid lines (for visual reference)
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, DARK_GREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, DARK_GREY, (0, y), (WIDTH, y))

    # Display game elements based on snake's alive status
    if my_snake.alive:
        # If alive: show food and snake
        food.draw(screen)
        my_snake.draw(screen)
    else:
        # If dead: display the Game Over screen

        # 1. Record the final score into the history list
        # Score = snake length - initial 3 segments
        score_list.append(len(my_snake.body) - 3)

        # 2. Display the highest score
        highest_score = max(score_list)   # Get the maximum from all sessions
        score_list_text = score_list_font.render(f'Highest score: {highest_score}', True, LIGHT_GREY)
        score_list_rect = score_list_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(score_list_text, score_list_rect)

        # 3. Display large red "GAMEOVER" text
        game_over_text = game_over_font.render("GAMEOVER", True, RED)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(game_over_text, text_rect)

        # 4. Display white restart instruction
        hint_text = font.render("Press R to Restart", True, LIGHT_GREY)
        hint_rect = hint_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(hint_text, hint_rect)

    # 5. Always display the current score in the top-left corner
    # Score = snake length - 3 (initial length)
    score_text = font.render(f'Score: {len(my_snake.body) - 3}', True, WHITE)
    screen.blit(score_text, (10, 10))

    #8d. Update the Display
    pygame.display.update()

    #8e. Control Game Speed
    clock.tick(SPEED)
