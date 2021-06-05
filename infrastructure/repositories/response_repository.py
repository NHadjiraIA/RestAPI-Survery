from flask.globals import session
from sqlalchemy.orm import query
#from domain.entities.question_response import QuestionResponse
from domain.entities.question import Question 
import sys
import json
from domain.entities.response import Response
from infrastructure.repositories import repository_base

class ResponseRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(ResponseRepository, self).__init__(db)

    def get_all(self):
        try:
            return self.session().query(Response).all()
        except:
            return None

    def get_by_id(self, id):
        try:
            return self.session().query(Response).filter_by(id_response=id).one()
        except:
            return None
    def get_by_question_response_chosed(self,id_question,id_chosen_answer):
        try:
            # result = self.session().query(QuestionResponse.id_response, Response.content_response, Question.content_question)\
            #           .join(QuestionResponse, QuestionResponse.id_question == Question.id_question)\
            #           .join(Response, QuestionResponse.id_response == Response.id_response)\
            #           .filter(Question.id_question == id)
            return None
           
        except:
            return None    
    def get_by_content(self, content):
        try:
            return self.session().query(Response).filter_by(content_response=content).all()
        except:
            return None
            


