from rich.table import Table
from rich.text import Text
from textual import events
from textual.app import ComposeResult
from textual.widgets import Static, TextLog
from chem_data.data_set import load_data_frame
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
            table.add_row(str(index), row["name"], row["formula"], row["state"])
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
        # panel = Panel(Text(self.INSTRUCTIONS), expand=False, title="Instructions")
        text = Text(self.INSTRUCTIONS)
        instructions_window.write(text)

class OutputPanel(Static):
    def _on_mount(self, event: events.Mount) -> None:
        reactants_log = self.query_one("#reactants", TextLog)
        reactants_log.write("Reactants:")
        products_log = self.query_one("#products", TextLog)
        products_log.write("Products:")

    def compose(self) -> ComposeResult:
        yield TextLog(id = "reactants")
        yield TextLog(id="products")
        yield TextLog(id= "output")