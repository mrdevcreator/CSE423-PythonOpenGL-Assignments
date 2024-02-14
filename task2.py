from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from time import time
import random


points = []  
freeze_points = False   



def draw_point(x, y, color):
    glPointSize(5)
    glColor3f(*color)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_points():
    global points
    for i in points:
        x= i[0]
        y= i[1]
        color=i[2]
        draw_point(x, y, color)

def mouse_click(button, state, x, y):
    global blink_speed, points
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if not freeze_points:
              color = [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)]
              direction = (random.uniform(-1, 1), random.uniform(-1, 1))
            # Correct the y-coordinate by subtracting it from the window height
              y = glutGet(GLUT_WINDOW_HEIGHT) - y
              points.append([x, y, color, direction])
              glutPostRedisplay()
              
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if not freeze_points:
                pass



def update_points():
    for i in range(len(points)):
        x, y, color, direction = points[i]

        if not freeze_points:
            x += direction[0]  
            y += direction[1] 

            if x < 0:
                x = 800
            elif x > 800:
                x = 0
            if y < 0:
                y = 600
            elif y > 600:
                y = 0
            points[i] = (x, y, color, direction)
     

def keyboard(key, x, y):
    global freeze_points, blinking_states
    if key == b' ':
        freeze_points = not freeze_points
    elif key == b"d":
        if not freeze_points:
                blinking_states = not blinking_states
                

def special_key_pressed(key, x, y):
    if key == GLUT_KEY_UP:
        blink_speed +=0.2          
    elif key == GLUT_KEY_DOWN:
        blink_speed -=0.2       
    

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 800.0, 0.0, 600.0)
    if not freeze_points:
        draw_points()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Amazing Box")
glutDisplayFunc(draw)
glutMouseFunc(mouse_click)
glutIdleFunc(update_points)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_key_pressed)
glutMainLoop()
