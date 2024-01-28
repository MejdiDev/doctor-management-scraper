from time import sleep
from selenium import webdriver

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

driver.get ('https://www.vaidam.com/hospitals/tunisia?page=1')
sleep(2)

data_array = []
hospital_row_elements = driver.find_elements(By.CLASS_NAME , "list-card-row")

for hospital_row in hospital_row_elements:
    res_name = ""
    res_bio = ""

    res_name = (hospital_row.find_element(By.CLASS_NAME , "primary-heading-md").text)

    bio = hospital_row.find_elements(By.CSS_SELECTOR , ".text-body.add-view-more li")
    for bio_text in bio:
        if(len(bio_text.text) > 1): res_bio += bio_text.text + "\n"

    data_array.append({
        "name": res_name,
        "bio": res_bio
    })

with open(r"C:\Users\mejdc\Desktop\doctor_management\src\data\hospital_data.json", "w", encoding='utf8') as outfile:
    json.dump(data_array, outfile, ensure_ascii=False)

sleep(60)
driver.close()