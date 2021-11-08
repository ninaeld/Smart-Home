#Interfacing Smart Homes to their local Smart Grid
###Bachelor Thesis by Nina Eldridge

##Prerequisites
* Internet connection
* Python version 3 installed
* The packages matplotlib, numpy, requests, pysolar and schedule need to be installed
* To install them use pip install <package_name> for Windows

##How to use
1. Download the whole file
2. Run the Main.py file
3. Use the Graphical User Interface to interact with the program

##Important
* The program only works with local storage, all changes made will be lost when closing 
  the program

* Towns, Houses and some Appliances are already added in the main file, such that
the program can already be used
  
* Towns cannot be altered once the program is running

* The calculations and schedulings are done in real time, i.e. every hour.
To test the program uncomment lines 42, 53 and 61 or 62 in Main.py and comment line
  58 in Main.py. That way calculations and schedulings are done every minute or every 15 seconds to test whether they work.