import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy

aresta = 2
m_aresta = 0.5 * aresta

n_bolas = 15
raio = 0.15

delta_t = 0.1

pos = []
vel = []

for i in range(0, n_bolas):
    #Define a posição inicial de cada bolinha (x,y,z) 
    r1 = (random.random()-0.5)
    r2 = (random.random()-0.5)  
    r3 = (random.random()-0.5)
    #Coloca os valores na 'string' de componentes de posicao
    r = numpy.array([r1,r2,r3])
    #Como a posicao inicial como velocidade inicial eh um valor muito alto multiplica-se por 0.4  
    v = numpy.array([r1*0.3,r2*0.3,r3*0.3])
    #velociade fica em media (mas com excecoes) entre 0.1 e 0.01
    pos.append(r) #adiciona a stack de pos
    vel.append(v) #adiciona a stack de vel

#Produto escalar algebrico
def p_escalar(v1,v2):
    return v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]

#Retorna o modulo da 'coisa'
def modulo(coisa):
    return math.sqrt(p_escalar(coisa,coisa))

#Calcula distancia entre duas particulas
def dist(r1,r2):
    return modulo((pos[r1]-pos[r2]))

def repulsao(a,b):
    d = pos[b]-pos[a]
    #print(d)
    v_med = (vel[b] + vel[a])/2.0
    #se v1 for negativo entao a conlisao vai acontecer???
    v1 = vel[a] - v_med
    v2 = vel[b] - v_med
    v_dr = p_escalar(v1,d)
    # como d e v1 devem ser neg pra colidir o prod escalar eh positivo >0
    if v_dr > 0:
        vel[b] = v_med + v2 + 2 * v1
        vel[a] = v_med + v1 - 2 * v1
        #print("colidiu")
    
def colisao():
    for i in range(0,n_bolas-1):
        for j in range(i+1, n_bolas):
            if dist(i,j) < (raio*2):
                 repulsao(i,j)

def parede():
    for i in range(0,n_bolas):
        for j in range(0,3):
            if pos[i][j] > m_aresta - raio:
                 vel[i][j] = (-1) * vel[i][j]
            if pos[i][j] < -m_aresta + raio:
                 vel[i][j] = (-1) * vel[i][j]

def atualiza():
    v = 0.0
    for i in range(0, n_bolas):
        pos[i] += vel[i] * delta_t
    colisao()
    parede()
    

vert = (
    (-m_aresta, -m_aresta, m_aresta),
    (-m_aresta, m_aresta, m_aresta),
    (m_aresta, -m_aresta, m_aresta),
    (m_aresta, m_aresta, m_aresta),
    (-m_aresta, -m_aresta, -m_aresta),
    (-m_aresta, m_aresta, -m_aresta),
    (m_aresta, -m_aresta, -m_aresta),
    (m_aresta, m_aresta, -m_aresta)
    )

edges = (
    (0,1),
    (0,2),
    (0,4),
    (3,1),
    (3,2),
    (3,7),
    (5,1),
    (5,4),
    (5,7),
    (6,2),
    (6,4),
    (6,7),
    )

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vert[vertex])
    glEnd()

quad = gluNewQuadric()
gluQuadricDrawStyle(quad, GLU_FILL)
gluQuadricTexture(quad, GL_TRUE)
gluQuadricNormals(quad, GL_SMOOTH)

def Sphere():
    for i in range(0, n_bolas):
        glPushMatrix()
        #glTranslatef(random.uniform(-1+raio,1-raio),random.uniform(-1+raio,1-raio),random.uniform(-1+raio,1-raio))
        glTranslatef(pos[i][0], pos[i][1], pos[i][2])
        #glColor3fv((0,1,0))
        gluSphere(quad, raio, 50, 50)
        glPopMatrix()
        
def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    gluPerspective(35, (display[0]/display[1]), 0.1, 50)
    glTranslatef(0,0.05, -5)

    light_pos = ( 1, 1, 1, 1.0)
    light_ambient = (1.5,1.5,1.5,1.0)
    light_diffuse = (2.0,2.0,2.0,1.0)
    light_specular = (2.0,0.0,0.0,0.0)

    glLightfv(GL_LIGHT0, GL_POSITION,light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT,light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE,light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR,light_specular)
    
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    
    glRotatef(5, 1, 1, 0)

    time = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        atualiza()
        time += 1
        
        if time % 1 == 0:
            Cube()
            Sphere()
            
            pygame.display.flip()
            time = 0 

        pygame.time.wait(10)

main()
