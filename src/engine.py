import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import glm # NOUVEAU: Importer la bibliothèque glm

class Engine:
    def __init__(self):
        pygame.init()
        self.display = (800, 600)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Mon Moteur 3D - Phase 2")
        glClearColor(0.1, 0.2, 0.2, 1.0)

        # NOUVEAU: Activer le test de profondeur
        # Cela garantit que les triangles les plus proches cachent ceux qui sont derrière.
        glEnable(GL_DEPTH_TEST)

        self.shader = self.create_shader("shaders/vertex.glsl", "shaders/fragment.glsl")
        self.triangle_mesh = self.create_triangle_mesh()
        
        glUseProgram(self.shader)

        # NOUVEAU: Créer nos matrices de Vue et de Projection
        # Elles ne changent pas à chaque frame, donc on peut les définir ici.

        # Matrice de Vue (notre caméra)
        # On se place en (0, 0, -3), on regarde vers le centre (0, 0, 0),
        # et notre tête est orientée vers le haut (le vecteur "up" est (0, 1, 0)).
        view_matrix = glm.lookAt(glm.vec3(0, 0, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

        # Matrice de Projection (la perspective)
        # Champ de vision (FOV) de 45 degrés, ratio de la fenêtre,
        # distance de vue proche (0.1) et lointaine (100).
        projection_matrix = glm.perspective(glm.radians(45), self.display[0] / self.display[1], 0.1, 100.0)

        # NOUVEAU: Récupérer l'emplacement des uniforms dans le shader
        self.model_loc = glGetUniformLocation(self.shader, "model")
        self.view_loc = glGetUniformLocation(self.shader, "view")
        self.proj_loc = glGetUniformLocation(self.shader, "projection")

        # NOUVEAU: Envoyer les matrices qui ne changent pas au shader
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, np.array(view_matrix.to_list(), dtype=np.float32))
        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, np.array(projection_matrix.to_list(), dtype=np.float32))

    # ... (les fonctions create_shader et create_triangle_mesh ne changent pas) ...
    def create_shader(self, vertex_filepath, fragment_filepath):
        with open(vertex_filepath, 'r') as f:
            vertex_src = f.readlines()
        with open(fragment_filepath, 'r') as f:
            fragment_src = f.readlines()
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
        return shader

    def create_triangle_mesh(self):
        vertices = np.array([[-0.5, -0.5, 0.0], [0.5, -0.5, 0.0], [0.0, 0.5, 0.0]], dtype=np.float32)
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        return vao
    # ...

    def run(self):
        game_is_running = True
        while game_is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    game_is_running = False

            # --- Rendu ---
            # NOUVEAU: On efface aussi le buffer de profondeur
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # NOUVEAU: Calculer la matrice Modèle pour cette frame
            # On la fait tourner en fonction du temps qui passe
            time = pygame.time.get_ticks() / 1000 # temps en secondes
            model_matrix = glm.mat4(1.0) # Commence avec une matrice identité (pas de transformation)
            # Applique une rotation sur l'axe Y qui augmente avec le temps
            model_matrix = glm.rotate(model_matrix, time, glm.vec3(0, 1, 0))
            
            # NOUVEAU: Envoyer la matrice Modèle (qui change à chaque frame) au shader
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, np.array(model_matrix.to_list(), dtype=np.float32))

            glBindVertexArray(self.triangle_mesh)
            glDrawArrays(GL_TRIANGLES, 0, 3)

            pygame.display.flip()

        self.quit()

    def quit(self):
        glDeleteVertexArrays(1, (self.triangle_mesh,))
        glDeleteProgram(self.shader)
        pygame.quit()
        print("Moteur arrêté proprement.")

if __name__ == "__main__":
    mon_moteur = Engine()
    mon_moteur.run()