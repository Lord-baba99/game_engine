// --- shaders/fragment.glsl (mis à jour) ---
#version 330 core

// NOUVEAU: On reçoit la coordonnée de texture (interpolée par le GPU)
in vec2 v_texCoord;

// NOUVEAU: Le 'sampler2D' est notre image de texture.
uniform sampler2D u_texture;

out vec4 FragColor;

void main()
{
    // NOUVEAU: La couleur finale est la couleur de la texture à la coordonnée donnée.
    FragColor = texture(u_texture, v_texCoord);
}