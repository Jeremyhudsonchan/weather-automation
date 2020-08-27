import unittest
import csv
import pandas as pd
from datetime import date, timedelta

class TestResults(unittest.TestCase):
    directory_name = input("directory name of csv: ")
    file_name = input("csv file name: ")
    pathCSV = directory_name + '/' + file_name
    data = pd.read_csv(pathCSV) 
    df = pd.DataFrame(data)

    first_day_of_current_month = date.today().replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    d = last_day_of_previous_month.strftime('%d')

    def check_first_day(self):
        self.assertEqual(self.df['DAY'][0], 1)
        print("check_first_day Test Passed")

    def check_last_day(self):
        self.assertEqual(self.df['DAY'][len(self.df) - 1], int(self.d))
        print("check_last_day Test Passed")
    
    def check_first_day_min_max(self):
        self.assertLess(self.df['LOW'][0], self.df['HIGH'][0])
        print("check_first_day_min_max Test Passed")
    
    def check_last_day_min_max(self):
        self.assertLess(self.df['LOW'][len(self.df) - 1], self.df['HIGH'][len(self.df) - 1])
        print("check_last_day_min_max Test Passed")
    
    def check_number_of_days(self):
        self.assertGreater(len(self.df), 27)
        print("check_number_of_days Test Passed")

if __name__ == "__main__":
    test = TestResults()
    test.check_first_day()
    test.check_last_day()
    test.check_first_day_min_max()
    test.check_last_day_min_max()
    test.check_number_of_days()