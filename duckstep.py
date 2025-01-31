import pygame

pygame.init() # init pygame
pygame.joystick.init() #interact w controller

# Game clock for framerate
clock = pygame.time.Clock()

# Creates game screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# constants go here 
# (lane config)
LANE_WIDTH = SCREEN_WIDTH // 6
NOTE_HEIGHT = 20
# Load bread note image
bread_image = pygame.image.load("bread.png")
bread_image = pygame.transform.scale(bread_image, (LANE_WIDTH - 20, NOTE_HEIGHT))
# (player variables)
playerX, playerY = 400, 300  # Initial player position
playerX_change, playerY_change = 0, 0

# Placeholder for notes (lane_num, y_position); gonna make csv later
notes = [
    # [i % 6, -NOTE_HEIGHT * i*5] for i in range(50)
    [0, -100], [1, -200], [2, -300], [3, -400], [4, -500], [5, -600],
    [0, -700], [1, -800], [2, -900], [3, -1000], [4, -1100], [5, -1200]
]
score = 0

# lanes - keyboard binds
key_to_lane = {
    pygame.K_s: 0,
    pygame.K_d: 1,
    pygame.K_f: 2,
    pygame.K_j: 3,
    pygame.K_k: 4,
    pygame.K_l: 5,
}

# lanes - snes controller binds
snes_button_to_lane = {
    13: 0, # Left on D-pad
    12: 1, # Down on D-pad
    14: 2, # Right on D-pad
    3: 3, # Y button
    1: 4, # B button
    0: 5, # A button
}

# def draw methods to draw stuff on to the screen
def draw_board():
    """Draws the six lanes on the screen."""
    for i in range(1, 6):
        pygame.draw.line(screen, (255, 255, 255), (i * LANE_WIDTH, 0), (i * LANE_WIDTH, SCREEN_HEIGHT), 2)

def draw_notes():
    """Draws falling notes on the screen."""
    global notes
    for note in notes:
        lane, y_pos = note
        screen.blit(bread_image, (lane * LANE_WIDTH + 10, y_pos))
    # move notes down
    for note in notes:
        note[1] += 5  # Move notes downward
    # remove notes that go off the screen
    notes = [note for note in notes if note[1] < SCREEN_HEIGHT]

def check_hit(lane):
    """Checks if there is a note at the bottom of the screen in the given lane."""
    global notes, score
    for note in notes:
        if note[0] == lane and SCREEN_HEIGHT - NOTE_HEIGHT - 5 <= note[1] <= SCREEN_HEIGHT:
            notes.remove(note)
            score += 1
            print(f"Score: {score}")
            return

# game go brr
running = True # infinite loop
while running:
    screen.fill((50,60,70)) #rgb fill screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # exit game

        # Keyboard controls for hitting notes
        if event.type == pygame.KEYDOWN:
            if event.key in key_to_lane:
                check_hit(key_to_lane[event.key])

        # SNES controller button press handling
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button in snes_button_to_lane:
                check_hit(snes_button_to_lane[event.button])

    # draw methods here
    draw_board()
    draw_notes()

    pygame.display.update() # display update
    clock.tick(60) # 60fps