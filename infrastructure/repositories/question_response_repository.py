from domain.entities.chosen_answer import ChosenAnswer
from domain.entities.question import Question
from domain.entities.response import Response
from sqlalchemy import and_
import sys
import json
#from domain.entities.question_response import QuestionResponse
from infrastructure.repositories import repository_base

class QuestionResponseRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(QuestionResponseRepository, self).__init__(db)

    # def get_all(self):
    #     try:
    #         return self.session().query(QuestionResponse).all()
    #     except:
    #         return None

    # def get_by_id_question(self, id):
    #     try:
    #         return self.session().query(QuestionResponse).filter_by(id_question = id).one()
             
    #     except:
    #         return None
                   
     
    def get_by_id_response(self, id):
        try:
           # return self.session().query(QuestionResponse).filter_by(id_response=id).one()
           return None
        except:
            return None
    def get_answerChosen_by_question(self, id_question,id_chosen_answer):
        try:
           result = self.session().query(Question.id_question, ChosenAnswer.id_chosen_answer).distinct()\
                  .join(Response, Question.id_response == Response.id_response )\
                  .join(ChosenAnswer, Response.id_response == ChosenAnswer.id_response)\
                  .filter(and_(Question.id_question == id_question ,ChosenAnswer.id_chosen_answer == id_chosen_answer))
             
           return result
        except:
            return None        
            


