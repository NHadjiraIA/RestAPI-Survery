from domain.entities.sub_question import SubQuestion
from domain.entities.field import Field
from domain.entities.chosen_answer import ChosenAnswer
from domain.entities.user import User
import sys
from sqlalchemy import and_
from domain.entities.question_response_user import QuestionResponseUser
from infrastructure.repositories import repository_base

class QuestionResponseUserRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(QuestionResponseUserRepository, self).__init__(db)

    def get_all(self):
        try:
            return self.session().query(QuestionResponseUser).all()
        except:
            return None

    def get_response_by_user_question_answer_chosen(self, id_user,id_question,id_chosen_answer):
        try:
            result= self.session().query(QuestionResponseUser)\
                .filter(and_(QuestionResponseUser.id_question == id_question ,QuestionResponseUser.id_chosen_answer == id_chosen_answer,QuestionResponseUser.id_user == id_user))
            print('This is the result')
            print(result.count())
            if(result.count() == 0):
                return None

            return result
               
        except:
            return None
    def get_message_by_response_user(self, id_user,id_field):
        try:
            result = self.session().query(User.id_user, ChosenAnswer.id_chosen_answer, ChosenAnswer.id_response , ChosenAnswer.message, User.first_name_user,User.last_name_user,QuestionResponseUser.datetime_response,Field.name_field).distinct()\
                  .join(QuestionResponseUser, QuestionResponseUser.id_chosen_answer == ChosenAnswer.id_chosen_answer)\
                  .join(User, User.id_user == QuestionResponseUser.id_user )\
                  .join(SubQuestion, SubQuestion.id_question == QuestionResponseUser.id_question)\
                  .join(Field, Field.id_field == SubQuestion.id_field)\
                  .filter(and_(User.id_user == id_user ,Field.id_field == id_field))\
                  .group_by(QuestionResponseUser.id_response)
           
            return result
        except:
            return None
    def get_by_id_response(self, id):
        try:
            return self.session().query(QuestionResponseUser).filter_by(id_response=id).one()
        except:
            return None
    def get_by_id_user(self, id):
        try:
            return self.session().query(QuestionResponseUser).filter_by(id_user=id).one()
        except:
            return None        
            


