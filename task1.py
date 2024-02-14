from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


rain_direction = 0 
light = 1.0

def is_point_inside_polygon(x, y):
    vertices = [(92, 300), (200, 400), (308, 300)]

    crossings = 0
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]

        if y1 != y2:
            if y <= min(y1, y2):
                continue
            if y > max(y1, y2):
                continue
            if x <= max(x1, x2):
                if y1 != y2:
                    x_inters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                    if x <= x_inters:
                        crossings += 1

    return crossings % 2 == 1

def draw_house():
    if light > 0.5:
        glColor3f(0.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)

    glLineWidth(14)
    glBegin(GL_LINES)

    glVertex2i(99, 100)
    glVertex2i(301, 100)

    glVertex2i(298, 100)
    glVertex2i(298, 300)

    glVertex2i(308, 300)
    glVertex2i(92, 300)

    glVertex2i(102, 300)
    glVertex2i(102, 100)

    glVertex2i(92, 300)
    glVertex2i(200, 400)

    glVertex2i(200, 400)
    glVertex2i(308, 300)
    glEnd()
    
    draw_door()
    draw_window()

def draw_door():
    glLineWidth(4)
    glBegin(GL_LINES)
    glVertex2i(135, 100)
    glVertex2i(135, 238)

    glVertex2i(135, 238)
    glVertex2i(185, 238)

    glVertex2i(185, 238)
    glVertex2i(185, 100)
    glEnd()

    glPointSize(8) 
    glBegin(GL_POINTS)
    glVertex2f(175.0,169.0) 
 
    glEnd()

def draw_window():
    glLineWidth(4)
    glBegin(GL_LINES)

    glVertex2i(235, 185)
    glVertex2i(235, 225)

    glVertex2i(235, 225)
    glVertex2i(270, 225)

    glVertex2i(270, 225)
    glVertex2i(270, 185)

    glVertex2i(270, 185)
    glVertex2i(235, 185)
     
    glEnd()
    
    glLineWidth(2)
    glBegin(GL_LINES)
  
    glVertex2f(252.5, 185.0)
    glVertex2f(252.5, 225.0)

    glEnd()

    glPointSize(7) 
    glBegin(GL_POINTS)
    glVertex2f(247.0,205.0) 
    glVertex2f(258.0,205.0) 
    glEnd()

def draw_rain():
    if light > 0.5:
        glColor3f(0.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2)

    house_base_x1 = 92
    house_base_x2 = 308
    house_base_y1 = 100
    house_base_y2 = 300

    house_roof_x1 = 92
    house_roof_x2 = 308
    house_roof_y2 = 400

    raindrop_lengths = [8, 10, 12]
    i = 0

    for x in range(60, 345, 8):
        for y in range(500, 250, -20):
            if not (house_base_x1 <= x <= house_base_x2 and
                    house_base_y1 <= y <= house_base_y2 and
                    house_roof_x1 <= x <= house_roof_x2 and
                    y <= house_roof_y2) and not is_point_inside_polygon(x, y):

                glBegin(GL_LINES)
                raindrop_length = raindrop_lengths[i]

                if rain_direction == -1:
                    glVertex2f(x, y)
                    glVertex2f(x - 5, y - raindrop_length)
                elif rain_direction == 1:
                    glVertex2f(x, y)
                    glVertex2f(x + 5, y - raindrop_length)
                else:
                    glVertex2f(x, y)
                    glVertex2f(x, y - raindrop_length)

                glEnd()

                i = (i + 1) % len(raindrop_lengths)                 

def iterate():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 500.0, 0.0, 500.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClearColor(light,light,light,1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    iterate()
    draw_house()
    draw_rain()
    glutSwapBuffers()

def key_pressed(key, x, y):
    global light
    if key == b'd':
        light += 0.2
        if light > 1.0:
            light = 1.0
    elif key == b'n':
        light -= 0.2
        if light < 0.0:
            light = 0.0

def special_key_pressed(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction = -1          
    elif key == GLUT_KEY_RIGHT:
        rain_direction = 1      
    else:
        rain_direction = 0
        

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(900, 700)
glutInitWindowPosition(0, 10)
wind = glutCreateWindow(b"House in Rainfall")
glutDisplayFunc(showScreen)
glutKeyboardFunc(key_pressed)
glutSpecialFunc(special_key_pressed)
glutIdleFunc(showScreen)
glutMainLoop()
