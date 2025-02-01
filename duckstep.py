import pygame
import random

pygame.init() # init pygame
pygame.joystick.init() #interact w controller

# Game clock for framerate
clock = pygame.time.Clock()

# Creates game screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# constants go here 
# (lane config)
MARGIN = 50 # so that theres a border
LANE_WIDTH = (SCREEN_WIDTH - 2 * MARGIN) // 6
NOTE_HEIGHT = 20
HIT_ZONE_Y = SCREEN_HEIGHT - MARGIN - 100  # Bottom 100 pixels as the hit zone
HIT_ZONE_HEIGHT = 100  # Height of the hit detection area
HIT_BUFFER = 50  # Allow hitting notes 50 pixels above the hit zone
# Load bread note image
bread_image = pygame.image.load("bread.png")
bread_image = pygame.transform.scale(bread_image, (LANE_WIDTH - 20, NOTE_HEIGHT))
# (player variables)
playerX, playerY = 400, 300  # Initial player position
playerX_change, playerY_change = 0, 0

# Placeholder for notes (lane_num, y_position); gonna make csv later
notes = [
    [random.randint(0,5), -NOTE_HEIGHT * i*5, False, 0] for i in range(50)
    # [0, -100], [1, -300], [2, -500], [3, -700], [4, -900], [5, -1100],
    # [0, -700], [1, -800], [2, -900], [3, -1000], [4, -1100], [5, -1200]
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

# tracking missed lanes and red tint duration
missed_lanes = {i: 0 for i in range(6)}  # tracks how long lane was red

# def draw methods to draw stuff on to the screen
def draw_board():
    # border for screen
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    # hit notes here:
    pygame.draw.rect(screen, (100, 100, 100), (MARGIN, HIT_ZONE_Y, SCREEN_WIDTH - 2 * MARGIN, HIT_ZONE_HEIGHT))
    """Draws the six lanes on the screen."""
    for i in range(6):
        x_pos = MARGIN + i * LANE_WIDTH
        pygame.draw.rect(screen, (50, 60, 70), (x_pos, MARGIN, LANE_WIDTH, HIT_ZONE_Y - MARGIN))
        if missed_lanes[i] > 0:
            pygame.draw.rect(screen, (205, 100, 100), (x_pos, MARGIN, LANE_WIDTH, HIT_ZONE_Y - MARGIN))  # Missed lane effect
        pygame.draw.line(screen, (255, 255, 255), (x_pos, MARGIN), (x_pos, SCREEN_HEIGHT - MARGIN), 2)
    # Draw rightmost white line for the last lane
    pygame.draw.line(screen, (255, 255, 255), (MARGIN + 6 * LANE_WIDTH, MARGIN), (MARGIN + 6 * LANE_WIDTH, SCREEN_HEIGHT - MARGIN), 2)

def draw_notes():
    """Draws falling notes on the screen."""
    global notes
    for note in notes:
        lane, y_pos = note[0], note[1]
        x_pos = MARGIN + lane * LANE_WIDTH + 10
        screen.blit(bread_image, (x_pos, y_pos))
    # move notes down
    for i in range(len(notes)):
        notes[i][1] += 5  # Move notes downward
        if notes[i][1] >= SCREEN_HEIGHT - MARGIN and not notes[i][2]:  # mark missed if not already marked
            notes[i][2] = True
            missed_lanes[notes[i][0]] = 10  # turn the lane red for 10 frames
    # remove notes that go off the screen
    notes[:] = [note for note in notes if note[1] < SCREEN_HEIGHT - MARGIN + NOTE_HEIGHT]

def check_hit(lane):
    """Checks if there is a note in the hit zone for the given lane."""
    global notes, score
    for note in notes[:]:  # Iterate over a copy of the list
        if note[0] == lane and (HIT_ZONE_Y - HIT_BUFFER) <= note[1] <= HIT_ZONE_Y + HIT_ZONE_HEIGHT:
            notes.remove(note)  # Remove note safely
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
        if event.type == pygame.KEYDOWN and event.key in key_to_lane:
            check_hit(key_to_lane[event.key])
        # SNES controller button press handling
        if event.type == pygame.JOYBUTTONDOWN and event.button in snes_button_to_lane:
            check_hit(snes_button_to_lane[event.button])

    # Update missed lanes
    for lane in missed_lanes:
        if missed_lanes[lane] > 0:
            missed_lanes[lane] -= 1  # countdown red tint duration

    # draw methods here
    draw_board()
    draw_notes()

    pygame.display.update() # display update
    clock.tick(60) # 60fps