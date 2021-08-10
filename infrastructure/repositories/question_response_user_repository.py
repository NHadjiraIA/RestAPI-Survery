from marshmallow.fields import Boolean
from sqlalchemy.sql.expression import distinct
from domain.entities.response import Response
from domain.entities.question import Question
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

    def get_response_by_user_question_answer_chosen(self, id_user,id_question,id_chosen_answer,code_user_response):
        print("this is get_response_by_user_question_answer_chosen" )
        try:
            result= self.session().query(QuestionResponseUser)\
                .filter(and_(QuestionResponseUser.id_question == id_question ,QuestionResponseUser.id_chosen_answer == id_chosen_answer,QuestionResponseUser.id_user == id_user,QuestionResponseUser.code_user_response==code_user_response))
            print('This is the result')
            print(result.count())
            if(result.count() == 0):
                return None

            return result
               
        except:
            return None
      
    def get_question_by_user_with_answer_chosen(self, code_user_response):
        try:
            result= self.session().query(QuestionResponseUser.code_user_response,Question.content_question, Question.id_question, Response.id_response, ChosenAnswer.content_chosen_answer,QuestionResponseUser.id_chosen_answer).distinct()\
                .join(Question, QuestionResponseUser.id_question == Question.id_question)\
                .join(Response, Response.id_response == Question.id_response)\
                .join(ChosenAnswer, ChosenAnswer.id_response == Response.id_response)\
                .filter(and_(QuestionResponseUser.code_user_response == code_user_response))
            print('This is the result')
            print(result.count())
            if(result.count() == 0):
                return None
            
            return result
            
               
        except:
            return None
    def get_response_by_user_survery(self, id_user,id_question,code_user_response):
        print("this is get_response_by_user_question_answer_chosen" )
        try:
            result= self.session().query(QuestionResponseUser)\
                .filter(and_(QuestionResponseUser.id_question == id_question, QuestionResponseUser.id_user == id_user,QuestionResponseUser.code_user_response==code_user_response))
            if(result.count() == 0):
                print("get_response_by_user_survery")
                print(result)
                return None
            return result
        
        except:
            return None
    
    def get_response_by_user_question(self, id_user,id_question):
        print("this is get_response_by_user_question")
        try:
            result= self.session().query(QuestionResponseUser)\
                .filter(and_(QuestionResponseUser.id_user==id_user, QuestionResponseUser.id_question == id_question))
            print('This is the result')
            print(result.count())
            if(result.count() == 0):
                return None

            return result
               
        except:
            return None        
    def get_message_by_response_user(self, code_user_response):
        try:
            result = self.session().query(User.id_user, ChosenAnswer.id_chosen_answer, ChosenAnswer.id_response , ChosenAnswer.message, User.first_name_user,User.last_name_user,QuestionResponseUser.datetime_response,Field.name_field).distinct()\
                  .join(QuestionResponseUser, QuestionResponseUser.id_chosen_answer == ChosenAnswer.id_chosen_answer)\
                  .join(User, User.id_user == QuestionResponseUser.id_user )\
                  .join(SubQuestion, SubQuestion.id_question == QuestionResponseUser.id_question)\
                  .join(Field, Field.id_field == SubQuestion.id_field)\
                  .filter(QuestionResponseUser.code_user_response == code_user_response)\
                  .group_by(QuestionResponseUser.id_question)
           
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

    def Update(self, item):
        try:
            existing = self.session().query(QuestionResponseUser).filter_by(id_question_response_user=item.id_question_response_user).one()
            if existing:
                existing.id_question_response_user = item.id_question_response_user
                existing.id_question = item.id_question
                existing.id_user = item.id_user
                existing.datetime_response = item.datetime_response
                existing.id_chosen_answer = item.id_chosen_answer
                existing.code_user_response = item.code_user_response
                self.session().commit()
                return existing
            return None
        except:
            return None    


    def delete(self, id_user, id_question, userCode):
        try:
            existing = self.session().query(QuestionResponseUser)\
                .filter(and_(QuestionResponseUser.id_question == id_question, QuestionResponseUser.id_user == id_user,QuestionResponseUser.code_user_response== userCode))\
                .one()
            # self.session().query(QuestionResponseUser)\
            #     .filter(and_(QuestionResponseUser.id_user==id_user, QuestionResponseUser.id_question==id_question, QuestionResponseUser.code_user_response == userCode)).one()
            if existing:
                self.session().delete(existing)
                self.session().commit()
                return True
            return False
        except:
            return False               


    def delete_answers(self, questions, userId, surveryCode) -> Boolean:
        try:
            for question in questions:
                self.delete(userId, question, surveryCode)
            
            return True
        except:
            return False  


