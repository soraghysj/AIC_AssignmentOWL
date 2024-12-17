from owlready2 import get_ontology
from math import pi, prod
import tkinter as tk
from tkinter import ttk
import numbers


ontology_file = "VolumeOWL.owl"  # RDF/XML format
mainElement = None
allClasses = []
allFormulas = {}
parameters = {}
variables = {}

def contains_number(s):
    for char in s:
        if char.isdigit():
            return True
    return False

def clean_variables():
    for cls in allClasses:
        key = 0
        variables[cls] = []
        for p in parameters[cls]:
            if contains_number(p):
                parameters[cls][key] = eval(p)
            elif p == "pi":
                 parameters[cls][key] = pi
            else:
                variables[cls].append(p)
            key+=1
        variables[cls]= list(set(variables[cls]))

def fetch_main_class():
    for cls in ontology.classes():
        if "Thing" in [str(parent.name) for parent in cls.is_a]:
            return cls.name

# Function to fetch top-level classes
def fetch_classes():    
    for cls in ontology.classes():
        if mainElement in [str(parent.name) for parent in cls.is_a]:
            allClasses.append(cls.name)

def fetch_formulas():
    for cls in allClasses:
        for ind in ontology.individuals():
            if cls in ind.name:
                parameters[cls] = ind.comment[0].split(" * ")
                allFormulas[cls] = ind.comment[0]
        
def update_formula(event):
    selected_shape = shape_var.get()
    formula = allFormulas.get(selected_shape, "Select a shape to see its formula.")
    formula_label.config(text=formula)
    
    # Clear previous input fields
    for widget in input_frame.winfo_children():
        widget.destroy()
        
    # Create new input fields for the selected shape
    inputs.clear()
    variabless = variables[selected_shape]
    for var in variabless:
        tk.Label(input_frame, text=var, font=("Arial", 12)).pack(anchor="w", pady=2)
        entry = tk.Entry(input_frame, font=("Arial", 12))
        entry.pack(fill="x", pady=2)
        inputs[var] = entry
        
def calculate_volume():
    selected_shape = shape_var.get()
    variabless = variables[selected_shape]
    try:
        # Extract input values
        values = {var.split()[0].lower(): float(inputs[var].get()) for var in variabless}
        volume = None
        formula = parameters[selected_shape].copy()
        i = 0
        for f in formula:
            if not isinstance(f, numbers.Number):
                formula[i] = values[f]
            i+=1
        volume = prod(formula)
        # Update the result label
        result_label.config(text=f"Volume: {volume:.2f}")
    except ValueError:
        result_label.config(text="Error: Please enter valid numeric values.")

ontology = get_ontology(ontology_file).load()
mainElement = fetch_main_class()
fetch_classes()
fetch_formulas()
clean_variables()

# Create the main window
root = tk.Tk()
root.geometry("600x600")
root.configure(background='#7FFFD4')
root.title("Volume Formula Viewer")

# Dropdown label
dropdown_label = tk.Label(root, text="Select a shape:", font=("Arial", 14))
dropdown_label.pack(pady=10)

# Dropdown menu
shape_var = tk.StringVar()
shape_dropdown = ttk.Combobox(root, textvariable=shape_var, font=("Arial", 14))
shape_dropdown["values"] = list(allFormulas.keys())
shape_dropdown["state"] = "readonly"
shape_dropdown.pack(pady=10)

# Formula label
formula_label = tk.Label(root, text="Select a shape to see its formula.", font=("Arial", 14), wraplength=400, justify="center")
formula_label.pack(pady=20)

# Input frame for dynamic fields
input_frame = tk.Frame(root)
input_frame.pack(pady=10, fill="x", padx=20)

# Calculate button
calculate_button = tk.Button(root, text="Calculate Volume", font=("Arial", 14), command=calculate_volume)
calculate_button.pack(pady=10)

# Bind dropdown selection to update function
shape_dropdown.bind("<<ComboboxSelected>>", update_formula)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

# Dictionary to hold input fields
inputs = {}
# Run the Tkinter main loop
root.mainloop()
