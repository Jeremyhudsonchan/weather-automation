from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from time import sleep
from datetime import date, timedelta
import os
import csv

class GetData():
    def __init__(self, selected_location, file_name, selected_month, data_path):
        self.file_name = file_name
        self.selected_location = selected_location
        self.selected_month = selected_month
        self.data_path = data_path
    
    def results(self):
        path = 'chromedriver/chromedriver'
        driver = webdriver.Chrome(path)
        driver.implicitly_wait(30)
        driver.get("https://weather.com/")
        sleep(5)

        location_search = driver.find_element_by_id("LocationSearch_input")

        location_search.send_keys(selected_location)
        sleep(2)
        location_search.send_keys(Keys.RETURN)
        sleep(5)

        monthly_search = driver.find_element_by_link_text("Monthly")
        sleep(3)
        monthly_search.click()
        sleep(3)

        month_selection = Select(driver.find_element_by_id("month-picker"))
        sleep(3)

        if selected_month == 'last':
            first_day_of_current_month = date.today().replace(day=1)
            last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
            default_selected_month = last_day_of_previous_month.strftime('%b %Y')
            month_selection.select_by_visible_text(default_selected_month)
            sleep(4)
        else:
            month_selection.select_by_visible_text(selected_month)
            sleep(4)

        x = driver.find_element_by_class_name("forecast-monthly__calendar")

        temp = {}
        start = False
        for i, v in enumerate(x.text.split('\n')):
            if v == '1':
                start = True
            if start:
                if i % 3 == 0:
                    if v in temp and v == '1':
                        break
                    temp[v] = {}
                else:
                    last_key = list(temp)[-1]
                    if i % 3 == 1:
                        temp[last_key]['hi'] = v[:-1]
                    else:
                        temp[last_key]['low'] = v[:-1]
        
        if not os.path.exists(data_path):
            os.makedirs(data_path)
            print("Created new directory " + data_path)
        os.chdir(data_path)
        try:
            os.remove(file_name)
        except OSError:
            pass

        with open(file_name, mode='w') as file:
            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            columns = ('DAY', 'LOW', 'HIGH')
            file_writer.writerow(columns)
            for day, t in temp.items():
                file_writer.writerow([day, t['low'], t['hi']])

        print("written to file")
        sleep(1)
        print("Ending Program")

        driver.quit()


if __name__ == "__main__":
    selected_location = input("Enter desired location (i.e. Hong Kong): ")
    selected_month = input("Enter desired month (i.e. Jul 2020): ")
    file_name = input("Enter file name (.csv format): ")
    data_path = input("Enter data storage directory: ")

    if not selected_location or not selected_month or not file_name or not data_path:
        raise ValueError ("Enter values in all fields")
    else:
        weather = GetData(selected_location, file_name, selected_month, data_path)
        weather.results()