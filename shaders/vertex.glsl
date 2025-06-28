// --- shaders/vertex.glsl (mis à jour) ---
#version 330 core

layout (location = 0) in vec3 a_position;
// NOUVEAU: Accepter les coordonnées de texture (location = 1)
layout (location = 1) in vec2 a_texCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// NOUVEAU: Passer les coordonnées de texture au fragment shader
out vec2 v_texCoord;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    
    // NOUVEAU: On passe simplement la coordonnée de texture à l'étape suivante.
    v_texCoord = a_texCoord;
}