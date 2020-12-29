import time
import yaml


class AutoLog():

    MOODLE_LOGIN_URL = 'https://moodle2.e-wsb.pl/login/index.php?authCAS=CAS'

    def __init__(self, driver):
        self.driver = driver

    def find_form_elements(self):
        username = self.driver.find_element_by_xpath(
            "//input[@name='username2']")
        password = self.driver.find_element_by_xpath(
            "//input[@name='password']")
        submit = self.driver.find_element_by_xpath(
            "//input[@id='login_button']")
        return username, password, submit

    @staticmethod
    def write_username_and_password(username, password):
        try:
            with open('login.yml', 'r') as file:
                parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            print("You can create file 'login.yml' with 'login'"
                  "and 'password' variables")
            print("====")
            print("Login to continue")
            return
        time.sleep(4)
        username.send_keys(parsed_yaml_file['login'])
        password.send_keys(parsed_yaml_file['password'])

    def login(self):
        self.driver.get(self.MOODLE_LOGIN_URL)
        username, password, submit = self.find_form_elements()
        self.write_username_and_password(username, password)
        submit.click()
        time.sleep(10)
