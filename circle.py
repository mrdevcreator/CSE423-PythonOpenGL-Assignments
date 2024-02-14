from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class MidpointCircle:
    def __init__(self):
        self.__radius = None
    def draw_point(self,x,y,center_x,center_y):
        glVertex2f(x + center_x, y + center_y)
        glVertex2f(y + center_x, x + center_y)

        glVertex2f(y + center_x, -x + center_y)
        glVertex2f(x + center_x, -y + center_y)

        glVertex2f(-x + center_x, -y + center_y)
        glVertex2f(-y + center_x, -x + center_y)

        glVertex2f(-y + center_x, x + center_y)
        glVertex2f(-x + center_x, y + center_y)


    def midpoint_circle_algorithm(self, radius, center_x=0.0, center_y=0.0, y=0):
        glBegin(GL_POINTS)
        glColor3f(1.0,0.0,0.0)
        d = 1 - radius
        x = 0
        y = radius
        self.draw_point(x,y,center_x,center_y)
       
        while x < y:
            if d < 0:
                d = d + 2 * x + 3
            else:
                d = d + 2 * x - 2 * y + 5
                y = y - 1
            x+=1
            self.draw_point(x,y,center_x,center_y)
        glEnd()
   

class Circle:
    WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
    def __init__(self):
        self.paused = False
        self.radius = 20
        self.increase = 1
        self.circle_center_points = []

    def handle_key(self, key, x, y):
        if key == b' ':
            self.paused = not self.paused

    def special_keys(self, key, x, y):
        if key == GLUT_KEY_LEFT and not self.paused:
            if self.increase<10:
              self.increase += 1 
             
        elif key == GLUT_KEY_RIGHT and not self.paused:
            if self.increase>1:
              self.increase -= 1
               
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.initialaize()
        midpoint_cir = MidpointCircle()
        for circle in self.circle_center_points:
          midpoint_cir.midpoint_circle_algorithm(circle['rad'],circle['center_x'], circle['center_y'])    
        glutSwapBuffers()

    def initialaize(self):
        glViewport(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.WINDOW_WIDTH, 0,self.WINDOW_HEIGHT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def animation(self):
        if not self.paused:
          circles_to_remove = []
          for circle in self.circle_center_points:
            circle['rad'] = (circle['rad']+self.increase)

            x_min = circle['center_x'] - circle['rad']
            x_max = circle['center_x'] + circle['rad']
            y_min = circle['center_y'] - circle['rad']
            y_max = circle['center_y'] + circle['rad']

            if x_min < 0 or x_max > self.WINDOW_WIDTH or y_min < 0 or y_max > self.WINDOW_HEIGHT:
                circles_to_remove.append(circle)
          for circle in circles_to_remove:
            self.circle_center_points.remove(circle)

        glutPostRedisplay()
 
    def mouse_callback(self,button, state, x, y):
      if (state == GLUT_DOWN):
        if not self.paused:
          center_x = x 
          center_y = y 
          self.circle_center_points.append({"rad":self.radius,'center_x': center_x, 'center_y': center_y})
        
    def main(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        glutCreateWindow("Catch the Diamonds!")
        glutDisplayFunc(self.display)
        glutIdleFunc(self.animation)
        glutMouseFunc(self.mouse_callback)
        glutKeyboardFunc(self.handle_key)
        glutSpecialFunc(self.special_keys)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glutMainLoop()

if __name__ == "__main__":
    circle_instance = Circle()
    circle_instance.main()


