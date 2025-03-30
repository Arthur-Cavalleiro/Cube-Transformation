import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Definição dos vértices do cubo
vertices = [
    (0.5, -0.5, 0.5),   # A segunda coordenada (Y = -0.5) define a base inferior do cubo
    (-0.5, -0.5, 0.5),
    (0.5, 0.5, 0.5),    # A segunda coordenada (Y = 0.5) define o topo do cubo
    (-0.5, 0.5, 0.5),
    (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),
    (0.5, -0.5, -0.5),
    (-0.5, -0.5, -0.5),
    (0.5, 0.5, 0.5),
    (-0.5, 0.5, 0.5),
    (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),
    (0.5, -0.5, -0.5),
    (0.5, -0.5, 0.5),
    (-0.5, -0.5, 0.5),
    (-0.5, -0.5, -0.5),
    (-0.5, -0.5, 0.5),
    (-0.5, 0.5, 0.5),
    (-0.5, 0.5, -0.5),
    (-0.5, -0.5, -0.5),
    (0.5, -0.5, -0.5),
    (0.5, 0.5, -0.5),
    (0.5, 0.5, 0.5),
    (0.5, -0.5, 0.5)
]

# Índices para desenhar os triângulos (faces) do cubo
triangles = [
    0, 2, 3,  0, 3, 1,
    8, 4, 5,  8, 5, 9,
    10, 6, 7, 10, 7, 11,
    12, 13, 14, 12, 14, 15,
    16, 17, 18, 16, 18, 19,
    20, 21, 22, 20, 22, 23
]

def wireCube():
    """Desenha o cubo utilizando linhas para as arestas."""
    for i in range(0, len(triangles), 3):
        # Desenha a linha entre o primeiro e o segundo vértice
        glBegin(GL_LINES)
        glVertex3fv(vertices[triangles[i]])
        glVertex3fv(vertices[triangles[i+1]])
        glEnd()
        # Linha entre o segundo e o terceiro vértice
        glBegin(GL_LINES)
        glVertex3fv(vertices[triangles[i+1]])
        glVertex3fv(vertices[triangles[i+2]])
        glEnd()
        # Linha entre o terceiro e o primeiro vértice
        glBegin(GL_LINES)
        glVertex3fv(vertices[triangles[i+2]])
        glVertex3fv(vertices[triangles[i]])
        glEnd()

def initialise():
    """Configura o ambiente OpenGL e a projeção."""
    glClearColor(0, 0, 0, 1)
    glColor3f(1, 1, 1)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glEnable(GL_DEPTH_TEST)

def display():
    """Renderiza os dois cubos com as transformações:
       - Translação para posicioná-los lado a lado e com oscilação vertical;
       - Rotação (um no sentido horário e o outro anti-horário);
       - Espelhamento no cubo da direita;
       - Escala pulsante que aumenta e retorna ao tamanho padrão a cada 3 segundos.
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Escala pulsante: ciclo de 3 segundos
    default_scale = 1
    amplitude_scale = 0.8
    t_mod = pygame.time.get_ticks() % 3000  # 3000 ms = 3 segundos
    pulsating_scale = default_scale + amplitude_scale * math.sin(math.pi * t_mod / 3000)
    
    # Oscilação vertical: também com período de 3 segundos
    t = pygame.time.get_ticks() / 1000.0  # tempo em segundos
    vertical_amplitude = 0.5  # amplitude do movimento vertical
    period_y = 2.0  # período de 3 segundos
    vertical_offset = vertical_amplitude * math.sin(2 * math.pi * t / period_y)
    
    # --- Cubo da Esquerda: Rotação normal, escala pulsante e movimento vertical ---
    glPushMatrix()
    # Posiciona o cubo à esquerda, adicionando o deslocamento vertical
    # Mudamos 1.0 para -0.5 para posicionar o cubo mais abaixo
    glTranslatef(-2.0, 0 + vertical_offset, 0.0)
    glRotatef(pygame.time.get_ticks() * 0.05, 0, 1, 0)
    glScalef(pulsating_scale, pulsating_scale, pulsating_scale)  # Esta linha escala a altura
    wireCube()
    glPopMatrix()
    
    # --- Cubo da Direita: Espelhamento, rotação oposta, escala pulsante e movimento vertical ---
    glPushMatrix()
    # Posiciona o cubo à direita, também com deslocamento vertical
    # Mudamos 1.0 para -0.5 para posicionar o cubo mais abaixo
    glTranslatef(2.0, 0 + vertical_offset, 0.0)
    glRotatef(-pygame.time.get_ticks() * 0.05, 0, 1, 0)
    # Aplica espelhamento no eixo X e a escala pulsante
    glScalef(-pulsating_scale, pulsating_scale, pulsating_scale)  # Esta linha escala a altura
    wireCube()
    glPopMatrix()
    
    pygame.display.flip()

# Configurações da janela e inicialização do pygame
pygame.init()
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Cubos: Movimento Vertical com Espelhamento')

initialise()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    display()
    pygame.time.wait(10)

pygame.quit()