import pygame
from pygame.surface import Surface


class Track:
    def __init__(self) -> None:
        # Define track boundaries (Clockwise order recommended)
        # x is distance from the left
        # y is distance from the top
        # the track should always be 60 pixels wide
        self.outer_coords: list[tuple[int, int]] = [
            # Curve 1 (Right Side) (Right Turn)
            (10, 690),
            (11, 625),
            (15, 575),
            (21, 525),
            (30, 475),
            (41, 425),
            (55, 375),
            (71, 325),
            (90, 275),
            (111, 225),
            # Turn 1 (Right Side) (Right Turn)
            (135, 175),
            (165, 125),
            (205, 85),
            (255, 55),
            (315, 35),
            # Straight 1 (Top)
            (380, 25),
            (450, 25),
            (550, 25),
            (1150, 25),
            # Hairpin 1 (Sharp) (Right Side) (Right Turn)
            (1207, 48),
            (1230, 105),
            (1207, 162),
            (1150, 185),
            # Downward Curve 2 (Right Side) (Left Turn)
            (1050, 190),
            (960, 210),
            (880, 245),
            (820, 295),
            # Upward Curve 3 (Middle Side) (Right Turn)
            (720, 335),
            (620, 345),
            (530, 325),
            (450, 285),
            (400, 225),
            # Hairpin 2 (gentle) (Left Side) (Left Turn)
            (384, 211),
            (354, 203),
            (324, 211),
            (302, 233),
            (294, 263),
            (302, 293),
            (324, 315),
            (354, 323),
            (400, 323),
            # Straight 2
            (450, 323),
            # Hairpin 2 (Sharp) (Right Turn)
            (507, 346),
            (530, 403),
            (507, 460),
            (450, 483),
            # Upward Curve 4 (Left Side) (Right Turn)
            (395, 479),
            (340, 470),
            (290, 460),
            (240, 445),
            # Hairpin 4 (Sharp) (Left Turn)
            (217, 434),
            (196, 443),
            (187, 464),
            (196, 485),
            # Straight 3
            (250, 525),
            # Serpentine 1 (Heading Right)
            (350, 565),
            (450, 525),
            (550, 565),
            (650, 525),
            (750, 565),
            (850, 525),
            (950, 565),
            # 90 Degree 1 (Left Turn)
            (1000, 565),
            (1000, 475),
            # 90 Degree 2 (Left Turn)
            (1000, 475),
            (850, 475),
            # Serpentine 2 (Heading Left)
            (850, 475),
            (750, 515),
            (650, 475),
            (550, 515),
            # 90 Degree 3 (Right Turn)
            (550, 515),
            (550, 350),
            # 90 Degree 4 (Right Turn)
            (800, 350),
            # Gentle Upward Curve (Left Turn)
            (830, 340),
            (860, 315),
            (900, 275),
            (950, 240),
            (1010, 215),
            (1080, 200),
            # Large Downward Curve (Right Turn)
            (1140, 210),
            (1200, 245),
            (1250, 305),
            (1270, 385),
            (1270, 475),
            (1250, 565),
            (1200, 635),
            (1150, 690),
            # Final Straight
            (10, 690),
        ]
        self.inner_coords: list[tuple[int, int]] = [
            # Curve 1 (Right Side) (Right Turn)
            (70, 630),
            (74, 580),
            (80, 533),
            (88, 486),
            (99, 439),
            (112, 392),
            (127, 344),
            (145, 297),
            # Turn 1 (Right Side) (Right Turn)
            (165, 249),
            (187, 203),
            (212, 161),
            (241, 132),
            (280, 109),
            (329, 93),
            # Straight 1 (Top)
            (384, 84),
            (450, 85),
            (550, 85),
            (1150, 85),
            # Sharp Hairpin 1 (Right Side) (Right Turn)
            (1164, 91),
            (1170, 105),
            (1164, 119),
            (1150, 125),
            # Downward Curve 2 (Right Side) (Left Turn)
            (1047, 130),
            (947, 152),
            (856, 191),
            (782, 249),
            # Upward Curve 3 (Middle Side) (Right Turn)
            (698, 280),
            (614, 286),
            (543, 267),
            (476, 232),
            (446, 187),
            # Hairpin 2 (gentle) (Left Side) (Left Turn)
            (414, 159),
            (354, 143),
            (294, 159),
            (250, 203),
            (234, 263),
            (250, 323),
            (294, 367),
            (354, 383),
            (400, 383),
            # Straight 2
            (450, 383),
            # Hairpin 3 (Sharp) (Right Turn)
            (464, 389),
            (470, 403),
            (464, 417),
            (450, 423),
            # Upward Curve 4 (Left Side) (Right Turn)
            (405, 419),
            (360, 410),
            (310, 400),
            (260, 385),
            # Hairpin 4 (Sharp) (Left Turn)
            (243, 380),
            (154, 401),
            (127, 464),
            (154, 527),
            # Straight 3
            (250, 585),
            # Serpentine 1 (Heading Right)
            (350, 625),
            (450, 585),
            (550, 625),
            (650, 585),
            (750, 625),
            (850, 585),
            (950, 625),
            # 90 Degree 1 (Left Turn)
            (1060, 625),
            (1060, 475),
            # 90 Degree 2 (Left Turn)
            (1060, 415),
            (850, 415),
            # Serpentine 2 (Heading Left)
            (850, 415),
            (750, 455),
            (650, 415),
            (600, 435),
            # 90 Degree 3 (Right Turn)
            (600, 435),
            (600, 410),
            # 90 Degree 4 (Right Turn)
            (800, 410),
            # Gentle Upward Curve (Left Turn)
            (845, 398),
            (890, 365),
            (935, 320),
            (985, 290),
            (1040, 270),
            (1100, 260),
            # Large Downward Curve (Right Turn)
            (1120, 270),
            (1170, 295),
            (1210, 345),
            (1210, 405),
            (1210, 475),
            (1190, 535),
            (1150, 595),
            (1100, 630),
            # Final Straight
            (70, 630),
        ]

        # Convert to segments for NEAT raycasting
        # Format: [((x1, y1), (x2, y2)), ...]
        self.walls: list[tuple[tuple[int, int], tuple[int, int]]] = []
        self._create_segments(self.outer_coords)
        self._create_segments(self.inner_coords)

    def _create_segments(self, coords: list[tuple[int, int]]) -> None:
        if len(coords) < 2:
            return
        for i in range(len(coords) - 1):
            # Connect current point to next point (no wrap around)
            p1: tuple[int, int] = coords[i]
            p2: tuple[int, int] = coords[i + 1]
            self.walls.append((p1, p2))

    def draw(self, screen: Surface) -> None:
        # Fill the track
        # pygame.draw.polygon(screen, (0, 0, 0), self.outer_coords)
        # pygame.draw.polygon(screen, BACKGROUND_COLOR, self.inner_coords)

        # Draw visible lines
        pygame.draw.lines(screen, (255, 255, 255), False, self.outer_coords, 3)
        pygame.draw.lines(screen, (255, 255, 255), False, self.inner_coords, 3)

        # Debug: Visualize start/end of a segment (Optional)
        # for start, end in self.walls:
        #     pygame.draw.circle(screen, (0, 255, 0), start, 5)

    def get_walls(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """Returns list of segments for the Car's raycasting logic"""
        return self.walls
