# Class created for WGUPS packages
class WGUPSPackage:
    def __init__(self, package_id, destination_address, destination_city, destination_state, destination_zip, deadline, package_weight, delivery_status):
        # These attributes/variables below are associated to the package class and function above
        self.package_id = package_id
        self.destination_address = destination_address
        self.destination_city = destination_city
        self.destination_state = destination_state
        self.destination_zip = destination_zip
        self.deadline = deadline
        self.package_weight = package_weight
        self.delivery_status = delivery_status
        self.left_hub_time = None
        self.arrival_time = None

    # Below formats the object of the class in a more presentable and concise manner by using formatted strings
    # It will force a string representation of the class object
    def __str__(self):
        return f"{self.package_id}, {self.destination_address}, {self.destination_city}, {self.destination_state}, {self.destination_zip}, {self.deadline}, {self.package_weight}, {self.arrival_time}, {self.delivery_status}"

    # The status_update method below checks the current times of the packages in their stages of delivery
    # If they align with the equations/assumptions below they will either say:
    # "Delivered", "En Route to Destination", or say "At Central Hub"
    def status_update(self, timedelta_convert):
        if self.arrival_time < timedelta_convert:
            self.delivery_status = "DELIVERED"
        elif self.left_hub_time > timedelta_convert:
            self.delivery_status = "EN ROUTE TO DESTINATION"
        else:
            self.delivery_status = "AT CENTRAL HUB"