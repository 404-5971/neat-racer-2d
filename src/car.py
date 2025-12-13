import math
from typing import Literal

import pygame
from pygame.rect import Rect
from pygame.surface import Surface


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

    def draw_raycasts(
        self, screen: Surface, walls: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        # Draw 16 raycasts
        number_of_rays: int = 16
        ray_length: int = 100
        center: tuple[float, float] = (
            self.position[0] + self.center[0],
            self.position[1] + self.center[1],
        )
        for i in range(number_of_rays):
            angle: float = math.radians(i * 22.5)
            dx: float = ray_length * math.cos(angle)
            dy: float = ray_length * math.sin(angle)
            end_pos: tuple[float, float] = (center[0] + dx, center[1] + dy)
            pygame.draw.line(screen, (255, 255, 255), center, end_pos, 1)

            # Check for intersection with walls
            closest_intersection: tuple[float, float] | None = None
            min_dist: float = float("inf")

            for wall_start, wall_end in walls:
                x1, y1 = wall_start
                x2, y2 = wall_end
                x3, y3 = center
                x4, y4 = end_pos

                denom: float = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
                if denom == 0:
                    continue

                ua: float = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
                ub: float = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

                if 0 <= ua <= 1 and 0 <= ub <= 1:
                    intersection_x: float = x1 + ua * (x2 - x1)
                    intersection_y: float = y1 + ua * (y2 - y1)
                    dist: float = math.hypot(
                        intersection_x - center[0], intersection_y - center[1]
                    )
                    if dist < min_dist:
                        min_dist = dist
                        closest_intersection = (intersection_x, intersection_y)

            if closest_intersection:
                pygame.draw.circle(screen, (255, 0, 0), closest_intersection, 3)

    def check_death(self, walls: list[tuple[tuple[int, int], tuple[int, int]]]) -> bool:
        # Calculate car corners
        cx, cy = self.position[0] + self.center[0], self.position[1] + self.center[1]
        w, h = self.size
        hw, hh = w / 2, h / 2

        # Corners relative to center
        relative_corners: list[tuple[float, float]] = [
            (-hw, -hh),
            (hw, -hh),
            (hw, hh),
            (-hw, hh),
        ]

        rad: float = math.radians(self.rotation)
        cos_a: float = math.cos(rad)
        sin_a: float = math.sin(rad)

        corners: list[tuple[float, float]] = []
        for rx, ry in relative_corners:
            # Screen space rotation
            rot_x: float = rx * cos_a + ry * sin_a
            rot_y: float = -rx * sin_a + ry * cos_a
            corners.append((cx + rot_x, cy + rot_y))

        # Check intersection with walls
        for wall_start, wall_end in walls:
            x1, y1 = wall_start
            x2, y2 = wall_end

            for i in range(4):
                x3, y3 = corners[i]
                x4, y4 = corners[(i + 1) % 4]

                denom: float = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
                if denom == 0:
                    continue

                ua: float = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
                ub: float = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

                if 0 <= ua <= 1 and 0 <= ub <= 1:
                    return True

        return False
