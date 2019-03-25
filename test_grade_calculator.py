'''
Unittest Module for Grade Calculator
Author: Joshua Costa
Created: 3/15/19
'''

import unittest
from grade_calculator import GradeCalculator

class Test_Calculator(unittest.TestCase):
    def setUp(self):
        self.calculator = GradeCalculator()

    def test_add_category(self):
        self.calculator.add_category('Homework', '20')
        new_categories = {'Homework': (20, {})}
        self.assertEqual(self.calculator.categories, new_categories)

    def test_add_category_too_large(self):
        self.calculator.add_category('Homework', '20')
        self.calculator.add_category('Tests', '80')
        new_categories = {'Homework': (20, {}), 'Tests': (80, {})}
        self.assertEqual(self.calculator.categories, new_categories)
        self.assertRaises(ValueError, self.calculator.add_category, 'Quizzes', '10')

    def test_add_first_category_too_large(self):
        new_calculator = GradeCalculator()
        self.assertRaises(ValueError, new_calculator.add_category, 'Tests', '101')
        self.assertEqual(new_calculator.categories, {})

    def test_add_assignment(self):
        self.calculator.add_category('Homework', '20')
        self.calculator.add_assignment('Homework', 'Homework #1', '15/20')
        new_categories = {'Homework': (20, {'Homework #1': (15, 20)})}
        self.assertEqual(self.calculator.categories, new_categories)
        self.calculator.add_assignment('Homework', 'Homework #2', '20/20')
        new_categories = {'Homework': (20, {'Homework #1': (15, 20), 'Homework #2': (20, 20)})}
        self.assertEqual(self.calculator.categories, new_categories)

    def test_add_assignment_wrong_category(self):
        self.calculator.add_category('Homework', '20')
        self.assertRaises(KeyError, self.calculator.add_assignment, 'Tests', 'Homework #1', '40/50')

    def test_calculate_category_grade(self):
        self.calculator.add_category('Homework', '20')
        self.calculator.add_assignment('Homework', 'Homework #1', '15/20')
        self.calculator.add_assignment('Homework', 'Homework #2', '20/20')
        self.assertEqual(self.calculator._calculate_category_grade('Homework'), 17.5)

    def test_calculate_total_grade(self):
        self.calculator.add_category('Homework', '20')
        self.calculator.add_assignment('Homework', 'Homework #1', '15/20')
        self.calculator.add_assignment('Homework', 'Homework #2', '20/20')
        self.calculator.add_category('Tests', '80')
        self.calculator.add_assignment('Tests', 'Test #1', '97/100')
        self.calculator.add_assignment('Tests', 'Test #2', '87/100')
        self.assertEqual(self.calculator._calculate_category_grade('Homework'), 17.5)
        self.assertEqual(self.calculator._calculate_category_grade('Tests'), 73.6)
        self.assertAlmostEqual(self.calculator.calculate_total_grade(), .911)

    def test_remove_category(self):
        self.calculator.add_category('Homework','20')
        self.calculator.add_category('Tests','80')
        self.assertEqual(self.calculator.categories, {'Homework': (20, {}), 'Tests': (80, {})})
        self.assertRaises(KeyError, self.calculator.remove_category, 'Quizzes')
        self.calculator.remove_category('Tests')
        self.assertEqual(self.calculator.categories, {'Homework': (20, {})})
        self.calculator.remove_category('Homework')
        self.assertEqual(self.calculator.categories, {})
        
