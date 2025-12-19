import math
from typing import Literal

import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface


def get_line_intersection(
    p1: Vector2, p2: Vector2, p3: Vector2, p4: Vector2
) -> Vector2 | None:
    """
    Calculates intersection between line segment p1-p2 and p3-p4.
    Returns the Vector2 point of intersection or None.
    """
    denominator: float = (p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y)
    if denominator == 0:
        return None  # Parallel lines

    unit_a: float = (
        (p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x)
    ) / denominator
    unit_b: float = (
        (p2.x - p1.x) * (p1.y - p3.y) - (p2.y - p1.y) * (p1.x - p3.x)
    ) / denominator

    if 0 <= unit_a <= 1 and 0 <= unit_b <= 1:
        # Return the actual intersection point
        return Vector2(p1.x + unit_a * (p2.x - p1.x), p1.y + unit_a * (p2.y - p1.y))
    return None


class Car:
    def __init__(self) -> None:
        self.size: tuple[int, int] = (35, 20)
        self.position: tuple[float, float] = (15.0, 640.0)

        # positive is left, negative is right
        self._rotation: float = 90.0
        self._center: tuple[float, float] = (self.size[0] // 2, self.size[1] // 2)

        self.acceleration: float = 0.0
        self.max_acceleration: float = 0.2
        self.friction: float = 0.05

        self.speed: float = 0.0
        self.max_speed: float = 10.0

        self.braking_power: float = 0.0
        self.max_braking_power: float = 0.5

        self.steering_power: float = 0.0
        self.max_steering_power: float = 10.0
        self.steering_direction: Literal["Left", "Right"] = "Right"

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, value: float) -> None:
        self._rotation = (value + 180) % 360 - 180

    @property
    def center(self) -> tuple[float, float]:
        return self._center

    def draw(self, screen: Surface) -> None:
        # Create a surface for the car
        car_surface: Surface = Surface(self.size, pygame.SRCALPHA)
        car_surface.fill((255, 0, 0))

        # Draw a green dot on the front (right side)
        pygame.draw.circle(
            car_surface, (0, 255, 0), (self.size[0] - 5, self.center[1]), 5
        )

        # Draw a white dot in the center
        pygame.draw.circle(car_surface, (255, 255, 255), self.center, 5)

        # Rotate the surface
        rotated_surface: Surface = pygame.transform.rotate(car_surface, self.rotation)

        # Get the rect of the rotated surface and center it at the car's position
        center: tuple[float, float] = (
            self.position[0] + self.center[0],
            self.position[1] + self.center[1],
        )
        rotated_rect: Rect = rotated_surface.get_rect(center=center)

        screen.blit(rotated_surface, rotated_rect)

    def update(self) -> None:
        match self.steering_direction:
            case "Left":
                self.rotation += self.steering_power
            case "Right":
                self.rotation -= self.steering_power

        self.speed += self.acceleration

        if self.speed > 0:
            self.speed -= self.friction
            if self.speed < 0:
                self.speed = 0

        elif self.speed < 0:
            self.speed = 0

        if self.speed > self.max_speed:
            self.speed = self.max_speed

        if self.braking_power > 0:
            self.speed -= self.braking_power
            if self.speed < 0:
                self.speed = 0

        # we need to travel the direction of our rotation
        radians: float = math.radians(self.rotation)
        dx: float = self.speed * math.cos(radians)
        dy: float = self.speed * math.sin(radians)
        self.position = (self.position[0] + dx, self.position[1] - dy)

    def get_raycast_hits(
        self,
        walls: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> list[Vector2 | None]:
        center: Vector2 = Vector2(self.position) + Vector2(self.center)
        ray_length: int = 100
        hit_list: list[Vector2 | None] = []

        # Cast 16 rays
        for i in range(16):
            # Create a vector pointing right, then rotate it
            ray_direction: Vector2 = Vector2(ray_length, 0).rotate(i * 22.5)
            ray_end: Vector2 = center + ray_direction

            hit_point: Vector2 | None = None
            min_dist_sq: float = float("inf")  # Use squared distance for performance

            for start, end in walls:
                wall_start: Vector2 = Vector2(start)
                wall_end: Vector2 = Vector2(end)
                hit: Vector2 | None = get_line_intersection(
                    wall_start, wall_end, center, ray_end
                )

                if hit:
                    # compare squared distances to avoid costly sqrt calls
                    dist_sq: float = center.distance_squared_to(hit)
                    if dist_sq < min_dist_sq:
                        min_dist_sq = dist_sq
                        hit_point = hit

            hit_list.append(hit_point)

        return hit_list

    def draw_raycast_hits(
        self,
        screen: pygame.Surface,
        walls: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        for hit in self.get_raycast_hits(walls):
            if hit:
                pygame.draw.circle(screen, (255, 0, 0), (int(hit.x), int(hit.y)), 3)

    def draw_raycast_lines(
        self,
        screen: pygame.Surface,
        walls: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        center: Vector2 = Vector2(self.position) + Vector2(self.center)
        ray_length: int = 100
        hit_list: list[Vector2 | None] = []

        # Cast 16 rays
        for i in range(16):
            # Create a vector pointing right, then rotate it
            ray_direction: Vector2 = Vector2(ray_length, 0).rotate(i * 22.5)
            ray_end: Vector2 = center + ray_direction

            hit_point: Vector2 | None = None
            min_dist_sq: float = float("inf")  # Use squared distance for performance

            for start, end in walls:
                wall_start: Vector2 = Vector2(start)
                wall_end: Vector2 = Vector2(end)
                hit: Vector2 | None = get_line_intersection(
                    wall_start, wall_end, center, ray_end
                )

                if hit:
                    # compare squared distances to avoid costly sqrt calls
                    dist_sq: float = center.distance_squared_to(hit)
                    if dist_sq < min_dist_sq:
                        min_dist_sq = dist_sq
                        hit_point = hit

            hit_list.append(hit_point)

        for hit in hit_list:
            if hit:
                pygame.draw.line(screen, (255, 255, 255), center, hit, 1)

    def check_death(self, walls: list[tuple[tuple[int, int], tuple[int, int]]]) -> bool:
        center: Vector2 = Vector2(self.position) + Vector2(self.center)
        width: int = self.size[0]
        height: int = self.size[1]

        # Define unrotated corners relative to (0,0)
        # Top-Left, Top-Right, Bottom-Right, Bottom-Left
        corners_rel: list[Vector2] = [
            Vector2(-width / 2, -height / 2),
            Vector2(width / 2, -height / 2),
            Vector2(width / 2, height / 2),
            Vector2(-width / 2, height / 2),
        ]

        # Rotate all corners by car's rotation and shift to absolute position
        # Note: Pygame rotation is typically negative degrees for clockwise
        corners: list[Vector2] = [
            c.rotate(-self.rotation) + center for c in corners_rel
        ]

        for start, end in walls:
            wall_start: Vector2 = Vector2(start)
            wall_end: Vector2 = Vector2(end)

            # Check every edge of the car against every wall
            for i in range(4):
                p1: Vector2 = corners[i]
                p2: Vector2 = corners[(i + 1) % 4]  # Connects back to 0 at the end

                if get_line_intersection(wall_start, wall_end, p1, p2):
                    return True

        return False
