import argparse
import random
import typing as T

from render_engine import RenderEngine
from simulation import Circle, Simulation


def main():
    # ·window size, min/max circle radius values, spawn limit, gravity
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--size_x", type=int, default=800, help="Set width of window")
    parser.add_argument("-y", "--size_y", type=int, default=600, help="Set height of window")
    parser.add_argument("-min_rad", type=float, default=10, help="Set minimum radii of generated circles")
    parser.add_argument("-max_rad", type=float, default=50, help="Set maximum radii of generated circles")
    parser.add_argument("-spawn_limit", type=int, default=100, help="Set maximum number of circles to spawn")
    parser.add_argument("-gravity", type=float, default=9.8, help="Set value of gravity")
    p = parser.parse_args()

    # World attributes
    size_x, size_y = p.size_x, p.size_y
    gravity = p.gravity

    # Circle generation related attributes
    spawn_rate, spawn_timer = 1000.0, 0.0  # in ms
    spawn_count, spawn_max = 0, p.spawn_limit
    min_rad, max_rad = p.min_rad, p.max_rad

    object_pool = list()

    # Add objects
    for _ in range(spawn_max):
        rad = random.uniform(min_rad, max_rad)
        x, y = (
            random.uniform(rad + 10, size_x - rad - 10),
            random.uniform(size_y * 2 / 3, size_y - rad) - 10.0,
        )
        object_pool.append(
            Circle(
                (x, y),
                rad,
                velocity=(random.uniform(-300.0, 300.0), random.uniform(-500.0, -250.0)),
                acceleration=(0.0, -gravity),
                mass=5.0 + (rad / max_rad) * 10.0,
                restitution= 0.3 + (rad / max_rad) * 0.25,  # 0.9
            )
        )

    # Set up simulation
    sim = Simulation(size_x, size_y, gravity)
    render = RenderEngine(
        size_x, size_y, max_fps=60, hw_render=False, scale=1.0
    )
    render.create()

    # Main update loop
    prev_time = render.get_elapsed_time()
    while render.running:
        curr_time = render.get_elapsed_time()
        dt = (curr_time - prev_time)  # in ms
        prev_time = curr_time

        # Check if it's time to add a new circle
        if spawn_count < spawn_max:
            spawn_timer += dt
            if spawn_timer >= spawn_rate:
                sim.add_object(object_pool.pop())
                spawn_count += 1
                spawn_timer = 0

        # Update simulation
        # Update in multiple steps between renders
        # for _ in range(3):
        #     sim.update(dt / (1000.0 * 3))
        sim.update(dt / 1000.0)
        
        # Draw stuff
        render.clear()
        for c in sim.circles:
            (x, y) = c.position.astype(int).tolist()
            rad = c.radius.astype(int).item()
            render.draw_circle(x, y, rad)
            # color = int(15 + (c.mass / 11) * 238)
            # render.draw_circle(x, y, rad, color=(255, 0, 0, color))

        render.process_eventes()
        render.update()

        # Delay until next frame (if fps is capped)
        if render.frame_time > 0:
            if (
                elapsed_time := render.get_elapsed_time() - curr_time
            ) < render.frame_time:
                render.delay(render.frame_time - elapsed_time)


if __name__ == "__main__":
    main()
