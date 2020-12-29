import yaml

class QuestionManager():
    def __init__(self, title=""):
        self.title = title
        self.question_dict = {}

    def _get_file_name(self):
        file_name = self.title
        file_name = file_name.replace(" ","_")
        file_name = file_name.lower()
        file_name += ".yml"
        return file_name

    def load_data(self):
        if self.title:
            print(f"Loading data from 'data/{self._get_file_name()}'")
            try:
                with open(f'data/{self._get_file_name()}', 'r', encoding='utf-8') as file:
                    questions = yaml.load(file, Loader=yaml.FullLoader)
            except FileNotFoundError:
               questions = None
            if not questions:
                print("Creating new question base")
                self.question_dict = {}
                return
            self.question_dict = {el['a']: el['b'] for el in questions}

    def get_answer(self, question):
        if question[-1] == ":":
            question = question[0:-1]
        return self.question_dict.get(question, [])

    def save_answer(self, question, answer):
        if question[-1] == ":":
            question = question[0:-1]
        self.question_dict[question] = answer

    def save_data(self):
        if self.title:
            questions = [{'a': key, 'b': val} for key, val in self.question_dict.items()]
            yaml_content = yaml.dump(questions, allow_unicode=True)
            print(f"Saving data from 'data/{self._get_file_name()}'")
            with open(f'data/{self._get_file_name()}', 'w', encoding='utf-8') as file:
                file.write(yaml_content)