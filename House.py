#House class, where instances of houses are created

import config
from SolarPanel import SolarPanel
from threading import Lock

class House:
    def __init__(self, name, town, solarPanel):
        self.lock = Lock()
        self.name = name
        #to store all appliances that belong to this house
        self.myAppliances = []
        self.solarPanel = solarPanel
        self.town = town
        self.currentEnergyProduction = 0.0
        self.appendSelfToTown()


    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self.lock.acquire()
        #name should be a string
        if not isinstance(value, str):
            self.lock.release()
            raise TypeError("Name is of wrong type")
        self._name = value
        self.lock.release()

    @property
    def solarPanel(self):
        return self._solarPanel
    @solarPanel.setter
    def solarPanel(self, value):
        #make sure that the solar panel is of class SolarPanel
        if not isinstance(value, SolarPanel):
            raise TypeError("Solar Panel is of wrong type")
        self._solarPanel = value

    def __str__(self):
        return f"House: {self.name}\n" \
               f"Current energy production: {self.currentEnergyProduction} W/h\n" \
               f"Solar panel properties:\n " \
               f"area: {self.solarPanel.area} m^2\n " \
               f"efficiency: {self.solarPanel.efficiency}\n " \
               f"angle: {self.solarPanel.angle}°\n " \
               f"orientation: {self.solarPanel.orientation}"

    #function that house appends itself to the town list
    def appendSelfToTown(self):
        self.town.addHouse(self)
    #function that house deletes itself from the town list
    def removeSelfFromTown(self):
        self.town.removeHouse(self)

    #function that an appliance is added to the appliance list of this house
    def addAppliance(self, appliance):
        self.lock.acquire()
        self.myAppliances.append(appliance)
        self.lock.release()
    #function that this appliance is deleted from the list of this house
    def removeAppliance(self, appliance):
        self.lock.acquire()
        self.myAppliances.remove(appliance)
        self.lock.release()

    #function to list all appliances in the list
    def listAppliances(self):
        print("List of Appliances in " + self.name + ":")
        name = [n[0] for n in self.myAppliances]
        for app in name:
            print(app.name)
        print("\n")