import pickle
import os
import sys

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Maps the names of the classes to the correct module name
        class_module_dict = {
            'Employee': 'Employee_class',
            'Client': 'Client_and_guest_classes',
            'Guest': 'Client_and_guest_classes'}
        if name in class_module_dict:
            module = class_module_dict[name]
        # Import the module and return the class
        __import__(module)
        return getattr(sys.modules[module], name)

def load_data(filename):
    """Load data from a binary file using a custom unpickler"""
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            unpickler = CustomUnpickler(file)
            return unpickler.load()
    return {}

def save_data(data, filename):
    """Save data to a binary file using pickle"""
    with open(filename, 'wb') as file:
        pickle.dump(data, file)