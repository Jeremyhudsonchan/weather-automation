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

class GetMonthlyTemperature():
    def __init__(self, file_name, selected_location):
        self.file_name = file_name
        self.selected_location = selected_location
    
    def results(self):
        path = 'drivers/chromedriver'
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
        first_day_of_current_month = date.today().replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        d = last_day_of_previous_month.strftime('%b %Y')
        month_selection.select_by_visible_text(d)
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
    file_name = input("Enter file name(csv): ")
    selected_location = input("Enter desired location: ")

    try:
        os.remove(file_name)
    except OSError:
        pass

    print("run")
    
    weather = GetMonthlyTemperature(file_name, selected_location)
    weather.results()