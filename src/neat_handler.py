import neat
from neat import genome

from car import Car


class NeatCar:
    def __init__(self, car: Car, genome: genome) -> None:
        self.car = car
        self.genome = genome
