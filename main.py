import pyglet

window = pyglet.window.Window(800, 600, "Hello 3D Game Engine")

@window.event
def on_draw():
    window.clear()
    # Ici, vous pouvez dessiner vos objets 3D

if __name__ == "__main__":
    pyglet.app.run()
