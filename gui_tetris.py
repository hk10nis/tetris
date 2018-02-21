#!/usr/bin/env python
#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys
from tetris import Tetris

#using class file tetris.py

class gui_tetris(Tetris):

    def __init__(self):
        super().__init__()
        self.timercount = 0
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
        #glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
        glutInitWindowSize(480, 800)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(b"TETRIS")
        self.init()
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutTimerFunc(100, self.gltTimer, 0);
        glutMainLoop()
        
        

    def draw_block(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.grid_display[i][j] == 1:
                    glColor3f(1.0, 0.0, 0.0)
                    glBegin(GL_QUADS)
                    glVertex2f(j, i)
                    glVertex2f(j, i+1)
                    glVertex2f(j+1, i+1)
                    glVertex2f(j+1, i)
                    glEnd()
                if self.grid_display[i][j] == 2:
                    glColor3f(1.0, 1.0, 0.0)
                    glBegin(GL_QUADS)
                    glVertex2f(j, i)
                    glVertex2f(j, i+1)
                    glVertex2f(j+1, i+1)
                    glVertex2f(j+1, i)
                    glEnd()
                if self.grid_display[i][j] == 3:
                    glColor3f(1.0, 0.0, 1.0)
                    glBegin(GL_QUADS)
                    glVertex2f(j, i)
                    glVertex2f(j, i+1)
                    glVertex2f(j+1, i+1)
                    glVertex2f(j+1, i)
                    glEnd()

    

    def init(self):
        glClearColor(0.0, 0.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0.0, 12.0, 21.0, 0.0)

    def gltTimer(self,arg):
        
        self.timercount = self.timercount + 1
        if self.timercount % 100 == 20:
            self.block_y = self.block_y + 1
            glutPostRedisplay()
        glutTimerFunc(10, self.gltTimer, 0)


    def keyboard(self,key,x,y):
        if key == b"q":
            sys.exit()
        else:
            super().move_block(key)
            glutPostRedisplay()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)
        super().execute_grid()
        self.draw_block()
        glFlush()
        #glutSwapBuffers()

if __name__ == "__main__":
    
    main = gui_tetris()
    