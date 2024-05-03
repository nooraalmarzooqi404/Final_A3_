from Person_class import Person
from Employee_class import Employee, JobTitle, Department
from Client_and_guest_classes import Client, Gender, PersonType, Guest
from Event import Event, EventType
from Supplier_and_caterer_classes import Service, Supplier, Caterer
from Venue_class import Venue
from data_loader import load_data, save_data
from datetime import datetime
import tkinter as tk
from tkinter import Label, Entry, Button, Toplevel, StringVar, messagebox, OptionMenu, Menu

def load_all_person_data():
    """Loading data when starting the program"""
    Person.people_dictionary = load_data('people.pkl') or {}
    Supplier.suppliers = load_data('suppliers.pkl') or {}
    Event.events = load_data('events.pkl') or {}
    Venue.venues = load_data('venues.pkl') or {}

load_all_person_data()         # Calling the function

def add_employee():
    """A function to add an employee and save his details"""
    def save_employee():
        """A function to collect user input and use the backend function 'add_employee'"""
        try:
            # Ensuring enum values are collected correctly to avoid errors
            selected_gender = Gender[gender_var.get()]
            selected_job_title = JobTitle[job_title_var.get()]
            selected_department = Department[department_var.get()]
            # Ensuring manager ID can be None or the value the user enters
            manager_id = manager_id_var.get()
            manager_id = None if not manager_id.strip() else manager_id

            new_employee = Employee(
                name_var.get(),
                id_var.get(),
                int(age_var.get()),    # Convert phone number to integer
                selected_gender,
                dob_var.get(),
                int(phone_var.get()),  # Convert phone number to integer
                email_var.get(),
                address_var.get(),
                selected_job_title,
                selected_department,
                float(salary_var.get()),   # Convert salary to a float
                passport_var.get(),
                manager_id
            )
            # Using the back-end function 'add_employee'
            Employee.add_person(new_employee)
            # Save data after adding the employee
            save_data(Person.people_dictionary, 'people.pkl')

            messagebox.showinfo("Success", "Employee added successfully!")
            add_window.destroy()
        except ValueError as e:
            # Show error messages and allow user to continue editing
            messagebox.showerror("Error", str(e))
        except KeyError as e:
            messagebox.showerror("Error", f"Invalid enum selection: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            add_window.lift()

    add_window = Toplevel()
    add_window.title("Add Employee")

    # Set up variables for GUI elements
    name_var, id_var, age_var, dob_var, phone_var, email_var, address_var, salary_var, passport_var, manager_id_var = [StringVar() for i in range(10)]
    # Ensuring a right set up for the enum values as well
    gender_var = StringVar(add_window, Gender.Male.name)
    job_title_var = StringVar(add_window, JobTitle.Sales_Manager.name)
    department_var = StringVar(add_window, Department.Sales.name)

    # The form fields
    fields = [("Name", name_var),
        ("Gender", gender_var),
        ("Job Title", job_title_var),
        ("Department", department_var),
        ("ID", id_var),
        ("Age", age_var),
        ("Date of Birth", dob_var),
        ("Phone", phone_var),
        ("Email", email_var),
        ("Address", address_var),
        ("Basic Salary", salary_var),
        ("Passport Details", passport_var),
        ("Manager ID (Optional)", manager_id_var)]

    # Creating option menue for all enum variables
    for i, (label, var) in enumerate(fields):
        Label(add_window, text=label).grid(row=i, column=0)
        if label in ["Gender", "Job Title", "Department"]:
            OptionMenu(add_window, var, *[e.name for e in eval(label.replace(" ", ""))]).grid(row=i, column=1)
        else:
            Entry(add_window, textvariable=var).grid(row=i, column=1)

    Button(add_window, text="Save", command=save_employee).grid(row=len(fields), column=1)   # Adding the save button

def modify_employee():
    """A function to allow the user to modify a registered employee. It asks for the employee ID and allows
     fetching their details and finally the user can edit any of the attributes"""
    def fetch_details():
        """A function to fetch pre-defined employee details"""
        # Checking if the employee exits, if not show this message
        employee = Employee.people_dictionary.get(id_var.get())
        if not employee:
            messagebox.showerror("Error", "Employee not found.")
            return

        # Filling the form fields with the pre-define details
        name_var.set(employee.get_name())
        gender_var.set(employee.get_gender().name)
        job_title_var.set(employee.get_job_title().name)
        department_var.set(employee.get_department().name)
        age_var.set(str(employee.get_age()))
        dob_var.set(employee.get_dob())
        phone_var.set(str(employee.get_phone()))
        email_var.set(employee.get_email())
        address_var.set(employee.get_address())
        salary_var.set(str(employee.get_salary()))
        passport_var.set(employee.get_passport_details())
        manager_id_var.set(employee.get_manager_id() if employee.get_manager_id() else "")

    def update_employee():
        """This function allows the user to update the details after it is being fetched"""
        # Checking if the employee exits
        try:
            employee = Employee.people_dictionary.get(id_var.get())
            if not employee:
                raise Exception("Employee not found.")

            # Update only the modified details
            employee.set_name(name_var.get())
            employee.set_gender(Gender[gender_var.get()])
            employee.set_job_title(JobTitle[job_title_var.get()])
            employee.set_department(Department[department_var.get()])
            employee.set_age(int(age_var.get()))
            employee.set_dob(dob_var.get())
            employee.set_phone(phone_var.get())  # phone_var holds the phone number as a string
            employee.set_email(email_var.get())
            employee.set_address(address_var.get())
            employee.set_salary(float(salary_var.get()))
            employee.set_passport_details(passport_var.get())
            manager_id = manager_id_var.get()
            employee.set_manager_id(manager_id if manager_id.strip() else None)

            messagebox.showinfo("Success", "Employee details updated successfully!")   # Show this message after updating the employee
            save_data(Person.people_dictionary, 'people.pkl')
            modify_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            modify_window.lift()

    modify_window = Toplevel()
    modify_window.title("Modify Employee")

    # Variables for the form
    name_var, id_var, age_var, dob_var, phone_var, email_var, address_var, salary_var, passport_var, manager_id_var = [StringVar() for i in range(10)]
    gender_var = StringVar(modify_window)
    job_title_var = StringVar(modify_window)
    department_var = StringVar(modify_window)

    # Form fields
    fields = [("Employee ID (to modify)", id_var),
        ("Name", name_var),
        ("Gender", gender_var),
        ("Job Title", job_title_var),
        ("Department", department_var),
        ("Age", age_var),
        ("Date of Birth", dob_var),
        ("Phone", phone_var),
        ("Email", email_var),
        ("Address", address_var),
        ("Basic Salary", salary_var),
        ("Passport Details", passport_var),
        ("Manager ID (Optional)", manager_id_var)]

    # Creating option menu for enum variables
    for i, (label, var) in enumerate(fields):
        Label(modify_window, text=label).grid(row=i, column=0)
        if label in ["Gender", "Job Title", "Department"]:
            OptionMenu(modify_window, var, *[e.name for e in eval(label.replace(" ", ""))]).grid(row=i, column=1)
        else:
            Entry(modify_window, textvariable=var).grid(row=i, column=1)

    Button(modify_window, text="Fetch Details", command=fetch_details).grid(row=0, column=2)  # Button to fetch details
    Button(modify_window, text="Update", command=update_employee).grid(row=len(fields), column=1) # Button to update details

def delete_employee():
    """A function to delete employees"""
    def fetch_employee_details():
        """Allowing to fetch the ID, name and email of the employee to confirm their identity before deletion"""
        employee_id = id_var.get().strip()
        employee = Person.people_dictionary.get(employee_id)
        if employee:
            details.set(f"ID: {employee.get_id()}, Name: {employee.get_name()}, Email: {employee.get_email()}")
        else:
            messagebox.showerror("Error", "Employee not found.")

    def perform_deletion():
        """Using the backend function 'delete_person' to delete an employee"""
        employee_id = id_var.get().strip()
        employee = Person.people_dictionary.get(employee_id)
        if employee and employee.delete_person():
            messagebox.showinfo("Success", "Employee deleted successfully!")
            save_data(Person.people_dictionary, 'people.pkl')
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to delete employee or employee not found.")

    delete_window = Toplevel()
    delete_window.title("Delete Employee")
    id_var = StringVar()
    details = StringVar()

    # Creating labels, buttons and entries for the delete employee window
    Label(delete_window, text="Employee ID (to delete):").grid(row=0, column=0)
    Entry(delete_window, textvariable=id_var).grid(row=0, column=1)
    Button(delete_window, text="Fetch Details", command=fetch_employee_details).grid(row=0, column=2)

    Label(delete_window, text="Details:").grid(row=1, column=0)
    Label(delete_window, textvariable=details).grid(row=1, column=1, columnspan=2)

    Button(delete_window, text="Delete", command=perform_deletion).grid(row=2, column=1)

def display_employee_details():
    """Using the backend function print_details in the employee class"""
    def fetch_employee_details():
        employee_id = id_var.get().strip()
        employee = Person.people_dictionary.get(employee_id)
        if employee:
            details.set(employee.print_details())  # Use the instance's own method
        else:
            messagebox.showerror("Error", "Employee not found.")

    # Setting up the window
    display_window = Toplevel()
    display_window.title("Display Employee Details")
    id_var = StringVar()
    details = StringVar()

    Label(display_window, text="Employee ID (to display):").grid(row=0, column=0)
    Entry(display_window, textvariable=id_var).grid(row=0, column=1)
    Button(display_window, text="Fetch Details", command=fetch_employee_details).grid(row=0, column=2)

    Label(display_window, text="Details:").grid(row=1, column=0)
    Label(display_window, textvariable=details, wraplength=500).grid(row=1, column=1, columnspan=2, sticky="w")


def add_client():
    """A function to add a client"""
    def save_client():
        """A function to save a client"""
        try:
            # Creating an instance
            selected_gender = Gender[gender_var.get()]
            new_client = Client(
                name=name_var.get(),
                person_type=PersonType.Client,
                person_id=id_var.get(),
                age=int(age_var.get()),
                gender=selected_gender,
                date_of_birth=dob_var.get(),
                phone=phone_var.get(),
                email=email_var.get(),
                address=address_var.get(),
                budget=float(budget_var.get()))

            # Using the back-end function 'add_person' to add a client and adding the window
            Client.add_person(new_client)
            messagebox.showinfo("Success", "Client added successfully!")
            save_data(Person.people_dictionary, 'people.pkl')
            add_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            add_window.lift()

    add_window = Toplevel()
    add_window.title("Add Client")

    # Create StringVars
    name_var, id_var, age_var, dob_var, phone_var, email_var, address_var, budget_var = [StringVar() for i in range(8)]
    gender_var = StringVar(add_window)
    gender_var.set("Male")  # Default value

    fields = [("Name", name_var),
        ("ID", id_var),
        ("Age", age_var),
        ("Gender", gender_var),
        ("Date of Birth", dob_var),
        ("Phone", phone_var),
        ("Email", email_var),
        ("Address", address_var),
        ("Budget", budget_var)]

    # Creating option menu for the enum variable gender
    for i, (label, var) in enumerate(fields):
        Label(add_window, text=label).grid(row=i, column=0)
        if label == "Gender":
            OptionMenu(add_window, var, *[g.name for g in Gender]).grid(row=i, column=1)
        else:
            Entry(add_window, textvariable=var).grid(row=i, column=1)

    Button(add_window, text="Save", command=save_client).grid(row=len(fields), column=1)


def modify_client():
    def fetch_details():
        # Fetch the client details based on ID and populate the form
        client = Client.people_dictionary.get(id_var.get())
        if not client:
            messagebox.showerror("Error", "Client not found.")
            return

        # Populate the form with existing client details
        name_var.set(client.get_name())
        gender_var.set(client.get_gender().name)
        age_var.set(str(client.get_age()))
        dob_var.set(client.get_dob())
        phone_var.set(client.get_phone())
        email_var.set(client.get_email())
        address_var.set(client.get_address())
        budget_var.set(str(client.get_budget()))

    def update_client():
        try:
            client = Client.people_dictionary.get(id_var.get())
            if not client:
                raise Exception("Client not found.")

            # Update client details from the form
            client.set_name(name_var.get())
            client.set_gender(Gender[gender_var.get()])
            client.set_age(int(age_var.get()))
            client.set_dob(dob_var.get())
            client.set_phone(phone_var.get())
            client.set_email(email_var.get())
            client.set_address(address_var.get())
            client.set_budget(float(budget_var.get()))

            messagebox.showinfo("Success", "Client details updated successfully!")
            save_data(Person.people_dictionary, 'people.pkl')
            modify_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            modify_window.lift()

    modify_window = Toplevel()
    modify_window.title("Modify Client")

    # Setup variables for form fields
    name_var, id_var, age_var, dob_var, phone_var, email_var, address_var, budget_var = [StringVar() for _ in range(8)]
    gender_var = StringVar(modify_window)
    gender_var.set("Male")  # Default value

    # Create form fields
    fields = [
        ("Client ID (to modify)", id_var),
        ("Name", name_var),
        ("Gender", gender_var),
        ("Age", age_var),
        ("Date of Birth", dob_var),
        ("Phone", phone_var),
        ("Email", email_var),
        ("Address", address_var),
        ("Budget", budget_var)
    ]
    # Creating option menu and adding labels and buttons
    for i, (label, var) in enumerate(fields):
        Label(modify_window, text=label).grid(row=i, column=0)
        if label == "Gender":
            OptionMenu(modify_window, var, *[g.name for g in Gender]).grid(row=i, column=1)
        else:
            Entry(modify_window, textvariable=var).grid(row=i, column=1)

    Button(modify_window, text="Fetch Details", command=fetch_details).grid(row=0, column=2)
    Button(modify_window, text="Update", command=update_client).grid(row=len(fields), column=1)

def delete_client():
    """A function to delete a client"""
    def fetch_client_details():
        """Fetching pre-defined details"""
        client_id = id_var.get().strip()
        client = Person.people_dictionary.get(client_id)
        if client and isinstance(client, Client):
            details.set(f"ID: {client.get_id()}, Name: {client.get_name()}, Email: {client.get_email()}")
        else:
            messagebox.showerror("Error", "Client not found.")

    def perform_deletion():

        # Deleting clients given their ID
        client_id = id_var.get().strip()
        client = Person.people_dictionary.get(client_id)
        if client and isinstance(client, Client) and client.delete_person():
            messagebox.showinfo("Success", "Client deleted successfully!")
            save_data(Person.people_dictionary, 'people.pkl')
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to delete client or client not found.")

    delete_window = Toplevel()
    delete_window.title("Delete Client")
    id_var = StringVar()
    details = StringVar()

    Label(delete_window, text="Client ID (to delete):").grid(row=0, column=0)
    Entry(delete_window, textvariable=id_var).grid(row=0, column=1)
    Button(delete_window, text="Fetch Details", command=fetch_client_details).grid(row=0, column=2)

    Label(delete_window, text="Details:").grid(row=1, column=0)
    Label(delete_window, textvariable=details).grid(row=1, column=1, columnspan=2)

    Button(delete_window, text="Delete", command=perform_deletion).grid(row=2, column=1)

def display_client_details():
    """A function to print the details of a client"""
    def fetch_client_details():

        # Fetching pre-defined details
        client_id = id_var.get().strip()
        client = Person.people_dictionary.get(client_id)
        if client and isinstance(client, Client):
            details.set(client.print_details())
        else:
            messagebox.showerror("Error", "Client not found.")

    display_window = Toplevel()
    display_window.title("Display Client Details")
    id_var = StringVar()
    details = StringVar()

    Label(display_window, text="Client ID (to display):").grid(row=0, column=0)
    Entry(display_window, textvariable=id_var).grid(row=0, column=1)
    Button(display_window, text="Fetch Details", command=fetch_client_details).grid(row=0, column=2)

    Label(display_window, text="Details:").grid(row=1, column=0)
    Label(display_window, textvariable=details).grid(row=1, column=1, columnspan=2, sticky="w")

def add_guest():
    """A function to add guests and save their info"""
    def save_guest():
        try:
            selected_gender = Gender[gender_var.get()]
            new_guest = Guest(
                name=name_var.get(),
                person_type=PersonType.Guest,
                person_id=id_var.get(),
                age=int(age_var.get()),
                gender=selected_gender,
                date_of_birth=dob_var.get(),
                phone=phone_var.get(),
                email=email_var.get(),
                address=address_var.get(),
                guest_requests=requests_var.get()
            )
            Person.people_dictionary[new_guest.get_id()] = new_guest
            messagebox.showinfo("Success", "Guest added successfully!")
            save_data(Person.people_dictionary, 'people.pkl')
            add_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            add_window.lift()

    add_window = Toplevel()
    add_window.title("Add Guest")

    # Variables for the form fields
    name_var = StringVar()
    id_var = StringVar()
    age_var = StringVar()
    dob_var = StringVar()
    phone_var = StringVar()
    email_var = StringVar()
    address_var = StringVar()
    requests_var = StringVar()  # For guest specific requests
    gender_var = StringVar(add_window)
    gender_var.set("Male")  # default value

    # Form fields
    fields = [("Name", name_var),
        ("ID", id_var),
        ("Age", age_var),
        ("Gender", gender_var),
        ("Date of Birth", dob_var),
        ("Phone", phone_var),
        ("Email", email_var),
        ("Address", address_var),
        ("Guest Requests", requests_var)]

    # Option menu creation
    for i, (label, var) in enumerate(fields):
        Label(add_window, text=label).grid(row=i, column=0)
        if label == "Gender":
            OptionMenu(add_window, gender_var, *Gender._member_names_).grid(row=i, column=1)
        else:
            Entry(add_window, textvariable=var).grid(row=i, column=1)

    Button(add_window, text="Save", command=save_guest).grid(row=len(fields), columnspan=2)


def modify_guest():
    """A function to modify pre-defined guest info"""
    def fetch_details():

        # Fetching details
        guest_id = id_var.get()
        guest = Person.people_dictionary.get(guest_id)
        if not guest:
            messagebox.showerror("Error", "Guest not found.")
            return

        name_var.set(guest.get_name())
        gender_var.set(guest.get_gender().name)
        dob_var.set(guest.get_dob())
        phone_var.set(str(guest.get_phone()))
        email_var.set(guest.get_email())
        address_var.set(guest.get_address())
        guest_requests_var.set(guest.get_guest_requests())

    def update_guest():
        """Updating guests info after fetching"""
        try:
            guest_id = id_var.get()
            guest = Person.people_dictionary.get(guest_id)
            if not guest:
                raise Exception("Guest not found.")

            # Update only the modified details
            guest.set_name(name_var.get())
            guest.set_gender(Gender[gender_var.get()])
            guest.set_dob(dob_var.get())
            guest.set_phone(phone_var.get())
            guest.set_email(email_var.get())
            guest.set_address(address_var.get())
            guest.set_guest_requests(guest_requests_var.get())

            messagebox.showinfo("Success", "Guest details updated successfully!")
            save_data(Person.people_dictionary, 'people.pkl')
            modify_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            modify_window.lift()

    modify_window = Toplevel()
    modify_window.title("Modify Guest")

    # Variables for the form
    name_var, id_var, dob_var, phone_var, email_var, address_var, guest_requests_var = [StringVar() for i in range(7)]
    gender_var = StringVar(modify_window)
    gender_var.set(Gender.Male.name)  # default value

    # Form fields
    fields = [("Guest ID (to modify)", id_var),
        ("Name", name_var),
        ("Gender", gender_var),
        ("Date of Birth", dob_var),
        ("Phone", phone_var),
        ("Email", email_var),
        ("Address", address_var),
        ("Guest Requests", guest_requests_var)]

    # Option menu creation
    for i, (label, var) in enumerate(fields):
        Label(modify_window, text=label).grid(row=i, column=0)
        if label == "Gender":
            OptionMenu(modify_window, var, *[e.name for e in Gender]).grid(row=i, column=1)
        else:
            Entry(modify_window, textvariable=var).grid(row=i, column=1)

    Button(modify_window, text="Fetch Details", command=fetch_details).grid(row=0, column=2)
    Button(modify_window, text="Update", command=update_guest).grid(row=len(fields), column=1)


def delete_guest():
    """A function to delete guest"""
    def fetch_guest_details():
        guest_id = id_var.get().strip()
        guest = Person.people_dictionary.get(guest_id)
        if guest and isinstance(guest, Guest):
            details.set(f"ID: {guest.get_id()}, Name: {guest.get_name()}, Email: {guest.get_email()}, Guest Requests: {guest.get_guest_requests()}")
        else:
            messagebox.showerror("Error", "Guest not found.")

    def perform_deletion():
        guest_id = id_var.get().strip()
        guest = Person.people_dictionary.get(guest_id)
        if guest and isinstance(guest, Guest) and guest.delete_person():
            messagebox.showinfo("Success", "Guest deleted successfully!")
            save_data(Person.people_dictionary, 'people.pkl')
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to delete guest or guest not found.")

    delete_window = Toplevel()
    delete_window.title("Delete Guest")
    id_var = StringVar()
    details = StringVar()

    Label(delete_window, text="Guest ID (to delete):").grid(row=0, column=0)
    Entry(delete_window, textvariable=id_var).grid(row=0, column=1)
    Button(delete_window, text="Fetch Details", command=fetch_guest_details).grid(row=0, column=2)

    Label(delete_window, text="Details:").grid(row=1, column=0)
    Label(delete_window, textvariable=details).grid(row=1, column=1, columnspan=2)

    Button(delete_window, text="Delete", command=perform_deletion).grid(row=2, column=1)

def display_guest_details():
    """A function to print the details of guests by their ID"""
    def fetch_guest_details():
        guest_id = id_var.get().strip()
        guest = Person.people_dictionary.get(guest_id)
        if guest and isinstance(guest, Guest):
            details.set(guest.print_details())  # Use the instance's own method to get details
        else:
            messagebox.showerror("Error", "Guest not found.")

    display_window = Toplevel()
    display_window.title("Display Guest Details")
    id_var = StringVar()
    details = StringVar()

    Label(display_window, text="Guest ID (to display):").grid(row=0, column=0)
    Entry(display_window, textvariable=id_var).grid(row=0, column=1)
    Button(display_window, text="Fetch Details", command=fetch_guest_details).grid(row=0, column=2)

    Label(display_window, text="Details:").grid(row=1, column=0)
    Label(display_window, textvariable=details).grid(row=1, column=1, columnspan=2, sticky="w")

    return display_window


def add_event():
    """A function to add an event"""
    def save_event():
        """A function that uses add_event function in the backend to save the event"""
        try:
            selected_event_type = EventType[event_type_var.get()]
            event_date_time = datetime.strptime(date_time_var.get(), '%Y-%m-%d %H:%M')

            new_event = Event(event_id=id_var.get(),    # Creating an instance
                event_type=selected_event_type,
                event_theme=theme_var.get(),
                date_time=event_date_time,
                duration=duration_var.get(),
                venue_address=venue_address_var.get(),
                client_id=client_id_var.get(),
                guest_list=guest_list_var.get().split(', '),  # Assuming guest list is input as comma-separated values
                catering_company=catering_var.get(),
                cleaning_company=cleaning_var.get(),
                decoration_company=decoration_var.get(),
                entertainment_company=entertainment_var.get(),
                furniture_company=furniture_var.get(),
                invoice=invoice_var.get())

            new_event.add_event()  # Using 'add_event' backend function
            messagebox.showinfo("Success", "Event added successfully!")
            save_data(Event.events, 'events.pkl')       # Saving changes
            add_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            add_window.lift()

    add_window = Toplevel()
    add_window.title("Add Event")

    # Variables for the form
    id_var = StringVar()
    event_type_var = StringVar()
    theme_var = StringVar()
    date_time_var = StringVar()
    duration_var = StringVar()
    venue_address_var = StringVar()
    client_id_var = StringVar()
    guest_list_var = StringVar()
    catering_var = StringVar()
    cleaning_var = StringVar()
    decoration_var = StringVar()
    entertainment_var = StringVar()
    furniture_var = StringVar()
    invoice_var = StringVar()
    event_type_var.set("Birthday")  # Default value

    fields = [
        ("Event ID", id_var),
        ("Event Type", event_type_var),
        ("Event Theme", theme_var),
        ("Date and Time (YYYY-MM-DD HH:MM)", date_time_var),
        ("Duration", duration_var),
        ("Venue Address", venue_address_var),
        ("Client ID", client_id_var),
        ("Guest List (comma separated)", guest_list_var),
        ("Catering Company", catering_var),
        ("Cleaning Company", cleaning_var),
        ("Decoration Company", decoration_var),
        ("Entertainment Company", entertainment_var),
        ("Furniture Company", furniture_var),
        ("Invoice", invoice_var) ]
    # Creating option menu for the enum variable event type
    for i, (label, var) in enumerate(fields):
        Label(add_window, text=label).grid(row=i, column=0)
        if label == "Event Type":
            OptionMenu(add_window, var, *[e.name for e in EventType]).grid(row=i, column=1)
        else:
            Entry(add_window, textvariable=var).grid(row=i, column=1)

    Button(add_window, text="Save", command=save_event).grid(row=len(fields), column=1)   # Adding a button to save


def modify_event():
    """A function to modify an event attributes"""
    def fetch_event_details():
        """Allows fetching pre-registered data"""
        event_id = id_var.get()
        event = Event.events.get(event_id)
        if not event:
            messagebox.showerror("Error", "Event not found.")
            return

        # Setting attributes
        event_type_var.set(event.get_event_type().name)
        event_theme_var.set(event.get_event_theme())
        datetime_var.set(event.get_datetime().strftime('%Y-%m-%d %H:%M'))
        duration_var.set(str(event.get_duration()))
        venue_address_var.set(event.get_venue_address())
        client_id_var.set(event.get_client_id())
        guest_list_var.set('; '.join(event.get_guest_list()))
        catering_var.set(event.get_catering())
        cleaning_var.set(event.get_cleaning())
        decoration_var.set(event.get_decoration())
        entertainment_var.set(event.get_entertainment())
        furniture_var.set(event.get_furniture())
        invoice_var.set(event.get_invoice())

    def update_event():
        """Updating event attributes"""
        try:
            event = Event.events.get(id_var.get())
            if not event:
                raise Exception("Event not found.")

            # Update event details from the form
            event.set_event_type(EventType[event_type_var.get()])
            event.set_event_theme(event_theme_var.get())
            event.set_datetime(datetime.strptime(datetime_var.get(), '%Y-%m-%d %H:%M'))
            event.set_duration(duration_var.get())  # Now accepts duration as a string
            event.set_venue_address(venue_address_var.get())
            event.set_client_id(client_id_var.get())
            event.set_guest_list(guest_list_var.get().split('; '))
            event.set_catering(catering_var.get())
            event.set_cleaning(cleaning_var.get())
            event.set_decoration(decoration_var.get())
            event.set_entertainment(entertainment_var.get())
            event.set_furniture(furniture_var.get())
            event.set_invoice(invoice_var.get())

            messagebox.showinfo("Success", "Event details updated successfully!")
            save_data(Event.events, 'events.pkl') # Save changes
            modify_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            modify_window.lift()

    modify_window = Toplevel()
    modify_window.title("Modify Event")

    # Create StringVars for form
    id_var = StringVar()
    event_type_var = StringVar(modify_window)
    event_theme_var = StringVar()
    datetime_var = StringVar()
    duration_var = StringVar()
    venue_address_var = StringVar()
    client_id_var = StringVar()
    guest_list_var = StringVar()
    catering_var = StringVar()
    cleaning_var = StringVar()
    decoration_var = StringVar()
    entertainment_var = StringVar()
    furniture_var = StringVar()
    invoice_var = StringVar()

    # Form fields
    fields = [
        ("Event ID (to modify)", id_var),
        ("Event Type", event_type_var),
        ("Event Theme", event_theme_var),
        ("Date and Time", datetime_var),
        ("Duration", duration_var),
        ("Venue Address", venue_address_var),
        ("Client ID", client_id_var),
        ("Guest List (separated by ';')", guest_list_var),
        ("Catering Company", catering_var),
        ("Cleaning Company", cleaning_var),
        ("Decoration Company", decoration_var),
        ("Entertainment Company", entertainment_var),
        ("Furniture Company", furniture_var),
        ("Invoice", invoice_var)]

    # Create form labels and entries and option menus
    for i, (label, var) in enumerate(fields):
        Label(modify_window, text=label).grid(row=i, column=0)
        if label == "Event Type":
            OptionMenu(modify_window, var, *[e.name for e in EventType]).grid(row=i, column=1)
        else:
            Entry(modify_window, textvariable=var).grid(row=i, column=1)

    Button(modify_window, text="Fetch Details", command=fetch_event_details).grid(row=0, column=2)
    Button(modify_window, text="Update", command=update_event).grid(row=len(fields), column=1)


def delete_event():
    """A function to delete an event"""
    def fetch_event_details():
        # Fetch the event details based on the ID and display them for confirmation
        event_id = id_var.get().strip()
        event = Event.events.get(event_id)
        if event:
            details.set(f"Event ID: {event.get_event_id()}, Type: {event.get_event_type().value}, Venue: {event.get_venue_address()}")
        else:
            messagebox.showerror("Error", "Event not found.")

    def perform_deletion():
        """Perform the deletion of the event"""

        event_id = id_var.get().strip()
        if event_id in Event.events:
            del Event.events[event_id]   # Delete event if the ID is found
            messagebox.showinfo("Success", "Event deleted successfully!")
            save_data(Event.events, 'events.pkl')
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Event not found.")

    delete_window = Toplevel()
    delete_window.title("Delete Event")
    id_var = StringVar()
    details = StringVar()

    # Creating labels and buttons
    Label(delete_window, text="Event ID (to delete):").grid(row=0, column=0)
    Entry(delete_window, textvariable=id_var).grid(row=0, column=1)
    Button(delete_window, text="Fetch Details", command=fetch_event_details).grid(row=0, column=2)

    Label(delete_window, text="Details:").grid(row=1, column=0)
    Label(delete_window, textvariable=details).grid(row=1, column=1, columnspan=2)

    Button(delete_window, text="Delete", command=perform_deletion).grid(row=2, column=1)

def display_event_details():
    """A function to return the details of an event based on its ID"""
    def fetch_event_details():
        """Fetching event pre-registered details"""
        event_id = id_var.get().strip()
        event = Event.events.get(event_id)
        if event:
            details.set(event.print_event_details())   # Using the backend function
        else:
            messagebox.showerror("Error", "Event not found.")

    display_window = Toplevel()
    display_window.title("Display Event Details")
    id_var = StringVar()
    details = StringVar()

    # Labels and buttons
    Label(display_window, text="Event ID (to display):").grid(row=0, column=0)
    Entry(display_window, textvariable=id_var).grid(row=0, column=1)
    Button(display_window, text="Fetch Details", command=fetch_event_details).grid(row=0, column=2)

    Label(display_window, text="Details:").grid(row=1, column=0)
    Label(display_window, textvariable=details, wraplength=500).grid(row=1, column=1, columnspan=2, sticky="w")

    return display_window

# Assuming the necessary classes and enums have already been imported and defined elsewhere in your project:

def add_supplier():
    """A fucntion to add a supplier"""
    def save_supplier():
        """A fucntion to save a supplier using a backend function 'add_supplier'"""
        try:
            selected_service = Service[service_var.get()]
            new_supplier = Supplier(    # Creating an instance
                supplier_id_var.get(),
                company_name_var.get(),
                selected_service,
                phone_var.get(),
                address_var.get() )

            if selected_service == Service.catering:
                """If the the selected service is catering, include its additional attributes as well"""
                new_caterer = Caterer(
                    supplier_id_var.get(),
                    company_name_var.get(),
                    selected_service,
                    phone_var.get(),
                    address_var.get(),
                    int(min_guests_var.get()),
                    int(max_guests_var.get()),
                    menu_var.get().split(';'))
                new_caterer.add_supplier()
            else:
                new_supplier.add_supplier()

            messagebox.showinfo("Success", "Supplier added successfully!")
            save_data(Supplier.suppliers, 'suppliers.pkl')
            add_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            add_window.lift()

    def update_fields(*args):
        """Updating the field when it is catering vs when its not"""
        if service_var.get() == "catering":
            min_guests_label.grid()
            min_guests_entry.grid()
            max_guests_label.grid()
            max_guests_entry.grid()
            menu_label.grid()
            menu_entry.grid()
        else:                                 # If it is not catering service, then delete the catering attributes
            min_guests_label.grid_remove()
            min_guests_entry.grid_remove()
            max_guests_label.grid_remove()
            max_guests_entry.grid_remove()
            menu_label.grid_remove()
            menu_entry.grid_remove()

    add_window = Toplevel()
    add_window.title("Add Supplier/Caterer")

    # Variables
    supplier_id_var = StringVar()
    company_name_var = StringVar()
    service_var = StringVar()
    phone_var = StringVar()
    address_var = StringVar()
    min_guests_var = StringVar()
    max_guests_var = StringVar()
    menu_var = StringVar()

    # Labels and enteries for the form fields
    Label(add_window, text="Supplier ID").grid(row=0, column=0)
    Entry(add_window, textvariable=supplier_id_var).grid(row=0, column=1)

    Label(add_window, text="Company Name").grid(row=1, column=0)
    Entry(add_window, textvariable=company_name_var).grid(row=1, column=1)

    Label(add_window, text="Service").grid(row=2, column=0)
    OptionMenu(add_window, service_var, *[s.name for s in Service], command=update_fields).grid(row=2, column=1)

    Label(add_window, text="Phone").grid(row=3, column=0)
    Entry(add_window, textvariable=phone_var).grid(row=3, column=1)

    Label(add_window, text="Address").grid(row=4, column=0)
    Entry(add_window, textvariable=address_var).grid(row=4, column=1)

    # Catering specific fields (hidden initially)
    min_guests_label = Label(add_window, text="Minimum Guests")
    min_guests_entry = Entry(add_window, textvariable=min_guests_var)
    max_guests_label = Label(add_window, text="Maximum Guests")
    max_guests_entry = Entry(add_window, textvariable=max_guests_var)
    menu_label = Label(add_window, text="Menu (separated by ';')")
    menu_entry = Entry(add_window, textvariable=menu_var)

    Button(add_window, text="Save", command=save_supplier).grid(row=10, column=1)


def modify_supplier():
    """A function to modify a supplier"""
    def fetch_details():
        """Fetching supplier pre-registered details"""
        supplier_id = id_var.get()
        supplier = Supplier.suppliers.get(supplier_id)
        if not supplier:
            messagebox.showerror("Error", "Supplier not found.")
            return

        # Populate the form with existing supplier details
        company_name_var.set(supplier.get_company_name())
        service_var.set(supplier.get_service().name)
        phone_var.set(supplier.get_phone())
        address_var.set(supplier.get_address())

        # Check if the supplier is a Caterer and set fields
        if isinstance(supplier, Caterer):
            min_guests_var.set(supplier.get_min_guests())
            max_guests_var.set(supplier.get_max_guests())
            menu_var.set(", ".join(supplier.get_menu()))
            toggle_caterer_fields(True)
        else:
            toggle_caterer_fields(False)

    def update_supplier():
        """A function to update supplier info"""
        try:
            supplier = Supplier.suppliers.get(id_var.get())
            if not supplier:
                raise Exception("Supplier not found.")

            # Update supplier details from the form
            supplier.set_company_name(company_name_var.get())
            supplier.set_service(Service[service_var.get()])
            supplier.set_phone(phone_var.get())
            supplier.set_address(address_var.get())

            if service_var.get() == "CATERING":  # If it is catering, then also include its attributes
                if isinstance(supplier, Caterer):
                    supplier.set_min_num_guests(int(min_guests_var.get()))
                    supplier.set_max_num_guests(int(max_guests_var.get()))
                    supplier.set_menu(menu_var.get().split(", "))
                else:
                    # Convert existing supplier to a Caterer if not already one
                    Supplier.suppliers[id_var.get()] = Caterer(
                        supplier_id=supplier.get_supplier_id(),
                        company_name=supplier.get_company_name(),
                        phone_num=supplier.get_phone(),
                        address=supplier.get_address(),
                        min_num_guests=int(min_guests_var.get()),
                        max_num_guests=int(max_guests_var.get()),
                        menu=menu_var.get().split(", ")
                    )

            messagebox.showinfo("Success", "Supplier details updated successfully!")
            save_data(Supplier.suppliers, 'suppliers.pkl')    # Saving changes
            modify_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            modify_window.lift()

    def toggle_caterer_fields(show):
        """Adding and removing catering attributes depending on the service chosen"""
        if show:
            min_guests_label.grid()
            min_guests_entry.grid()
            max_guests_label.grid()
            max_guests_entry.grid()
            menu_label.grid()
            menu_entry.grid()
        else:
            min_guests_label.grid_remove()
            min_guests_entry.grid_remove()
            max_guests_label.grid_remove()
            max_guests_entry.grid_remove()
            menu_label.grid_remove()
            menu_entry.grid_remove()

    modify_window = Toplevel()
    modify_window.title("Modify Supplier")

    # Create StringVars for form
    id_var = StringVar()
    company_name_var = StringVar()
    service_var = StringVar(modify_window)
    phone_var = StringVar()
    address_var = StringVar()
    min_guests_var = StringVar()
    max_guests_var = StringVar()
    menu_var = StringVar()

    # Form fields
    Label(modify_window, text="Supplier ID (to modify):").grid(row=0, column=0)
    Entry(modify_window, textvariable=id_var).grid(row=0, column=1)
    Button(modify_window, text="Fetch Details", command=fetch_details).grid(row=0, column=2)

    Label(modify_window, text="Company Name:").grid(row=1, column=0)
    Entry(modify_window, textvariable=company_name_var).grid(row=1, column=1)

    Label(modify_window, text="Service:").grid(row=2, column=0)
    OptionMenu(modify_window, service_var, *[s.name for s in Service]).grid(row=2, column=1)

    Label(modify_window, text="Phone:").grid(row=3, column=0)
    Entry(modify_window, textvariable=phone_var).grid(row=3, column=1)

    Label(modify_window, text="Address:").grid(row=4, column=0)
    Entry(modify_window, textvariable=address_var).grid(row=4, column=1)

    # Caterer-specific fields
    min_guests_label = Label(modify_window, text="Minimum Guests:")
    min_guests_entry = Entry(modify_window, textvariable=min_guests_var)
    max_guests_label = Label(modify_window, text="Maximum Guests:")
    max_guests_entry = Entry(modify_window, textvariable=max_guests_var)
    menu_label = Label(modify_window, text="Menu (separated by ','):")
    menu_entry = Entry(modify_window, textvariable=menu_var)

    Button(modify_window, text="Update", command=update_supplier).grid(row=10, column=1)

    # Initialize the visibility of caterer-specific fields
    service_var.trace("w", lambda *args: toggle_caterer_fields(service_var.get() == "CATERING"))
    toggle_caterer_fields(service_var.get() == "CATERING")

def delete_supplier():
    """A function to delete a supplier"""
    def fetch_supplier_details():
        """Fetching available details"""
        # Fetch the supplier details based on the ID and display them for confirmation
        supplier_id = id_var.get().strip()
        supplier = Supplier.suppliers.get(supplier_id)
        if supplier:
            details.set(f"Supplier ID: {supplier.get_supplier_id()}, Company: {supplier.get_company_name()}, Phone: {supplier.get_phone()}")
        else:
            messagebox.showerror("Error", "Supplier not found.")

    def perform_deletion():
        # Perform the deletion of the supplier using a backend function 'delete_supplier'
        supplier_id = id_var.get().strip()
        if supplier_id in Supplier.suppliers:
            del Supplier.suppliers[supplier_id]
            messagebox.showinfo("Success", "Supplier deleted successfully!")
            save_data(Supplier.suppliers, 'suppliers.pkl') # Save changes
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Supplier not found.")

    delete_window = Toplevel()
    delete_window.title("Delete Supplier")
    id_var = StringVar()
    details = StringVar()

    Label(delete_window, text="Supplier ID (to delete):").grid(row=0, column=0)
    Entry(delete_window, textvariable=id_var).grid(row=0, column=1)
    Button(delete_window, text="Fetch Details", command=fetch_supplier_details).grid(row=0, column=2)

    Label(delete_window, text="Details:").grid(row=1, column=0)
    Label(delete_window, textvariable=details).grid(row=1, column=1, columnspan=2)

    Button(delete_window, text="Delete", command=perform_deletion).grid(row=2, column=1)

def display_supplier_details():
    """A function to display supplier details"""
    def fetch_supplier_details():
        """A function to fetch pre-registered details about the supplier"""
        supplier_id = id_var.get().strip()
        supplier = Supplier.suppliers.get(supplier_id)
        if supplier:
            details.set(supplier.print_details())
        else:
            messagebox.showerror("Error", "Supplier not found.")

    display_window = Toplevel()
    display_window.title("Display Supplier Details")
    id_var = StringVar()
    details = StringVar()
    # Creating labels, enteries and buttons
    Label(display_window, text="Supplier ID (to display):").grid(row=0, column=0)
    Entry(display_window, textvariable=id_var).grid(row=0, column=1)
    Button(display_window, text="Fetch Details", command=fetch_supplier_details).grid(row=0, column=2)

    Label(display_window, text="Details:").grid(row=1, column=0)
    Label(display_window, textvariable=details, wraplength=500).grid(row=1, column=1, columnspan=2, sticky="w")


def add_venue():
    """A function to add a venue"""
    def save_venue():
        """A function to save a venue using a backend function 'add_venue'"""
        try:
            new_venue = Venue(                  # Creating an instance and setting attributes
                venue_id=id_var.get(),
                name=name_var.get(),
                min_num_guests=int(min_guests_var.get()),
                max_num_guests=int(max_guests_var.get()),
                phone_num=phone_var.get(),
                address=address_var.get())

            new_venue.add_venue()  # Using the backend function
            messagebox.showinfo("Success", "Venue added successfully!")
            save_data(Venue.venues, 'venues.pkl')  # Save changes
            add_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            add_window.lift()

    add_window = Toplevel()
    add_window.title("Add Venue")

    # Variables for the form
    id_var = StringVar()
    name_var = StringVar()
    min_guests_var = StringVar()
    max_guests_var = StringVar()
    phone_var = StringVar()
    address_var = StringVar()

    fields = [
        ("Venue ID", id_var),
        ("Name", name_var),
        ("Minimum Number of Guests", min_guests_var),
        ("Maximum Number of Guests", max_guests_var),
        ("Phone Number", phone_var),
        ("Address", address_var)]
    # Creating labels and enteries
    for i, (label, var) in enumerate(fields):
        Label(add_window, text=label).grid(row=i, column=0)
        Entry(add_window, textvariable=var).grid(row=i, column=1)

    Button(add_window, text="Save", command=save_venue).grid(row=len(fields), column=1)

def modify_venue():
    """A function to modify a venue"""
    def fetch_venue_details():
        venue_id = id_var.get()
        venue = Venue.venues.get(venue_id)
        if not venue:
            messagebox.showerror("Error", "Venue not found.")
            return

        # Populate the form with existing venue details
        name_var.set(venue.get_venue_name())
        min_guests_var.set(str(venue.get_min_num_guests()))
        max_guests_var.set(str(venue.get_max_num_guests()))
        phone_var.set(venue.get_phone())
        address_var.set(venue.get_address())

    def update_venue():
        """Using a backend function to update a venue"""
        try:
            venue = Venue.venues.get(id_var.get())
            if not venue:
                raise Exception("Venue not found.")

            # Update venue details from the form
            venue.set_venue_name(name_var.get())
            venue.set_min_num_guests(int(min_guests_var.get()))
            venue.set_max_num_guests(int(max_guests_var.get()))
            venue.set_phone(phone_var.get())
            venue.set_address(address_var.get())

            messagebox.showinfo("Success", "Venue details updated successfully!")
            save_data(Venue.venues, 'venues.pkl')   # Save data
            modify_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            modify_window.lift()

    modify_window = Toplevel()
    modify_window.title("Modify Venue")

    # Create StringVars for form
    id_var = StringVar()
    name_var = StringVar()
    min_guests_var = StringVar()
    max_guests_var = StringVar()
    phone_var = StringVar()
    address_var = StringVar()

    # Form fields
    fields = [
        ("Venue ID (to modify)", id_var),
        ("Name", name_var),
        ("Minimum Number of Guests", min_guests_var),
        ("Maximum Number of Guests", max_guests_var),
        ("Phone", phone_var),
        ("Address", address_var)]

    # Create form labels and entries
    for i, (label, var) in enumerate(fields):
        Label(modify_window, text=label).grid(row=i, column=0)
        Entry(modify_window, textvariable=var).grid(row=i, column=1)

    Button(modify_window, text="Fetch Details", command=fetch_venue_details).grid(row=0, column=2)
    Button(modify_window, text="Update", command=update_venue).grid(row=len(fields), column=1)

def delete_venue():
    """A function to delete a venue"""
    def fetch_venue_details():
        # Fetch the venue details based on the ID and display them for confirmation
        venue_id = id_var.get().strip()
        venue = Venue.venues.get(venue_id)
        if venue:
            details.set(f"Venue ID: {venue.get_venue_id()}, Name: {venue.get_venue_name()}, Address: {venue.get_address()}")
        else:
            messagebox.showerror("Error", "Venue not found.")

    def perform_deletion():
        # Perform the deletion of the venue using a backend function 'delete_venue'
        venue_id = id_var.get().strip()
        if venue_id in Venue.venues:
            del Venue.venues[venue_id]
            messagebox.showinfo("Success", "Venue deleted successfully!")
            save_data(Venue.venues, 'venues.pkl')      # Save changes
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Venue not found.")

    delete_window = Toplevel()
    delete_window.title("Delete Venue")
    id_var = StringVar()
    details = StringVar()
    # Creating labels, entries and buttons
    Label(delete_window, text="Venue ID (to delete):").grid(row=0, column=0)
    Entry(delete_window, textvariable=id_var).grid(row=0, column=1)
    Button(delete_window, text="Fetch Details", command=fetch_venue_details).grid(row=0, column=2)

    Label(delete_window, text="Details:").grid(row=1, column=0)
    Label(delete_window, textvariable=details).grid(row=1, column=1, columnspan=2)

    Button(delete_window, text="Delete", command=perform_deletion).grid(row=2, column=1)

def display_venue_details():
    """A function to display the venue details"""
    def fetch_venue_details():
        """Fetching available details of the venue"""
        venue_id = id_var.get().strip()
        venue = Venue.venues.get(venue_id)
        if venue:
            details.set(venue.print_venue_details())
        else:
            messagebox.showerror("Error", "Venue not found.")

    display_window = Toplevel()
    display_window.title("Display Venue Details")
    id_var = StringVar()
    details = StringVar()

    Label(display_window, text="Venue ID (to display):").grid(row=0, column=0)
    Entry(display_window, textvariable=id_var).grid(row=0, column=1)
    Button(display_window, text="Fetch Details", command=fetch_venue_details).grid(row=0, column=2)

    Label(display_window, text="Details:").grid(row=1, column=0)
    Label(display_window, textvariable=details).grid(row=1, column=1, columnspan=2, sticky="w")


# Main window
def create_main_window():
    """A function that creates the main window"""
    root = tk.Tk()
    root.title("The Best Events Company Management System")
    root.geometry("800x600")

    menu_bar = tk.Menu(root)       # Setting the menu bar where we include all classes and functions
    root.config(menu=menu_bar)

    # Employee menu
    employee_menu = tk.Menu(menu_bar, tearoff=0)
    employee_menu.add_command(label="Add Employee", command=add_employee)
    employee_menu.add_command(label="Modify Employee", command=modify_employee)
    employee_menu.add_command(label="Delete Employee", command=delete_employee)
    employee_menu.add_command(label="Display Employee Details", command=display_employee_details)
    menu_bar.add_cascade(label="Employees", menu=employee_menu)

    # Client menu
    client_menu = tk.Menu(menu_bar, tearoff=0)
    client_menu.add_command(label="Add Client", command=add_client)
    client_menu.add_command(label="Modify Client", command=modify_client)
    client_menu.add_command(label="Delete Client", command=delete_client)
    client_menu.add_command(label="Display Client Details", command=display_client_details)
    menu_bar.add_cascade(label="Clients", menu=client_menu)

    # Guest menu
    guest_menu = tk.Menu(menu_bar, tearoff=0)
    guest_menu.add_command(label="Add Guest", command=add_guest)
    guest_menu.add_command(label="Modify Guest", command=modify_guest)
    guest_menu.add_command(label="Delete Guest", command=delete_guest)
    guest_menu.add_command(label="Display Guest Details", command=display_guest_details)
    menu_bar.add_cascade(label="Guests", menu=guest_menu)


    # Event menu setup
    event_menu = tk.Menu(menu_bar, tearoff=0)
    event_menu.add_command(label="Add Event", command=add_event)
    event_menu.add_command(label="Modify Event", command=modify_event)
    event_menu.add_command(label="Delete Event", command=delete_event)
    event_menu.add_command(label="Display Event Details", command=display_event_details)
    menu_bar.add_cascade(label="Events", menu=event_menu)


    # Supplier menu
    supplier_menu = tk.Menu(menu_bar, tearoff=0)
    supplier_menu.add_command(label="Add Supplier", command=add_supplier)
    supplier_menu.add_command(label="Modify Supplier", command=modify_supplier)
    supplier_menu.add_command(label="Delete Supplier", command=delete_supplier)
    supplier_menu.add_command(label="Display Supplier Details", command=display_supplier_details)
    menu_bar.add_cascade(label="Suppliers", menu=supplier_menu)

    # Venue menu

    venue_menu = tk.Menu(menu_bar, tearoff=0)
    venue_menu.add_command(label="Add Venue", command=add_venue)
    venue_menu.add_command(label="Modify Venue", command=modify_venue)  # Add modify_venue here
    venue_menu.add_command(label="Delete Venue", command=delete_venue)  # Add modify_venue here
    venue_menu.add_command(label="Display Venue Details", command=display_venue_details)  # Add modify_venue here
    menu_bar.add_cascade(label="Venues", menu=venue_menu)

    menu_bar.add_command(label="Exit", command=root.quit)

    root.mainloop()

# Run the application
create_main_window()