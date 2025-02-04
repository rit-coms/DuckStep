import pygame
import random

# color variables
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (100, 100, 100)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE_LANE = (50, 60, 70)
COLOR_RED_LANE = (70, 60, 50)
COLOR_RED_MISS = (205, 100, 100)
COLOR_FEEDBACK_RED = (255,0,0)
COLOR_FEEDBACK_GREEN = (0,255,0)
COLOR_FEEDBACK_BLUE = (50, 200, 255)
# other
NUM_LANES = 6
SPEED = 5

# Initialization
pygame.init() # init pygame
pygame.joystick.init() #interact w controller
pygame.event.pump()  # force pygame to refresh devices to detect controller
pygame.mixer.init() # init sound

# Check if a joystick is connected
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("controller 😁🎉")
else:
    print("No controller found! 😭🙏")

# sound stuff
quack1 = pygame.mixer.Sound("quack/quack1.mp3") # load sound
quack2 = pygame.mixer.Sound("quack/quack2.mp3") # load sound
quack3 = pygame.mixer.Sound("quack/quack3.mp3") # load sound
quack4 = pygame.mixer.Sound("quack/quack4.mp3") # load sound
quack5 = pygame.mixer.Sound("quack/quack5.mp3") # load sound
quack6 = pygame.mixer.Sound("quack/quack6.mp3") # load sound

# Game clock for framerate
clock = pygame.time.Clock()

# Creates game screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# constants go here 
# (lane config)
MARGIN = 50 # so that theres a border
LANE_WIDTH = (SCREEN_WIDTH - 2 * MARGIN) // NUM_LANES
NOTE_HEIGHT = 20
HIT_ZONE_Y = SCREEN_HEIGHT - MARGIN - 100  # Bottom 100 pixels as the hit zone
HIT_ZONE_HEIGHT = 100  # Height of the hit detection area
HIT_BUFFER = SPEED*10 +SPEED # Allow hitting notes 50 pixels above the hit zone
# Load bread note image
bread_image = pygame.image.load("bread.png")
bread_image = pygame.transform.scale(bread_image, (LANE_WIDTH - 20, NOTE_HEIGHT+20))

# Placeholder for notes (lane_num, y_position); gonna make csv later
notes = [
    [random.randint(0,NUM_LANES-1), -NOTE_HEIGHT * i*SPEED, False, 0] for i in range(50)
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

# play correct quack
lane_to_quack = {
    0: quack1,
    1: quack2,
    2: quack3,
    3: quack4,
    4: quack5,
    5: quack6
}

# tracking missed lanes and red tint duration
missed_lanes = {i: 0 for i in range(NUM_LANES)}  # tracks how long lane was red

# feedback message so player knows if note hit
feedback_message = ""
feedback_color = COLOR_WHITE
feedback_timer = 0  # Countdown to clear the message

# def draw methods to draw stuff on to the screen
def draw_board():
    # border for screen
    pygame.draw.rect(screen, COLOR_BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    # hit notes here:
    pygame.draw.rect(screen, COLOR_GRAY, (MARGIN, HIT_ZONE_Y, SCREEN_WIDTH - 2 * MARGIN, HIT_ZONE_HEIGHT))
    """Draws the six lanes on the screen."""
    for i in range(NUM_LANES):
        x_pos = MARGIN + i * LANE_WIDTH
        lane_color = COLOR_BLUE_LANE if i < NUM_LANES//2 else COLOR_RED_LANE  # left vs right lanes
        pygame.draw.rect(screen, lane_color, (x_pos, MARGIN, LANE_WIDTH, HIT_ZONE_Y - MARGIN))
        if missed_lanes[i] > 0:
            pygame.draw.rect(screen, COLOR_RED_MISS, (x_pos, MARGIN, LANE_WIDTH, HIT_ZONE_Y - MARGIN))  # Missed lane effect
        pygame.draw.line(screen, COLOR_WHITE, (x_pos, MARGIN), (x_pos, SCREEN_HEIGHT - MARGIN), 2)
    # Draw rightmost white line for the last lane
    pygame.draw.line(screen, COLOR_WHITE, (MARGIN + NUM_LANES * LANE_WIDTH, MARGIN), (MARGIN + NUM_LANES * LANE_WIDTH, SCREEN_HEIGHT - MARGIN), 2)

def draw_notes():
    """Draws falling notes on the screen."""
    global notes, feedback_message, feedback_color, feedback_timer
    for note in notes:
        lane, y_pos = note[0], note[1]
        x_pos = MARGIN + lane * LANE_WIDTH + 10
        screen.blit(bread_image, (x_pos, y_pos))
    # move notes down
    for i in range(len(notes)):
        notes[i][1] += SPEED  # Move notes downward
        if notes[i][1] >= SCREEN_HEIGHT - MARGIN and not notes[i][2]:  # mark missed if not already marked
            notes[i][2] = True
            missed_lanes[notes[i][0]] = 10  # turn the lane red for 10 frames
            feedback_message = "Missed"
            feedback_color = COLOR_FEEDBACK_RED
            feedback_timer = 30  # Display for half a second
    # remove notes that go off the screen
    notes[:] = [note for note in notes if note[1] < SCREEN_HEIGHT - MARGIN + NOTE_HEIGHT]

# show score
def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, COLOR_WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 150, 20))

# show feedback message
def draw_feedback():
    global feedback_timer, feedback_message, feedback_color
    if feedback_timer > 0:
        font = pygame.font.Font(None, 48)
        text = font.render(feedback_message, True, feedback_color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(text, text_rect)
        feedback_timer -= 1
    else:
        feedback_message = ""

def check_hit(lane):
    """Checks if there is a note in the hit zone for the given lane."""
    global notes, score, feedback_message, feedback_color, feedback_timer
    for note in notes[:]:  # Iterate over a copy of the list
        if note[0] == lane:
            if HIT_ZONE_Y - HIT_BUFFER <= note[1] <= HIT_ZONE_Y + HIT_ZONE_HEIGHT:
                notes.remove(note)
                lane_to_quack[lane].play()
                if HIT_ZONE_Y <= note[1] <= HIT_ZONE_Y + HIT_ZONE_HEIGHT - HIT_BUFFER:
                    feedback_message = "Perfect"
                    feedback_color = COLOR_FEEDBACK_BLUE
                    score += 2
                else:
                    feedback_message = "Good"
                    feedback_color = COLOR_FEEDBACK_GREEN
                    score += 1
                feedback_timer = 30  # Display for half a second
                return

# game go brr
running = True # infinite loop
while running:
    screen.fill(COLOR_BLUE_LANE) #rgb fill screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # exit game
        # Keyboard controls for hitting notes
        if event.type == pygame.KEYDOWN and event.key in key_to_lane:
            check_hit(key_to_lane[event.key])
        # SNES controller button press handling
        if (joystick == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONDOWN) and event.button in snes_button_to_lane:
            check_hit(snes_button_to_lane[event.button])

    # Update missed lanes
    for lane in missed_lanes:
        if missed_lanes[lane] > 0:
            missed_lanes[lane] -= 1  # countdown red tint duration

    # draw methods here
    draw_board()
    draw_notes()
    draw_score()
    draw_feedback()

    pygame.display.update() # display update
    clock.tick(60) # 60fps