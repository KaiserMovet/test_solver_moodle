import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time


from chrome_tab import ChromeTab
from moodle_solver import MoodleSolver
from auto_log import AutoLog


def case_resolve_one():
    driver = webdriver.Chrome()
    AutoLog(driver).login()
    solver = MoodleSolver(driver)
    while(True):
        print("Select quiz and hit ENTER")
        input()
        solver.start()


def _find_all_quiz_el(driver):
    el = driver.find_elements_by_class_name("modtype_quiz")
    el = [e.find_element(By.XPATH, ".//a").get_attribute('href') for e in el]
    return el


def case_analyze_answers():
    driver = webdriver.Chrome()
    AutoLog(driver).login()
    solver = MoodleSolver(driver)

    while(True):
        print("Select answers list and hit ENTER")
        input()
        solver.get_answers()


def case_resolve_all():
    driver = webdriver.Chrome()
    AutoLog(driver).login()
    solver = MoodleSolver(driver)

    while(True):
        print("Select subject and hit ENTER")
        input()
        links_list = _find_all_quiz_el(driver)
        for i, link in enumerate(links_list):
            driver.execute_script(f"window.open('');")
            # Switch to the new window and open URL B
            driver.switch_to.window(driver.window_handles[1])
            driver.get(link)
            # …Do something here
            time.sleep(1)
            solver.start()
            # Close the tab with URL B
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print(F"==== Resolved {i+1}/{len(links_list)} ====")


def main():
    mode = " " if len(sys.argv) < 1 else sys.argv[1]
    if mode == 'resolve_one':
        case_resolve_one()
    elif mode == 'resolve_all':
        case_resolve_all()
    # elif mode == 'get_ans':
    #     case_analyze_answers()
    else:
        print("Valid modes are: 'resolve_one', 'resolve_all'")


if __name__ == "__main__":
    main()
