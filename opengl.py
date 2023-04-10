from cmath import pi
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from qiskit import QuantumCircuit, execute, Aer

# Create a quantum circuit with one qubit
qc = QuantumCircuit(1)

def measure():
    # Create a copy of the quantum circuit
    meas_circ = qc.copy()

    # Measure all qubits
    meas_circ.measure_all()

    # Execute the circuit on a simulator
    backend = Aer.get_backend('qasm_simulator')
    job = execute(meas_circ, backend, shots=100)
    result = job.result()

    # Get the counts of the measurement results
    counts = result.get_counts()

    # Calculate the probability of measuring 0 or 1
    prob_0 = counts.get('0', 0) / 100
    prob_1 = counts.get('1', 0) / 100

    # Use the probabilities to determine the color to display
    color = (prob_1, 0, prob_0) # RGB color tuple

    return color

def draw_operator(x, y, filename):
    # Load the image
    image = pygame.image.load(filename)
    image = pygame.transform.scale(image, (48, 48))

    # Draw the image on the screen
    screen = pygame.display.get_surface()
    screen.blit(image, (x - image.get_width() / 2, y - image.get_height() / 2))

# Initialize Pygame and set up the display
pygame.init()
display = (1200, 800)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

# Set up the perspective and camera
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -7)

color = measure()
target_color = (1, 0, 1) # Magenta

# Keep the window open until the user closes it
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse cursor
            x, y = pygame.mouse.get_pos()

            # Check which operator was clicked
            if x < display[0] / 2:
                # Apply an rx gate with a positive angle to rotate towards 0
                qc.rx(pi/8, 0)
            else:
                # Apply an rx gate with a negative angle to rotate towards 1
                qc.rx(-pi/8, 0)

            color = measure()

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    # Set the color of the first sphere
    glColor3fv(color)

    # Draw the first sphere
    glPushMatrix()
    glTranslatef(0.0, -1.5, 0.0)
    quadric = gluNewQuadric()
    gluSphere(quadric, 1, 32, 32)
    glPopMatrix()

    # Set the color of the second sphere (target color)
    glColor3fv(target_color)

    # Draw the second sphere (target color)
    glPushMatrix()
    glTranslatef(0.0, 1.5, 0.0)
    quadric = gluNewQuadric()
    gluSphere(quadric, 1, 32, 32)
    glPopMatrix()

    # Draw the operators
    draw_operator(50, 50, 'left.png')
    draw_operator(display[0] * 3/4, display[1] / 2, 'right.png')

    # Update the display
    pygame.display.flip()
    pygame.time.wait(10)