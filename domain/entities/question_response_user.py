class QuestionResponseUser(object):
    def __init__(self, id_question_response_user = None , id_question=None,id_field = None ,id_chosen_answer = None, id_user=None, datetime_response=None,code_user_response=None):
        self.id_question_response_user = id_question_response_user
        self.code_user_response = code_user_response
        self.id_question= id_question 
        self.id_field =id_field
        self.id_user = id_user
        self.id_chosen_answer =id_chosen_answer
        self.datetime_response = datetime_response
         