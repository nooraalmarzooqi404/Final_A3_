from enum import Enum
import re
# Enum class for an attribute in the Supplier class
class Service(Enum):
    catering = "Catering"
    cleaning = "Cleaning"
    supplying_furniture = "Supplying Furniture"
    decoration = "Decoration"

class Supplier:
    """A class to represent a supplier"""
    suppliers = {}            # A dictionary to store suppliers. The key is the supplier ID

    # Constructor
    def __init__(self, supplier_id, company_name, service: Service, phone_num, address):
        self._supplier_id = self.validate_supplier_id(supplier_id)
        self._company_name = self.validate_company_name(company_name)
        self._service = self.validate_service(service)
        self._phone = self.validate_phone(phone_num)
        self._address = self.validate_address(address)

    # Exception Handling
    def validate_supplier_id(self, supplier_id):
        """Validate the supplier ID to ensure it is in the format 'Sxxx', where 'xxx' are digits"""
        if not re.match(r'S\d{3}', supplier_id):
            raise ValueError("Supplier ID must be in the format 'Sxxx', where 'xxx' are digits")
        return supplier_id

    def validate_company_name(self, company_name):
        """Validate the company name to ensure it is non-empty"""
        if not company_name:
            raise ValueError("Company name must be non-empty")
        return company_name

    def validate_service(self, service):
        """Validate the service to ensure it is a valid Service enum member"""
        if not isinstance(service, Service):
            raise ValueError("Invalid service specified")
        return service

    def validate_phone(self, phone):
        """Validate the phone number to ensure it is an integer of 10 digits"""
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone number must be a 10-digit number")
        return phone

    def validate_address(self, address):
        """Validate the address to ensure it is non-empty"""
        if not address:
            raise ValueError("Address must be non-empty")
        return address


    def add_supplier(self):
        """"A method to add a supplier to the dictionary"""
        Supplier.suppliers[self._supplier_id] = self

    def delete_supplier(self, supplier_id):
        """A method to delete a supplier"""
        if supplier_id in Supplier.suppliers:          # If supplier exits, delete it. Else, show this message
            del Supplier.suppliers[supplier_id]
            print("Supplier deleted successfully")
        else:
            print("Supplier not found")

    def print_details(self):
        """Returns the details of a supplier"""
        details = (f"Supplier ID: {self._supplier_id}, "
                   f"Company Name: {self._company_name}, "
                   f"Service: {self._service.value}, "
                   f"Phone Number: {self._phone}, "
                   f"Address: {self._address}")
        return details
    # Setter and getter
    def set_supplier_id(self, supplier_id):
        self._supplier_id = self.validate_supplier_id(supplier_id)

    def get_supplier_id(self):
        return self._supplier_id

    def set_company_name(self, company_name):
        self._company_name = self.validate_company_name(company_name)

    def get_company_name(self):
        return self._company_name

    def set_service(self, service):
        self._service = self.validate_service(service)

    def get_service(self):
        return self._service

    def set_phone(self, phone_num):
        self._phone = self.validate_phone(phone_num)

    def get_phone(self):
        return self._phone

    def set_address(self, address):
        self._address = self.validate_address(address)

    def get_address(self):
        return self._address


class Caterer(Supplier):
    """A child class of Supplier to represent a catering company"""

    # Constructor
    def __init__(self, supplier_id, company_name, service=Service.catering, phone_num = 0, address = "", min_num_guests=0, max_num_guests=0, menu=[]):
        super().__init__(supplier_id, company_name, Service.catering, phone_num, address) # Inheritance
        self.__min_num_guests = self.validate_guest_count(min_num_guests)
        self.__max_num_guests = self.validate_guest_count(max_num_guests)
        self.__menu = menu

    def validate_guest_count(self, num):
        """Validates the number of guests to ensure they are positive integers"""
        if not isinstance(num, int) or num < 0:
            raise ValueError("Number of guests must be a positive integer")
        return num

    def print_details(self):
        """Overriding the print details method to include caterer specific details"""
        basic_details = super().print_details() # Inheritance
        caterer_details = (f"Minimum Number of Guests: {self.__min_num_guests}, "
                           f"Maximum Number of Guests: {self.__max_num_guests}, "
                           f"Menu: {', '.join(self.__menu)}")
        return f"{basic_details}, {caterer_details}"

    # Setter and getter
    def set_min_num_guests(self, min_num_guests):
        self._min_num_guests = self.validate_guest_count(min_num_guests)

    def get_min_guests(self):
        return self._min_num_guests

    def set_max_num_guests(self, max_num_guests):
        self._max_num_guests = self.validate_guest_count(max_num_guests)

    def get_max_guests(self):
        return self._max_num_guests

    def set_menu(self, menu):
        self._menu = menu

    def get_menu(self):
        return self._menu


