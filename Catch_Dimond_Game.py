from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

class MidpointLine:
    def __init__(self):
        self.__midpoint_points = []

    def find_zone(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1

        if abs(dx) > abs(dy):
            if dx >= 0 and dy >= 0:
                return 0
            elif dx <= 0 and dy >= 0:
                return 3
            elif dx <= 0 and dy <= 0:
                return 4
            elif dx >= 0 and dy <= 0:
                return 7
        else:
            if dx >= 0 and dy >= 0:
                return 1
            elif dx <= 0 and dy >= 0:
                return 2
            elif dx <= 0 and dy <= 0:
                return 5
            elif dx >= 0 and dy <= 0:
                return 6

    def convert_to_zone0(self, x1, y1, zone):
        if zone == 0:
            return x1, y1
        elif zone == 1:
            return y1, x1
        elif zone == 2:
            return y1, -x1
        elif zone == 3:
            return -x1, y1
        elif zone == 4:
            return -x1, -y1
        elif zone == 5:
            return -y1, -x1
        elif zone == 6:
            return -y1, x1
        elif zone == 7:
            return x1, -y1

    def convert_to_original_zone(self, x1, y1, zone):

        if zone == 0:
            return x1, y1
        elif zone == 1:
            return y1, x1
        elif zone == 2:
            return -y1, x1
        elif zone == 3:
            return -x1, y1
        elif zone == 4:
            return -x1, -y1
        elif zone == 5:
            return -y1, -x1
        elif zone == 6:
            return y1, -x1
        elif zone == 7:
            return x1, -y1

    def midpoint(self, x1, y1, x2, y2,color):
        glBegin(GL_POINTS)
        glColor3f(*color)
            
        zone = self.find_zone(x1, y1, x2, y2)

        x1_to_z0, y1_to_z0 = self.convert_to_zone0(x1, y1, zone)
        x2_to_z0, y2_to_z0 = self.convert_to_zone0(x2, y2, zone)

        dy = y2_to_z0 - y1_to_z0
        dx = x2_to_z0 - x1_to_z0
        d = 2 * dy - dx
        d_E = 2 * dy
        d_NE = 2 * (dy - dx)

        x = x1_to_z0
        y = y1_to_z0

        original_x, original_y = self.convert_to_original_zone(x, y, zone)
        glVertex2f(original_x, original_y)

        while x <= x2_to_z0:
            self.__midpoint_points.append((original_x, original_y))

            if d < 0:
                x = x + 1
                d = d + d_E
            else:
                x = x + 1
                y = y + 1
                d = d + d_NE

            original_x, original_y = self.convert_to_original_zone(x, y, zone)
            glVertex2f(original_x, original_y)

        glEnd()

class MidpointCircle:
    def __init__(self):
        self.__radius = None
        self.__center_x = None
        self.__center_y = None
        self.__midpoint_points = []

    def set_circle_values(self, radius, center_x=0, center_y=0):
        self.__radius = radius
        self.__center_x = center_x
        self.__center_y = center_y

    def convert_to_other_zone(self, x1, y1, zone):
        if zone == 0:
            return x1, y1
        elif zone == 1:
            return y1, x1
        elif zone == 2:
            return -y1, x1
        elif zone == 3:
            return -x1, y1
        elif zone == 4:
            return -x1, -y1
        elif zone == 5:
            return -y1, -x1
        elif zone == 6:
            return y1, -x1
        elif zone == 7:
            return x1, -y1

    def midpoint_circle_algorithm(self, radius, center_x=0.0, center_y=0.0, y=0):
        glBegin(GL_POINTS)
        
        d = 1 - radius
        
        x = radius
        glVertex2f(x + center_x, y + center_y)

        for i in range(8):
            x_other, y_other = self.convert_to_other_zone(x, y, i)
            glVertex2f(x_other + center_x, y_other + center_y)

        while x > y:
            if d < 0:
                y = y + 1
                d = d + 2 * y + 3
            else:
                x = x - 1
                y = y + 1
                d = d + 2 * y - 2 * x + 5

            self.__midpoint_points.append((x, y))

            glVertex2f(x + center_x, y + center_y)

            for i in range(8):
                x_other, y_other = self.convert_to_other_zone(x, y, i)
                self.__midpoint_points.append((x_other, y_other))
                glVertex2f(x_other + center_x, y_other + center_y)

        glEnd()

    def filled_circle(self, radius, center_x=0, center_y=0):
        for i in range(radius):
            self.midpoint_circle_algorithm(radius, center_x, center_y)
            #self.midpoint_circle_algorithm(i, center_x, center_y)

class Game:
    WINDOW_WIDTH, WINDOW_HEIGHT = 650, 700
    CATCHER_WIDTH, CATCHER_HEIGHT = 75, 12
    DIAMOND_SIZE = 24

    def __init__(self):
        self.catcher_x = (self.WINDOW_WIDTH - self.CATCHER_WIDTH) // 2
        self.catcher_y = self.WINDOW_HEIGHT - (self.WINDOW_HEIGHT - 20)
        self.diamond_x, self.diamond_y = random.randint(1, self.WINDOW_WIDTH - self.DIAMOND_SIZE), (
                    self.WINDOW_HEIGHT - 100)
        self.diamond_speed = 1.0
        self.score = 0
        self.game_over = False
        self.paused = False

    def is_point_inside(self,x, y,button_type):
        if button_type == "x":
            x2,y2 = 628,25
        elif button_type == "||":
            x2,y2 = 322,25
        else:
            x2,y2 = 20,25

        if ((x-x2)**2)+((y-y2)**2) <= (22**2):
          return True
        else:
          return False

    def draw_x(self, midpoint_line):
        color = [1.0, 0.0, 0.0]

        x1, y1 = self.WINDOW_WIDTH - 35, self.WINDOW_HEIGHT - 35
        x2, y2 = self.WINDOW_WIDTH - 8, self.WINDOW_HEIGHT - 8
        midpoint_line.midpoint(x1, y1, x2, y2, color)

        x3, y3 = self.WINDOW_WIDTH - 35, self.WINDOW_HEIGHT - 8
        x4, y4 = self.WINDOW_WIDTH - 8, self.WINDOW_HEIGHT - 35
        midpoint_line.midpoint(x3, y3, x4, y4, color)

    def draw_arrow(self, midpoint_line):
        color = [0.0, 1.0, 0.0]
        x1, y1 = self.WINDOW_WIDTH - (self.WINDOW_WIDTH - 25), self.WINDOW_HEIGHT - 9
        x2, y2 = self.WINDOW_WIDTH - (self.WINDOW_WIDTH - 25), self.WINDOW_HEIGHT - 35

        x3, y3 = self.WINDOW_WIDTH - (self.WINDOW_WIDTH - 8), self.WINDOW_HEIGHT - 22
        midpoint_line.midpoint(x1, y1, x3, y3, color)
        midpoint_line.midpoint(x3 - 0.2, y3 - 0.2, x2, y2, color)
        midpoint_line.midpoint(x3, y3, x2 + 20, y3, color)

    def draw_button(self, midpoint_line, is_play):
        color = [0.9, 0.5, 0.3]

        if not is_play:
            x1, y1 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) - 6), self.WINDOW_HEIGHT - 8
            x2, y2 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) - 6), self.WINDOW_HEIGHT - 35
            midpoint_line.midpoint(x1, y1, x2, y2, color)

            x3, y3 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) + 6), self.WINDOW_HEIGHT - 8
            x4, y4 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) + 6), self.WINDOW_HEIGHT - 36
            midpoint_line.midpoint(x3, y3, x4, y4, color)
        else:
            x1, y1 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) + 15), self.WINDOW_HEIGHT - 8
            x2, y2 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) + 15), self.WINDOW_HEIGHT - 36
            midpoint_line.midpoint(x1, y1, x2, y2, color)

            x3, y3 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) - 15), self.WINDOW_HEIGHT - 22
            midpoint_line.midpoint(x1, y1, x3, y3, color)
            midpoint_line.midpoint(x3, y3, x2 - 0.5, y2 - 0.5, color)

    def draw_catcher(self, midpoint_line):
        if not self.game_over:
            color = [1.0, 1.0, 1.0]
        else:
            color = [1.0, 0.0, 0.0]

        x1, y1 = self.catcher_x - 5, self.catcher_y + self.CATCHER_HEIGHT
        x2, y2 = self.catcher_x + self.CATCHER_WIDTH + 5, self.catcher_y + self.CATCHER_HEIGHT
        midpoint_line.midpoint(x1, y1, x2, y2, color)
        x3, y3 = self.catcher_x + 1, self.catcher_y
        x4, y4 = self.catcher_x + self.CATCHER_WIDTH - 1, self.catcher_y
        midpoint_line.midpoint(x3, y3, x4, y4, color)
        midpoint_line.midpoint(x1, y1, x3, y3, color)
        midpoint_line.midpoint(x2, y2, x4, y4, color)

    def draw_diamond(self, midpoint_line):
        color = [random.uniform(.7, 1.0), random.uniform(.6, .8), random.uniform(.2, .4)]
       
        x1, y1 = self.diamond_x + self.DIAMOND_SIZE // 2, self.diamond_y + 5

        x2, y2 = self.diamond_x, self.diamond_y - self.DIAMOND_SIZE // 2
        midpoint_line.midpoint(x1, y1, x2, y2, color)

        x3, y3 = self.diamond_x + self.DIAMOND_SIZE // 2, self.diamond_y - (self.DIAMOND_SIZE + 5)
        midpoint_line.midpoint(x2, y2, x3, y3, color)

        x4, y4 = self.diamond_x + self.DIAMOND_SIZE, self.diamond_y - self.DIAMOND_SIZE // 2
        midpoint_line.midpoint(x3, y3, x4, y4, color)

        midpoint_line.midpoint(x4, y4, x1, y1, color)

    def has_collided(self, box1, box2):
        return box1[0] < box2[0] + box2[2] and \
               box1[0] + box1[2] > box2[0] and \
               box1[1] < box2[1] + box2[3] and \
               box1[1] + box1[3] > box2[1]
    
    def draw_game_over_text(self):
        sc = str(self.score)
        new_sc = "Game Over! Your score is " + sc
        x, y = self.WINDOW_WIDTH // 2 - 130, self.WINDOW_HEIGHT // 2
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos2i(x, y)
        rainbow_colors = [(1.0, 0.0, 0.0)]
        color_index = 0

        for character in new_sc:
          glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(character))
          
    def draw_cir(self,midpoint_cir):
        #midpoint_cir.set_circle_values(200, self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)  
        midpoint_cir.filled_circle(200, self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)


    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.reshape()
        if self.game_over:
          midpoint_line = MidpointLine()
          midpoint_cir = MidpointCircle()
          self.draw_game_over_text()
          self.draw_x(midpoint_line)
          self.draw_button(midpoint_line, self.paused)
          self.draw_arrow(midpoint_line)
          self.draw_cir(midpoint_cir)
          glutSwapBuffers()
          return

    
        if not self.game_over and not self.paused:
            self.diamond_y -= self.diamond_speed
            if (self.diamond_y+self.DIAMOND_SIZE) < 0:
                self.game_over = True
                print("Game over!! Restart.....")
            else:
                if self.has_collided([self.catcher_x, (self.catcher_y+self.CATCHER_HEIGHT), self.CATCHER_WIDTH, self.CATCHER_HEIGHT],
                                     [self.diamond_x, (self.diamond_y-self.DIAMOND_SIZE), self.DIAMOND_SIZE, self.DIAMOND_SIZE]):
                    self.score += 1
                    print("Score:", self.score)
                    self.diamond_y = (self.WINDOW_HEIGHT - 10)
                    self.diamond_x = random.randint(1, self.WINDOW_WIDTH - self.DIAMOND_SIZE)
                    self.diamond_speed += 0.1

        midpoint_line = MidpointLine()
        self.draw_catcher(midpoint_line)
        self.draw_diamond(midpoint_line)
        self.draw_x(midpoint_line)
        self.draw_button(midpoint_line, self.paused)
        self.draw_arrow(midpoint_line)

        glutSwapBuffers()

    def reshape(self):
        glViewport(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.WINDOW_WIDTH, 0,self.WINDOW_HEIGHT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def special_keys(self, key, x, y):
        if self.score==5:
          speed = 12
        elif self.score==10:
          speed = 14
        elif self.score==15:
          speed = 15
        else:
            speed = 10
            
        if key == GLUT_KEY_LEFT and self.catcher_x > 0 and not self.game_over and not self.paused:
            self.catcher_x -= speed
        elif key == GLUT_KEY_RIGHT and self.catcher_x < self.WINDOW_WIDTH - self.CATCHER_WIDTH and not self.game_over and not self.paused:
            self.catcher_x += speed

    def update(self, value):
        glutPostRedisplay()
        glutTimerFunc(16, self.update, 0) 

    def mouse_callback(self,button, state, x, y):
      if (state == GLUT_DOWN):
        if self.is_point_inside(x,y,"x"):
          glutDestroyWindow(glutGetWindow())
          print(f"Goodbye")
        elif self.is_point_inside(x,y,"||"):
            self.paused = not self.paused
        elif self.is_point_inside(x,y,"<-"):
            print("Starting Over !")
            self.game_over = False
            self.paused = False
            self.diamond_speed = 1.0
            self.score = 0
            self.catcher_x = (self.WINDOW_WIDTH - self.CATCHER_WIDTH) // 2
            self.catcher_y = self.WINDOW_HEIGHT - (self.WINDOW_HEIGHT - 20)
            self.diamond_x, self.diamond_y = random.randint(1, self.WINDOW_WIDTH - self.DIAMOND_SIZE), (
                        self.WINDOW_HEIGHT - 10)

 

    def main(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        glutCreateWindow("Catch the Diamonds!")
        glutDisplayFunc(self.display)
        glutSpecialFunc(self.special_keys)
        glutMouseFunc(self.mouse_callback)
        glutTimerFunc(25, self.update, 0) 
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glutMainLoop()

if __name__ == "__main__":
    game_instance = Game()
    game_instance.main()
