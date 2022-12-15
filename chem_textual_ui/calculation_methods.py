def calculate_enthalpy_change(data_frame, reactants: list, products: list):
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


def calculate_free_energy(data_frame, reactants: list, products: list):
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


def calculate_entropy_change(data_frame, reactants: list, products: list):
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