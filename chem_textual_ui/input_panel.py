from textual.app import ComposeResult
from textual.widgets import Static, Button, Label, Input


#Container for the input fields and two buttons
class UserInputArea(Static):
    def compose(self) -> ComposeResult:
        yield InputArea()
        yield Button("Calculate!", id="btn_calculate", variant="success")
        yield Button("Clear", id="btn_clear", variant="error")

class InputArea(Static):
    def compose(self) -> ComposeResult:
        yield Label("Reactants")
        yield Input(placeholder="Example: 3,2 to enter 2 mol butane", id="reactant_input")
        yield Label("Products")
        yield Input(placeholder="Example: 0,5 to enter 5 mol methane", id="product_input")