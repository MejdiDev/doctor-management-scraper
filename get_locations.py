#select2 select2-container select2-container--default select2-container--above select2-container--focus

from time import sleep
from selenium import webdriver
import arabic_reshaper

import json 

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('start-maximized')

svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc, options=options)

driver.get ('https://www.med.tn/ar')
sleep(2)

def format_arabic(text):
    return arabic_reshaper.reshape(text)[::-1]

location_options_wrapper = driver.find_element(By.XPATH , "//div[@id='field_gouvernorat_doctor_main']")
location_options_wrapper.click()

location_options = location_options_wrapper.find_elements(By.TAG_NAME , "option")
res_array = []

for location in location_options:
    if(location.text != "------------------" and location.text != ""):
        res_array.append(location.text)

with open(r"C:\Users\mejdc\Desktop\doctor_management\src\data\location_data.json", "w", encoding='utf8') as outfile:
    json.dump(res_array, outfile, ensure_ascii=False)

sleep(60)
driver.close()