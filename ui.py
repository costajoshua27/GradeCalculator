'''
UI Module for Grade Calculator
Author: Joshua Costa
Created: 3/15/19
'''

import tkinter as tk 
from grade_calculator import GradeCalculator
import tkinter.messagebox

TITLE_FONT = ('Times New Roman', 40)
HEADER_FONT = ('Times New Roman', 18)
DEFAULT_FONT = ('Times New Roman', 13)

class AppGUI(tk.Tk):

    def __init__(self, *args, **kwargs):

        # Initialize the window
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Grade Calculator')
        self.geometry("600x650")
        self.resizable(0,0)

        # Create the Frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Allow for different pages
        self.frames = {}
        for Page in (MainMenuPage, CalculatorPage):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start the application on the main menu
        self.show_frame(MainMenuPage)


    def show_frame(self, container):
        '''Changes the current page'''
        frame = self.frames[container]
        frame.tkraise()


class MainMenuPage(tk.Frame):

    def __init__(self, parent, controller):

        # Initialize the Frame
        tk.Frame.__init__(self, parent, bg='light grey')

        # Label for the title
        self.title = tk.Label(self, text='Grade Calculator', font=TITLE_FONT, bg='light grey')
        self.title.place(relx=.25, rely=.2)

        # Label for the author
        self.author = tk.Label(self, text='by Joshua Costa', font=HEADER_FONT, bg='light grey')
        self.author.place(relx=.39, rely=.3)

        # Start button
        self.calc_button = tk.Button(self, text='Start', font=DEFAULT_FONT, command=(lambda: self._change_frame_and_start_button_text(controller)))
        self.calc_button.place(relx=.46, rely=.4)

        # Exit button
        self.exit_button = tk.Button(self, text='Exit', font=DEFAULT_FONT, command=controller.destroy)
        self.exit_button.place(relx=.47, rely=.47)

    def _change_frame_and_start_button_text(self, controller):
        controller.show_frame(CalculatorPage)
        self.calc_button.config(text='Resume')


class CalculatorPage(tk.Frame):

    def __init__(self, parent, controller):

        # Initialize the Frame
        tk.Frame.__init__(self, parent, bg='light grey')

        # Create new GradeCalculator class
        self.calculator = GradeCalculator()

        # Create boolean variables
        self.can_add_assignments = False
        self.can_calculate_grade = False

        # Create the field that adds new categories
        self.category_name_label = tk.Label(self, text='Category Name', font=HEADER_FONT, bg='light grey')
        self.category_name_label.grid(row=0,column=0)

        self.new_category = tk.StringVar()
        self.category_name_entry = tk.Entry(self, textvariable=self.new_category, font=DEFAULT_FONT)
        self.category_name_entry.grid(row=1,column=0)

        self.category_percentage_label = tk.Label(self, text='Percentage of Category', font=HEADER_FONT, bg='light grey')
        self.category_percentage_label.grid(row=2,column=0)

        self.new_category_percentage = tk.StringVar()
        self.category_percentage_entry = tk.Entry(self, textvariable=self.new_category_percentage, font=DEFAULT_FONT)
        self.category_percentage_entry.grid(row=3, column=0)

        self.category_button = tk.Button(self, text= "Add new grade category", font=DEFAULT_FONT, command=(lambda: self._create_new_category(self.new_category.get(), self.new_category_percentage.get())))
        self.category_button.grid(row=4, column=0, pady=5)

        # Create category removal capabilities
        self.remove_category_button = tk.Button(self, text="Remove grade category", font=DEFAULT_FONT, command=(lambda: self._remove_category(self.chosen_category.get())))
        self.remove_category_button.grid(row=5, column=0, pady=5)

        # Create the field that adds new assignments
        self.assignment_name_label = tk.Label(self, text='Assignment Name', font=HEADER_FONT, bg='light grey')
        self.assignment_name_label.grid(row=0,column=1)

        self.new_assignment = tk.StringVar()
        self.assignment_name_entry = tk.Entry(self, textvariable=self.new_assignment, font=DEFAULT_FONT)
        self.assignment_name_entry.grid(row=1,column=1)

        self.assignment_score_label = tk.Label(self, text='Assignment Score (Score/Possible Score)', font=HEADER_FONT, bg='light grey')
        self.assignment_score_label.grid(row=2,column=1)

        self.new_assignment_score = tk.StringVar()
        self.assignment_score_entry = tk.Entry(self, textvariable=self.new_assignment_score, font=DEFAULT_FONT)
        self.assignment_score_entry.grid(row=3,column=1)

        self.chosen_category = tk.StringVar()
        self.chosen_category.set('Choose a Category')
        self.category_chooser = tk.OptionMenu(self, self.chosen_category, 'Choose a Category')
        self.category_chooser.config(font=DEFAULT_FONT)
        self.category_chooser.grid(row=4,column=1, pady = 10)

        self.assignment_button = tk.Button(self, text="Add new assignment", font=DEFAULT_FONT, command=(lambda: self._create_new_assignment(self.chosen_category.get(), self.new_assignment.get(), self.new_assignment_score.get())))
        self.assignment_button.grid(row=5,column=1)
            
        # Create the text box that shows all categories and assignments
        self.class_info = tk.Text(self)
        self.class_info.grid(row=6, column=0, columnspan=2, padx=15, pady=15)
        self.class_info.config(state='disabled', font=DEFAULT_FONT)

        # Create a button that allows the user to go back to the main menu
        self.back_button = tk.Button(self, text='Back', font=DEFAULT_FONT, command=(lambda: controller.show_frame(MainMenuPage)))
        self.back_button.grid(row=8,column=0, sticky='w', padx=10)

        # Create a button that allows the user to reset the calculator
        self.reset_button = tk.Button(self, text='Reset', font=DEFAULT_FONT, command=self._reset_calculator)
        self.reset_button.grid(row=8, column=1, sticky='e', padx=10)

        # Create a button that calculates the grade and creates a pop up
        self.calculate_grade_button = tk.Button(self, text='Calculate grade', font=DEFAULT_FONT, command=self._calculate_current_grade)
        self.calculate_grade_button.grid(row=7, column=1, stick='e', pady=10, padx=10)


    def _create_new_category(self, category_name, category_percentage):
        '''Adds a new category to the GradeCalculator object'''
        try:
            # Set boolean value to True
            self.can_add_assignments = True

            # Add the category to the GradeCalculator object
            self.calculator.add_category(category_name, category_percentage)

            # Clear the entries
            for entry in (self.category_name_entry, self.category_percentage_entry):
                entry.delete(0, 'end')

            # Update the text field to reflect the changes
            self.class_info.config(state='normal')
            self.class_info.delete(0.0,tk.END)
            self.class_info.insert(tk.INSERT, str(self.calculator))
            self.class_info.config(state='disabled')

            # Add the new category to the drop down menu used to add assignments
            self.category_chooser['menu'].add_command(label=category_name, command=(lambda: self.chosen_category.set(category_name)))

        # Catch exceptions raised by the GradeCalculator, show the explanation of the error and clear the entries
        except Exception as e:
            tkinter.messagebox.showerror(title='Error', message=str(e))
            for entry in (self.category_percentage_entry, self.category_name_entry):
                entry.delete(0,'end')

    def _remove_category(self, category_name):
        '''Removes a category from the GradeCalculator object'''
        try:
            # Remove the category from the GradeCalculator object
            self.calculator.remove_category(category_name)

            # Update the text field to reflect the changes
            self.class_info.config(state='normal')
            self.class_info.delete(0.0,tk.END)
            self.class_info.insert(tk.INSERT, str(self.calculator))
            self.class_info.config(state='disabled')

            # Remove category from the drop down menu
            self.category_chooser['menu'].delete(category_name)

            # Default the drop down to be "Choose a Category"
            self.chosen_category.set('Choose a Category')

        # Catch exceptions raised by the GradeCalculator, show the explanation of the error and clear the entries
        except Exception as e:
            tkinter.messagebox.showerror(title='Error', message=str(e))



    def _create_new_assignment(self, category_name, assignment_name, score):
        '''Add a new assignment to the chosen category'''
        # If there are no categories, prevent user from adding assignments
        if not self.can_add_assignments:
            tkinter.messagebox.showerror(title='Cannot add assignment', message= 'There are no categories added, so assignments cannot be added yet')
            for entry in (self.assignment_name_entry, self.assignment_score_entry):
                entry.delete(0,'end')
            return

        try:
            # Add the assignment to the GradeCalculator object
            self.calculator.add_assignment(category_name, assignment_name, score)

            # Clear the entries
            for entry in (self.assignment_name_entry, self.assignment_score_entry):
                entry.delete(0, 'end')

            # Update the text field to reflect the changes
            self.class_info.config(state='normal')
            self.class_info.delete(0.0,tk.END)
            self.class_info.insert(tk.INSERT, str(self.calculator))
            self.class_info.config(state='disabled')

        # Catch exceptions raised by the GradeCalculator, show the explanation of the error and clear the entries
        except Exception as e:
            tkinter.messagebox.showerror(title='Error', message=str(e))
            for entry in (self.assignment_name_entry, self.assignment_score_entry):
                entry.delete(0,'end')


    def _reset_calculator(self):
        '''Reinstantiates the GradeCalculator object, clears all entries, resets the boolean values, text field, and assignment chooser'''
        # Reinstantiate a GradeCalculator object
        self.calculator = GradeCalculator()

        # Clear the entries
        for entry in (self.assignment_name_entry, self.assignment_score_entry, self.category_name_entry, self.category_percentage_entry):
            entry.delete(0, 'end')

        # Reset the boolean variables
        self.can_add_assignments = False
        self.can_calculate_grade = False

        # Update the text field to reflect the changes
        self.class_info.config(state='normal')
        self.class_info.delete(0.0,tk.END)
        self.class_info.insert(tk.INSERT, str(self.calculator))
        self.class_info.config(state='disabled')

        # Reset the assignment chooser
        self.category_chooser.destroy()
        self.chosen_category = tk.StringVar()
        self.chosen_category.set('Choose a Category')
        self.category_chooser = tk.OptionMenu(self, self.chosen_category, 'Choose a Category')
        self.category_chooser.config(font=DEFAULT_FONT)
        self.category_chooser.grid(row=4,column=1, pady = 10)

    def _calculate_current_grade(self):
        '''Calculates the current grade if possible, else raises an error window to the user'''
        # Determine if a grade can be calculated
        if len(self.calculator.categories) > 0:
            self.can_calculate_grade = all([len(v[GradeCalculator.ASSIGNMENTS]) > 0 for v in self.calculator.categories.values()])

        if not self.can_calculate_grade:
            tkinter.messagebox.showerror(title='Cannot calculate grade yet', message='A category must exist before a grade can be calculated. All categories must have at least one assignment before a grade can be calculated.')
            return

        tkinter.messagebox.showinfo(title='Grade Calculator - Calculated Grade', message=f'Calculated grade for class: {self.calculator.calculate_total_grade() * 100}%')


if __name__ == '__main__':
    app = AppGUI()
    app.mainloop()
