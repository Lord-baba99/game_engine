// --- shaders/vertex.glsl (mis à jour) ---
#version 330 core

layout (location = 0) in vec3 a_position;
// NOUVEAU: Accepter la normale (location = 1)
layout (location = 1) in vec3 a_normal;
// Les coordonnées de texture passent à la location 2
layout (location = 2) in vec2 a_texCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
// NOUVEAU: La matrice spéciale pour transformer les normales
uniform mat3 normalMatrix;

// NOUVEAU: Passer la position et la normale transformées au fragment shader
out vec3 v_normal;
out vec3 v_fragPos; // Position du fragment dans l'espace "monde"
out vec2 v_texCoord;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    
    // NOUVEAU: Calculer la position du sommet dans le monde et la passer
    v_fragPos = vec3(model * vec4(a_position, 1.0));
    
    // NOUVEAU: Transformer la normale et la passer
    // On la normalise pour s'assurer qu'elle reste de longueur 1.
    v_normal = normalize(normalMatrix * a_normal);

    v_texCoord = a_texCoord;
}