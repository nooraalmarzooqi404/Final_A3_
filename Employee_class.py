from Person_class import Person, PersonType, Gender
from enum import Enum
import re

# Enum options for Employee class
class JobTitle(Enum):
    Sales_Manager = "Sales Manager"
    Salesperson = "Salesperson"
    Marketing_Manager = "Marketing Manager"
    Marketer = "Marketer"
    Accountant = "Accountant"
    Designer = "Designer"
    Handyman = "Handyman"


class Department(Enum):
    Sales = "Sales"
    Marketing = "Marketing"
    Accounting = "Accounting"
    Design = "Design"
    Maintenance = "Maintenance"

class Employee(Person):
    """A child class of the Person class to represent an employee"""
    # Constructor (The attributes are private)
    def __init__(self, name, person_id, age, gender: Gender, date_of_birth, phone, email, address, job_title: JobTitle, department: Department, basic_salary, passport_details, manager_id=None):
        super().__init__(name, PersonType.Employee, person_id, age, gender, date_of_birth, phone, email, address)
        self.__job_title = self.validate_job_title(job_title)
        self.__department = self.validate_department(department)
        self.__basic_salary = self.validate_basic_salary(basic_salary)
        self.__passport = self.validate_passport_details(passport_details)
        self.__manager_id = self.validate_manager_id(manager_id)     # If an employee has a manager

    # Exception Handling
    def validate_job_title(self, job_title):
        """Validate the job title to ensure it is an enum option defined above"""
        if not isinstance(job_title, JobTitle):
            raise ValueError("Invalid job title specified")
        return job_title

    def validate_department(self, department):
        """Validate the department to ensure it is an enum option defined above"""
        if not isinstance(department, Department):   # if it is not one of the enum options, raise an error
            raise ValueError("Invalid department specified")
        return department

    def validate_basic_salary(self, basic_salary):
        """Validate basic salary to ensure it is a positive integer or float"""
        if not isinstance(basic_salary, (int, float)) or basic_salary <= 0:
            raise ValueError("Basic salary must be a positive number")
        return basic_salary

    def validate_passport_details(self, passport_details):
        """Validate passport details such that it is not an empty string"""
        if not isinstance(passport_details, str) or not passport_details.strip():
            raise ValueError("Invalid passport details")
        return passport_details.strip()

    def validate_manager_id(self, manager_id):
        """Validate manager ID by confirming it either follows the 'Pxxx' format or is None if no manager is assigned"""
        if manager_id is not None and not re.match(r'P\d{3}', manager_id):
            raise ValueError("Manager ID must be in the format 'Pxxx', where 'xxx' are digits")
        return manager_id


    def print_details(self):
        """Calling the parent's class method and printing employee-specific details"""
        general_details = super().print_details()
        specific_details = (f"Job Title: {self.__job_title.value}, Department: {self.__department.value}, "
                                f"Basic Salary: {self.__basic_salary}, Passport Details: {self.__passport}, "
                                f"Manager ID: {self.__manager_id if self.__manager_id else 'N/A'}")
        return f"{general_details}, {specific_details}"

    # Setter and getter

    def set_job_title(self, job_title):
        self.__job_title = self.validate_job_title(job_title)

    def get_job_title(self):
        return self.__job_title

    def set_department(self, department):
        self.__department = self.validate_department(department)

    def get_department(self):
        return self.__department

    def set_salary(self, basic_salary):
        self.__basic_salary = self.validate_basic_salary(basic_salary)

    def get_salary(self):
        return self.__basic_salary

    def set_passport_details(self, passport_details):
        self.__passport = self.validate_passport_details(passport_details)

    def get_passport_details(self):
        return self.__passport

    def set_manager_id(self, manager_id):
        self.__manager_id = self.validate_manager_id(manager_id)

    def get_manager_id(self):
        return self.__manager_id