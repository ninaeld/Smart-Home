#Solar Panel class, where instances of solar panels are created
import config
from threading import Lock

class SolarPanel:

    def __init__(self, area, angle, orientation, efficiency):
        self.lock = Lock()
        self.area = area
        self.angle = angle
        self.orientation = orientation
        self.efficiency = efficiency

    @property
    def area(self):
        return self._area
    @area.setter
    def area(self, value):
        self.lock.acquire()
        #make sure of type float and that the area isn't smaller than 0
        if not isinstance(value, float):
            self.lock.release()
            raise TypeError("Area is of wrong type")
        if (value < 0):
            self.lock.release()
            raise ValueError("Area can't be negative")
        self._area = value
        self.lock.release()

    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, value):
        self.lock.acquire()
        #angle should be of type int and not smaller than 0 and not bigger than 90 degrees
        if not isinstance(value, int):
            self.lock.release()
            raise TypeError("Angle is of wrong type")
        if (value < 0 or value > 90):
            self.lock.release()
            raise ValueError("Angle can't be smaller than 0 or bigger than 90 degrees")
        self._angle = value
        self.lock.release()

    @property
    def orientation(self):
        return self._orientation
    @orientation.setter
    def orientation(self, value):
        self.lock.acquire()
        #make sure of right type and of right value
        if not isinstance(value, str):
            self.lock.release()
            raise TypeError("Orientation is of wrong Type")
        if not (value == "East" or value == "South East" or value == "South" or value == "South West" or value == "West"):
            self.lock.release()
            raise ValueError("Orientation has to be between East, South and West")
        self._orientation = value
        self.lock.release()

    @property
    def efficiency(self):
        return self._efficiency
    @efficiency.setter
    def efficiency(self, value):
        self.lock.acquire()
        #make sure efficiency is a float and between 0 and 1
        if not isinstance(value, float):
            self.lock.release()
            raise TypeError("Efficiency is of wrong type")
        if (value < 0 or value > 1):
            self.lock.release()
            raise ValueError("Efficiency has to be between 0 and 1")
        self._efficiency = value
        self.lock.release()

    def __str__(self):
        return f"This is a solar panel and has properties: area: {self.area}, angle: {self.angle}," \
               f" orientation: {self.orientation} and efficiency: {self.efficiency}"