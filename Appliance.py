#Appliance class, for creating appliance instances

import datetime
import config
from threading import Lock


class Appliance():
    #static variable, that saves the type of appliances that already exist
    TypeList = [("Washing Machine", 500, 2), ("Dishwasher", 1800, 1),
                ("E-Bike Battery", 100, 5), ("Car Battery Hybrid", 1200, 3),
                ("Car Battery Tesla", 7200, 8), ("Phone Charge", 5, 2),
                ("Tablet Charge", 12, 2), ("Power Bank", 20, 2)]

    def __init__(self, house, name, type, endTime):
        self.lock = Lock()
        self.house = house
        self.name = name
        self.type = type
        #checks for the right values of watt and duration in the type triple
        for triple in Appliance.TypeList:
            n, watt, hour = triple
            if n == type:
                self.power = watt
                self.duration = hour
        # until when it should be done
        self.endTime = endTime
        #these attributes need to be defined for the
        #scheduling to work
        self.scheduledTime = datetime.datetime.now()
        self.finishedTime = datetime.datetime.now()

        #when creating a new appliance, it always has to wait to be scheduled
        self.state = "waiting"
        #the appliance adds itself to the appliance list of the house it belongs to
        house.addAppliance(self)

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
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self.lock.acquire()
        #type should be a string
        if not isinstance(value, str):
            self.lock.release()
            raise TypeError("Type is of wrong type")
        self._type = value
        self.lock.release()

    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, value):
        self.lock.acquire()
        #state is a string and can only take certain values
        if not isinstance(value, str):
            self.lock.release()
            raise TypeError("State is of wrong type")
        if not (value == "waiting" or value == "running" or value == "finished" or value == "scheduled"):
            self.lock.release()
            raise ValueError("State is of wrong value")
        self._state = value
        self.lock.release()

    @property
    def endTime(self):
        return self._endTime
    @endTime.setter
    def endTime(self, value):
        self.lock.acquire()
        #end time is a datetime object
        if not isinstance(value, datetime.datetime):
            self.lock.release()
            raise TypeError("State is of wrong type")
        #checks whether the set endtime is sufficiently in the future, such that the appliance
        #can still be run
        if (value < datetime.datetime.now()+ datetime.timedelta(hours = self.duration)):
            self.lock.release()
            raise ValueError("End time lies in the past")
        self._endTime = value
        self.lock.release()

    @property
    def duration(self):
        return self._duration
    @duration.setter
    def duration(self, value):
        self.lock.acquire()
        if not isinstance(value, int):
            self.lock.release()
            raise TypeError("Duration is of wrong type")
        if (value < 1 or value > 24):
            self.lock.release()
            raise ValueError("Duration must be between 1 and 24 hours")
        self._duration = value
        self.lock.release()

    @property
    def power(self):
        return self._power
    @power.setter
    def power(self, value):
        self.lock.acquire()
        if not isinstance(value, int):
            self.lock.release()
            raise TypeError("Power is of wrong type")
        if (value < 1):
            self.lock.release()
            raise ValueError("Power must be at least 1 Watt")
        self._power = value
        self.lock.release()


    def __str__(self):
        return f"This is a: {self.type}, has the name {self.name}, duration is {self.duration}" \
               f" state is {self.state} and has to be done until {self.endTime}"

    def __eq__(self, other):
        return (isinstance(other, Appliance) and self.name == other.name and self.house == other.house and
                self.endTime == other.endTime and self.type == other.type)
    def __ne__(self, other):
        return not self == other


    #calculates the energy that is needed, in joules
    def energyNeeded(self):
        self.energy = self.duration * self.power * 3600
        return self.energy

    #define a field for scheduled time/date
    #scheduling class should call this function
    def setScheduleTime(self, time):
        self.lock.acquire()
        if not isinstance(time, datetime.datetime):
            self.lock.release()
            raise TypeError("Scheduled time for appliance is of wrong type")
        self.scheduledTime = time
        self.lock.release()
        self.setFinishedTime()
    def resetScheduledTime(self):
        self.lock.acquire()
        self.scheduledTime = datetime.datetime.now()
        self.lock.release()

    def setFinishedTime(self):
        self.lock.acquire()
        self.finishedTime = self.scheduledTime + datetime.timedelta(hours=self.duration)
        self.lock.release()

    #functions to remove or add an appliance to the house
    def removeSelfFromHouse(self):
        self.house.removeAppliance(self)
    def appendSelfToHouse(self):
        self.house.addAppliance(self)
