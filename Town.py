#Town class, that stores the houses belonging to the same town
import config
from threading import Lock

class Town:

    def __init__(self, name):
        self.name = name
        self.lock = Lock()
        self.cloud_prediction = []
        self.energy_prediction = []
        self.houseList = []
        #attribute of how much energy is used in this town
        #at the moment
        self.energyUsed=0

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        #make sure name is a string
        if not isinstance(value, str):
            raise TypeError("State is of wrong type")
        self._name = value

    def __str__(self):
        return f"This is town {self.name} and has cloud prediction {self.cloud_prediction} and " \
               f"energy prediction {self.energy_prediction}"

    #removes a House from the town
    def removeHouse(self, house):
        self.lock.acquire()
        self.houseList.remove(house)
        self.lock.release()
    #adds a house to the town
    def addHouse(self, house):
        self.lock.acquire()
        self.houseList.append(house)
        self.lock.release()

    #prints all houses in the town
    def listHouses(self):
        print("List of Houses in " + self.name + ":")
        for house in self.houseList:
            print(house.name)