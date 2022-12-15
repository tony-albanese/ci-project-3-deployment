def extract_chemical_formulas(df, chemical_list):
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