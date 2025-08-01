import pygame
import random
import collections
import datetime # Import the datetime module

# --- Game Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255) # For AI path visualization (optional)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# --- Snake Class ---
class Snake:
    def __init__(self):
        # Initial position in the middle of the screen
        self.body = collections.deque([(GRID_WIDTH // 2, GRID_HEIGHT // 2)])
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.grow_pending = False # Flag to indicate if snake should grow

    def move(self):
        # Calculate new head position
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.appendleft(new_head) # Add new head

        if not self.grow_pending:
            self.body.pop() # Remove tail if not growing
        else:
            self.grow_pending = False # Reset grow flag

    def change_direction(self, new_direction):
        # Prevent immediate 180-degree turns
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def grow(self):
        self.grow_pending = True
        self.score += 1

    def check_collision(self):
        head_x, head_y = self.body[0]

        # Wall collision
        if not (0 <= head_x < GRID_WIDTH and 0 <= head_y < GRID_HEIGHT):
            return True

        # Self-collision (check if head collides with any part of the body except itself)
        if len(self.body) > 1 and self.body[0] in list(self.body)[1:]:
            return True

        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# --- Food Class ---
class Food:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)

    def generate_position(self, snake_body):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_body: # Ensure food doesn't spawn on snake
                return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# --- AI Logic (Simple Greedy Pathfinding) ---
def get_safe_direction(snake, food):
    # Get current head position
    head_x, head_y = snake.body[0]

    # Possible directions
    possible_directions = [UP, DOWN, LEFT, RIGHT]
    random.shuffle(possible_directions) # Shuffle to add some randomness if multiple paths are equally good

    best_direction = snake.direction # Default to current direction if no better path found

    # Calculate distance to food for each possible move
    min_distance = float('inf')

    for dx, dy in possible_directions:
        next_x, next_y = head_x + dx, head_y + dy
        next_pos = (next_x, next_y)

        # Check for immediate collision with walls or self
        if not (0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT):
            continue # Skip if it leads to wall collision

        # Temporarily add the new head and check for self-collision
        # Create a temporary body to simulate the move
        temp_body = collections.deque(list(snake.body))
        temp_body.appendleft(next_pos)
        if not snake.grow_pending: # Simulate popping the tail if not growing
            temp_body.pop()

        if next_pos in list(temp_body)[1:]: # Check if the new head collides with the *simulated* body
            continue # Skip if it leads to self-collision

        # If it's a safe move, calculate distance to food
        distance = abs(food.position[0] - next_x) + abs(food.position[1] - next_y)

        # Prioritize moves that get closer to food
        if distance < min_distance:
            min_distance = distance
            best_direction = (dx, dy)
        elif distance == min_distance:
            # If distances are equal, prefer continuing in the same general direction
            # This helps prevent unnecessary zig-zagging
            if (dx, dy) == snake.direction:
                best_direction = (dx, dy)

    # If no safe path to food, try to find any safe path to survive
    if best_direction == snake.direction: # Means no better path was found based on food distance
        for dx, dy in possible_directions:
            next_x, next_y = head_x + dx, head_y + dy
            next_pos = (next_x, next_y)

            if not (0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT):
                continue

            temp_body = collections.deque(list(snake.body))
            temp_body.appendleft(next_pos)
            if not snake.grow_pending:
                temp_body.pop()

            if next_pos in list(temp_body)[1:]:
                continue

            return (dx, dy) # Return the first safe direction found

    return best_direction

# --- Main Game Function ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Self-Playing Snake")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36) # Default font, size 36

    snake = Snake()
    food = Food(snake.body)

    game_over = False
    game_speed = 10 # Frames per second
    game_end_time = None # Variable to store the time when the game ends

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # AI decides the next move
        new_direction = get_safe_direction(snake, food)
        snake.change_direction(new_direction)

        snake.move()

        # Check for eating food
        if snake.body[0] == food.position:
            snake.grow()
            food = Food(snake.body) # Generate new food

        # Check for collision after moving
        if snake.check_collision():
            game_over = True
            game_end_time = datetime.datetime.now() # Capture the current time when game ends

        # --- Drawing ---
        screen.fill(BLACK) # Clear screen

        snake.draw(screen)
        food.draw(screen)

        # Display score
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip() # Update display
        clock.tick(game_speed) # Control game speed

    # --- Game Over Screen ---
    game_over_text = font.render("GAME OVER!", True, WHITE)
    final_score_text = font.render(f"Final Score: {snake.score}", True, WHITE)
    
    # Format and display the end time
    if game_end_time:
        time_text = font.render(f"Time: {game_end_time.strftime('%Y-%m-%d %H:%M:%S')}", True, WHITE)
    else:
        time_text = font.render("Time: N/A", True, WHITE) # Fallback if time somehow isn't captured

    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)

    screen.fill(BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 70)) # Adjusted position
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20)) # Adjusted position
    screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30)) # New line for time
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80)) # Adjusted position
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main() # Restart the game
                    waiting_for_input = False
                elif event.key == pygame.K_q:
                    waiting_for_input = False

    pygame.quit()

if __name__ == "__main__":
    main()
