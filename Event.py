from enum import Enum
import datetime
import re

class EventType(Enum):
    Birthday = "Birthdays"
    Wedding = "Wedding"
    Themed_party = "Themed Party"
    Graduation = "Graduation"

class Event:
    """A class to represent an event"""
    events = {}     # To store events. The key is the event ID

    # Constructor
    def __init__(self, event_id , event_type: EventType, event_theme, date_time, duration, venue_address, client_id, guest_list, catering_company, cleaning_company, decoration_company, entertainment_company, furniture_company, invoice):
        self.__event_id = self.validate_event_id(event_id)
        self.__event_type = self.validate_event_type(event_type)
        self.__event_theme = event_theme
        self.__datetime = self.validate_datetime(date_time)
        self.__duration = duration
        self.__venue_address = venue_address
        self.__client_id = self.validate_client_id(client_id)
        self.__guest_list = guest_list
        self.__catering_company = catering_company
        self.__cleaning_company = cleaning_company
        self.__decoration_company = decoration_company
        self.__entertainment_company = entertainment_company
        self.__furniture_company = furniture_company
        self.__invoice = invoice

    # Exception Handling
    def validate_event_id(self, event_id):
        """Validate the event ID to ensure it follows the 'EVxxx' format"""
        if not re.match(r'EV\d{3}', event_id):       # This format should be followed, else raise error
            raise ValueError("Event ID must be in the format 'EVxxx', where 'xxx' are digits")
        return event_id

    def validate_event_type(self, event_type):
        """Validate the event type to ensure it is an instance of the EventType enum."""
        if not isinstance(event_type, EventType):      # Ensure it is one of the enum values
            raise ValueError("Invalid event type specified")
        return event_type

    def validate_datetime(self, datetime_input):
        """Validate the date and time to ensure it is in the correct datetime format."""
        if isinstance(datetime_input, datetime.datetime):
            datetime_str = datetime_input.strftime('%Y-%m-%d %H:%M')  # Should follow this format
        else:
            datetime_str = datetime_input

        try:
            return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ValueError("Datetime must be in the format 'YYYY-MM-DD HH:MM'")

    def validate_client_id(self, client_id):
        """Validate the client ID to ensure it follows the 'CLxxx' format"""
        if not re.match(r'CL\d{3}', client_id):
            raise ValueError("Client ID must be in the format 'CLxxx', where 'xxx' are digits")
        return client_id

    def add_event(self):
        """A method to add an event to the event dictionary"""
        Event.events[self.__event_id] = self         # Add event to the event dictionary using its ID

    def delete_event(self, event_id):
        """A method to delete an event by its ID"""
        if event_id in Event.events:    # If event is in the dict, delete it. Else, print event not found
            del Event.events[event_id]
            print("Event deleted successfully")
        else:
            print("Event not found")

    def print_event_details(self):
        """This method prints the details of an event"""
        return (f"Event ID: {self.__event_id}, Event Type: {self.__event_type.value}, "
                f"Event Theme: {self.__event_theme}, Date and Time: {self.__datetime}, "
                f"Event Duration: {self.__duration}, Venue Address: {self.__venue_address}, "
                f"Client ID: {self.__client_id}, Guest List: {', '.join(self.__guest_list)}, "
                f"Catering Company: {self.__catering_company}, Cleaning Company: {self.__cleaning_company}, "
                f"Decoration Company: {self.__decoration_company}, Entertainment Company: {self.__entertainment_company}, "
                f"Furniture Company: {self.__furniture_company}, Invoice: {self.__invoice}")

    # Setter and getter
    def set_event_id(self, event_id):
        self.__event_id = self.validate_event_id(event_id)

    def get_event_id(self):
        return self.__event_id

    def set_event_type(self, event_type):
        self.__event_type = self.validate_event_type(event_type)

    def get_event_type(self):
        return self.__event_type

    def set_event_theme(self, theme):
        self.__event_theme = theme

    def get_event_theme(self):
        return self.__event_theme

    def set_datetime(self, date_time):
        self.__datetime = self.validate_datetime(date_time)

    def get_datetime(self):
        return self.__datetime

    def set_duration(self, duration):
        self.__duration = duration

    def get_duration(self):
        return self.__duration

    def set_venue_address(self, address):
        self.__venue_address = address

    def get_venue_address(self):
        return self.__venue_address

    def set_client_id(self, id):
        self.__client_id = id

    def get_client_id(self):
        return self.__client_id

    def set_guest_list(self, list):
        self.__guest_list = list

    def get_guest_list(self):
        return self.__guest_list

    def set_catering(self, company):
        self.__catering_company = company

    def get_catering(self):
        return self.__catering_company

    def set_cleaning(self, company):
        self.__cleaning_company = company

    def get_cleaning(self):
        return self.__cleaning_company

    def set_decoration(self, company):
        self.__decoration_company = company

    def get_decoration(self):
        return self.__decoration_company

    def set_entertainment(self, company):
        self.__entertainment_company = company

    def get_entertainment(self):
        return self.__entertainment_company

    def set_furniture(self, company):
        self.__furniture_company = company

    def get_furniture(self):
        return self.__furniture_company

    def set_invoice(self, invoice):
        self.__invoice = invoice

    def get_invoice(self):
        return self.__invoice

