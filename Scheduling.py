#scheduling class that says when which appliance should be run
import config
import datetime

class Scheduling:

    @staticmethod
    def schedule_appliances(t, this_date, lock):
        lock.acquire()

        waitingList = []
        scheduledList = []
        runningList = []

        #the next full hour for which the scheduling should be done
        next_hour = (this_date.hour + 1) % 24
        this_date = this_date.replace(hour = next_hour)

        #make a copy of the energy prediction of the town to work with
        availableEnergy = config.Towns[t].energy_prediction.copy()

        #go through all houses and their lists of appliances and pool them together
        for j in range(0, len(config.Towns[t].houseList)):
            waitingListj = [app for app in config.Towns[t].houseList[j].myAppliances if app.state == "waiting"]
            waitingList = waitingList + waitingListj
            scheduledListj = [app for app in config.Towns[t].houseList[j].myAppliances if app.state == "scheduled"]
            scheduledList = scheduledList+scheduledListj
            runningListj = [app for app in config.Towns[t].houseList[j].myAppliances if app.state == "running"]
            runningList = runningList + runningListj

        #sorts the list by duration of the appliances, from longest to shortest
        waitingList.sort(key = lambda waitingList: waitingList.endTime)
        scheduledList.sort(key = lambda scheduledList: scheduledList.scheduledTime)
        runningList.sort(key = lambda runningList: runningList.scheduledTime)

        ### step 1: take away energy that is used for already running appliances ###
        for app in runningList:
            difference = this_date - app.scheduledTime
            tot_sec = difference.total_seconds()
            hour_difference = int(tot_sec/3600)
            #if duration is over, the app is finished and can be set to finished
            if (hour_difference == app.duration):
                app.state = "finished"
                #if the app has already finished, no energy has to
                continue
            else:
                #hours left to run are the duration minus the hours already gone by
                hours_left = app.duration-hour_difference
                for i in range(0, hours_left):
                    #available energy will be the energy from solar panels minus the power needed for the app
                    availableEnergy[i] = availableEnergy[i] - app.power

        #update the real appliance that it has finished
        for app in runningList:
            if app.state == "finished":
                #if the app has finished, go update the state in the Towns list
                for i in range(0, len(config.Towns[t].houseList)):
                    for realApp in config.Towns[t].houseList[i].myAppliances:
                        if app == realApp:
                            realApp.state = "finished"
                            break

        ### step 2: take away energy that will be used by appliances that are already scheduled ###
        for app in scheduledList:
            difference =  abs(this_date - app.scheduledTime)
            tot_sec = difference.total_seconds()
            #hour difference is in how many hours the appliance will start to run
            hour_difference = int(tot_sec / 3600)
            for i in range((hour_difference), (hour_difference+app.duration)):
                availableEnergy[i] = availableEnergy[i] - app.power
            if hour_difference == 0:
                app.state= "running"
        #update the real apps for those that are running now
        for app in scheduledList:
            if app.state == "running":
                #if the app has finished, go update the state in the Towns list
                for i in range(0, len(config.Towns[t].houseList)):
                    for realApp in config.Towns[t].houseList[i].myAppliances:
                        if app == realApp:
                            realApp.state = "running"
                            break

        ### step 3: go through all waiting appliances and schedule them ###
        for app in waitingList:
            #check if the appliance has to run within the next 48hours, if not
            #then it isn't scheduled and stays in state waiting
            difference = app.endTime -  this_date
            tot_sec = difference.total_seconds()
            # hour difference is in how many hours the appliance will start to run
            hour_difference = int(tot_sec / 3600)
            if (hour_difference > 48):
                #then too far in the future -> continue to next appliance
                continue

            maxRestEnergy=0
            index = 0
            #max will have to start with the first time interval
            for k in (0, app.duration):
                maxRestEnergy = maxRestEnergy + (availableEnergy[k]-app.power)

            #iterate over the energy list, but only until the point where the duration would
            #still be able, e.g. for appliance with duration of 2h, it would be until index 46
            #start at 1 because the first interval is the one set to the reference max
            for i in range(1, (hour_difference-app.duration)):
                #look for timespan over which the energy left in grid is maximal
                restEnergy = 0
                for j in range(i, i+app.duration):
                    restEnergy = restEnergy + (availableEnergy[j]-app.power)
                #if the rest energy in the grid is bigger for this time interval, then change
                #the max rest energy to current rest energy
                if maxRestEnergy < restEnergy:
                    maxRestEnergy = restEnergy
                    index = i

            #found the max rest energy and have the index -> set the scheduled time
            dateNow = datetime.datetime(this_date.year, this_date.month, this_date.day, next_hour, 0,0,0)
            if index == 0:
                app.setScheduleTime(dateNow)
                app.state = "running"
            else:
                #add the amount of hours in the future
                chosenDate = dateNow + datetime.timedelta(hours= index)
                #set this date as schedule
                app.setScheduleTime(chosenDate)
                app.state = "scheduled"
            #take away energy needed for this scheduled appliance from available energy list
            for x in (index, index+app.duration):
                availableEnergy[x] = availableEnergy[x]-app.power

        for app in waitingList:
            if app.state == "scheduled":
                #update the real app to scheduled and set the scheduled time
                for house in config.Towns[t].houseList:
                    for realApp in house.myAppliances:
                        if app == realApp:
                            realApp.state = "scheduled"
                            realApp.setScheduleTime(app.scheduledTime)
                            break

        ### step 4: delete all finished apps, that have been finished for 24hours ###
        #go through each house in the town
        for house in config.Towns[t].houseList:
            #go through each app in the house and check whether the state is finished and for the last 24h
            for app in house.myAppliances:
                difference = this_date - app.finishedTime
                tot_sec = difference.total_seconds()
                hour_difference = int(tot_sec / 3600)
                if app.state== "finished" and hour_difference>=24:
                    #delete app from the house
                    app.removeSelfFromHouse()

        ### update the energy used for this hour in this town ###
        config.Towns[t].energyUsed = config.Towns[t].energy_prediction[0] - availableEnergy[0]

        lock.release()