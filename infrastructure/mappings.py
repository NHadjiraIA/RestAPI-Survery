from datetime import datetime
from sqlalchemy.sql.sqltypes import DateTime
from infrastructure.repositories.report_repository import ReportRepository
from domain.entities.question_response_user import QuestionResponseUser
from infrastructure.repositories.question_field_repository import QuestionFieldRepository
from sqlalchemy import String
from sqlalchemy.orm import backref, relationship
from domain.entities.planet import Planet
from domain.entities.user import User
from domain.entities.exemple import Exemple
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from domain.entities.survey import Survey
from domain.entities.question import Question
from domain.entities.field import Field
# from domain.entities.question_survey import QuestionSurvey
from domain.entities.response import Response
from domain.entities.report import Report
from domain.entities.sub_question import SubQuestion
from domain.entities.chosen_answer import ChosenAnswer
from domain.entities.question_response_user import QuestionResponseUser
 
def init(db):
    user_mapping = db.Table('users',
                            db.Column('id_user', db.Integer, primary_key=True),
                            db.Column('first_name_user', db.String(50)),
                            db.Column('last_name_user', db.String(50)),
                            db.Column('email_user', db.String(100)),
                            db.Column('password_user', db.String(100))
                            #db.Column(db.Integer, db.ForeignKey('id_report'), nullable=False),
                            #questions = db.relationship("question_response_user", back_populates="users"),
                            #question_id = db.Column(db.Integer, db.ForeignKey("question_id"), nullable=False)
                           # responses = db.relationship("question_response_user", back_populates="users")
                            )

    planet_mapping = db.Table('planets',
                            db.Column('planet_id', db.Integer, primary_key=True),
                            db.Column('planet_name', db.String(50)),
                            db.Column('planet_type', db.String(50)),
                            db.Column('home_star', db.String(50)),
                            db.Column('mass', db.Float),
                            db.Column('radius', db.Float),
                            db.Column('distance', db.Float)
                           # db.Column('exemple_id', db.Integer, db.ForeignKey("exemples.exemple_id"))
                            #db.Column('exemple_id',db.Integer, db.ForeignKey('exemple_id'))
                           # db.Column('exemple_id',db.Integer, db.ForeignKey('exemple_id'), nullable=False)                                                     
                            )
 
    question_mapping = db.Table('questions',
                           db.Column('id_question',db.Integer,primary_key=True),
                           db.Column('content_question', db.Text(60)),
                           db.Column('id_response',db.Integer,db.ForeignKey('responses.id_response'))
                           #db.relationship("responses", secondary="questions_response", backref=db.backref("responsess", lazy ="dynamic"))
   #                           surverys = db.relationship("question_survery", back_populates="questions"),
   #                           fileds = db.relationship("question_field", back_populates="questions"),
   #                           users = db.relationship("question_response_user", back_populates="questions")
                            )
    sub_question_mapping = db.Table('sub_questions',
                            db.Column('id',db.Integer,primary_key=True),
                            db.Column('id_question',db.Integer,db.ForeignKey('questions.id_question'), primary_key=True),
                            db.Column('id_sub_question',db.Integer),
                            db.Column('level',db.Integer),
                            db.Column('id_response',db.Integer,db.ForeignKey('responses.id_response')),
                            db.Column('id_field',db.Integer,db.ForeignKey('fields.id_field')),
                            db.Column('id_chosen_answer',db.Integer,db.ForeignKey('chosenAnswers.id_chosen_answer'))
                            )                         
    exemple_mapping = db.Table('exemples',
                                db.Column('exemple_id', db.Integer, primary_key=True),
                                db.Column('exemple_name', db.String(50)),
                                db.Column('date_report', db.Date)
                              #  # db.relationship("planets",
                              #       primaryjoin="and_(exemples.exemples_id==planets.exemples_id, "
                              #     "planets.planet_name=='Earth')")
                                   #db.relationship('planets', backref='exemple', lazy=True)
                                #db.Column(db.Integer, db.ForeignKey('id_field'), nullable=False),                        
                                #db.relationship('planets', backref='exemple')
    )
                            
    survey_mapping = db.Table('surveys',
                             db.Column('id_survey', db.Integer, primary_key=True),
                             db.Column('number_questions', db.Integer),
                             db.Column('title_suvery', db.String(50))
                            # db.Column('id_field',db.Integer, db.ForeignKey('id_field'), nullable=False)
                             #questions = db.relationship("question_survery", back_populates="surveys")
                             )
                             
    field_mapping = db.Table('fields',
                             db.Column('id_field', db.Integer, primary_key=True),
                             db.Column('name_field', db.String(50)),
                             db.Column('id_question',db.Integer,db.ForeignKey('questions.id_question'))
                            )                         
       
    question_response_mapping = db.Table('questions_response',
                            db.Column('id_question',db.Integer,db.ForeignKey('questions.id_question'), primary_key=True),
                            db.Column('id_response',db.Integer,db.ForeignKey('responses.id_response'), primary_key=True)
                            )    

   #  question_survery_mapping = db.Table('questions_survery',
   #                          db.Column('id_question',db.Integer,db.ForeignKey('id_question'), primary_key=True),
   #                          db.Column('id_survery',db.Integer,db.ForeignKey('id_survery'), primary_key=True)
   #                          )  
   #  question_field_mapping = db.Table('questions_field',
   #                          db.Column('id_question',db.Integer,db.ForeignKey('id_question'), primary_key=True),
   #                          db.Column('id_field',db.Integer,db.ForeignKey('id_field'), primary_key=True)
   #                          )                        
    responses_mapping = db.Table('responses',
                             db.Column('id_response',db.Integer,primary_key=True),
                             db.Column('content_response', db.String(50))
                            #  question = db.relationship("question_response_user", back_populates="responses"),
                            #  users = db.relationship("question_response_user", back_populates="responses")
                             
    )
    chosenAnswer_mapping = db.Table('chosenAnswers', 
                            db.Column('id_chosen_answer',db.Integer,primary_key=True),
                            db.Column('content_chosen_answer', db.String(50)),
                            db.Column('title_chosen_answer', db.String(50)),
                            db.Column('message', db.String(50)),
                            db.Column('id_response',db.Integer,db.ForeignKey('responses.id_response'))
                            

    )
    question_response_user_mapping = db.Table('questionsResponseUser',    
                            db.Column('id_question_response_user',db.Integer,primary_key=True),                            
                            db.Column('id_question',db.Integer,db.ForeignKey('questions.id_question')),
                            db.Column('id_response',db.Integer,db.ForeignKey('responses.id_response')),
                            db.Column('id_user',db.Integer,db.ForeignKey('users.id_user')),
                            db.Column('id_chosen_answer',db.Integer,db.ForeignKey('chosenAnswers.id_chosen_answer')),
                            db.Column('datetime_response', db.DateTime)
                            ) 
    report_mapping = db.Table('reports',
                            db.Column('id_report',db.Integer,primary_key=True),
                            db.Column('title_report', db.String(50)),
                            db.Column('content_report', db.String(50)),
                            db.Column('date_report', db.Date),
                            db.Column('id_user',db.Integer,db.ForeignKey('users.id_user'))
                             )
    db.mapper(User, user_mapping)
    db.mapper(Planet, planet_mapping)   
    db.mapper(Question, question_mapping)
    db.mapper(Exemple, exemple_mapping)
    db.mapper(Survey, survey_mapping)
    db.mapper(Field, field_mapping)
    db.mapper(Response, responses_mapping)
    db.mapper(SubQuestion,sub_question_mapping)
    db.mapper(ChosenAnswer,chosenAnswer_mapping)
    db.mapper(QuestionResponseUser, question_response_user_mapping)
   #  db.mapper(QuestionSurvey, question_survery_mapping)
   #  db.mapper(QuestionFieldRepository, question_field_mapping)
   #  db.mapper(QuestionResponseUser, question_response_user_mapping)
    db.mapper(Report, report_mapping)