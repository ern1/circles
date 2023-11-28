import numpy as np

class Circle:
    dtype = np.dtype(
        [
            ("position", float, 2),
            ("radius", float),
            ("velocity", float, 2),
            ("acceleration", float, 2),
            ("mass", float),
            ("restitution", float),
        ]
    )

    def __init__(self, position, radius, velocity, acceleration, mass, restitution):
        self._data = np.array(
            (
                np.array(position),
                np.float64(radius),
                np.array(velocity),
                np.array(acceleration),
                np.float64(mass),
                np.float64(restitution),
            ),
            dtype=self.dtype,
        )

    @property
    def position(self):
        return self._data["position"]

    @property
    def radius(self):
        return self._data["radius"]

    @property
    def velocity(self):
        return self._data["velocity"]

    @property
    def acceleration(self):
        return self._data["acceleration"]

    @property
    def mass(self):
        return self._data["mass"]

    @property
    def inverse_mass(self):
        return 1 / self._data["mass"]

    @property
    def restitution(self):
        return self._data["restitution"]

    def check_collision_rectangle(self, rec):
        cl, cr, cb, ct = (
            self.position[0] - self.radius,
            self.position[0] + self.radius,
            self.position[1] - self.radius,
            self.position[1] + self.radius,
        )
        rl, rr, rb, rt = (
            rec.position[0],
            rec.position[0] + rec.width,
            rec.position[1],
            rec.position[1] + rec.height,
        )

        if cl < rl:
            return 0
        elif cr > rr:
            return 0
        elif cb < rb:
            return 1
        elif ct > rt:
            return 1
        return None

    def handle_collision_rectangle(self, rec, coll_axis):
        self._data["velocity"][coll_axis] *= -1.0
        self._data["velocity"] = self._data["velocity"] * self.restitution

        # Keep circle inside rectangle
        # self._data["position"][coll_axis] += coll_depth
        np.clip(
            self._data["position"],
            self.radius + 0.001,
            [rec.width - self.radius, rec.height - self.radius],
            out=self._data["position"],
        )

    def check_collision_circle(self, c2):
        distance = np.linalg.norm(self.position - c2.position)
        sum_radius = self.radius + c2.radius

        return distance <= sum_radius

    def handle_collision_circle(self, c2):
        # Calculate the relative position and velocity
        rel_pos = c2.position - self.position
        dist = np.linalg.norm(rel_pos)

        # Calculate the collision normal and tangential vectors
        collision_normal = rel_pos / dist  # from self to c2
        collision_tangent = np.array([-collision_normal[1], collision_normal[0]])

        # Calculate the components of the velocities along the normal and tangential directions
        vel1_normal = np.dot(self.velocity, collision_normal)
        vel2_normal = np.dot(c2.velocity, collision_normal)
        vel1_tangent = np.dot(self.velocity, collision_tangent)
        vel2_tangent = np.dot(c2.velocity, collision_tangent)

        # Calculate the new velocities along the normal direction after collision
        restitution = np.minimum(self.restitution, c2.restitution)
        rel_mass = self.mass + c2.mass
        new_vel1_normal = (
            (self.mass - c2.mass) * vel1_normal
            + (1 + restitution) * c2.mass * vel2_normal
        ) / (self.mass + c2.mass)
        new_vel2_normal = (
            (c2.mass - self.mass) * vel2_normal
            + (1 + restitution) * self.mass * vel1_normal
        ) / (self.mass + c2.mass)

        # Update velocities
        new_vel1 = new_vel1_normal * collision_normal + vel1_tangent * collision_tangent
        new_vel2 = new_vel2_normal * collision_normal + vel2_tangent * collision_tangent
        np.put(self._data["velocity"], [0, 1], new_vel1)
        np.put(c2._data["velocity"], [0, 1], new_vel2)

        # move circles apart from each other relative to their weigth (to not overlap)
        coll_depth = (self.radius + c2.radius) - dist
        self._data["position"] -= self.mass / rel_mass * coll_depth * collision_normal
        c2._data["position"] += c2.mass / rel_mass * coll_depth * collision_normal

    def move(self, dt):
        self._data["velocity"] += (
            self.acceleration * self.mass * dt
        )  # Todo: how to decrease acceleration with velocity? (or something...)
        self._data["position"] += self.velocity * dt


class Rectangle:
    dtype = np.dtype(
        [
            ("position", float, 2),
            ("width", float),
            ("height", float),
        ]
    )

    def __init__(self, position, width, height):
        self._data = np.array(
            (np.array(position), np.float64(width), np.float64(height)),
            dtype=self.dtype,
        )

    @property
    def position(self):
        return self._data["position"]

    @property
    def width(self):
        return self._data["width"]

    @property
    def height(self):
        return self._data["height"]


class Simulation:
    def __init__(self, size_x, size_y, gravity=1):
        self.gravity = gravity
        self.size_x = size_x
        self.size_y = size_y

        self.world_aabb = Rectangle(
            (0, 0), size_x, size_y
        )  # Bounding box for the world

        self.circles = list()  # dynamic objects
        # self.circle_array = np.array([], dtype=Circle.dtype)

    def add_object(self, circle):
        self.circles.append(circle)

    def update(self, dt):
        # Check and handle collisions
        for c1 in self.circles:
            coll_axis = c1.check_collision_rectangle(self.world_aabb)
            if coll_axis is not None:
                c1.handle_collision_rectangle(self.world_aabb, coll_axis)

        # circle-circle collisions
        circles = list(self.circles)
        while circles:
            c1 = circles.pop()
            for c2 in circles:
                if c1.check_collision_circle(c2):
                    c1.handle_collision_circle(c2)

        # Move circles
        for c in self.circles:
            c.move(dt)
