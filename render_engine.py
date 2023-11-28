import sdl2
import sdl2.ext
import sdl2.sdlgfx


class RenderEngine:
    def __init__(self, w=800, h=600, max_fps=0, hw_render=False, scale=1.0):
        self.w = w
        self.h = h
        self.frame_time = 1000 // max_fps if max_fps > 0 else 0
        self.hw_render = hw_render
        self.scale = scale
        self.running = False

    def create(self):
        sdl2.ext.init()
        window = sdl2.ext.Window(b"Circles", size=(self.w, self.h))
        window.show()

        if self.hw_render:
            render_flags = (
                sdl2.render.SDL_RENDERER_ACCELERATED
                | sdl2.render.SDL_RENDERER_PRESENTVSYNC
            )
        else:
            render_flags = sdl2.render.SDL_RENDERER_SOFTWARE
        self.ctx = sdl2.ext.Renderer(window, flags=render_flags)

        info = sdl2.render.SDL_RendererInfo()
        sdl2.SDL_GetRendererInfo(self.ctx.sdlrenderer, info)

        self.ctx.present()
        self.running = True

    def clear(self):
        self.ctx.clear(0xFFFFFFFF)

    def update(self):
        self.ctx.present()

    def process_eventes(self):
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                self.running = False
                break

    def draw_circle(self, x, y, radius, color=(255, 0, 0, 255)): # color = 0xFF0000FF
        if (sdl2.sdlgfx.circleColor(self.ctx.sdlrenderer, x, self.h - y, radius, sdl2.ext.Color(*color)) == -1):
            print(f"Error in draw_circle: (x: {x}, y: {y}, radius: {radius}, color: {color})")

    # in ms
    def get_elapsed_time(self):
        return sdl2.SDL_GetTicks()

    def delay(self, delay_ms):
        sdl2.SDL_Delay(delay_ms)

    # def draw_circles(self, positions, radius, color = (255, 0, 0, 255)):
    #     for pos in positions:
    #         sdl2.sdlgfx.circleColor(self.ctx, pos[0], pos[1], radius, color)
