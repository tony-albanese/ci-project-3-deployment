import pandas
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table, Column
from rich.text import Text
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button, Header, Footer, Static, Placeholder, Input, Label, TextLog
import re
from list_item import ListItem
from list_view_class import ListView
from data_set import *


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
        if(self.validate_reaction_entry(user_input) and self.value_is_valid(44, user_input)):
            pair = user_input.split(",")
            row = int(pair[0])
            coefficient = int(pair[1])
            asTuple = (row, coefficient)
            return asTuple
        else:
            output_log = self.query_one('#output', TextLog)
            output_log.write("Something went wrong.")
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
        if int(values[0]) > max:
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

class DataWindow(Static):
    def compose(self) -> ComposeResult:
        print("DataWindow compose()")
        yield TextLog(id="data_log_window")

    def _on_mount(self, event: events.Mount) -> None:
        log = self.query_one(TextLog)
        table = self.generate_data_table()
        log.write(table)
    def generate_data_table(self):
        df = load_data_frame()
        table = Table(title="Chemical Data")
        table.add_column('index')
        table.add_column('Name')
        table.add_column('formula')
        table.add_column('state')
        for index, row in df.iterrows():
            table.add_row(str(index), row["name"],row["formula"],row["state"] )
        return table

class InstructionsWindow(Static):

    INSTRUCTIONS = '''
    Instructions\n
    This app will calculate the changes in enthalpy,
    free energy, and entropy for a set 
    reactants and products you select.
    
    Use the table to find the chemical you need and enter
    the index and the coefficient separated by a comma.
    There is an input box for reactants and one for
    products. Press the Calculate button to perform
    the calculations. Clear will clear the screen.
    '''
    def compose(self) -> ComposeResult:
        yield TextLog(id="instruction_log_window")

    def _on_mount(self, event: events.Mount) -> None:
        instructions_window = self.query_one("#instruction_log_window")
        #panel = Panel(Text(self.INSTRUCTIONS), expand=False, title="Instructions")
        text = Text(self.INSTRUCTIONS)
        instructions_window.write(text)


class OutputPanel(Static):
    def compose(self) -> ComposeResult:
        yield TextLog(id = "reactants")
        yield TextLog(id="products")
        yield TextLog(id= "output")


#Container for the input fields and two buttons
class UserInputArea(Static):
    def compose(self) -> ComposeResult:
        yield InputArea()
        yield Button("Calculate!", id="btn_calculate", variant="success")
        yield Button("Clear", id="btn_clear", variant="error")

class OutputWindow(Static):
    def compose(self) -> ComposeResult:
        yield Placeholder()

class InputArea(Static):
    def compose(self) -> ComposeResult:
        yield Label("Reactants")
        yield Input(placeholder="Example: 3,2 to enter 2 mol butane", id="reactant_input")
        yield Label("Products")
        yield Input(placeholder="Example: 0,5 to enter 5 mol methane", id="product_input")