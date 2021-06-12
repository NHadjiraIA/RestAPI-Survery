import sys
from domain.entities.response import Response
from domain.entities.chosen_answer import ChosenAnswer
from domain.entities.question import Question
from infrastructure.repositories import repository_base
from sqlalchemy.orm import query 
from sqlalchemy import and_

class QuestionRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(QuestionRepository, self).__init__(db)

    def get_all(self):
        try:
            return self.session().query(Question).all()
        except:
            return None

    def get_by_id(self, id):
        try:
            result = self.session().query(Question.id_response, ChosenAnswer.content_chosen_answer,Question.id_question,Question.content_question,ChosenAnswer.id_chosen_answer).distinct()\
                  .join(Response, Question.id_response == Response.id_response) \
                  .join(ChosenAnswer, Response.id_response == ChosenAnswer.id_response)\
                  .filter(Question.id_question == id)

            return result
        except:
            return None

    def get_by_content(self, content):
        try:
            return self.session().query(Question).filter_by(content_question=content).one()
        except:
            return None
            


