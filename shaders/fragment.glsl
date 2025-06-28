// --- fragment.glsl ---
#version 330 core

// 'in' signifie qu'on reçoit cette donnée du vertex shader.
// OpenGL interpole automatiquement la couleur pour chaque pixel à l'intérieur du triangle.
in vec3 v_color;

// 'out' signifie que c'est la sortie finale de ce shader.
// 'FragColor' est le nom standard pour la couleur finale du pixel.
out vec4 FragColor;

void main()
{
    // On assigne la couleur reçue (et interpolée) à la couleur finale du pixel.
    // On met la composante alpha (transparence) à 1.0 (opaque).
    FragColor = vec4(v_color, 1.0);
}