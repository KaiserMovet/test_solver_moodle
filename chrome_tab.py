from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class ChromeTab:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def get(self, url):
        self.driver.get(url)

    def click_button(self, id):
        button = self.driver.find_element_by_class_name("singlebutton quizstartbuttondiv")
        print(button)
        #button.click()

