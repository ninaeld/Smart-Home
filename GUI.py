#Class to create the graphical user interface

from Appliance import Appliance
from House import House
from SolarPanel import SolarPanel
import datetime
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
import config

WIDTH = 25
PADX_ENTRIES = 10
PADY_ENTRIES = 5
PADX_FRAMES = 10
PADY_FRAMES = 10


class GUI:

    #static list and method are necessary to call the functions
    #for the GUI from the other thread
    instance_list = []
    @staticmethod
    def updateFrontpage():
        for window in GUI.instance_list:
            window.updateEnergyDisplay()
            window.show_appliances_of_town()
            #do this only if the window is non empty
            if (window.combobox3.get() != "" and window.HouseCombobox3.get() != ""):
                window.getApplianceValues()

    def __init__(self, master):

        #all changes to the root window
        master.title("Smart Home")
        master.geometry('800x600+100+20')
        #can't resize the window (might want it depending on widgets)
        master.resizable(True, False)
        #append the instance to the static class list
        GUI.instance_list.append(self)

        #create notebook to organise the GUI
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(pady=0, expand=True)
        framesize = {'width': 800, 'height': 600}

        ###### Frame for Start page ##############
        self.frame1 = ttk.Frame(self.notebook, **framesize)
        self.frame1.columnconfigure(0, weight=1, minsize=200)

        self.topSelectTownFrame = ttk.Frame(self.frame1)
        self.topSelectTownFrame.grid(column=0, row=0, pady=PADY_FRAMES, padx=PADX_FRAMES, sticky=tk.W)
        self.topSelectTownFrame.columnconfigure(0, weight=1, minsize=120)
        self.topSelectTownFrame.columnconfigure(1, weight=2)

        self.SelectTownLabel1 = ttk.Label(self.topSelectTownFrame, text='Select Town:', font=('Arial', 14))
        self.SelectTownLabel1.grid(column=0, row=0, padx=PADX_ENTRIES, sticky=tk.W)
        SelTown = tk.StringVar()
        self.SelectTownCombobox1 = ttk.Combobox(self.topSelectTownFrame, textvariable=SelTown, width=WIDTH)
        self.SelectTownCombobox1['values'] = [t.name for t in config.Towns]
        self.SelectTownCombobox1.bind('<<ComboboxSelected>>', lambda x: self.getTownValue1())
        self.SelectTownCombobox1.grid(column=1, row=0, padx=PADX_ENTRIES, sticky=tk.W)

        self.TownEnergyLabel = ttk.Label(self.topSelectTownFrame, text='Town Energy this hour:')
        self.TownEnergyLabel.grid(column=0, row=1, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)
        self.TownEnergyDisplay= ttk.Label(self.topSelectTownFrame, text='energy in watt/h')
        self.TownEnergyDisplay.grid(column=1, row=1, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)
        self.EnergyUsedLabel = ttk.Label(self.topSelectTownFrame, text='Used energy:')
        self.EnergyUsedLabel.grid(column=0, row=2, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)
        self.EnergyUsedDisplay = ttk.Label(self.topSelectTownFrame, text='energy in watt/h')
        self.EnergyUsedDisplay.grid(column=1, row=2, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)

        self.separator = ttk.Separator(self.frame1, orient='horizontal')
        self.separator.grid(column=0, row=1, pady=PADY_FRAMES, sticky=tk.E + tk.W)

        self.middleFrame1 = ttk.Frame(self.frame1)
        self.middleFrame1.grid(column=0, row=2, pady=PADY_FRAMES, padx=PADX_FRAMES, sticky=tk.W)
        self.middleFrame1.columnconfigure(0, weight=1, minsize=120)
        self.middleFrame1.columnconfigure(1, weight=2)
        self.SelectHouseLabel1 = ttk.Label(self.middleFrame1, text='Select House:', font=('Arial', 14))
        self.SelectHouseLabel1.grid(column=0, row=0, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)
        SelHouse = tk.StringVar()
        self.selectHouseCombobox1 = ttk.Combobox(self.middleFrame1, textvariable=SelHouse, width=WIDTH)
        self.selectHouseCombobox1.bind('<<ComboboxSelected>>', lambda x: self.show_appliances_of_town())
        self.selectHouseCombobox1.grid(column=1, row=0, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)

        self.houseInfoLabel = ttk.Label(self.middleFrame1, text="House information:")
        self.houseInfoLabel.grid(column=0, row=1, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.NW)
        self.RunningAppLabel = ttk.Label(self.middleFrame1, text='Running appliances:')
        self.RunningAppLabel.grid(column=0, row=2, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.NW)
        self.ScheduledAppLabel = ttk.Label(self.middleFrame1, text='Scheduled appliances:')
        self.ScheduledAppLabel.grid(column=0, row=3, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.NW)
        self.FinishedAppLabel = ttk.Label(self.middleFrame1, text='Finished appliances:')
        self.FinishedAppLabel.grid(column=0, row=4, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.NW)
        self.houseInfoDisplay = scrolledtext.ScrolledText(self.middleFrame1, width=3*WIDTH, height=5)
        self.houseInfoDisplay['state'] = 'disabled'
        self.houseInfoDisplay.grid(column=1, row=1, padx=PADY_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)
        self.RunningAppScroll = scrolledtext.ScrolledText(self.middleFrame1, width=3*WIDTH, height=5)
        self.RunningAppScroll['state'] = 'disabled'
        self.RunningAppScroll.grid(column=1, row=2, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)
        self.ScheduledAppScroll = scrolledtext.ScrolledText(self.middleFrame1, width=3*WIDTH, height=5)
        self.ScheduledAppScroll['state'] = 'disabled'
        self.ScheduledAppScroll.grid(column=1, row=3, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)
        self.FinishedAppScroll = scrolledtext.ScrolledText(self.middleFrame1, width=3*WIDTH, height=5)
        self.FinishedAppScroll['state']='disabled'
        self.FinishedAppScroll.grid(column=1, row=4, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)




        ######## Frame 2 for House page #############
        self.frame2 = ttk.Frame(self.notebook, **framesize)
        self.frame2.columnconfigure(0, weight=1, minsize=200)


        self.topFrame = ttk.Frame(self.frame2)
        self.topFrame.grid(column=0, row=0, pady=PADY_FRAMES, padx=PADX_FRAMES, sticky=tk.W)

        self.selectTownLabel = ttk.Label(self.topFrame, text='Select Town:', font=('Arial', 14))
        self.selectTownLabel.pack(anchor=tk.W, side=tk.LEFT, padx=PADX_ENTRIES)
        # Combobox creation
        n = tk.StringVar()
        # attributes with keyword arguments
        self.combobox = ttk.Combobox(self.topFrame, width=WIDTH, textvariable=n)
        # Adding combobox drop down list, attributes as dictionary
        self.combobox['values'] = [t.name for t in config.Towns]
        self.combobox.pack(anchor=tk.W, side=tk.RIGHT, padx=PADX_ENTRIES)
        self.combobox.bind('<<ComboboxSelected>>', lambda x: self.getTownValue2())


        self.middleFrame = ttk.Frame(self.frame2)
        self.middleFrame.grid(column=0, row=1,padx=PADX_FRAMES,  pady=PADY_FRAMES, sticky=tk.W)
        self.optionsLabel = ttk.Label(self.middleFrame, text="Options:", font=('Arial', 14))
        self.optionsLabel.pack(anchor=tk.W, side=tk.LEFT, padx=PADX_ENTRIES)
        #radio buttons to choose what to do
        v = tk.IntVar()
        self.r1 = ttk.Radiobutton(self.middleFrame, text = "add a new house", variable=v, value=1,
                                  command=self.from_change_to_add_House)
        self.r1.pack(anchor=tk.W, side=tk.LEFT, padx=PADX_ENTRIES)
        self.r2 = ttk.Radiobutton(self.middleFrame, text='change a property of a house', variable =v, value=2,
                                  command=self.from_add_to_change_House)
        self.r2.pack(anchor=tk.W, side=tk.RIGHT, padx=PADX_ENTRIES)

        self.separator = ttk.Separator(self.frame2, orient='horizontal')
        self.separator.grid(column=0, row=2, columnspan=1, sticky = tk.W + tk.E, pady=PADY_FRAMES)

        #Frame for adding a new house
        self.addHouseFrame = ttk.Frame(self.frame2)
        self.addHouseFrame.grid(column=0, row=3, padx=PADX_FRAMES, pady=PADY_FRAMES, sticky=tk.W)
        self.addHouseFrame.columnconfigure(0, weight=1, minsize=120)
        self.addHouseFrame.columnconfigure(1, weight=2)

        self.addHouseLabel1 = ttk.Label(self.addHouseFrame, text='Add a new house:', font=('Arial', 14))
        self.addHouseLabel1.grid(column=0,row=0, columnspan=2, sticky=tk.W, padx=10, pady=10)

        self.nameLabel = ttk.Label(self.addHouseFrame, text='Name:')
        self.nameLabel.grid(column=0, row=1, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)
        name = tk.StringVar()
        self.nameEntry = ttk.Entry(self.addHouseFrame, textvariable = name, width=WIDTH)
        self.nameEntry.grid(column=1, row=1, sticky=tk.W, padx=PADX_ENTRIES,pady=PADY_ENTRIES)

        self.areaLabel = ttk.Label(self.addHouseFrame, text='Area:')
        self.areaLabel.grid(column=0, row=2, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        area=tk.DoubleVar()
        self.areaEntry = ttk.Entry(self.addHouseFrame, textvariable=area, width=WIDTH)
        self.areaEntry.grid(column=1, row=2, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.efficiencyLabel = ttk.Label(self.addHouseFrame, text='Efficiency:')
        self.efficiencyLabel.grid(column=0, row=3, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        efficiency =tk.DoubleVar()
        self.efficiencyEntry=ttk.Entry(self.addHouseFrame, textvariable=efficiency, width=WIDTH)
        self.efficiencyEntry.grid(column=1, row=3, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.angleLabel = ttk.Label(self.addHouseFrame, text='Angle:')
        self.angleLabel.grid(column=0, row=4, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        angle = tk.IntVar()
        self.angleEntry = ttk.Entry(self.addHouseFrame, textvariable=angle, width=WIDTH)
        self.angleEntry.grid(column=1, row=4, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.orientationLabel = ttk.Label(self.addHouseFrame, text='Orientation:')
        self.orientationLabel.grid(column=0, row=5, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        orientation=tk.StringVar()
        self.orientationEntry = ttk.Combobox(self.addHouseFrame, textvariable=orientation, width=WIDTH)
        self.orientationEntry.grid(column=1, row=5, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        self.orientationEntry['values']= ["East", "South East", "South", "South West", "West"]

        self.addHouseButton = ttk.Button(self.addHouseFrame, text='Add house', width=WIDTH)
        self.addHouseButton.grid(column=1, row=6, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        self.addHouseButton.bind("<Button-1>", lambda x: self.new_House_creation())


        # Frame for changing a house
        self.changeHouseFrame = ttk.Frame(self.frame2)
        self.changeHouseFrame.grid(column=0, row=3,padx=PADX_FRAMES, pady=PADY_FRAMES, sticky=tk.W)
        self.changeHouseFrame.columnconfigure(0, weight=1, minsize=120)
        self.changeHouseFrame.columnconfigure(1, weight=2)

        self.changeHouseLabel = ttk.Label(self.changeHouseFrame, text='Change a property of the House:', font=('Arial', 14))
        self.changeHouseLabel.grid(column=0, row=0, columnspan=2, sticky=tk.W, padx=10, pady=10)

        self.selectHouseLabel = ttk.Label(self.changeHouseFrame, text='Select House:')
        self.selectHouseLabel.grid(column=0, row=1, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        housename = tk.StringVar()
        self.HouseCombobox = ttk.Combobox(self.changeHouseFrame, textvariable = housename, width=WIDTH)
        self.HouseCombobox.grid(column=1, row=1, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.selectChangeLabel = ttk.Label(self.changeHouseFrame, text='Change:')
        self.selectChangeLabel.grid(column=0, row=2, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        changing = tk.StringVar()
        self.changePropertyCombobox = ttk.Combobox(self.changeHouseFrame, textvariable=changing, width=WIDTH)
        self.changePropertyCombobox.grid(column=1, row=2, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        self.changePropertyCombobox['values']=["name", "area", "efficiency","angle","orientation"]

        self.newValueLabel = ttk.Label(self.changeHouseFrame, text='New value:')
        self.newValueLabel.grid(column=0, row=3, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        newValue = tk.StringVar()
        self.newValueEntry = ttk.Entry(self.changeHouseFrame, textvariable=newValue, width=WIDTH)
        self.newValueEntry.grid(column=1, row=3, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.changePropertyButton = ttk.Button(self.changeHouseFrame, text='Change property', width=WIDTH)
        self.changePropertyButton.grid(column=1, row=4, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        self.changePropertyButton.bind("<Button-1>", lambda x: self.new_value_house_button())

        self.orHouseLabel = ttk.Label(self.changeHouseFrame, text='or', width=WIDTH)
        self.orHouseLabel.grid(column=1, row=5, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)
        self.deleteHouseButton = ttk.Button(self.changeHouseFrame, text='Delete house', width=WIDTH)
        self.deleteHouseButton.grid(column=1, row=6, sticky=tk.W, padx=PADX_FRAMES, pady=PADY_FRAMES)
        self.deleteHouseButton.bind("<Button-1>", lambda x: self.delete_house_button())

        #forget the frame that you don't want to see first
        self.changeHouseFrame.grid_forget()




        ###### Frame 3 for Appliances ##########
        self.frame3 = ttk.Frame(self.notebook, **framesize)
        self.frame3.columnconfigure(0, weight=1 )

        self.topFrame3 = ttk.Frame(self.frame3)
        self.topFrame3.grid(column=0, row=0, pady=PADY_FRAMES, padx=PADX_FRAMES, sticky=tk.W)

        self.selectTownLabel3 = ttk.Label(self.topFrame3, text='Select Town:', font=('Arial', 14))
        self.selectTownLabel3.pack(anchor=tk.W, side=tk.LEFT, padx=PADX_ENTRIES)
        # Combobox creation
        n3 = tk.StringVar()
        # attributes with keyword arguments
        self.combobox3 = ttk.Combobox(self.topFrame3, width=WIDTH, textvariable=n3)
        # Adding combobox drop down list, attributes as dictionary
        self.combobox3['values'] = [t.name for t in config.Towns]
        self.combobox3.pack(anchor=tk.W, side=tk.RIGHT, padx=PADX_ENTRIES)
        self.combobox3.bind('<<ComboboxSelected>>', lambda x: self.getTownValue3())

        self.middleFrame3 = ttk.Frame(self.frame3)
        self.middleFrame3.grid(column=0, row=1, padx=PADX_FRAMES, pady=PADY_FRAMES, sticky=tk.W)

        self.selectHouseLabel3 = ttk.Label(self.middleFrame3, text='Select House:', font=('Arial', 14))
        self.selectHouseLabel3.pack(anchor=tk.W, side=tk.LEFT, padx=PADX_ENTRIES)
        n4 = tk.StringVar()
        self.HouseCombobox3 = ttk.Combobox(self.middleFrame3, width=WIDTH, textvariable=n4)
        self.HouseCombobox3.pack(anchor=tk.W, side=tk.RIGHT, padx=PADX_ENTRIES)
        self.HouseCombobox3.bind('<<ComboboxSelected>>', lambda x: self.getApplianceValues())

        self.bottomFrame3 = ttk.Frame(self.frame3)
        self.bottomFrame3.grid(column=0, row=2, padx=PADX_FRAMES, pady=PADY_FRAMES, sticky=tk.W)
        self.optionsLabel3 = ttk.Label(self.bottomFrame3, text="Options:", font=('Arial', 14))
        self.optionsLabel3.pack(anchor=tk.W, side=tk.TOP, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        # radio buttons to choose what to do
        v3 = tk.IntVar()
        self.radioButton3 = ttk.Radiobutton(self.bottomFrame3, text="schedule an appliance", variable=v3, value=1,
                                  command=self.from_x_to_add_application)
        self.radioButton3.pack(anchor=tk.W, side=tk.LEFT, padx=PADX_ENTRIES)
        self.radioButton4 = ttk.Radiobutton(self.bottomFrame3, text='change an appliance', variable=v3, value=2,
                                  command=self.from_x_to_change_application)
        self.radioButton4.pack(anchor=tk.W, side=tk.LEFT, padx=PADX_ENTRIES)
        self.radioButton5 = ttk.Radiobutton(self.bottomFrame3, text="add a new type of appliance", variable=v3,
                                            value=3, command=self.from_x_to_create_new_application)
        self.radioButton5.pack(anchor=tk.W, side=tk.LEFT, padx=PADX_ENTRIES)

        self.separator3 = ttk.Separator(self.frame3, orient='horizontal')
        self.separator3.grid(column=0, row=3, columnspan=1, sticky=tk.W + tk.E, pady=PADY_FRAMES)


        #schedule application frame
        self.scheduleAppFrame = ttk.Frame(self.frame3)
        self.scheduleAppFrame.grid(column=0, row=4, padx=PADX_FRAMES, pady=PADY_FRAMES, sticky=tk.W)
        self.scheduleAppFrame.columnconfigure(0, weight=1, minsize=120)
        self.scheduleAppFrame.columnconfigure(1, weight=2, minsize=450)

        self.scheduleAppLabel = ttk.Label(self.scheduleAppFrame, text='Schedule an appliance:', font=('Arial', 14))
        self.scheduleAppLabel.grid(column=0, row=0, columnspan=2, sticky=tk.W, padx=10, pady=10)

        self.scheduleNameLabel = ttk.Label(self.scheduleAppFrame, text='Name:')
        self.scheduleNameLabel.grid(column=0, row=1, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        appName = tk.StringVar()
        self.appNameEntry = ttk.Entry(self.scheduleAppFrame, textvariable=appName, width=WIDTH)
        self.appNameEntry.grid(column=1, row=1, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.scheduleTypeLabel = ttk.Label(self.scheduleAppFrame, text='Type:')
        self.scheduleTypeLabel.grid(column=0, row=2, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        appType = tk.StringVar()
        self.appTypeCombobox = ttk.Combobox(self.scheduleAppFrame, textvariable=appType, width=WIDTH)
        self.appTypeCombobox['values'] = [t for t, p, d in Appliance.TypeList]
        self.appTypeCombobox.grid(column=1, row=2, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.appDateLabel = ttk.Label(self.scheduleAppFrame, text='Date:')
        self.appDateLabel.grid(column=0, row=3, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        self.appDayLabel = ttk.Label(self.scheduleAppFrame, text='Day')
        self.appDayLabel.grid(column=1, row=3, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        self.appMonthLabel = ttk.Label(self.scheduleAppFrame, text='Month')
        self.appMonthLabel.grid(column=1, row=3, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        self.appYearLabel = ttk.Label(self.scheduleAppFrame, text='Year')
        self.appYearLabel.grid(column=1, row=3, sticky=tk.E, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        Day = tk.IntVar()
        self.appDaySpinbox = ttk.Spinbox(self.scheduleAppFrame, from_=1, to=31, textvariable=Day)
        self.appDaySpinbox.grid(column=1, row=4, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        Month = tk.IntVar()
        self.appMonthSpinbox = ttk.Spinbox(self.scheduleAppFrame, from_=1, to=12, textvariable=Month)
        self.appMonthSpinbox.grid(column=1, row=4, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        Year = tk.IntVar()
        self.appYearSpinbox = ttk.Spinbox(self.scheduleAppFrame, from_=2021, to=2050, textvariable=Year)
        self.appYearSpinbox.grid(column=1, row=4, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.E)

        self.appTimeLabel = ttk.Label(self.scheduleAppFrame, text='Time:')
        self.appTimeLabel.grid(column=0, row=5, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)
        self.appHourLabel = ttk.Label(self.scheduleAppFrame, text='Hour')
        self.appHourLabel.grid(column=1, row=5, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        self.appMinuteLabel = ttk.Label(self.scheduleAppFrame, text='Minute')
        self.appMinuteLabel.grid(column=1, row=5, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        Hour = tk.IntVar()
        self.appHourSpinbox = ttk.Spinbox(self.scheduleAppFrame, from_=0, to=23, textvariable=Hour)
        self.appHourSpinbox.grid(column=1, row=6, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)
        Minute=tk.IntVar()
        self.appMinuteCombobox = ttk.Combobox(self.scheduleAppFrame, textvariable=Minute)
        self.appMinuteCombobox['values'] = ["00", "30"]
        self.appMinuteCombobox.grid(column=1, row=6, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.scheduleAppButton = ttk.Button(self.scheduleAppFrame, text='Schedule appliance', width=WIDTH)
        self.scheduleAppButton.grid(column=1, row=7, padx=PADX_FRAMES, pady=PADY_FRAMES, sticky=tk.W)
        self.scheduleAppButton.bind("<Button-1>", lambda x: self.schedule_application_button())




        #change an appliance frame
        self.changeAppFrame = ttk.Frame(self.frame3)
        self.changeAppFrame.grid(column=0, row=4, padx=PADX_FRAMES, pady=PADY_FRAMES, sticky=tk.W)
        self.changeAppFrame.columnconfigure(0, weight=1, minsize=140)
        self.changeAppFrame.columnconfigure(1, weight=2, minsize=430)

        self.changeAppLabel = ttk.Label(self.changeAppFrame, text='Change an appliance:', font=('Arial', 14))
        self.changeAppLabel.grid(column=0, row=0, columnspan=2, sticky=tk.W, padx=10, pady=10)

        self.selectAppLabel = ttk.Label(self.changeAppFrame, text="Select an appliance:")
        self.selectAppLabel.grid(column=0, row=1, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        app = tk.StringVar()
        self.selectAppCombobox = ttk.Combobox(self.changeAppFrame, textvariable=app, width=WIDTH)
        self.selectAppCombobox.grid(column=1, row=1, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.changePropertyLabel = ttk.Label(self.changeAppFrame, text='Change:')
        self.changePropertyLabel.grid(column=0, row=2, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        changeApp = tk.StringVar()
        self.changeAppCombobox = ttk.Combobox(self.changeAppFrame, textvariable=changeApp, width=WIDTH)
        self.changeAppCombobox.grid(column=1, row=2, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        self.changeAppCombobox['values'] = ["name", "duration", "power", "year", "month", "day", "hour", "minute"]

        self.newAppValueLabel = ttk.Label(self.changeAppFrame, text='New value:')
        self.newAppValueLabel.grid(column=0, row=3, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        newAppValue = tk.StringVar()
        self.newAppValueEntry = ttk.Entry(self.changeAppFrame, textvariable=newAppValue, width=WIDTH)
        self.newAppValueEntry.grid(column=1, row=3, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.enterNewValueAppButton = ttk.Button(self.changeAppFrame, text='Change value', width=WIDTH)
        self.enterNewValueAppButton.grid(column=1, row=4, sticky=tk.W, padx=PADX_FRAMES, pady=PADY_FRAMES)
        self.enterNewValueAppButton.bind("<Button-1>", lambda x: self.new_value_app_button())

        self.orAppLabel = ttk.Label(self.changeAppFrame, text='or', width=WIDTH)
        self.orAppLabel.grid(column=1, row=8, padx=PADX_ENTRIES, pady=PADY_ENTRIES, sticky=tk.W)
        self.deleteAppButton = ttk.Button(self.changeAppFrame, text='Delete the appliance', width=WIDTH)
        self.deleteAppButton.grid(column=1, row=9, sticky=tk.W, padx=PADX_FRAMES, pady=PADY_FRAMES)
        self.deleteAppButton.bind("<Button-1>", lambda x: self.delete_application_button())

        self.changeAppFrame.grid_forget()


        #add new type of applicance frame
        self.newTypeAppFrame = ttk.Frame(self.frame3)
        self.newTypeAppFrame.grid(column=0, row=4, padx=PADX_FRAMES, pady=PADY_FRAMES, sticky=tk.W)
        self.newTypeAppFrame.columnconfigure(0, weight=1, minsize=140)
        self.newTypeAppFrame.columnconfigure(1, weight=2, minsize=430)

        self.addNewTypeLabel = ttk.Label(self.newTypeAppFrame, text='Add a new type of appliance:', font=('Arial', 14))
        self.addNewTypeLabel.grid(column=0, row=0, columnspan=2, sticky=tk.W, padx=PADX_FRAMES, pady=PADY_FRAMES)

        self.NewTypeLabel = ttk.Label(self.newTypeAppFrame, text='Type:')
        self.NewTypeLabel.grid(column=0, row=1, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        TypeEntry = tk.StringVar()
        self.NewTypeEntry = ttk.Entry(self.newTypeAppFrame, textvariable=TypeEntry, width=WIDTH)
        self.NewTypeEntry.grid(column=1, row=1, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.NewPowerLabel = ttk.Label(self.newTypeAppFrame, text='Power:')
        self.NewPowerLabel.grid(column=0, row=2, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        PowerEntry = tk.IntVar()
        self.NewPowerEntry = ttk.Entry(self.newTypeAppFrame, textvariable=PowerEntry, width=WIDTH)
        self.NewPowerEntry.grid(column=1, row=2, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.NewDurationLabel = ttk.Label(self.newTypeAppFrame, text='Duration:')
        self.NewDurationLabel.grid(column=0, row=3, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        DurationEntry = tk.IntVar()
        self.NewDurationEntry = ttk.Entry(self.newTypeAppFrame, textvariable=DurationEntry, width=WIDTH)
        self.NewDurationEntry.grid(column=1, row=3, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.addNewTypeAppButton = ttk.Button(self.newTypeAppFrame, text='Add new type', width=WIDTH)
        self.addNewTypeAppButton.grid(column=1, row=4, sticky=tk.W, padx=PADX_FRAMES, pady=PADY_FRAMES)
        self.addNewTypeAppButton.bind("<Button-1>", lambda x: self.add_new_type_application())

        self.showTypesLabel = ttk.Label(self.newTypeAppFrame, text = "Types:")
        self.showTypesLabel.grid(column=0, row=6, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)
        self.TypesDisplay = scrolledtext.ScrolledText(self.newTypeAppFrame, width=2*WIDTH+15, height=6)
        self.show_types_appliances()
        self.TypesDisplay.grid(column=1, row=6, sticky=tk.W, padx=PADX_ENTRIES, pady=PADY_ENTRIES)

        self.newTypeAppFrame.grid_forget()



        #pack all main frames into the notebook
        self.frame1.pack(fill='both', expand=True)
        self.frame2.pack(fill='both', expand=True)
        self.frame3.grid_propagate(False)

        self.notebook.add(self.frame1, text='      Start      ')
        self.notebook.add(self.frame2, text='      House      ')
        self.notebook.add(self.frame3, text = '      Appliance      ')

    #functions being reused
    def delete_scrolledtext(self):
        self.ScheduledAppScroll['state'] = 'normal'
        self.ScheduledAppScroll.delete('0.0', 'end')
        self.ScheduledAppScroll['state'] = 'disabled'
        self.RunningAppScroll['state'] = 'normal'
        self.RunningAppScroll.delete('0.0', 'end')
        self.RunningAppScroll['state'] = 'disabled'
        self.FinishedAppScroll['state'] = 'normal'
        self.FinishedAppScroll.delete('0.0', 'end')
        self.FinishedAppScroll['state'] = 'disabled'
        self.houseInfoDisplay['state']='normal'
        self.houseInfoDisplay.delete('0.0', 'end')
        self.houseInfoDisplay['state']='disabled'

    def strDate(self, date):
        if date.minute == 0:
            return f"{date.hour}:00, {date.day}.{date.month}.{date.year}"
        return f"{date.hour}:{date.minute}, {date.day}.{date.month}.{date.year}"

    def updateHouseCombobox1(self):
        #gets the town selected in the town selection combobox
        valueTownSelected = self.SelectTownCombobox1.get()
        # looks for the right town in towns list
        for i in range(0, len(config.Towns)):
            if config.Towns[i].name == valueTownSelected:
                chosen_town = config.Towns[i]
                # shows all houses in that town in the combobox house
                namesList = [h.name for h in chosen_town.houseList]
                namesList.sort()
                self.selectHouseCombobox1['values'] = namesList
                self.selectHouseCombobox1.delete(0, 'end')
    def updateHouseCombobox2(self):
        # get the value from the combobox of selected town
        valueTownSelected = self.combobox.get()
        # find the town in the Towns list
        for i in range(0, len(config.Towns)):
            if config.Towns[i].name == valueTownSelected:
                chosen_town = config.Towns[i]
                # list all houses in that town in the house combobox
                namesList = [h.name for h in chosen_town.houseList]
                namesList.sort()
                self.HouseCombobox['values'] = namesList
                self.HouseCombobox.delete(0, 'end')
    def updateHouseCombobox3(self):
        # selected town on appliance page
        valueTownSelected = self.combobox3.get()
        # looks for the right town in towns list
        for i in range(0, len(config.Towns)):
            if config.Towns[i].name == valueTownSelected:
                chosen_town = config.Towns[i]
                # shows all houses in that town in the combobox house
                namesList = [h.name for h in chosen_town.houseList]
                namesList.sort()
                self.HouseCombobox3['values'] = namesList
                self.HouseCombobox3.delete(0, 'end')

    def checkRightTown(self, t):
        count = 0
        #checks whether that town name exists
        for i in range(0, len(config.Towns)):
            if t != config.Towns[i].name:
                count = count + 1
        if count == len(config.Towns):
            return False
        else:
            return True
    def checkRightHouse(self, t , h):
        count = 0
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        count = count + 1
        if count == 1:
            return True
        else:
            return False
    def checkAppNameExists(self, t, h, n):
        count = 0
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        for app in house.myAppliances:
                            if app.name == n:
                                count = count + 1
        if count == 1:
            return True
        else:
            return False
    def checkHouseNameExists(self, t, h):
        count = 0
        for town in config.Towns:
            if town.name ==t:
                for house in town.houseList:
                    if house.name == h:
                        count = count + 1
        if count ==1:
            return True
        else:
            return False

    ###### functions for frame 1 ####
    #something changes on house and appliance page
    def updateEnergyDisplay(self):
        if (self.SelectTownCombobox1.get()== ""):
            return
        t = self.SelectTownCombobox1.get()
        try:
            if not (self.checkRightTown(t)):
                raise ValueError("Town doesn't exist")
        except:
            showerror('Error', "Please select a town")
            self.SelectTownCombobox1.delete(0, 'end')
            return
        for town in config.Towns:
            if town.name == t:
                energy = town.energy_prediction[0]
                usedEnergy = town.energyUsed
        self.TownEnergyDisplay.config(text=str(energy) + " W/h")
        # if currently used energy in the town exceeds that of the production
        # the label is red, to show that more energy is used
        if (energy - usedEnergy < 0):
            self.EnergyUsedDisplay.config(text=str(usedEnergy) + " W/h", foreground='red')
        else:
            self.EnergyUsedDisplay.config(text=str(usedEnergy) + " W/h", foreground='green')

    def getTownValue1(self):
        t = self.SelectTownCombobox1.get()
        try:
            if not(self.checkRightTown(t)):
                raise ValueError("Town doesn't exist")
        except:
            showerror('Error', "Please select a town")
            self.SelectTownCombobox1.delete(0, 'end')
            return
        for town in config.Towns:
            if town.name == t:
                energy =  town.energy_prediction[0]
                usedEnergy = town.energyUsed
        self.TownEnergyDisplay.config(text = str(energy)+" W/h")
        #if currently used energy in the town exceeds that of the production
        # the label is red, to show that more energy is used
        if (energy - usedEnergy < 0):
            self.EnergyUsedDisplay.config(text = str(usedEnergy)+" W/h", foreground='red')
        else:
            self.EnergyUsedDisplay.config(text = str(usedEnergy)+" W/h", foreground='green')

        self.delete_scrolledtext()
        self.updateHouseCombobox1()

    def show_appliances_of_town(self):
        t = self.SelectTownCombobox1.get()
        h = self.selectHouseCombobox1.get()
        #set the state such that the scrollbar can be changed
        self.RunningAppScroll['state'] = 'normal'
        #delete the content that is inside
        self.RunningAppScroll.delete('0.0', 'end')
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        count = 1
                        self.houseInfoDisplay['state']='normal'
                        self.houseInfoDisplay.delete('0.0','end')
                        self.houseInfoDisplay.insert('0.0', str(house))
                        self.houseInfoDisplay['state']='disabled'
                        appliancesList = house.myAppliances
                        appliancesList.sort(key=lambda appliancesList: appliancesList.finishedTime)
                        for k in range(0, len(appliancesList)):
                            position = str(count)+'.0'
                            app = appliancesList[k]
                            if (app.state == "running"):
                                self.RunningAppScroll.insert(position, app.name+", will finish at: "+self.strDate(app.finishedTime)+"\n")
                                count = count +1
        self.RunningAppScroll['state'] = 'disabled'

        self.ScheduledAppScroll['state'] = 'normal'
        self.ScheduledAppScroll.delete('0.0', 'end')
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        count=1
                        appliancesList = house.myAppliances
                        appliancesList.sort(key = lambda appliancesList: appliancesList.scheduledTime)
                        for k in range(0, len(appliancesList)):
                            app = appliancesList[k]
                            if (app.state == 'scheduled'):
                                position = str(count) + '.0'
                                self.ScheduledAppScroll.insert(position,
                                                           app.name + ", will run at: " + self.strDate(app.scheduledTime) + ", set end time is: "+self.strDate(app.endTime)+ "\n")
                                count = count +1
                        appliancesList.sort(key=lambda appliancesList: appliancesList.endTime)
                        for k in range(0, len(appliancesList)):
                            app = appliancesList[k]
                            if (app.state == 'waiting'):
                                position = str(count) + '.0'
                                self.ScheduledAppScroll.insert(position,
                                                           app.name + ", is waiting to be scheduled, set end time is: " +self.strDate(app.endTime) +"\n")
                                count = count +1
        self.ScheduledAppScroll['state'] = 'disabled'

        self.FinishedAppScroll['state'] = 'normal'
        self.FinishedAppScroll.delete('0.0', 'end')
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        count = 1
                        appliancesList = house.myAppliances
                        appliancesList.sort(key=lambda appliancesList: appliancesList.finishedTime)
                        for k in range(0, len(appliancesList)):
                            position = str(count) + '.0'
                            app = appliancesList[k]
                            if (app.state == "finished"):
                                self.FinishedAppScroll.insert(position,
                                                             app.name + ", finished at: " + self.strDate(app.finishedTime) + "\n")
                                count = count + 1
        self.FinishedAppScroll['state'] = 'disabled'

    #### functions for frame 2 ####
    def from_add_to_change_House(self):
        # when radiobutton is pressed, it changes the shown frames in house
        self.changeHouseFrame.grid(column=0, row=3, padx=PADX_FRAMES, pady=PADY_FRAMES,sticky=tk.W)
        self.addHouseFrame.grid_forget()

    def from_change_to_add_House(self):
        #when radiobutton is pressed, it changes the shown frames in house
        self.addHouseFrame.grid(column=0, row=3,padx=PADX_FRAMES,pady=PADY_FRAMES, sticky=tk.W)
        self.changeHouseFrame.grid_forget()

    def getTownValue2(self):
        #get the value from the combobox of selected town
        valueTownSelected= self.combobox.get()
        #find the town in the Towns list
        for town in config.Towns:
            if town.name == valueTownSelected:
                chosen_town = town
        #list all houses in that town in the house combobox
        namesList = [h.name for h in chosen_town.houseList]
        namesList.sort()
        self.HouseCombobox['values']= namesList
        self.HouseCombobox.delete(0, 'end')

    def new_House_creation(self):
        #get selected town
        t = self.combobox.get()
        try:
            if (not(self.checkRightTown(t)) or t == ""):
                raise ValueError("Town doesn't exist")
        except:
            showerror('Error', "Please select a town")
            self.combobox.delete(0, 'end')
            return
        #get the new values
        n = self.nameEntry.get()
        try:
            if (self.checkHouseNameExists(t, n) or n ==""):
                raise ValueError("A House with that name already exists")
        except:
            showerror('Error', "A house with that name already exists")
            self.nameEntry.delete(0, 'end')
            return
        try:
            a = float(self.areaEntry.get())
        except:
            showerror('Error', "Area has to be a number")
            self.areaEntry.delete(0, 'end')
            return
        try:
            if (a < 0):
                raise ValueError("Area can't be negative")
        except:
            showerror('Error', "Area can't be negative")
            self.areaEntry.delete(0, 'end')
            return
        try:
            e = float(self.efficiencyEntry.get())
        except:
            showerror('Error', "Efficiency has to be a number")
        try:
            if (e < 0 or e > 1):
                raise ValueError("Efficiency has to be between 0 and 1")
        except:
            showerror('Error', "Efficiency has to be between 0 and 1")
            self.efficiencyEntry.delete(0, 'end')
            return
        try:
            ang = int(self.angleEntry.get())
        except:
            showerror('Error', "Angle has to be a number")
            self.angleEntry.delete(0, 'end')
            return
        try:
            if (ang < 0 or ang > 90):
                raise ValueError("Angle can't be smaller than 0 or bigger than 90 degrees")
        except:
            showerror('Error', "Angle has to be between 0 and 90 degrees")
            self.angleEntry.delete(0, 'end')
            return
        o = self.orientationEntry.get()
        try:
            if not (o in ["East", "South East", "South", "South West", "West"]):
                raise ValueError("Orientation has to be between East, South and West")
        except:
            showerror('Error', "Orientation has to be between East, South and West")
            self.orientationEntry.delete(0, 'end')
            return

        for town in config.Towns:
            if town.name == t:
                for check in town.houseList:
                    try:
                        if check.name == n:
                            raise ValueError(f"A house with this name already exists in this town")
                    except:
                        showerror('Error', f"A house with this name already exists in {town.name}")
                        self.nameEntry.delete(0, 'end')
                        return
                House(n,town, SolarPanel(a, ang, o, e))
                break
        # find the town in the Towns list
        for town in config.Towns:
            if town.name == t:
                chosen_town = town
                # list all houses in that town in the house combobox
                namesList = [house.name for house in chosen_town.houseList]
                namesList.sort()
                self.HouseCombobox['values'] = namesList
        self.updateHouseCombobox1()
        self.updateHouseCombobox3()
        self.delete_scrolledtext()
        self.nameEntry.delete(0, 'end')
        self.areaEntry.delete(0, 'end')
        self.orientationEntry.delete(0, 'end')
        self.efficiencyEntry.delete(0, 'end')
        self.angleEntry.delete(0, 'end')
        self.show_appliances_of_town()

        showinfo('Information', "Your house has been added to the town")

    def delete_house_button(self):
        # get selected town
        t = self.combobox.get()
        try:
            if (not(self.checkRightTown(t)) or t == ""):
                raise ValueError("Town doesn't exist")
        except:
            showerror('Error', "Please select a town")
            self.combobox.delete(0, 'end')
            return
        h = self.HouseCombobox.get()
        try:
            if (not (self.checkRightHouse(t, h)) or h == ""):
                raise ValueError("House doesn't exist")
        except:
            showerror('Error', "Please select a house")
            self.HouseCombobox.delete(0, 'end')
            return
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        house.removeSelfFromTown()
                        break

        self.HouseCombobox.delete(0, 'end')
        # find the town in the Towns list
        for town in config.Towns:
            if town.name == t:
                chosen_town = town
                # list all houses in that town in the house combobox
                namesList = [house.name for house in chosen_town.houseList]
                namesList.sort()
                self.HouseCombobox['values'] = namesList

        self.updateHouseCombobox1()
        self.updateHouseCombobox3()
        self.delete_scrolledtext()
        self.show_appliances_of_town()
        showinfo('Information', "Your house has been deleted")

    def new_value_house_button(self):
        t = self.combobox.get()
        try:
            if not(self.checkRightTown(t)):
                raise ValueError("Town doesn't exist")
        except:
            showerror('Error', "Please select a town")
            self.combobox.delete(0, 'end')
            return
        h = self.HouseCombobox.get()
        try:
            if not (self.checkRightHouse(t, h)):
                raise ValueError("House doesn't exist")
        except:
            showerror('Error', "Please select a house")
            self.HouseCombobox.delete(0, 'end')
            return
        change = self.changePropertyCombobox.get()
        try:
            if not (change in ["name", "area", "orientation", "efficiency", "angle"]):
                raise ValueError("property wrong")
        except:
            showerror('Error', "Select a property to be changed")
            self.changePropertyCombobox.delete(0, 'end')
            return
        value = self.newValueEntry.get()
        if change == "name":
            try:
                if (self.checkHouseNameExists(t, value) or value == "" ):
                    raise ValueError("House name already exists")
            except:
                showerror('Error', "A house with that name already exists")
                self.newValueEntry.delete(0, 'end')
                return
        #go through the town to find the right house
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        if change == 'name':
                            house.name = value
                        if change == 'area':
                            try: area = float(value)
                            except:
                                showerror('Error', "Area has to be a number")
                                self.newValueEntry.delete(0, 'end')
                                return
                            try:
                                house.solarPanel.area = float(value)
                            except:
                                showerror('Error', "Area can't be negative")
                                self.newValueEntry.delete(0, 'end')
                                return
                        if change == 'efficiency':
                            try: efficiency = float(value)
                            except:
                                showerror('Error', "Efficiency has to be a number")
                                self.newValueEntry.delete(0, 'end')
                                return
                            try:
                                house.solarPanel.efficiency = float(value)
                            except:
                                showerror('Error', "Efficiency must be greater than 0 but smaller than 1")
                                self.newValueEntry.delete(0, 'end')
                                return
                        if change == 'angle':
                            try: angle = int(value)
                            except:
                                showerror('Error', "Angle must be a number")
                                self.newValueEntry.delete(0, 'end')
                                return
                            try:
                                house.solarPanel.angle = int(value)
                            except:
                                showerror('Error', "Angle must be between 0 and 95 degrees")
                                self.newValueEntry.delete(0, 'end')
                                return
                        if change == 'orientation':
                            try:
                                house.solarPanel.orientation = value
                            except:
                                showerror('Error', "Orientation isn't valid, please enter something between East, "
                                                   "South and West")
                                self.newValueEntry.delete(0, 'end')
                                return
                        break
        self.HouseCombobox.delete(0, 'end')
        # find the town in the Towns list
        for town in config.Towns:
            if town.name == t:
                chosen_town = town
                # list all houses in that town in the house combobox
                namesList = [h.name for h in chosen_town.houseList]
                namesList.sort()
                self.HouseCombobox['values'] = namesList
        self.updateHouseCombobox1()
        self.updateHouseCombobox3()
        self.changePropertyCombobox.delete(0, 'end')
        self.newValueEntry.delete(0, 'end')
        self.show_appliances_of_town()
        showinfo('Information', "Your house has been changed")

    ###### functions for frame 3 #######
    def from_x_to_add_application(self):
        # when radiobutton is pressed, it changes the shown frames in application
        self.scheduleAppFrame.grid(column=0, row=4, padx=PADX_FRAMES, pady=PADY_FRAMES, sticky=tk.W)
        self.changeAppFrame.grid_forget()
        self.newTypeAppFrame.grid_forget()

    def from_x_to_change_application(self):
        # when radiobutton is pressed, it changes the shown frames in application
        self.changeAppFrame.grid(column=0, row=4, padx=PADX_FRAMES, pady=PADY_FRAMES, sticky=tk.W)
        self.scheduleAppFrame.grid_forget()
        self.newTypeAppFrame.grid_forget()

    def from_x_to_create_new_application(self):
        # when radiobutton is pressed, it changes the shown frames in application
        self.newTypeAppFrame.grid(column=0, row=4, padx=PADX_FRAMES, pady=PADY_FRAMES, sticky=tk.W)
        self.changeAppFrame.grid_forget()
        self.scheduleAppFrame.grid_forget()

    def show_types_appliances(self):
        self.TypesDisplay['state']='normal'
        self.TypesDisplay.delete('0.0', 'end')
        for i in range(0, len(Appliance.TypeList)):
            name, power, duration = Appliance.TypeList[i]
            position = str(i+1)+'.0'
            self.TypesDisplay.insert(position, name+" has power "+str(power)+"W and duration "+str(duration)+
                                     "h\n")
        self.TypesDisplay['state']='disabled'

    def getTownValue3(self):
        #gets the town selected in the town selection combobox
        valueTownSelected= self.combobox3.get()
        try:
            if not(self.checkRightTown(valueTownSelected)):
                raise ValueError("Town doesn't exist")
        except:
            showerror('Error', "Please select a town")
            self.combobox3.delete(0, 'end')
            return
        #looks for the right town in towns list
        for town in config.Towns:
            if town.name == valueTownSelected:
                chosen_town = town
        #shows all houses in that town in the combobox house
        namesList = [h.name for h in chosen_town.houseList]
        namesList.sort()
        self.HouseCombobox3['values']=namesList
        self.HouseCombobox3.delete(0, 'end')
        #when a new town is selected, it should delete what already is written
        #in combobox, so it will change correctly
        self.selectAppCombobox.delete(0, 'end')
        self.selectAppCombobox['values']=[]

    def schedule_application_button(self):
        t = self.combobox3.get()
        try:
            if not(self.checkRightTown(t)):
                raise ValueError("Town doesn't exist")
        except:
            showerror('Error', "Please select a town")
            self.combobox3.delete(0, 'end')
            return
        h = self.HouseCombobox3.get()
        try:
            if not (self.checkRightHouse(t, h)):
                raise ValueError("House doesn't exist")
        except:
            showerror('Error', "Please select a house")
            self.HouseCombobox3.delete(0, 'end')
            return
        n = self.appNameEntry.get()
        try:
            for town in config.Towns:
                if town.name == t:
                    # look for right house
                    for house in town.houseList:
                        if house.name == h:
                            for app in house.myAppliances:
                                if (app.name == n or n ==""):
                                    raise RuntimeError("Name for appliance already exists")

        except:
            showerror('Error', f"An appliance with this name already exists in this house, please chose another name")
            self.appNameEntry.delete(0, 'end')
            return
        type = self.appTypeCombobox.get()
        try:
            count = 0
            for triple in Appliance.TypeList:
                x, y, z = triple
                if x != type:
                    count= count+1
            #if type doesn't match any existing type, the counter will be as
            #high as the number of types, then it will raise an error
            if count == len(Appliance.TypeList):
                raise RuntimeError("The type isn't in the type list")
        except:
            showerror('Error', "The type input doesn't exist")
            self.appTypeCombobox.delete(0,'end')
            return

        try:
            year = int(self.appYearSpinbox.get())
        except:
            showerror('Error', "Year has to be a number")
            self.appYearSpinbox.delete(0, 'end')
            return
        try:
            month = int(self.appMonthSpinbox.get())
        except:
            showerror('Error', "Month has to be a number")
            self.appMonthSpinbox.delete(0, 'end')
            return
        try:
            day = int(self.appDaySpinbox.get())
        except:
            showerror('Error', "Day has to be a number")
            self.appDaySpinbox.delete(0, 'end')
            return
        try:
            hour = int(self.appHourSpinbox.get())
        except:
            showerror('Error', "Hour has to be a number")
            self.appHourSpinbox.delete(0, 'end')
            return
        try:
            minute = int(self.appMinuteCombobox.get())
        except:
            showerror('Error', "Minute has to be a number")
            self.appMinuteCombobox.delete(0, 'end')
            return

        for town in config.Towns:
            #look for right town
            if town.name == t:
                #look for right house
                for house in town.houseList:
                    if house.name == h:
                        try:
                            date = datetime.datetime(year, month, day, hour, minute)
                        except:
                            showerror('Error', "Invalid date")
                            self.appYearSpinbox.delete(0, 'end')
                            self.appMonthSpinbox.delete(0, 'end')
                            self.appDaySpinbox.delete(0, 'end')
                            self.appHourSpinbox.delete(0, 'end')
                            self.appMinuteCombobox.delete(0, 'end')
                            return
                        try:
                            Appliance(house, n, type, date)
                        except:
                            showerror('Error', "The end time isn't far enough in the future for the duration of the application")
                            self.appYearSpinbox.delete(0, 'end')
                            self.appMonthSpinbox.delete(0, 'end')
                            self.appDaySpinbox.delete(0, 'end')
                            self.appHourSpinbox.delete(0, 'end')
                            self.appMinuteCombobox.delete(0, 'end')
                            return
                        break
        # looks for all applications in that house from that town
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        self.selectAppCombobox['values'] = [app.name for app in house.myAppliances if (app.state == "waiting" or app.state=="scheduled")]
        self.appNameEntry.delete(0, 'end')
        self.appTypeCombobox.delete(0,'end')
        self.appYearSpinbox.delete(0,'end')
        self.appMonthSpinbox.delete(0, 'end')
        self.appDaySpinbox.delete(0, 'end')
        self.appHourSpinbox.delete(0, 'end')
        self.appMinuteCombobox.delete(0, 'end')
        self.show_appliances_of_town()
        self.getApplianceValues()
        showinfo('Information', "Your appliance has been added to the list")

    def getApplianceValues(self):
        #gets the values from town and house
        t = self.combobox3.get()
        try:
            if not(self.checkRightTown(t)):
                raise ValueError("Town doesn't exist")
        except:
            showerror('Error', "Please select a town")
            self.combobox3.delete(0, 'end')
            return
        h = self.HouseCombobox3.get()
        try:
            if not (self.checkRightHouse(t, h)):
                raise ValueError("House doesn't exist")
        except:
            showerror('Error', "Please select a house")
            self.HouseCombobox3.delete(0, 'end')
            return
        #looks for all applications in that house from that town
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        self.selectAppCombobox['values']= [app.name for app in house.myAppliances if (app.state == "waiting" or app.state=="scheduled")]

    def new_value_app_button(self):
        #function to update a new value
        t = self.combobox3.get()
        try:
            if not(self.checkRightTown(t)):
                raise ValueError("Town doesn't exist")
        except:
            showerror('Error', "Please select a town")
            self.combobox3.delete(0, 'end')
            return
        h = self.HouseCombobox3.get()
        try:
            if not (self.checkRightHouse(t, h)):
                raise ValueError("House doesn't exist")
        except:
            showerror('Error', "Please select a house")
            self.HouseCombobox3.delete(0, 'end')
            return
        a = self.selectAppCombobox.get()
        try:
            if (not a in self.selectAppCombobox['values'] or a == ""):
                raise ValueError("App not valid")
        except:
            showerror('Error', "Please select an appliance")
            self.selectAppCombobox.delete(0, 'end')
            return
        change = self.changeAppCombobox.get()
        try:
            if not (change in ["name", "duration", "power", "year", "month", "day", "hour", "minute"]):
                raise ValueError("property not valid")
        except:
            showerror('Error', "Please select the property to be changed")
            self.changeAppCombobox.delete(0, 'end')
            return
        value = self.newAppValueEntry.get()
        if change == "name":
            try:
                if self.checkAppNameExists(t, h, value):
                    raise ValueError("App with that name already exists")
            except:
                showerror('Error', "An appliance with that name already exists" )
                self.newAppValueEntry.delete(0, 'end')
                return
        #goes through the town, then house, then finds the application that should be changed
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        for app in house.myAppliances:
                            #looks for the attribute that should be changed
                            if app.name == a:
                                if change == 'name':
                                    app.name = value
                                if change == 'year':
                                    #try exception to make sure the date values are correct
                                    try:
                                        app.endTime = app.endTime.replace(year=int(value))
                                        #if appliance is changed, the state should go back to waiting
                                        #such that it is rescheduled
                                        app.state = "waiting"
                                        app.resetScheduledTime()
                                    except:
                                        showerror('Error', "Year doesn't exist, please enter a valid date")
                                        self.newAppValueEntry.delete(0, 'end')
                                        return
                                if change == 'month':
                                    try:
                                        app.endTime = app.endTime.replace(month=int(value))
                                        app.state = "waiting"
                                        app.resetScheduledTime()
                                    except:
                                        showerror('Error', "Month doesn't exist, please enter a valid date")
                                        self.newAppValueEntry.delete(0, 'end')
                                        return
                                if change == 'day':
                                    try:
                                        app.endTime = app.endTime.replace(day=int(value))
                                        app.state = "waiting"
                                        app.resetScheduledTime()
                                    except:
                                        showerror('Error', "Day doesn't exist, please enter a valid date")
                                        self.newAppValueEntry.delete(0, 'end')
                                        return
                                if change == 'hour':
                                    try:
                                        app.endTime = app.endTime.replace(hour=int(value))
                                        app.state = "waiting"
                                        app.resetScheduledTime()
                                    except:
                                        showerror('Error', "Hour doesn't exist, please enter a valid time")
                                        self.newAppValueEntry.delete(0, 'end')
                                        return
                                if change == 'minute':
                                    try:
                                        if not (value == '0' or value == '00' or value == '30'):
                                            raise ValueError ('Minute is of wrong value')
                                    except:
                                        showerror('Error', "Minute value isn't acceptable, please enter a valid value")
                                        self.newAppValueEntry.delete(0, 'end')
                                        return
                                    app.endTime= app.endTime.replace(minute=int(value))
                                    app.state = "waiting"
                                    app.resetScheduledTime()
                                if change == 'duration':
                                    try: d = int(value)
                                    except:
                                        showerror('Error', "Duration must be a number")
                                        self.newAppValueEntry.delete(0, 'end')
                                        return
                                    try:
                                        if (datetime.datetime.now() + datetime.timedelta(hours=(1 + int(value))) > app.endTime):
                                            raise RuntimeError
                                    except:
                                        showerror('Error', "Duration is past the set end time")
                                        self.newAppValueEntry.delete(0, 'end')
                                        return
                                    try:
                                        app.duration = int(value)
                                        app.state = "waiting"
                                        app.resetScheduledTime()
                                    except:
                                        showerror('Error', "Duration must be between 1 and 24 hours")
                                        self.newAppValueEntry.delete(0, 'end')
                                        return
                                if change == 'power':
                                    try: p = int(value)
                                    except:
                                        showerror('Error', "Power must be a number")
                                        self.newAppValueEntry.delete(0, 'end')
                                        return
                                    try:
                                        app.power = int(value)
                                        app.state = "waiting"
                                        app.resetScheduledTime()
                                    except:
                                        showerror('Error', "Power must be at least 1 Watt")
                                        self.newAppValueEntry.delete(0, 'end')
                                        return
                                break
        # looks for all applications in that house from that town
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        #can only change appliances that aren't running yet or not yet finished
                        self.selectAppCombobox['values'] = [app.name for app in house.myAppliances if (app.state == "waiting" or app.state=="scheduled")]
        self.selectAppCombobox.delete(0, 'end')
        self.changeAppCombobox.delete(0, 'end')
        self.newAppValueEntry.delete(0, 'end')
        self.show_appliances_of_town()
        self.getApplianceValues()
        showinfo('Information', "Your application has been changed")

    def delete_application_button(self):
        t = self.combobox3.get()
        try:
            if not(self.checkRightTown(t)):
                raise ValueError("Town doesn't exist")
        except:
            showerror('Error', "Please select a town")
            self.combobox3.delete(0, 'end')
            return
        h = self.HouseCombobox3.get()
        try:
            if not (self.checkRightHouse(t, h)):
                raise ValueError("House doesn't exist")
        except:
            showerror('Error', "Please select a house")
            self.HouseCombobox3.delete(0, 'end')
            return
        a = self.selectAppCombobox.get()
        try:
            if a == "":
                raise ValueError("Empty string")
        except:
            showerror('Error', "Chose an appliance")
            return
        count = 0
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        for app in house.myAppliances:
                            if app.name == a:
                                app.removeSelfFromHouse()
                                count = 1
                                break
        try:
            if count == 0:
                raise ValueError("app name doesn't exist")
        except:
            showerror('Error', "Please select an appliance")
            self.selectAppCombobox.delete(0, 'end')
            return
        for town in config.Towns:
            if town.name == t:
                for house in town.houseList:
                    if house.name == h:
                        self.selectAppCombobox['values'] = [app.name for app in house.myAppliances if (app.state == "waiting" or app.state=="scheduled")]
        self.changeAppCombobox.delete(0, 'end')
        self.selectAppCombobox.delete(0, 'end')
        self.HouseCombobox3.delete(0, 'end')
        self.combobox3.delete(0, 'end')
        self.show_appliances_of_town()
        showinfo('Information', "Your application has been deleted")

    def add_new_type_application(self):
        t = self.NewTypeEntry.get()
        try:
            if t =="":
                raise ValueError("Empty string")
        except:
            showerror('Error', "Chose a name for the new appliance type")
            return
        try:
            for type in Appliance.TypeList:
                tName, pow, dur = type
                if tName == t:
                    raise ValueError("Type name already exists")
        except:
            showerror('Error', "Type name already exists")
            self.NewTypeEntry.delete(0, 'end')
            return
        try: p = int(self.NewPowerEntry.get())
        except:
            showerror('Error', "Power must be a number")
            self.NewPowerEntry.delete(0, 'end')
            return
        try:
            if (p < 1):
                raise ValueError("Power must be at least 1 Watt")
        except:
            showerror('Error', "Power must be at least 1 Watt")
            self.NewPowerEntry.delete(0, 'end')
            return
        try: d = int(self.NewDurationEntry.get())
        except:
            showerror('Error', "Duration must be a number")
            self.NewDurationEntry.delete(0, 'end')
            return
        try:
            if (d < 1 or d > 24):
                raise ValueError("Duration must be between 1 and 24 hours")
        except:
            showerror('Error', "Duration must be between 1 and 24 hours")
            self.NewDurationEntry.delete(0, 'end')
            return

        Appliance.TypeList.append((t,p,d))
        self.appTypeCombobox['values'] = [t for t, p, d in Appliance.TypeList]
        self.NewTypeEntry.delete(0, 'end')
        self.NewPowerEntry.delete(0, 'end')
        self.NewDurationEntry.delete(0, 'end')
        self.show_types_appliances()
        showinfo('Information', "New type has been added")