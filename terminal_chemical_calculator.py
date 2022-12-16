import pandas

from term_app_helper_methods import *
class TerminalChemApp():

    welcome_message = '''
        This app allows you to perform thermodynamic calculations by 
        selecting chemicals from a data table.
    '''

    def __init__(self) -> None:
        self.products = []
        self.reactants = []
        self.data = load_data_frame()
        self.truncated_data = self.data[['name', 'formula', 'state']]

    def get_instructions(self) -> str:
        instructions = '''
        Enter a formula like this: NH3 
        To see the data, enter "d" and hit Enter. 
        To exit, enter "q" and hit Enter.
        To see a list of your products, enter "p" and hit Enter.
        To see a list of reactants, enter "r" and hit Enter.
        To see these instructions, enter "i" and hit Enter.
        To perform the calculations, enter "c" and hit Enter.
        To start over, type "clear" and hit Enter.
        '''
        return instructions

    def display_data(self):
        i = 0
        while i < len(self.truncated_data):
            for i in range(i, i +5):
                row = f"{self.truncated_data.loc[i, 'name']} {self.truncated_data.loc[i, 'formula']} {self.truncated_data.loc[i, 'state']}"
                print(row)
                i = i + 1
            key = input("Press c to continue. Or press enter to go back.\n")
            if key == '' or key == ' ':
                break

    def print_data_frame(self, df: pandas.DataFrame):
        print(df)
    def handle_user_input(self, entry: str):
        #remove leading whitespace
        entry = entry.strip()
        #search the dataframe
        result = self.data.loc[self.data['formula'] == entry]
        list_of_indices = []
        for row in result.index:
            list_of_indices.append(row)
        print(list_of_indices)

        if result.empty :
            print("Invalid entry. Please try again.")
        elif len(list_of_indices) > 1:
            print(f"More than one result.")
            self.print_data_frame(result)
            choice_is_made = False
            while not choice_is_made:
                index = input("Which do you want? Enter the index: \n")
                if not index.isdigit() or not (int(index) in list_of_indices):
                    print("That is not a valid entry.")
                else:
                    choice_is_made = True
                    print(f"You chose {index}")
                    self.add_chemical_to_list(int(index))
        else:
            print("Found something!")
            print(result)
            self.add_chemical_to_list(list_of_indices[0])


    def run(self):
        print(self.welcome_message)
        print(self.get_instructions())

        while True:
            entry = input("Command: \n") #Don't forget backspace before entry.
            entry.strip()
            if entry == 'q':
                break
            elif entry == 'd':
                self.display_data()
            elif entry == 'i':
                print(self.get_instructions())
            elif entry == 'c':
                print(self.calculate())
            elif entry == 'clear':
                self.clear_chemical_lists()
            elif entry == 'p':
                formulas = extract_chemical_formulas(self.data, self.products)
                print(f"Products: {formulas}")
            elif entry == 'r':
                formulas = extract_chemical_formulas(self.data, self.reactants)
                print(f"Reactants: {formulas}")
            else:
                self.handle_user_input(entry)


    def clear_chemical_lists(self):
        self.products.clear()
        self.reactants.clear()
        print("Choices cleared.")

    def add_chemical_to_list(self,  i: int):
        print("Enter the coeffcient from the chemical equation.")
        print("Enter 0 or just hit enter to not use this chemical")
        coefficient_string = str(input("Coefficient:\n"))
        coefficient_string.strip()
        entry_processed = False
        while not entry_processed:
            if coefficient_string == '':
                entry_processed = True
            elif coefficient_string == '0':
                entry_processed = True
            elif not coefficient_string.isdigit():
                print("That was not a valid response. Try again.")
                coefficient_string = str(input("Reinput coefficient:\n"))
            else:
                i = int(i)
                coefficient = int(coefficient_string)
                print("Enter p to add to products. Enter r to add to reactants.")
                choice_made = False
                while not choice_made:
                    choice = input("(p)roduct or (r)eactant?\n")

                    if choice == 'p':
                        self.products.append((i, coefficient))
                        print("Successfully added to products.")
                        choice_made = True

                    elif choice == 'r':
                        self.reactants.append((i, coefficient))
                        print("Successully added to reactants.")
                        choice_made = True
                entry_processed = True

    def calculate(self)->str:
        if len(self.products) == 0 or len(self.reactants) == 0:
            return "One of the data sets is empty. Cannot calculate with an empty data set."
        else:
            result = generate_thermodynamic_calculations(self.data, self.reactants, self.products)
            return result

