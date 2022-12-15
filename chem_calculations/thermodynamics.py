import pandas.core.frame

from chem_data.data_set import *
from rich import print
import re


def calculate_thermodynamic_properties():
    reactants = []
    products = []
    while True:
        print("Enter a reactant and the coefficient from the balanced equation separated by a comma.")
        print("When you are done entering reactants, type done")
        reactant = input("Reactant: ")
        if reactant == 'done':
            break


def get_reactants():
    reactants = []
    while True:
        print("Enter a reactant and the coefficient from the balanced equation separated by a comma.")
        print("When you are done entering reactants, type done")
        user_input = input("Reactant: ")

        if user_input == 'done':
            break
        if validate_reaction_entry(user_input) and value_is_valid(44, user_input):
            pair = user_input.split(",")
            row = int(pair[0])
            coefficient = int(pair[1])
            asTuple = (row, coefficient)
            reactants.append(asTuple)
        else:
            print("Invalid input")

    return reactants


def get_products():
    products = []
    while True:
        print("Enter a product and the coefficient from the balanced equation separated by a comma.")
        print("When you are done entering products, type done")
        user_input = input("Product: ")

        if user_input == 'done':
            break
        if validate_reaction_entry(user_input) and value_is_valid(44, user_input):
            pair = user_input.split(",")
            row = int(pair[0])
            coefficient = int(pair[1])
            asTuple = (row, coefficient)
            products.append(asTuple)
        else:
            print("Invalid input")

    print(products)
    return products


def validate_reaction_entry(entry):
    pattern = '[0-9]+,[1-9]+'
    is_match = re.match(pattern, entry)
    if is_match is not None:
        return True
    else:
        return False


def value_is_valid(max, entry):
    values = entry.split(",")
    if int(values[0]) > max:
        return False
    else:
        return True


def calculate_enthalpy_change(data_frame: pandas.core.frame.DataFrame, reactants: list, products: list):
    column_name = 'dH'
    sum_products = 0
    sum_reactants = 0

    for reactant in reactants:
        row = reactant[0]
        coefficient = reactant[1]
        enthalpy = data_frame._get_value(row, column_name)
        sum_reactants = sum_reactants + enthalpy * coefficient

    for product in products:
        row = product[0]
        coefficient = product[1]
        enthalpy = data_frame._get_value(row, column_name)
        sum_products = sum_products + enthalpy * coefficient

    enthalpy_change = sum_products - sum_reactants
    return enthalpy_change


def calculate_free_energy(data_frame: pandas.core.frame.DataFrame, reactants: list, products: list):
    column_name = 'dG'
    sum_products = 0
    sum_reactants = 0

    for reactant in reactants:
        row = reactant[0]
        coefficient = reactant[1]
        enthalpy = data_frame._get_value(row, column_name)
        sum_reactants = sum_reactants + enthalpy * coefficient

    for product in products:
        row = product[0]
        coefficient = product[1]
        enthalpy = data_frame._get_value(row, column_name)
        sum_products = sum_products + enthalpy * coefficient

    energy_change = sum_products - sum_reactants

    print("Sum products: ")
    print(sum_products)
    print("Sum of reactants:")
    print(sum_reactants)
    return energy_change


def calculate_entropy_change(data_frame: pandas.core.frame.DataFrame, reactants: list, products: list):
    column_name = 'dS'
    sum_products = 0
    sum_reactants = 0

    for reactant in reactants:
        row = reactant[0]
        coefficient = reactant[1]
        enthalpy = data_frame._get_value(row, column_name)
        sum_reactants = sum_reactants + enthalpy * coefficient

    for product in products:
        row = product[0]
        coefficient = product[1]
        enthalpy = data_frame._get_value(row, column_name)
        sum_products = sum_products + enthalpy * coefficient

    # Divide by 1000 because of J to kJ unit conversion
    entropy_change = (sum_products - sum_reactants) / 1000

    print("Sum products: ")
    print(sum_products)
    print("Sum of reactants:")
    print(sum_reactants)
    return entropy_change

def generate_thermodynamic_calculations():
    df = load_data_frame()
    reactants = get_reactants()
    products = get_products()

    dH = calculate_enthalpy_change(df, reactants, products)
    dG = calculate_free_energy(df, reactants, products)
    dS = calculate_entropy_change(df, reactants, products)

    reactant_formulas = extract_chemical_formulas(df, reactants)
    product_formulas = extract_chemical_formulas(df, products)

    report = f"""
    The reactants are: {reactant_formulas}
    The products are: {product_formulas} 
    The enthalpy change (dH) is: {dH} kJ per mol
    The free energy change (dG) is: {dG} kJ per mol
    The entropy change (dS) is: {dS} kJ per mol per Kelvin
    """
    print(report)
    return report

def extract_chemical_formulas(df: pandas.core.frame.DataFrame, chemical_list: list):
    product_formulas = []
    col_name = 'name'
    col_state = 'state'
    col_formula = 'formula'
    for chemical in chemical_list:
        row = chemical[0]
        name = df._get_value(row, col_name)
        formula = df._get_value(row, col_formula)
        state = df._get_value(row, col_state)
        full_formula = f'{formula} {name} {state}'
        product_formulas.append(full_formula)

    return product_formulas