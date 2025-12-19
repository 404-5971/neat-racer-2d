import pygame
from pygame import QUIT, Surface
from pygame.key import ScancodeWrapper

from car import Car
from track import Track

BACKGROUND_COLOR: tuple[int, int, int] = (50, 50, 50)


def main() -> None:
    pygame.init()
    screen: Surface = pygame.display.set_mode((1280, 720))
    clock: pygame.time.Clock = pygame.time.Clock()
    running: bool = True

    track = Track()
    car = Car()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        track.draw(screen)

        keys: ScancodeWrapper = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.steering_direction = "Left"
            car.steering_power = car.max_steering_power
        elif keys[pygame.K_RIGHT]:
            car.steering_direction = "Right"
            car.steering_power = car.max_steering_power
        else:
            car.steering_power = 0.0

        if keys[pygame.K_UP]:
            car.acceleration = car.max_acceleration
        else:
            car.acceleration = 0.0
            if keys[pygame.K_DOWN]:
                car.braking_power = car.max_braking_power
            else:
                car.braking_power = 0.0

        track_walls: list[tuple[tuple[int, int], tuple[int, int]]] = track.get_walls()

        car.update()

        car.draw(screen)

        # Drawing these is completely optional
        car.draw_raycast_lines(screen, track_walls)
        car.draw_raycast_hits(screen, track_walls)

        if car.check_death(track_walls):
            running = False

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
