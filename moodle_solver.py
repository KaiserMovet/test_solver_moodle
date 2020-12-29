from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
from question_manager import QuestionManager


class MoodleSolver:
    def __init__(self, driver):
        self.driver = driver

    def _validate_start(self):
        i = 5
        while i:
            try:
                self.driver.find_element_by_class_name('quizstartbuttondiv')
                self.driver.find_element_by_xpath("//button[@type='submit']")
            except NoSuchElementException:
                i -= 1
                time.sleep(1)
            else:
                return True
        return False

    def _analyze_questions(self, qm, save_all=False):
        question_list = [el.get_attribute(
            'innerHTML') for el in self.driver.find_elements_by_class_name('qtext')]
        answers_list = [el.get_attribute(
            'innerHTML') for el in self.driver.find_elements_by_class_name('rightanswer')]
        answer_status = [el.get_attribute(
            'innerHTML') for el in self.driver.find_elements_by_class_name('state')]

        all_questions_correct = True
        for status in answer_status:
            if "Poprawnie" not in status:
                all_questions_correct = False
                break
        if not save_all and all_questions_correct:
            return True
        for question, answer in zip(question_list, answers_list):
            answers = answer.split(':')[-1]
            qm.save_answer(question, answers)
        return False

    def _validate_question_site(self):
        i = 3
        while i:
            try:
                self.driver.find_element_by_id('page-mod-quiz-attempt')
                self.driver.find_element_by_xpath("//input[@type='submit']")
            except NoSuchElementException:
                i -= 1
                time.sleep(1)
            else:
                return True
        return False

    def _answer_current_question(self, qm):
        question_name = self.driver.find_element_by_class_name(
            'qtext').get_attribute('innerHTML')
        answer = qm.get_answer(question_name)

        all_questions_was_answered = True

        # Answer question
        if answer and all_questions_was_answered:
            possible_answers = [el.get_attribute(
                'innerHTML') for el in self.driver.find_elements_by_class_name('flex-fill')]
            el_to_choose = []
            # Get radio and checkbox elements to click
            el_to_choose += self.driver.find_elements_by_xpath(
                "//div[@class='answer']//input")
            if not el_to_choose:
                1 / 0
            print(f"Answer to:")
            print(f"  {question_name}")
            time.sleep(1)
            for el, pos_ans in zip(el_to_choose, possible_answers):
                if pos_ans in answer:
                    print(f"  - {pos_ans}")
                    action = ActionChains(self.driver)
                    action.move_to_element(el).perform()
                    self._click(el)
        else:
            all_questions_was_answered = False

    def _answer_questions(self, qm):
        while True:
            if not self._validate_question_site():
                break
            time.sleep(1)
            self._answer_current_question(qm)
            # Next Question
            self._click(self.driver.find_elements_by_xpath(
                "//input[@type='submit']")[-1])

    def _start_quiz_loop(self):
        title = self.driver.find_element_by_class_name(
            "page-title").get_attribute('innerHTML').split('-')[0].strip()
        qm = QuestionManager(title)
        qm.load_data()
        while True:
            # Start quiz
            self._click(self.driver.find_element_by_xpath(
                "//button[@type='submit']"))
            # Main question loop
            self._answer_questions(qm)
            # Submit
            time.sleep(1)
            self._click(self.driver.find_elements_by_xpath(
                "//button[@type='submit']")[-1])
            time.sleep(1)
            self._click(self.driver.find_elements_by_xpath(
                "//input[@type='button']")[0])
            time.sleep(1)
            # Analyze questions
            status = self._analyze_questions(qm)
            self._click(self.driver.find_elements_by_xpath(
                "//a[@class='mod_quiz-next-nav']")[-1])
            if status:
                # If success
                qm.save_data()
                print("Quiz was resolved!")
                break

    def _click(self, el):
        time.sleep(1)
        action = ActionChains(self.driver)
        action.move_to_element(el).perform()
        el.click()

    def start(self):
        if not self._validate_start():
            print("You open the wrong site")
            return False
        else:
            print("Correct site was picked")
        self._start_quiz_loop()

    # def get_answers(self):
    #     title = self.driver.find_element_by_class_name(
    #         "page-title").get_attribute('innerHTML').split('-')[0].strip()
    #     qm = QuestionManager(title)
    #     qm.load_data()
    #     self._analyze_questions(qm, save_all=True)
    #     qm.save_data()
    #     print("Answers was saved!")
