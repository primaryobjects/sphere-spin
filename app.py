import pygame
from qiskit import QuantumCircuit, Aer, execute
from random import random
from math import pi, cos, sin, acos, atan2

# Set the tolerance for how close the player's qubit must be to the target qubit to win
TOLERANCE = 10

# Initialize Pygame
pygame.init()

# Set screen size
screen = pygame.display.set_mode((640, 480))

# Set the window title
pygame.display.set_caption("Sphere Spin")

# Set colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

angle = 0
is_win = False

# Create a quantum circuit with one qubit
qc = QuantumCircuit(1)

# Set the initial state of the qubit to a superposition of |0> and |1>
qc.h(0)

# Create a target qubit with a random state
target_qc = QuantumCircuit(1)
target_qc.ry(random() * 2 * pi, 0)

# Initialize the player's score
score = 1

# Create buttons
font = pygame.font.Font(None, 36)
increase_button = pygame.Rect(150, 400, 110, 50)
decrease_button = pygame.Rect(390, 400, 110, 50)
# Create a new button
x_button = pygame.Rect(270, 400, 110, 50)

def draw_firework(screen, color, frame):
    # Set the number of lines and the length of each line
    num_lines = 20
    line_length = 200

    # Calculate the angle between each line
    angle_step = 2 * pi / num_lines

    # Draw the lines
    for i in range(num_lines):
        angle = i * angle_step
        x1 = 320 + int(line_length * cos(angle))
        y1 = 240 - int(line_length * sin(angle))
        x2 = x1 + int(frame * cos(angle))
        y2 = y1 - int(frame * sin(angle))
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 3)

def draw():
    global target_qc, score, score_color, is_win

    # Run the circuit on a simulator and get the measurement probabilities
    backend = Aer.get_backend('statevector_simulator')
    result = execute(qc, backend).result()
    statevector = result.get_statevector()
    probabilities = [abs(amplitude)**2 for amplitude in statevector]

    is_win = False

    # Clear the screen
    screen.fill(white)

    # Calculate the color of the player's sphere based on the qubit's state
    player_color = (int(red[0] * probabilities[0] + blue[0] * probabilities[1]),
                    int(red[1] * probabilities[0] + blue[1] * probabilities[1]),
                    int(red[2] * probabilities[0] + blue[2] * probabilities[1]))

    # Run the target circuit on a simulator and get the measurement probabilities
    result = execute(target_qc, backend).result()
    target_statevector = result.get_statevector()
    target_probabilities = [abs(amplitude)**2 for amplitude in target_statevector]

    # Calculate the color of the target sphere based on the target qubit's state
    target_color = (int(red[0] * target_probabilities[0] + blue[0] * target_probabilities[1]),
                    int(red[1] * target_probabilities[0] + blue[1] * target_probabilities[1]),
                    int(red[2] * target_probabilities[0] + blue[2] * target_probabilities[1]))

    # Check if the player has won
    color_distance = sum((player_color[i] - target_color[i]) ** 2 for i in range(3)) ** 0.5
    print(color_distance)

    if color_distance <= TOLERANCE:
        win_text = font.render("You win!", True, black)
        screen.blit(win_text,
                    (320 - win_text.get_width() // 2,
                     360 - win_text.get_height() // 2))

        # Choose a new target qubit with a random state
        target_qc = QuantumCircuit(1)
        target_qc.ry(random() * 2 * pi, 0)
        is_win = True

    # Draw the spheres on the screen
    pygame.draw.circle(screen, player_color, (320, 240), 100)
    pygame.draw.circle(screen, target_color, (160, 180), 50)

    goal_text = font.render(f"Goal", True, white)
    screen.blit(goal_text,
                (159 - goal_text.get_width() // 2,
                179 - goal_text.get_height() // 2))

    # Set the position of the text
    text_x = 50
    text_y = 60

    # Draw the text
    text = "The ry and rx gates rotate the state of the qubit\naround the y-axis and x-axis on the Bloch sphere."
    text_lines = text.split("\n")
    for i, line in enumerate(text_lines):
        font1 = pygame.font.Font("freesansbold.ttf", 18)
        text_surface = font1.render(line, True, black)
        screen.blit(text_surface, (text_x, text_y + i * text_surface.get_height()))

    # Draw the Bloch sphere lines
    pygame.draw.circle(screen, black, (320, 240), 100, 1)
    pygame.draw.line(screen, black, (320, 140), (320, 340))
    pygame.draw.line(screen, black, (220, 240), (420, 240))

    # Calculate the position of the qubit on the Bloch sphere
    theta = 2 * acos(statevector[0])
    phi = -atan2(statevector[1].imag, statevector[1].real)
    x = sin(theta) * cos(phi)
    y = sin(theta) * sin(phi)
    z = cos(theta)

    # Draw a point at the position of the qubit
    point_x = int(320 + x * 100)
    point_y = int(240 - z * 100)
    pygame.draw.circle(screen, red, (point_x, point_y), 5)

    # Set the position and size of the chart
    chart_x = 500
    chart_y = 75
    chart_width = 100
    chart_height = 200

    # Draw the background of the chart
    pygame.draw.rect(screen, white, (chart_x, chart_y, chart_width, chart_height))

    # Draw the bars
    bar_width = chart_width // 2
    bar_margin = (chart_width - 2 * bar_width) // 3
    for i in range(2):
        bar_height = int(probabilities[i] * chart_height)
        bar_x = chart_x + bar_margin + i * (bar_width + bar_margin)
        bar_y = chart_y + chart_height - bar_height
        pygame.draw.rect(screen, [red, blue][i], (bar_x, bar_y, bar_width, bar_height))

    # Draw the labels
    label_text = ["|0>", "|1>"]
    for i in range(2):
        label = font.render(label_text[i], True, black)
        label_x = chart_x + bar_margin + i * (bar_width + bar_margin) + bar_width // 2 - label.get_width() // 2
        label_y = chart_y + chart_height + 10
        screen.blit(label, (label_x, label_y))

    # Draw the buttons
    pygame.draw.rect(screen, black, increase_button)
    increase_text = font.render("Rotate Y-", True, white)
    screen.blit(increase_text,
                (increase_button.centerx - increase_text.get_width() // 2,
                 increase_button.centery - increase_text.get_height() // 2))
    pygame.draw.rect(screen, black, decrease_button)
    decrease_text = font.render("Rotate Y+", True, white)
    screen.blit(decrease_text,
                (decrease_button.centerx - decrease_text.get_width() // 2,
                 decrease_button.centery - decrease_text.get_height() // 2))

    # Draw the new button
    pygame.draw.rect(screen, black, x_button)
    x_text = font.render("X", True, white)
    screen.blit(x_text,
                (x_button.centerx - x_text.get_width() // 2,
                x_button.centery - x_text.get_height() // 2))

    # Draw the score rectangle
    pygame.draw.rect(screen, score_color, (0, 0, 640, 50))

    # Draw the player's score
    score_text = font.render(f"Sphere Spin | Round: {score}", True, white)
    screen.blit(score_text,
                (320 - score_text.get_width() // 2,
                25 - score_text.get_height() // 2))

    # Update the screen
    pygame.display.flip()

score_color = (100, 100, 100)
draw()

def handle_mouse_event(event):
    if increase_button.collidepoint(event.pos):
        increase_probability()
    elif decrease_button.collidepoint(event.pos):
        decrease_probability()
    elif x_button.collidepoint(event.pos):
        rotate_x_up()

def handle_key_event(event):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        increase_probability()
    elif keys[pygame.K_DOWN]:
        decrease_probability()
    elif keys[pygame.K_RIGHT]:
        rotate_x_up()
    elif keys[pygame.K_LEFT]:
        rotate_x_down()

def increase_probability():
    global target_qc, score, score_color, angle, is_win
    qc.ry(-0.1, 0)
    draw()
    angle -= 0.1

def decrease_probability():
    global target_qc, score, score_color, angle, is_win
    qc.ry(0.1, 0)
    draw()
    angle += 0.1

def rotate_x_up():
    global target_qc, score, score_color, is_win
    qc.rx(0.1, 0)
    draw()

def rotate_x_down():
    global target_qc, score, score_color, is_win
    qc.rx(-0.1, 0)
    draw()

# Wait for the user to close the window or click a button
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_event(event)

    handle_key_event(None)

    if is_win:
        for frame in range(100):
            draw_firework(screen, (random() * 255, random() * 255, random() * 255), frame)
            pygame.display.flip()
            pygame.time.wait(10)

        # Update the player's score
        score += 1

        # Update score color.
        score_color = (random() * 255, random() * 255, random() * 255)
        draw()

# Quit Pygame
pygame.quit()