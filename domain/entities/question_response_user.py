class QuestionResponseUser(object):
    def __init__(self, id_question_response_user = None , id_question=None,id_field = None, id_response=None,id_chosen_answer = None, id_user=None, date_reponse=None,hour_response=None):
        self.id_question_response_user = id_question_response_user
        self.id_question= id_question
        self.id_response = id_response
        self.id_field =id_field
        self.id_user = id_user
        self.id_chosen_answer =id_chosen_answer
        self.date_reponse = date_reponse
        self.hour_response = hour_response