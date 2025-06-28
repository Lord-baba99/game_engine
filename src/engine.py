import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import glm
from PIL import Image # NOUVEAU: Importer Pillow
import os
# NOUVEAU: Définir le répertoire de base pour les ressources
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Engine:
    def __init__(self):
        pygame.init()
        self.display = (800, 600)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Mon Moteur 3D - Phase 3 (Textures)")
        glClearColor(0.1, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)

        self.shader = self.create_shader("shaders/vertex.glsl", "shaders/fragment.glsl")
        self.triangle_mesh = self.create_triangle_mesh()
        
        # NOUVEAU: Charger notre texture
        self.texture = self.load_texture(os.path.join(BASE_DIR, "assets/PNG/Dark/texture_09.png"))

        glUseProgram(self.shader)

        # NOUVEAU: Dire au shader d'utiliser notre texture
        # On lie la texture à l'unité de texture 0
        glUniform1i(glGetUniformLocation(self.shader, "u_texture"), 0)

        # Création des matrices (identique à la Phase 2)
        view_matrix = glm.lookAt(glm.vec3(0, 0, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
        projection_matrix = glm.perspective(glm.radians(45), self.display[0] / self.display[1], 0.1, 100.0)
        self.model_loc = glGetUniformLocation(self.shader, "model")
        self.view_loc = glGetUniformLocation(self.shader, "view")
        self.proj_loc = glGetUniformLocation(self.shader, "projection")
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, glm.value_ptr(view_matrix))
        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, glm.value_ptr(projection_matrix))

    def create_shader(self, vertex_filepath, fragment_filepath):
        # (cette fonction ne change pas)
        with open(vertex_filepath, 'r') as f: vertex_src = f.readlines()
        with open(fragment_filepath, 'r') as f: fragment_src = f.readlines()
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
        return shader

    def create_triangle_mesh(self):
        # MODIFIÉ: Les données des sommets incluent maintenant la position (x, y, z) ET les coordonnées de texture (u, v)
        vertices = np.array(
            [
            # Position      # TexCoords
            -0.5, -0.5, 0.0,  0.0, 0.0, # Sommet 1: en bas à gauche
             0.5, -0.5, 0.0,  1.0, 0.0, # Sommet 2: en bas à droite
             0.0,  0.5, 0.0,  0.5, 1.0  # Sommet 3: en haut au centre
            ],
            dtype=np.float32
        )

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # MODIFIÉ: On doit maintenant décrire DEUX attributs
        
        # Attribut de Position (location = 0)
        # Il commence au début (offset 0)
        # Chaque sommet complet fait 5 floats de large (stride)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # Attribut de Coordonnée de Texture (location = 1)
        # Il commence après les 3 floats de la position (offset 3)
        # Chaque sommet complet fait toujours 5 floats de large (stride)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))
        glEnableVertexAttribArray(1)
        
        return vao

    def load_texture(self, filepath):
        # NOUVEAU: Fonction pour charger une image et l'envoyer au GPU
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        # Définir les paramètres de la texture
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # Charger l'image avec Pillow
        image = Image.open(filepath).convert("RGBA")
        img_data = np.array(list(image.getdata()), np.uint8)
        
        # Envoyer les données de l'image au GPU
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        return texture_id

    def run(self):
        game_is_running = True
        while game_is_running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    game_is_running = False

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Calcul de la matrice modèle (identique à la Phase 2)
            time = pygame.time.get_ticks() / 1000
            model_matrix = glm.rotate(glm.mat4(1.0), time, glm.vec3(0, 1, 0))
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, glm.value_ptr(model_matrix))

            # NOUVEAU: Activer notre texture avant de dessiner
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            
            glBindVertexArray(self.triangle_mesh)
            glDrawArrays(GL_TRIANGLES, 0, 3)

            pygame.display.flip()

        self.quit()

    def quit(self):
        # NOUVEAU: Détruire la texture
        glDeleteTextures(1, (self.texture,))
        glDeleteVertexArrays(1, (self.triangle_mesh,))
        glDeleteProgram(self.shader)
        pygame.quit()
        print("Moteur arrêté proprement.")

if __name__ == "__main__":
    mon_moteur = Engine()
    mon_moteur.run()