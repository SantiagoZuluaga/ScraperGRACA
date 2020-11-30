import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Driver:
    def __init__(self):
        load_dotenv()
        self.email = os.environ.get('EMAIL_USER')
        self.password = os.environ.get('PASSWORD_USER')

    def LoginApplication(self):
        self.driver = webdriver.Chrome(executable_path='/home/santiago/Santiago/Proyectos/Python/Drivers/chromedriver')
        self.driver.get("https://graca.site")
        loginbutton = self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/div/div/a[1]")
        loginbutton.click()
        self.driver.implicitly_wait(10)
        emailinput = self.driver.find_element_by_xpath("//*[@id='identifierId']")
        emailinput.send_keys(self.email)
        nextbutton = self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")
        nextbutton.click()
        self.driver.implicitly_wait(10)
        passwordinput = self.driver.find_element_by_name("password")
        passwordinput.send_keys(self.password)
        nextbutton = self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")
        nextbutton.click()
        while self.driver.current_url != "https://graca.site/home#" :
            pass
        return self.driver
