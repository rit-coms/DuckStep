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
# (player variables)
playerX, playerY = 400, 300  # Initial player position
playerX_change, playerY_change = 0, 0

# Placeholder for notes (lane_num, y_position); gonna make csv later
notes = [
    [0, 100], [1, 200], [2, 300], [3, 400], [4, 500], [5, 600]
]

# def draw methods to draw stuff on to the screen
def draw_board():
    """Draws the six lanes on the screen."""
    for i in range(1, 6):
        pygame.draw.line(screen, (255, 255, 255), (i * LANE_WIDTH, 0), (i * LANE_WIDTH, SCREEN_HEIGHT), 2)

def draw_notes():
    """Draws falling notes on the screen."""
    for note in notes:
        lane, y_pos = note
        pygame.draw.rect(screen, (255, 0, 0), (lane * LANE_WIDTH + 10, y_pos, LANE_WIDTH - 20, NOTE_HEIGHT))
        note[1] += 5  # Move notes downward

# game go brr
running = True # infinite loop
while running:
    screen.fill((50,60,70)) #rgb fill screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # exit game

        # is controller pluged in
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joy.init()
            print(f"Controller connected: {joy.get_name()}")
            print(f"Number of buttons: {joy.get_numbuttons()}")
            # done

        # movement with controller buttons
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # X button
                playerY_change = -5
            if event.button == 1:  # A button
                playerX_change = 5
            if event.button == 2:  # B button
                playerY_change = 5
            if event.button == 3:  # Y button
                playerX_change = -5
            if event.button == 8:  # Select button
                running = False

        # Stops continuous movement when button is lifted (Controller)
        if event.type == pygame.JOYBUTTONUP:
            if event.button in [0, 2]:
                playerY_change = 0
            if event.button in [1, 3]:
                playerX_change = 0


        # D-pad Controls (Goofy setup)
        if event.type == pygame.JOYAXISMOTION:
            print(event)
            if event.axis == 0:  # Left/Right movement
                if event.value < -0.5:
                    playerX_change = -5
                elif event.value > 0.5:
                    playerX_change = 5
                else:
                    playerX_change = 0
            if event.axis == 1:  # Up/Down movement
                if event.value < -0.5:
                    playerY_change = -5
                elif event.value > 0.5:
                    playerY_change = 5
                else:
                    playerY_change = 0

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_LEFT:
                playerX_change = -5

        # Stops continuous movement when button is lifted (Keyboard)
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                playerY_change = 0
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                playerX_change = 0

    # Changes player position 
    playerX += playerX_change
    playerY += playerY_change

    # Game bounds 
    playerX = max(0, min(768, playerX))
    playerY = max(0, min(568, playerY))

    # draw methods here
    draw_board()
    draw_notes()

    # update gui
    pygame.display.update()
    # Framerate 60 fps
    clock.tick(60)