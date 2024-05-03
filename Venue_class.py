import re
class Venue:
    """A class to represent a venue"""
    venues = {}      # A dictionary to store venues
    # Constructor
    def __init__(self, venue_id = "", name = "", min_num_guests = 0, max_num_guests = 0, phone_num = "", address = ""):
        self.__venue_id = self.validate_venue_id(venue_id)
        self.__venue_name = self.validate_venue_name(name)
        self.__min_num_guests = self.validate_num_guests(min_num_guests)
        self.__max_num_guests = self.validate_num_guests(max_num_guests, is_max=True)
        self.__phone = self.validate_phone(phone_num)
        self.__address = self.validate_address(address)

    # Exception Handling
    def validate_venue_id(self, venue_id):
        """Validate the venue ID to ensure it follows the format 'Vxxx', where 'xxx' are digits"""
        if not venue_id or not re.match(r'V\d{3}', venue_id):
            raise ValueError("Venue ID must be in the format 'Vxxx', where 'xxx' are digits")
        return venue_id
    def validate_venue_name(self, name):
        """Validate the venue name to ensure it is non-empty"""
        if not name:
            raise ValueError("Venue name must be non-empty")
        return name

    def validate_num_guests(self, num, is_max=False):
        """Validate the number of guests to ensure it is a positive integer"""
        if not isinstance(num, int) or num <= 0:
            raise ValueError(f"{'Maximum' if is_max else 'Minimum'} number of guests must be a positive integer")
        return num

    def validate_phone(self, phone):
        """Validate the phone number to ensure it is a 10-digit number"""
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone number must be a 10-digit number")
        return phone

    def validate_address(self, address):
        """Validate the address to ensure it is non-empty"""
        if not address:
            raise ValueError("Address must be non-empty")
        return address

    def add_venue(self):
        """A method to add a venue to the dictionary"""
        Venue.venues[self.__venue_id] = self

    def delete_venue(self, venue_id):
        """A method to delete a venue using its ID"""
        if venue_id in Venue.venues:            # Checking if the venue exists and delete it
            del Venue.venues[venue_id]
            print("Venue deleted successfully")
        else:
            print("Venue not found")

    def print_venue_details(self):
        """Prints all details of a venue"""
        venue_details = (f"Venue ID: {self.get_venue_id()}, "
                         f"Venue Name: {self.get_venue_name()}, "
                         f"Minimum Number of Guests: {self.get_min_num_guests()}, "
                         f"Maximum Number of Guests: {self.get_max_num_guests()}, "
                         f"Phone Number: {self.get_phone()}, "
                         f"Address: {self.get_address()}")
        return venue_details
    # Setter and getter
    def set_venue_id(self, venue_id):
        self.__venue_id = self.validate_venue_id(venue_id)

    def get_venue_id(self):
        return self.__venue_id

    def set_venue_name(self, name):
        self.__venue_name = self.validate_venue_name(name)

    def get_venue_name(self):
        return self.__venue_name

    def set_min_num_guests(self, min_num_guests):
        self.__min_num_guests = self.validate_num_guests(min_num_guests)

    def get_min_num_guests(self):
        return self.__min_num_guests

    def set_max_num_guests(self, max_num_guests):
        self.__max_num_guests = self.validate_num_guests(max_num_guests, is_max=True)

    def get_max_num_guests(self):
        return self.__max_num_guests

    def set_phone(self, phone_num):
        self.__phone = self.validate_phone(phone_num)

    def get_phone(self):
        return self.__phone

    def set_address(self, address):
        self.__address = self.validate_address(address)

    def get_address(self):
        return self.__address
