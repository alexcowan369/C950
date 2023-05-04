

# Alexander Cowan
# Student ID: #005261646
# WGU Package Delivery Service


import csv
import datetime
from DeliveryTruck import DT
from builtins import ValueError
# Note for clarity later: Modules are files that contain python
# Classes are within the modules, different from Java where classes do NOT have to match the file name in python that's why it threw me off
# From the MODULE (aka file named) DeliverHashTable I am importing the CLASS DeliveryHashTable inside the module
from DeliveryHashTable import DeliveryHashTable
from WGUPSPackage import WGUPSPackage

# Reads the specific CSV file associated with all the distance values inside it
with open("CSV_files/Distance_File.csv") as csvdistance:
    Distance_in_CSV = csv.reader(csvdistance)
    Distance_in_CSV = list(Distance_in_CSV)

# Reads the specific CSV file associated with all the address values inside it
with open("CSV_files/Address_File.csv") as csvaddress:
    Address_in_CSV = csv.reader(csvaddress)
    Address_in_CSV = list(Address_in_CSV)

# Reads the specific CSV file associated with all the package values inside it
with open("CSV_files/Package_File.csv") as csvpackage:
    Package_in_CSV = csv.reader(csvpackage)
    Package_in_CSV = list(Package_in_CSV)


# Package objects are created from the CSV package file which contain all the package data
# The package objects which were created are loaded in the hash table for future use: pack_hash_table
# From now on "pack" will be shortcut for package
def load_pack_data(filename, pack_hash_table):
    with open(filename) as package_csv_info:
        all_pack_data = csv.reader(package_csv_info)
        for package in all_pack_data:
            packID = int(package[0])
            packAddress = package[1]
            packCity = package[2]
            packState = package[3]
            packZipcode = package[4]
            packDeadline_time = package[5]
            packWeight = package[6]
            packStatus = "AT PACKAGE HUB"

            # Package object below aka new instance of WGUPSPackage class
            p = WGUPSPackage(packID, packAddress, packCity, packState, packZipcode, packDeadline_time, packWeight, packStatus)

            # Insert packID into hash table for use later
            # Reminder: "pack_hash_table" is an instance of the "DeliveryHashTable" class
            pack_hash_table.put(packID, p)


# Below is the method for finding distance between two addresses
# X and Y will act as the placeholders for the two values
def distance_between_pack(x, y):
    packdistance = Distance_in_CSV[x][y]
    if packdistance == '':
        packdistance = Distance_in_CSV[y][x]

    return float(packdistance)

# Method below extracts the address number form the correlating strings in csv
# row index of 2 is the index/location where addresses are stored in csv
# if an address is identified code grabs the number associated with it which is at index of 0
def find_csv_address_id(target_address):
    for csv_row in Address_in_CSV:
        current_address = csv_row[2]
        if target_address == current_address:
            address_id = int(csv_row[0])
            return address_id

# The three truck objects are below
# Truck object truck_A created which is the 1st of 3 trucks with truck_C being the 3rd.
# Naming method matching to an index for clarity where the first item is at index 0
# Order doesn't matter as Nearest Neighbor will sort the packages accoringly
truck_A = DT(
    max_capacity=16,
    travel_speed=18,
    current_load=None,
    package_list=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    distance_traveled=0.0,
    current_address="4001 South 700 East",
    departure_time=datetime.timedelta(hours=8)
)
# Truck object truck_B created
truck_B = DT(
    max_capacity=16,
    travel_speed=18,
    current_load=None,
    package_list=[13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
    distance_traveled=0.0,
    current_address="4001 South 700 East",
    departure_time=datetime.timedelta(hours=10, minutes=20)
)
# Truck object truck_C created
truck_C = DT(
    max_capacity=16,
    travel_speed=18,
    current_load=None,
    package_list=[29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
    distance_traveled=0.0,
    current_address="4001 South 700 East",
    departure_time=datetime.timedelta(hours=9, minutes=5)
)

# DeliveryHashTable instance created then stored in "pack_hash_table" variable
pack_hash_table = DeliveryHashTable()

# Hash table loaded with packages, function is called from above
load_pack_data("CSV_files/Package_File.csv", pack_hash_table)

# In the method below, the "Nearest neighbor algorithm" is used for ordering packages on the selected main_truck/trucks
# Distance a selected truck drives once packages are sorted is also calculated below
def deliver_packages(main_truck):
    # Empty list is created to store packages
    undelivered_packages = []
    # Below iterates or loops through the package IDs then is appended to "undelivered_packages" list
    for pkg_id in main_truck.package_list:
        pkg = pack_hash_table.get(pkg_id)
        undelivered_packages.append(pkg)
    # Packages list is cleared, "main_truck" object/instance will now store packages
    main_truck.package_list = []
    # Loop continues if there are undelivered packages
    while undelivered_packages:
        # Arbitrary high value is selected here to make sure the algorithm chooses the shortest distances later on
        closest_distance = 3500
        # This variable is initialized/created to store the package that is the closest to the truck
        closest_package = None
        # Iterating through packages in the "undelivered_packages" list
        for pkg in undelivered_packages:
            # Distance between the packages is calculated using the two functions
            # made earlier: "distance_between_pack" and "find_csv_address_id"
            current_distance = distance_between_pack(find_csv_address_id(main_truck.current_address), find_csv_address_id(pkg.destination_address))
            # Checking to see if current distance is less than OR equal to the closest distance so far
            if current_distance <= closest_distance:
                # Updating the with current distance
                closest_distance = current_distance
                # Assigns the closest package to the current package
                closest_package = pkg
        # Below the closest package ID is appended to the packages list
        main_truck.package_list.append(closest_package.package_id)
        # Closest package is then removed
        undelivered_packages.remove(closest_package)
        # Mileage is then updated by adding the closest distance to it
        main_truck.distance_traveled += closest_distance
        # Main_truck address is now updated to the closest_package address
        main_truck.current_address = closest_package.destination_address
        # Time is update accordingly using the 18 mph speed
        main_truck.current_time += datetime.timedelta(hours=closest_distance / 18)
        # The current delivery time is set to be the time of the closest package
        closest_package.arrival_time = main_truck.current_time
        # Departure time of the closest package is now set to the main_trucks departure time
        # Like going down steps of a ladder
        closest_package.left_hub_time = main_truck.departure_time
# Trucks utilize the algorithm above tp deliver packages
# Once this is completed the attributes I assigned to each truck will be updated accordingly
deliver_packages(truck_A)
deliver_packages(truck_B)
# Below makes sure truck_C does not leave too early
# It will leave as soon as truck_A or truck_B finishes their deliveries
truck_C.departure_time = min(truck_A.current_time, truck_B.current_time)
# After fulfilling the time requirements of above truck_C then leaves to deliver
deliver_packages(truck_C)

class CLI:
    # Below is the User Interface
    # As the program is run the text below is displayed in terminal
    print("Western Governors University Parcel Service (WGUPS) Incorporated")
    print("The total mileage for the route via the nearest neighbor algorithm is: ")
    print(truck_A.distance_traveled + truck_B.distance_traveled + truck_C.distance_traveled)  # Combines the mileage to get total mileage determined by algo
    # The user will be prompted to start the program by pressing enter
    text = input("---- Press enter key to start program ---- ")
    # The program will keep looping for multiple queries unless user inputs 'exit'
    while True:
        text = input("Enter 'time' to check package status or 'exit' to quit: ")
        # After pressing enter you are now prompted to enter 'time' or 'exit' to "maneuver" the program
        if text.lower() == "time":
            while True:
                # Since true was entered user enters the new nested while loop requesting a specific time to check
                try:
                    unique_time = input("Check status of packages by entering a time using format, HH:MM:SS ")
                    (h, m, s) = unique_time.split(":")
                    timedelta_convert = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    break
                # If time is invalid user is told to use to the correct time format to advance
                except ValueError:
                    print("Invalid time format, please try again and use HH:MM:SS.")
                    continue
            # User has passed the first loop which then advances them to the next loop
            # This loop below asks what status of package they want
            while True:
                second_input = input(
                    "For status of a single package type 'solo'. For a status of all packages type 'all': ")
                # Logic for the "solo" input below
                if second_input.lower() == "solo":
                    # Requests the package ID number from user then tests that number against the range of 1-41
                    # If an incorrect input is submitted it will break user out of loop and back to the previous prompt while explaining what to input
                    solo_input = int(input("Enter package ID number: "))
                    if 0 < solo_input < 41:
                        package = pack_hash_table.get(solo_input)
                        package.status_update(timedelta_convert)
                        print(str(package))
                        break
                    else:
                        print("Entry invalid sent back to previous prompt, input a number in the range of 1 to 40")
                # Logic for the "all" input below
                elif second_input.lower() == "all":
                    # self-explanatory as all packages are then shown on the screen during the selected time
                    for packageID in range(1, 41):
                        package = pack_hash_table.get(packageID)
                        package.status_update(timedelta_convert)
                        print(str(package))
                    break
                # If input is incorrect the following message is displayed to user
                else:
                    print("Entry invalid, input 'solo' or 'all'")
        # Option to terminate the program
        elif text.lower() == "exit":
            print("Program will now terminate please rerun to use again.")
            exit()
        # "Error" message explaining how to enter the correct input
        else:
            print("Entry invalid, please enter 'time' or 'exit' with no spaces")




