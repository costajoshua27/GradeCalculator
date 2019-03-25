'''
Class Module for Grade Calculator
Author: Joshua Costa
Created: 3/15/19
'''

class GradeCalculator:

    # Constants for accessing 
    PERCENTAGE_OF_GRADE = 0
    ASSIGNMENTS = 1

    def __init__(self):

        # Initialize the categories dict
        self.categories = {}

    def __str__(self):

        # Create base string
        return_str = ''
        
        # Loop through all categories
        for k,v in self.categories.items():

            if len(v[GradeCalculator.ASSIGNMENTS]) == 0:
                return_str += f'{k}({v[GradeCalculator.PERCENTAGE_OF_GRADE]}%):\n'

            elif len(v[GradeCalculator.ASSIGNMENTS]) == 1:
                return_str += f'{k}({v[GradeCalculator.PERCENTAGE_OF_GRADE]}%): '
                for k,v in v[GradeCalculator.ASSIGNMENTS].items():
                    return_str += f'{k}: {v[0]}/{v[1]}\n'

            else:
                return_str += f'{k}({v[GradeCalculator.PERCENTAGE_OF_GRADE]}%): '
                for k,v in v[GradeCalculator.ASSIGNMENTS].items():
                    return_str += f'{k}: {v[0]}/{v[1]}, '
                return_str = return_str[:-2]
                return_str += '\n'

        return return_str

    def add_category(self, category_name: str, percentage_of_grade: str) -> None:
        ''' 
        Adds a new category to self.categories, with a percentage of the overall grade and name.
        If adding the category changes the total possible grade to be over 100, raises ValueError.
        If the category name already exists, raises KeyError.
        If category name is of length 0, raises AssertionError.
        If percentage of grade string is of length 0, raises AssertionError.
        If casting percentage of grade string to a float type raises an exception, raises AssertionError.
        If the percentage of grade float is equal to 0, raise AssertionError.
        '''
        assert len(category_name) > 0, f'GradeCalculator.add_category: Category name must not be an empty string'
        assert len(percentage_of_grade) > 0, f'GradeCalculator.add_category: Category percentage must not be an empty string'

        try:
            percentage_of_grade = float(percentage_of_grade)
        except:
            raise AssertionError(f'GradeCalculator.add_category: Category percentage must be an int or float')

        assert percentage_of_grade > 0, f'GradeCalculator.add_category: Category percentage must be greater than 0'

        if category_name in self.categories:
            raise KeyError(f'GradeCalculator.add_category: Category {category_name} has already been added')
        self.categories[category_name] = (percentage_of_grade, {})

        if not self._is_possible_grade_less_than_or_equal_100():
            total_percentage_too_long = self._calculate_total_possible_grade()
            del self.categories[category_name]
            raise ValueError(f'GradeCalculator.add_category: Percentage {percentage_of_grade}% of category {category_name} would make the total possible percentage {total_percentage_too_long}%, which exceeds the possible 100%')

    def remove_category(self, category_name: str) -> None:
        '''
        Removes a category from self.categories, given a category name.
        If given an invalid category_name, raises KeyError
        '''
        if category_name not in self.categories:
            raise KeyError(f"GradeCalculator.remove_category: Category '{category_name}' is not a valid key")
        del self.categories[category_name]


    def add_assignment(self, category_name: str, assignment_name: str, score: str) -> None:
        ''' 
        Adds a new assignment to a specified category, with a score and possible score.
        If category name, assignment name, or score are empty strings, raise AssertionError.
        If '/' not in the score string or the string cannot be converted to two floats, raise AssertionError.
        If an unvalid category name is not provided, raises KeyError.
        If specified assignment name exists in specified category, raises KeyError.
        '''

        assert len(category_name) > 0, f'GradeCalculator.add_assignment: Chosen category name {category_name} must not be an empty string'
        assert len(assignment_name) > 0, f'GradeCalculator.add_assignment: New assignment name {assignment_name} must not be an empty string'
        assert len(score) > 0, 'GradeCalculator.add_assignment: Given score must not be an empty string'
        assert '/' in score, 'GradeCalculator.add_assignment: Given score must be formatted as "score/possible score"'
        
        try:
            score_split = score.split('/')
            earned_score = float(score_split[0])
            possible_score = float(score_split[1])
        except:
            raise AssertionError('GradeCalculator.add_assignment: Given earned score and possible score must be of type int or float')

        if category_name not in self.categories:
            raise KeyError(f'GradeCalculator.add_assignment: Category "{category_name}" not a valid category.')

        if assignment_name in self.categories[category_name][GradeCalculator.ASSIGNMENTS]:
            raise KeyError(f'GradeCalculator.add_assignment: Assignment {assignment_name} has already been added')

        self.categories[category_name][GradeCalculator.ASSIGNMENTS][assignment_name] = (earned_score, possible_score)

    def calculate_total_grade(self) -> float or int:
        '''Calculates the total grade for the class'''
        total_grade_points = 0

        for category in self.categories:
            total_grade_points += self._calculate_category_grade(category)

        return total_grade_points/self._calculate_total_possible_grade()
            
    def _calculate_category_grade(self, category_name: str) -> float or int:
        '''Calculates the grade for a single category'''
        total = 0
        for v in self.categories[category_name][GradeCalculator.ASSIGNMENTS].values():
            total += v[0]/v[1]
        return (total / len(self.categories[category_name][GradeCalculator.ASSIGNMENTS])) * self.categories[category_name][GradeCalculator.PERCENTAGE_OF_GRADE]

    def _is_possible_grade_less_than_or_equal_100(self) -> bool:
        '''Returns a bool to determine if the total percentage exceeds 100'''
        return sum([v[GradeCalculator.PERCENTAGE_OF_GRADE] for v in self.categories.values()]) <= 100

    def _calculate_total_possible_grade(self) -> float or int:
        '''Returns the total possible percentage of the grade'''
        return sum([v[GradeCalculator.PERCENTAGE_OF_GRADE] for v in self.categories.values()])
