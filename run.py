# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
from chem_data import data_set
from chem_textual_ui.chem_ui import ChemApp

def start_chem_app():
    app = ChemApp()
    app.run()
start_chem_app()