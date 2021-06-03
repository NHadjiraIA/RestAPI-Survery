class SubQuestion(object):
    def __init__(self, id_sub_question=None, id_question=None, level=None, id_response = None, id_chosen_answer = None, id_field = None):
        self.id_question= id_question
        self.id_sub_question = id_sub_question
        self.level = level
        self.id_response = id_response
        self.id_chosen_answer = id_chosen_answer
        self.id_field = id_field