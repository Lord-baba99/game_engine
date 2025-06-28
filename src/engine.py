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
        # ... initialisation de pygame et de la fenêtre ...
        pygame.init()
        self.display = (800, 600)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Mon Moteur 3D - Phase 3 (Éclairage)")
        glClearColor(0.1, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)

        self.shader = self.create_shader("shaders/vertex.glsl", "shaders/fragment.glsl")
        self.triangle_mesh = self.create_triangle_mesh()
        self.texture = self.load_texture(os.path.join(BASE_DIR, "assets/PNG/Dark/texture_09.png"))
        
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "u_texture"), 0)

        # NOUVEAU: Définir les propriétés de la lumière et de la caméra
        self.lightPos = glm.vec3(2, 5, 2)
        self.cameraPos = glm.vec3(0, 0, 3)

        view_matrix = glm.lookAt(self.cameraPos, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
        projection_matrix = glm.perspective(glm.radians(45), self.display[0] / self.display[1], 0.1, 100.0)
        
        # Récupérer les emplacements des uniforms
        self.model_loc = glGetUniformLocation(self.shader, "model")
        self.view_loc = glGetUniformLocation(self.shader, "view")
        self.proj_loc = glGetUniformLocation(self.shader, "projection")
        # NOUVEAU: Emplacements pour les nouvelles variables
        self.light_pos_loc = glGetUniformLocation(self.shader, "lightPos")
        self.view_pos_loc = glGetUniformLocation(self.shader, "viewPos")
        self.normal_matrix_loc = glGetUniformLocation(self.shader, "normalMatrix")

        # Envoyer les matrices qui ne changent pas (ou peu)
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, glm.value_ptr(view_matrix))
        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, glm.value_ptr(projection_matrix))
        # NOUVEAU: Envoyer les données de lumière et de caméra
        glUniform3fv(self.light_pos_loc, 1, glm.value_ptr(self.lightPos))
        glUniform3fv(self.view_pos_loc, 1, glm.value_ptr(self.cameraPos))
        glUniform3fv(glGetUniformLocation(self.shader, "lightColor"), 1, glm.value_ptr(glm.vec3(1, 1, 1))) # Lumière blanche

    def create_shader(self, vertex_filepath, fragment_filepath):
        # (cette fonction ne change pas)
        with open(vertex_filepath, 'r') as f: vertex_src = f.readlines()
        with open(fragment_filepath, 'r') as f: fragment_src = f.readlines()
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
        return shader

    def create_triangle_mesh(self):
        # MODIFIÉ: Les données de sommet incluent position, normale et coordonnée de texture
        vertices = np.array(
            [
            # Position        # Normale         # TexCoords
            -0.5, -0.5, 0.0,  0.0, 0.0, 1.0,  0.0, 0.0,
             0.5, -0.5, 0.0,  0.0, 0.0, 1.0,  1.0, 0.0,
             0.0,  0.5, 0.0,  0.0, 0.0, 1.0,  0.5, 1.0
            ],
            dtype=np.float32
        )
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        stride = 8 * vertices.itemsize
        # Attribut Position (location = 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # Attribut Normale (location = 1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * vertices.itemsize))
        glEnableVertexAttribArray(1)
        # Attribut Coordonnée de Texture (location = 2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * vertices.itemsize))
        glEnableVertexAttribArray(2)
        return vao

    def load_texture(self, filepath):
        # (cette fonction ne change pas)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = Image.open(filepath).convert("RGBA")
        img_data = np.array(list(image.getdata()), np.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return texture_id

    def run(self):
        game_is_running = True
        while game_is_running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    game_is_running = False

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            time = pygame.time.get_ticks() / 1000
            model_matrix = glm.rotate(glm.mat4(1.0), time, glm.vec3(0, 1, 0))
            
            # NOUVEAU: Calculer et envoyer la matrice des normales
            # C'est la transposée inverse de la matrice modèle (partie 3x3).
            # C'est la manière mathématiquement correcte de transformer les normales.
            normal_matrix = glm.transpose(glm.inverse(glm.mat3(model_matrix)))

            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, glm.value_ptr(model_matrix))
            glUniformMatrix3fv(self.normal_matrix_loc, 1, GL_FALSE, glm.value_ptr(normal_matrix))

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            
            glBindVertexArray(self.triangle_mesh)
            glDrawArrays(GL_TRIANGLES, 0, 3)

            pygame.display.flip()

        self.quit()
    
    def quit(self):
        # ... (la fonction quit ne change que par l'ajout de la suppression de la texture)...
        glDeleteTextures(1, (self.texture,))
        glDeleteVertexArrays(1, (self.triangle_mesh,))
        glDeleteProgram(self.shader)
        pygame.quit()
        print("Moteur arrêté proprement.")

if __name__ == "__main__":
    mon_moteur = Engine()
    mon_moteur.run()