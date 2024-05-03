from enum import Enum
import re
from datetime import datetime
# Enum classes for Person attributes
class PersonType(Enum):
    Employee = "Employee"
    Client = "Client"
    Guest = "Guest"

class Gender(Enum):
    Male = "Male"
    Female = "Female"

class Person:
    """A class to represent a person. It is a parent class to Employee, Client and Guest classes"""
    people_dictionary = {}          # A dictionary to store people. The key is the ID
    # Constructor (The attributes are protected to allow inheritance)
    def __init__(self, name, person_type: PersonType, person_id, age, gender: Gender, date_of_birth, phone, email, address):
        # Initialize the person attributes in which we validate each input
        self._name = self.validate_name(name)
        self._type = self.validate_person_type(person_type)
        self._id = self.validate_person_id(person_id)
        self._age = self.validate_age(age)
        self._gender = self.validate_gender(gender)
        self._dob = self.validate_dob(date_of_birth)
        self._phone = phone
        self._email = self.validate_email(email)
        self._address = self.validate_address(address)

    def validate_name(self, name):
        """Validate the name ensuring it is a not an empty string"""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        return name.strip()

    def validate_person_type(self, person_type):
        """Validate the person_type ensuring it is one of the enum options defined above"""
        if not isinstance(person_type, PersonType):
            raise ValueError("Invalid person type")
        return person_type

    def validate_person_id(self, person_id):
        """Validate the person ID ensuring it matches the appropriate format based on the person type"""
        # Employee ID must have a different format than client's and guest's to distinguish between them
        if self._type == PersonType.Employee:
            if not re.match(r'E\d{3}', person_id):
                raise ValueError("Employee ID must be in the format 'Exxx', where 'xxx' are digits")
        elif self._type == PersonType.Client:
            if not re.match(r'CL\d{3}', person_id):
                raise ValueError("Client ID must be in the format 'CLxxx', where 'xxx' are digits")
        elif self._type == PersonType.Guest:
            if not re.match(r'G\d{3}', person_id):
                raise ValueError("Guest ID must be in the format 'Gxxx', where 'xxx' are digits")
        else:
            raise ValueError("Invalid person type")
        return person_id

    def validate_age(self, age):
        """Validating age which should be an integer within the range 1 to 150"""
        if not isinstance(age, int) or not (1 < age < 150):
            raise ValueError("Age must be an integer greater than 1 and less than 150") # if it is not within the range, raise a valuerror
        return age

    def validate_gender(self, gender):
        """Validate gender ensuring it is one of the enum options defined above"""
        if not isinstance(gender, Gender):
            raise ValueError("Invalid gender specified")
        return gender

    def validate_dob(self, dob):
        """Validate the date of birth ensuring it is in 'YYYY-MM-DD' format"""
        try:
            datetime.strptime(dob, '%Y-%m-%d')
            return dob
        except ValueError:
            raise ValueError("Date of birth must be in the format 'YYYY-MM-DD'")



    def validate_email(self, email):
        """Validate the email so that it follows the traditional format"""
        if "@" not in email or "." not in email.split('@')[-1]:
            raise ValueError("Invalid email format")
        return email.lower()

    def validate_address(self, address):
        """Validate the address ensuring it is not an empty string"""
        if not isinstance(address, str) or not address.strip():
            raise ValueError("Address must be a non-empty string")
        return address

    def add_person(self):
        """A method to add a person to the dictionary by their ID"""
        Person.people_dictionary[self._id] = self          # Adding the person to the dictionary by his ID


    def delete_person(self):
        """Instance method to delete this person based on his ID"""
        if self._id in Person.people_dictionary:
            del Person.people_dictionary[self._id]
            return True
        else:
            return False

    def print_details(self):
        """Prints all details of the person"""
        return (f"Name: {self._name}, Type: {self._type.value}, ID: {self._id}, Age: {self._age}, "
                f"Gender: {self._gender.value}, Date of Birth: {self._dob}, Phone Number: {self._phone}, "
                f"Email: {self._email}, Address: {self._address}")

    # Setter and Getter methods will be used for modifications
    def set_name(self, name):
        self._name = self.validate_name(name)

    def get_name(self):
        return self._name

    def set_person_type(self, person_type):
        self._type = self.validate_person_type(person_type)

    def get_person_type(self):
        return self._type

    def set_id(self, person_id):
        self._id = self.validate_person_id(person_id)

    def get_id(self):
        return self._id

    def set_age(self, age):
        self._age = self.validate_age(age)

    def get_age(self):
        return self._age

    def set_gender(self, gender):
        self._gender = self.validate_gender(gender)

    def get_gender(self):
        return self._gender

    def set_dob(self, date_of_birth):
        self._dob = self.validate_dob(date_of_birth)

    def get_dob(self):
        return self._dob

    def set_phone(self, phone):
        self._phone = phone

    def get_phone(self):
        return self._phone

    def set_email(self, email):
        self._email = self.validate_email(email)

    def get_email(self):
        return self._email

    def set_address(self, address):
        self._address = self.validate_address(address)

    def get_address(self):
        return self._address

