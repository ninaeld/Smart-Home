
import requests
import pysolar.solar as solar
import datetime
import pysolar.radiation as radiation
import config
from math import sin, cos

class Calculations:

    #calculates the cloud and energyprediction for a given town
    @staticmethod
    def get_predictions(t, this_date, lock):
        lock.acquire()
        ### First part = cloud prediction ###
        #clear lists to update them afterwards
        config.Towns[t].cloud_prediction.clear()
        config.Towns[t].energy_prediction.clear()
        #use local variables to assign them to the town variables at the end
        cloud_p = []
        energy_p = [0]*48

        #the next full hour for which the scheduling should be done
        next_hour = (this_date.hour + 1) % 24
        this_date = this_date.replace(hour=next_hour)

        town = config.Towns[t].name.lower()
        link = 'https://prevision-meteo.ch/services/json/' + str(town)
        #request the weather website for the prediction
        response = requests.get(link)
        #check whether the request to the website was successful
        if not response.status_code == 200:
            raise ValueError("Request wasn't successful")

        #calculate the cloud prediction over the next 48 hours
        #first loop responsible for ending day 0
        for x in range(next_hour,24):
            hour = str(x) + 'H00'
            # gets the values out of the json file of the request
            # data in a range of 0 to 100
            value_high = response.json()['fcst_day_0']['hourly_data'][hour]['HCDC']
            value_mid = response.json()['fcst_day_0']['hourly_data'][hour]['MCDC']
            value_low = response.json()['fcst_day_0']['hourly_data'][hour]['LCDC']
            # cast the values from a string to a float
            HCDC = float(value_high)
            MCDC = float(value_mid)
            LCDC = float(value_low)
            # take the average value to get the average coverage of the sky
            average_value = (HCDC + MCDC + LCDC) / 3
            rounded_value = round(average_value, 0)
            #convert it to a decimal number, cause we need it later for the energy prediction
            decimal_value = rounded_value / 100

            # append the values into a list
            cloud_p.append(decimal_value)

        #second loop to get all 24h of the first day
        for y in range(24):
            hour = str(y) + 'H00'
            # gets the values out of the json file of the request
            # data in a range of 0 to 100
            value_high = response.json()['fcst_day_1']['hourly_data'][hour]['HCDC']
            value_mid = response.json()['fcst_day_1']['hourly_data'][hour]['MCDC']
            value_low = response.json()['fcst_day_1']['hourly_data'][hour]['LCDC']
            # cast the values from a string to a float
            HCDC = float(value_high)
            MCDC = float(value_mid)
            LCDC = float(value_low)
            # take the average value to get the average coverage of the sky
            average_value = (HCDC + MCDC + LCDC) / 3
            rounded_value = round(average_value, 0)
            # convert it to a decimal number, cause we need it later for the energy prediction
            decimal_value = rounded_value / 100

            # append the values into a list
            cloud_p.append(decimal_value)

        #third loop to get the remaining hours adding up to 48h
        for z in range(next_hour):
            hour = str(z) + 'H00'
            # gets the values out of the json file of the request
            # data in a range of 0 to 100
            value_high = response.json()['fcst_day_2']['hourly_data'][hour]['HCDC']
            value_mid = response.json()['fcst_day_2']['hourly_data'][hour]['MCDC']
            value_low = response.json()['fcst_day_2']['hourly_data'][hour]['LCDC']
            # cast the values from a string to a float
            HCDC = float(value_high)
            MCDC = float(value_mid)
            LCDC = float(value_low)
            # take the average value to get the average coverage of the sky
            average_value = (HCDC + MCDC + LCDC) / 3
            rounded_value = round(average_value, 0)
            # convert it to a decimal number, cause we need it later for the energy prediction
            decimal_value = rounded_value / 100

            # append the values into a list
            cloud_p.append(decimal_value)

        print("This is the cloud prediction for " + str(next_hour) + " in " + config.Towns[t].name)
        print(cloud_p)

        ### Second part = energy prediction ###
        #necessary information for irradiation
        lat = response.json()['city_info']['latitude']
        long = response.json()['city_info']['longitude']
        latitude = float(lat)
        longitude = float(long)

        #step 1: from data get approximated irradiation
        this_year = this_date.year
        this_month = this_date.month
        this_day = this_date.day

        for house in config.Towns[t].houseList:
            houseEnergy = []

            #do that for each house and add it up
            for x in range(next_hour,24):
                #calculates the expected radiation on a sunny day depending on the date/time
                current_date = datetime.datetime(this_year, this_month, this_day, x, 0, 0, 0, tzinfo=datetime.timezone.utc)
                current_altitude = solar.get_altitude(latitude, longitude, current_date)
                direct_radiation = radiation.get_radiation_direct(current_date, current_altitude)
                houseEnergy.append(direct_radiation)

            # have to account for a new day, which could also mean new month, maybe even new year
            next_day = this_date + datetime.timedelta(days=1)
            for y in range(24):
                # calculates the expected radiation on a sunny day depending on the date/time
                current_date = datetime.datetime(next_day.year, next_day.month, next_day.day, y, 0, 0, 0,
                                                     tzinfo=datetime.timezone.utc)
                current_altitude = solar.get_altitude(latitude, longitude, current_date)
                direct_radiation = radiation.get_radiation_direct(current_date, current_altitude)
                houseEnergy.append(direct_radiation)

            second_day = next_day + datetime.timedelta(days=1)
            for z in range(next_hour):
                # calculates the expected radiation on a sunny day depending on the date/time
                current_date = datetime.datetime(second_day.year, second_day.month, second_day.day, z, 0, 0, 0,
                                                 tzinfo=datetime.timezone.utc)
                current_altitude = solar.get_altitude(latitude, longitude, current_date)
                direct_radiation = radiation.get_radiation_direct(current_date, current_altitude)
                houseEnergy.append(direct_radiation)

            # step 2: update value in the house energy prediction
            # real irradiation = (1-cloudiness) * direct radiation from pySolar
            # this value is per square meter
            for i in range(48):
                real_irradiation = (1 - cloud_p[i]) * houseEnergy[i]
                rounded_irradiation = round(real_irradiation, 2)
                houseEnergy[i] = rounded_irradiation

            # step 3: adapt that energy depending on area and efficiency
            # iterate over the list of all houses -> getting their area, angle orientation and efficiency
            # while applying the available energy of that hour to each house
            # put it in new list energy available
            if(house.solarPanel.orientation == "East"):
                azimuthSolarPanel = 90
            elif(house.solarPanel.orientation == "South East"):
                azimuthSolarPanel = 135
            elif(house.solarPanel.orientation == "South"):
                azimuthSolarPanel = 180
            elif(house.solarPanel.orientation == "South West"):
                azimuthSolarPanel = 225
            else:
                azimuthSolarPanel = 270 #last case that it is West

            inclinationSolarPanel = house.solarPanel.angle
            print(azimuthSolarPanel)
            for i in range(0, (24-next_hour)):
                #get current date and time
                current_date = datetime.datetime(this_year, this_month, this_day, (next_hour+i), 0, 0, 0,
                                                 tzinfo=datetime.timezone.utc)
                #get the altitude of the sun at that time, and calculate theta
                thetaSun = 90 - solar.get_altitude(latitude, longitude, current_date)
                azimuthSun = solar.get_azimuth(latitude, longitude, current_date)

                effectiveArea = abs(house.solarPanel.area * (sin(thetaSun)*cos(azimuthSun)*sin(inclinationSolarPanel)*cos(azimuthSolarPanel) +
                                                        sin(thetaSun)*sin(azimuthSun)*sin(inclinationSolarPanel)*sin(azimuthSolarPanel)*cos(inclinationSolarPanel)
                                                         + cos(thetaSun)*cos(inclinationSolarPanel)))
                print("This is effective area")
                print(effectiveArea)

                #the energy output is then the effective area times the irradiation times the efficiency
                houseEnergy[i] = round(effectiveArea * houseEnergy[i] * house.solarPanel.efficiency, 1)
                energy_p[i] = round(energy_p[i] + houseEnergy[i], 1)
            for j in range((24-next_hour), (24-next_hour)+24):
                houseEnergy[j] = round(house.solarPanel.area * houseEnergy[j] * house.solarPanel.efficiency, 1)
                energy_p[j] = round(energy_p[j] + houseEnergy[j], 1)
            for k in range((24-next_hour)+24, 48):
                houseEnergy[k] = round(house.solarPanel.area * houseEnergy[k] * house.solarPanel.efficiency, 1)
                energy_p[k] = round(energy_p[k] + houseEnergy[k], 1)

            house.currentEnergyProduction = houseEnergy[0]

        print("This is the energy prediction for " + str(config.Towns[t].name) + " considering the area of solar panels")
        print(energy_p)

        config.Towns[t].cloud_prediction = cloud_p
        config.Towns[t].energy_prediction = energy_p

        lock.release()
