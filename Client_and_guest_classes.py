from Person_class import Person, Gender, PersonType

class Client(Person):
    """A child class derived from the Person class to represent a client"""
    # Constructor
    def __init__(self,name, person_type: PersonType, person_id, age, gender: Gender, date_of_birth, phone, email, address, budget):
        super().__init__(name, PersonType.Client, person_id, age, gender, date_of_birth, phone, email, address) # Inheritance
        self.__budget = self.validate_budget(budget)

    # Exception Handling
    def validate_budget(self, budget):
        """Validate the budget to ensure it is a positive integer or float"""
        if not isinstance(budget, (int, float)) or budget < 0:
            raise ValueError("Budget must be a positive number")
        return budget

    def print_details(self):
        """Printing all details"""
        general_details = super().print_details()
        specific_details = f"Budget: {self.__budget}"
        return f"{general_details}, {specific_details}"

    # Setter and getter

    def set_budget(self, budget):
        self.__budget = self.validate_budget(budget)

    def get_budget(self):
        return self.__budget



class Guest(Person):
    """A child class of person to represent a guest"""
    # Constructor
    def __init__(self,name, person_type: PersonType, person_id, age, gender: Gender, date_of_birth, phone, email, address, guest_requests):
        super().__init__(name, PersonType.Guest, person_id, age, gender, date_of_birth, phone, email, address) # Inheritance
        self.__requests = self.validate_guest_requests(guest_requests)       # Any special request by the guest

    # Exception Handling
    def validate_guest_requests(self, requests):
        """Validate guest requests to confirm it is a string"""
        if not isinstance(requests, str) or not requests.strip():
            raise ValueError("Guest requests must be a non-empty string")
        return requests.strip()


    def print_details(self):
        """Prints all details of a guest"""
        details = super().print_details()
        details = details.replace(f"Gender: {self._gender.name}", f"Gender: {self._gender.value}")
        return f"{details}, Guest Special Requests: {self.__requests}"

    # Setter and getter

    def set_guest_requests(self, guest_requests):
        self.__requests = self.validate_guest_requests(guest_requests)
    def get_guest_requests(self):
        return self.__requests