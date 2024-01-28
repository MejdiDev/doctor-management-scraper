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

def get_options():
    driver.get ('https://www.med.tn/ar')
    sleep(2)

    driver.find_element(By.XPATH , "//span[@class='selection']").click()
    return driver.find_elements(By.XPATH , "//li[@class='select2-results__option']")

def format_arabic(text):
    return arabic_reshaper.reshape(text)[::-1]

doctor_options = get_options()
json_res = {}

for i in range(len(doctor_options)):
    if(i != 0):
        doctor_options = get_options()

    element = doctor_options[i]
    res_spec = element.text

    if(len(res_spec) < 30): 

        element.click()
        driver.find_element(By.XPATH , "//a[@class='button button-search-submit pfsearch']").click()
        sleep(2)

        data_array = []
        doctor_card_elements = driver.find_elements(By.XPATH , "//div[@class='card-doctor-block ']")
        for doctor_card in doctor_card_elements:
            res_name = ""
            res_bio = ""

            res_name = (doctor_card.find_element(By.CLASS_NAME , "list__label--name").text)
            res_location = (doctor_card.find_element(By.CLASS_NAME , "list__label--adr").text)

            res_img = (doctor_card.find_element(By.TAG_NAME , "img").get_attribute("src"))
            res_img = res_img[res_img.rfind('https'):]

            bio = doctor_card.find_elements(By.CLASS_NAME , "list__bio")
            if(len(bio) > 0):
                res_bio = (bio[0].text)

            data_array.append({
                "img": res_img,
                "name": res_name, #format_arabic(res_name)[::-1],
                "bio": res_bio, #format_arabic(res_bio)[::-1]
                "location": res_location
            })

        if(i == 0): json_res[res_spec[:res_spec.find("\n")]] = data_array
        else: json_res[res_spec] = data_array

        with open(r"C:\Users\mejdc\Desktop\doctor_management\src\data\doctor_data.json", "w", encoding='utf8') as outfile:
            json.dump(json_res, outfile, ensure_ascii=False)

sleep(60)
driver.close()