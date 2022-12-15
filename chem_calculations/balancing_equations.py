from chemlib import Compound, Reaction

def enter_formulas():
    compounds = []
    while True:
        formula = input("Enter a formula: ")
        if(formula=='done'):
            break
        try:
            compound = Compound(formula)
            compounds.append(compound)
        except:
            print("I don't think you entered a valid formula.")
    return compounds

def balance_reaction(reactants: list, products: list):
    reaction: Reaction = Reaction(reactants, products)
    try:
        reaction.balance()
        return ChemResult(True, reaction)
    except:
        return ChemResult(False, reaction)

def generate_reaction()->Reaction:
    print("Enter reactants. Type 'done' when you are finished.")
    reactants = enter_formulas()
    print("Enter products. Type 'done' when you are finished.")
    products = enter_formulas()
    return Reaction(reactants, products)


class StoichiometryResult:
    def __init__(self, status: bool, formula_amounts: list, message : str =""):
        self.status = status
        self.formula_amounts = formula_amounts
        self.message = message

def calculate_stoichiometry_by_mass(reaction: Reaction, position: int, amount: float) -> StoichiometryResult:
    try:
        stoichiometry = reaction.get_amounts(position, grams=amount)
        return StoichiometryResult(True, stoichiometry)
    except:
        return StoichiometryResult(False, [], "Calculations could not be performed.")

def calculate_stoichiometry_by_mole(reaction: Reaction, position: int, amount: float) -> StoichiometryResult:
    try:
        stoichiometry = reaction.get_amounts(position, moles=amount)
        return StoichiometryResult(True, stoichiometry)
    except:
        return StoichiometryResult(False, [], "Calculations could not be performed.")

class ChemResult:
    def __init__(self, status: bool, reaction: Reaction):
        self.status = status
        self.reaction = reaction


