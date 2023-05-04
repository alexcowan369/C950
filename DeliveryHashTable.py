# Below is the hash table named "DeliveryHashTable"
# Initial number of buckets is set to 20
# Note: the lone "_" is used in this case to indicate a value is not needed, acting as a placeholder
class DeliveryHashTable:
    def __init__(self, initial_capacity=20):
        self.buckets = [list() for _ in range(initial_capacity)]

# This class is the INSERT FUNCTION
# The method takes a key value pair which will be used for the packages
# Updating and inserting will take place with the function
    def put(self, key, value):
        # Index to store the key-value is determined by calculating the hash of the key
        # and taking the modulus of the buckets
        index = hash(key) % len(self.buckets)
        bucket = self.buckets[index]  # Bucket is retrieved at selected index 0,1,2 etc
        # Enumerate is used in this case to iterate or loop through the key-value pairs in the bucket
        # Enumerate also allows the index to be tracked
        # Key value pair is a number and package
        for index, (number, package) in enumerate(bucket):
            if number == key:
                bucket[index] = (key, value)
                return True
        # Key-value pair is added to the end of bucket only if the key is not found above
        bucket.append((key, value))
        return True

    # This will be the LOOKUP FUNCTION
    # Below is similar to the insert function but this will search for the key in hash table instead
    def get(self, key):
        index = hash(key) % len(self.buckets)
        bucket = self.buckets[index]

        for current_number, package in bucket:
            # Checking is bucket is equal to the key inputted
            if current_number == key:
                # Correlating package is returned if key is found
                return package
        return None

    # This is the REMOVE FUNCTION of the hashtable
    # Inputted key-value pair is removed from the table
    def remove(self, key):
        index = hash(key) % len(self.buckets)
        bucket = self.buckets[index]

        for index, (number, package) in enumerate(bucket):
            if number == key:
                # Once key is located via being shown as equal delete it
                # from the list at the specific index
                del bucket[index]
                return True
        return False
