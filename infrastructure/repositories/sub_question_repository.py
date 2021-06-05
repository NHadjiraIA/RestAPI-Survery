from flask.globals import session
import sqlalchemy
from sqlalchemy.orm import query 
from sqlalchemy import and_
#from domain.entities.question_response import QuestionResponse
from domain.entities.question import Question 
from domain.entities.sub_question import SubQuestion
import sys
import json
from domain.entities.response import Response
from domain.entities.chosen_answer import ChosenAnswer
from infrastructure.repositories import repository_base

class SubQuestionRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(SubQuestionRepository, self).__init__(db)

    def get_all(self):
        try:
            return self.session().query(SubQuestion).all()
        except:
            return None

    def get_by_id_filed(self, id):
        try:
            return self.session().query(SubQuestion).filter_by(id_field=id).one()
        except:
            return None
    def get_by_question_response_chosed(self,id_question,id_chosen_answer):
        try:
           
          result = self.session().query(SubQuestion.id_field, ChosenAnswer.content_chosen_answer,Question.id_question,SubQuestion.id_response,Question.content_question,ChosenAnswer.id_chosen_answer).distinct()\
                  .join(Question, Question.id_question == SubQuestion.id_question )\
                  .join(Response, Question.id_response == Response.id_response) \
                  .join(ChosenAnswer, Response.id_response == ChosenAnswer.id_response)\
                  .filter(and_(SubQuestion.id_sub_question == id_question ,SubQuestion.id_chosen_answer == id_chosen_answer ,SubQuestion.id_question != SubQuestion.id_sub_question ))
           
          return result
           
        except:
            return None    
    def get_by_content(self, content):
        try:
            return self.session().query(Response).filter_by(content_response=content).all()
        except:
            return None
            


