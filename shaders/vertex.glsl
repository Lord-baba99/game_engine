// --- shaders/vertex.glsl (mis à jour) ---
#version 330 core

layout (location = 0) in vec3 a_position;

// NOUVEAU: Les matrices de transformation.
// 'uniform' signifie que c'est une variable globale qu'on envoie depuis Python.
// Elle est la même pour tous les sommets qu'on dessine en une fois.
uniform mat4 model;      // La matrice pour positionner/orienter notre objet dans le monde
uniform mat4 view;       // La matrice pour positionner la caméra
uniform mat4 projection; // La matrice pour créer la perspective

out vec3 v_color;

void main()
{
    // NOUVEAU: La transformation 3D !
    // L'ordre est crucial : d'abord le modèle, puis la vue, puis la projection.
    // Le résultat est la position finale du sommet sur l'écran.
    gl_Position = projection * view * model * vec4(a_position, 1.0);

    // On garde la même astuce pour la couleur pour l'instant.
    v_color = a_position * 0.5 + 0.5;
}