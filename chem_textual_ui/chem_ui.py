from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Static, Input, TextLog

from chem_data.data_set import load_data_frame
from chem_textual_ui.calculation_methods import calculate_free_energy, calculate_enthalpy_change, \
    calculate_entropy_change
from chem_textual_ui.helper_methods import extract_chemical_formulas
from chem_textual_ui.input_panel import UserInputArea
from chem_textual_ui.main_panel import InstructionsWindow, DataWindow, OutputPanel

import re


class ChemApp(App):
    CSS_PATH = "chem_ui.css"

    df = load_data_frame()
    reactants = []
    products = []
    def compose(self) -> ComposeResult:
        yield Footer()
        yield MainPanel()
        yield UserInputArea()

    #Handle the user input
    def on_input_submitted(self, message: Input.Submitted) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            if(message.input.id=='reactant_input'):
                log = self.query_one("#reactants")
                reactant = self.handle_input_response(message.value)
                if(reactant[0] != 'error'):
                    self.add_reactant(reactant)
                    log.write(self.get_chemical_name(reactant[0]))
                message.input.value = ""
            elif(message.input.id == 'product_input'):
                log = self.query_one("#products")
                product = self.handle_input_response(message.value)
                if (product[0] != 'error'):
                    self.add_product(product)
                    log.write(self.get_chemical_name(product[0]))
                message.input.value = ""

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'btn_clear':
            self.clear_ui()
        if event.button.id == 'btn_calculate':
            output_log = self.query_one('#output', TextLog)
            result = self.perform_calculations(output_log)

    def clear_ui(self):
        output_log = self.query_one('#output', TextLog)
        reactant_log = self.query_one("#reactants")
        product_log = self.query_one("#products")

        output_log.clear()
        reactant_log.clear()
        product_log.clear()

        self.reactants.clear()
        self.products.clear()
    def handle_input_response(self, user_input):
        #first remove whitespace from the input
        user_input = user_input.replace(' ', '')
        #If the input is invalid, the if statement will evaluate to false and the value_is_valid() method will
        #Not execute.
        if(self.validate_reaction_entry(user_input) and self.value_is_valid(57, user_input)):
            pair = user_input.split(",")
            row = int(pair[0])
            coefficient = int(pair[1])
            asTuple = (row, coefficient)
            return asTuple
        else:
            output_log = self.query_one('#output', TextLog)
            output_log.write("Invalid input.")
            return ("error", "bad input")

    def add_reactant(self, reactant):
        self.reactants.append(reactant)

    def add_product(self, product):
        self.products.append(product)
    def validate_reaction_entry(self, entry):
        pattern = '[0-9]+,[1-9]+'
        is_match = re.match(pattern, entry)
        if is_match is not None:
            return True
        else:
            return False

    def value_is_valid(self, max, entry):
        values = entry.split(",")
        if int(values[0]) > max or int(values[0]) < 0:
            return False
        else:
            return True

    def get_chemical_name(self, row_index):
        name = self.df._get_value(row_index, 'name')
        formula = self.df._get_value(row_index, 'formula')
        state = self.df._get_value(row_index, 'state')
        return f'{name} {formula} {state}'

    def perform_calculations(self, log: TextLog):
        dH = calculate_enthalpy_change(self.df, self.reactants, self.products)
        dG = calculate_free_energy(self.df, self.reactants, self.products)
        dS = calculate_entropy_change(self.df, self.reactants, self.products)

        reactant_formulas = extract_chemical_formulas(self.df, self.reactants)
        product_formulas = extract_chemical_formulas(self.df, self.products)

        log.write(reactant_formulas)
        log.write(product_formulas)
        log.write(f'The enthalpy change (dH) is: {dH} kJ per mol')
        log.write(f'The free energy change (dG) is: {dG} kJ per mol')
        log.write(f'The entropy change (dS) is: {dS} kJ per mol per Kelvin')

        report = f"""\
        The reactants are: {reactant_formulas}
        The products are: {product_formulas} 
        The enthalpy change (dH) is: {dH} kJ per mol
        The free energy change (dG) is: {dG} kJ per mol
        The entropy change (dS) is: {dS} kJ per mol per Kelvin
        """
        print(report)
        return report

class MainPanel(Static):
    def compose(self) -> ComposeResult:
        yield InstructionsWindow()
        yield DataWindow()
        yield OutputPanel()



