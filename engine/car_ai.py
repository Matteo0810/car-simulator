from abc import ABC, abstractmethod


class AI(ABC):
    @abstractmethod
    def get_wheel_speed(self, world, car):
        pass
    
    @abstractmethod
    def get_steer_angle(self, world, car):
        pass
    
    @abstractmethod
    def is_braking(self, world, car):
        pass
    
    # pas une méthode abstraite !
    def pre_tick(self):
        pass
