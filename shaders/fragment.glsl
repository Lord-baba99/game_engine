// --- shaders/fragment.glsl (mis à jour) ---
#version 330 core

in vec3 v_normal;
in vec3 v_fragPos;
in vec2 v_texCoord;

uniform sampler2D u_texture;
// NOUVEAU: Les propriétés de notre lumière et de notre caméra
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;

out vec4 FragColor;

void main()
{
    // --- Éclairage Ambiant ---
    // Une lumière de base pour que les zones sombres ne soient pas complètement noires.
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * lightColor;

    // --- Éclairage Diffus ---
    // Calcule la direction de la lumière (du fragment vers la source de lumière)
    vec3 lightDir = normalize(lightPos - v_fragPos);
    // Calcule l'impact de la lumière sur ce fragment (dot product)
    // max(..., 0.0) pour s'assurer de ne pas avoir de lumière négative
    float diff = max(dot(v_normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    // --- Couleur Finale ---
    // On récupère la couleur de base de l'objet depuis la texture
    vec4 texColor = texture(u_texture, v_texCoord);
    // Le résultat est la couleur de l'objet multipliée par la lumière calculée
    vec3 result = (ambient + diffuse) * texColor.rgb;
    
    FragColor = vec4(result, texColor.a);
}