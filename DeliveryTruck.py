
# Class created for the freight trucks which deliver the packages
class DT:
    def __init__(self, max_capacity, travel_speed, current_load, package_list, distance_traveled, current_address, departure_time):
        # Similar to package class, attributes/variables associated to function and class
        self.max_capacity = max_capacity
        self.travel_speed = travel_speed
        self.current_load = current_load
        self.package_list = package_list
        self.distance_traveled = distance_traveled
        self.current_address = current_address
        self.departure_time = departure_time
        self.current_time = departure_time

    # Below formats the object of the class in a more presentable and concise manner by using formatted strings
    # It will force a string representation of the class object
    def __str__(self):
        return f"{self.max_capacity}, {self.travel_speed}, {self.current_load}, {self.package_list}, {self.distance_traveled}, {self.current_address}, {self.departure_time}"




