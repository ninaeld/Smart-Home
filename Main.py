#Bachelor Thesis by Nina Eldridge, October 2021
#Interfacing the smart home to its local smart grid

from Appliance import Appliance
from GUI import GUI
from Calculations import Calculations
from House import House
from Town import Town
from SolarPanel import SolarPanel
import tkinter as tk
from Scheduling import Scheduling
import config
import datetime
import schedule
import time
from threading import Thread, Lock

##### initalisation ####
#configurate the global variable town
config.init()

#define certain Towns
basel = Town("Basel")
config.Towns.append(basel)
bern = Town("Bern")
config.Towns.append(bern)
binningen = Town("Binningen")
config.Towns.append(binningen)
lausanne = Town("Lausanne")
config.Towns.append(lausanne)
lugano = Town("Lugano")
config.Towns.append(lugano)

#function that is called every hour to update the energy prediction and the scheduling of
#the appliances for each town
def calculation():
    lock = Lock()
    # to make sure that the prediction arrays starts at the next full hour
    this_date = datetime.datetime.now()
    this_date = this_date.replace(minute=0, second=0, microsecond=0)
    #UNCOMMENT: to simulate an hour each minute / seconds
    this_date = this_date + datetime.timedelta(hours=config.hour_counter)
    print("Current date and time")
    print(this_date)
    for h in range(0, len(config.Towns)):
        Calculations.get_predictions(h, this_date, lock)
        Scheduling.schedule_appliances(h, this_date, lock)
    #before updating frontpage let it sleep for 3 seconds
    time.sleep(1)
    #update the front page with the new calculations
    GUI.updateFrontpage()
    #UNCOMMENT: to simulate an hour each minute
    config.hour_counter = config.hour_counter + 1

#scheduler function
def scheduler():
    # COMMENT: so the program doesn't run in real time
    #schedule.every().hour.at(":59").do(calculation)
    # UNCOMMENT: to simulate an hour each 15 seconds or each minute
    # IMPORTANT: uncomment only one line
    schedule.every(15).seconds.do(calculation)
    #schedule.every(1).minutes.do(calculation)
    while True:
        schedule.run_pending()
        time.sleep(1)
#GUI function
def open_GUI():
    root = tk.Tk()
    window = GUI(root)
    root.mainloop()

#create some houses
firstHouse = House("Eldridge", binningen, SolarPanel(24.0, 30, "South", 0.25))
secondHouse= House("Sunny", binningen, SolarPanel(26.0, 20, "South East", 0.2))

thirdHouse = House("Bucheli", bern, SolarPanel(23.0, 30, "South West", 0.2))
fourthHouse = House("Lerf", bern, SolarPanel(12.0, 40, "East", 0.25))
fifthHouse = House("Camozzi", bern, SolarPanel(15.0, 35, "South", 0.18))

sixthHouse = House("Poplawski", basel, SolarPanel(25.0, 45, "South", 0.25))
seventhHouse = House("Schubert", basel, SolarPanel(24.0, 35, "South East", 0.17))
eighthHouse = House("Barmet", basel, SolarPanel(30.0, 45, "South West", 0.2))

ninthHouse = House("Demont", lausanne, SolarPanel(31.0, 40, "South", 0.18))
tenthHouse = House("Carell", lausanne, SolarPanel(23.0, 45, "South East", 0.21))
eleventhHouse = House("Ghousson", lausanne, SolarPanel(34.0, 45, "South West", 0.2))
twelvethHouse = House("Guardini", lugano, SolarPanel(16.0, 30, "South", 0.19))
thirteenthHouse = House("Fontana", lugano, SolarPanel(19.0, 35, "South", 0.2))

#create some appliances
app1 = Appliance(firstHouse, "DW1", "Dishwasher", datetime.datetime.now()+datetime.timedelta(hours=7))
app2 = Appliance(firstHouse, "Car Toyota", "Car Battery Hybrid", datetime.datetime.now()+datetime.timedelta(hours=12))
app3 = Appliance(firstHouse, "Car Tesla", "Car Battery Tesla", datetime.datetime.now()+datetime.timedelta(hours=45))
app4 = Appliance(firstHouse, "WM1", "Dishwasher", datetime.datetime.now()+datetime.timedelta(hours=5))

app5 = Appliance(secondHouse, "WM1", "Washing Machine", datetime.datetime.now()+datetime.timedelta(hours=2))
app6 = Appliance(secondHouse, "WM2", "Washing Machine", datetime.datetime.now()+datetime.timedelta(hours=5))
app7 = Appliance(secondHouse, "Car Renault", "Car Battery Hybrid", datetime.datetime.now()+datetime.timedelta(hours=8))

app8 = Appliance(thirdHouse, "DW", "Dishwasher", datetime.datetime.now()+datetime.timedelta(hours=5))

app9 = Appliance(fourthHouse, "Wash", "Washing Machine", datetime.datetime.now()+datetime.timedelta(hours=18))
app10 = Appliance(fourthHouse, "Bike", "E-Bike Battery", datetime.datetime.now()+datetime.timedelta(hours=53))

app11 = Appliance(fifthHouse, "Bike", "E-Bike Battery", datetime.datetime.now()+datetime.timedelta(hours=11))

app12 = Appliance(sixthHouse, "DW1", "Dishwasher", datetime.datetime.now()+datetime.timedelta(hours=4))
app13 = Appliance(sixthHouse, "Washer", "Washing Machine", datetime.datetime.now()+datetime.timedelta(hours=9))

app14 = Appliance(seventhHouse, "Bicycle", "E-Bike Battery", datetime.datetime.now()+datetime.timedelta(hours=7))

app15 = Appliance(ninthHouse, "First Bike", "E-Bike Battery", datetime.datetime.now()+datetime.timedelta(hours=6))
app16 = Appliance(ninthHouse, "Car Tesla", "Car Battery Tesla", datetime.datetime.now()+datetime.timedelta(hours=46))

app17 = Appliance(eleventhHouse, "Car Toyota", "Car Battery Hybrid", datetime.datetime.now()+datetime.timedelta(hours=50))

app18 = Appliance(twelvethHouse, "Dish", "Dishwasher", datetime.datetime.now()+datetime.timedelta(hours=5))

app19 = Appliance(thirteenthHouse, "Washing", "Washing Machine", datetime.datetime.now()+datetime.timedelta(hours=13))
app20 = Appliance(thirteenthHouse, "Bicycle", "E-Bike Battery", datetime.datetime.now()+datetime.timedelta(hours=16))


#### Main ######
#run calculations before the program opens, to already
#get the data and the scheduler would only schedule every hour
#calculation()
for town in config.Towns:
    town.cloud_prediction = 48*[0]
    town.energy_prediction = 48*[0]
#open two threads
#set to daemon = True, such that it ends when main thread ends
calculationThread = Thread(target=scheduler, daemon=True)
GUIThread = Thread(target=open_GUI)

calculationThread.start()
GUIThread.start()

#join this thread, such that the calculation thread
#ends when the GUI is closed
GUIThread.join()

