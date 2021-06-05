from flask_marshmallow import Marshmallow

from infrastructure import mappings
from infrastructure.repositories import planet_repository
from infrastructure.repositories import question_repository
from infrastructure.repositories import exemple_repository
# from infrastructure.repositories import survey_repository
from infrastructure.repositories import field_repository
from infrastructure.repositories import question_response_repository
# from infrastructure.repositories import question_survey_repository
# from infrastructure.repositories import question_field_repository 
from infrastructure.repositories import response_repository
# from infrastructure.repositories import question_response_user_repository
from infrastructure.repositories import report_repository
from infrastructure.repositories import sub_question_repository
from presentation import register_filters

class SQLContext(object):

    def __init__(self, app):
        from flask_sqlalchemy import SQLAlchemy
        from infrastructure.repositories import user_repository
        db = SQLAlchemy(app)
        mappings.init(db)
        self.db = db
        self.user_repository = user_repository.UserRepository(app, db)
        self.planet_repository = planet_repository.PlanetRepository(app, db)
        self.question_repository = question_repository.QuestionRepository(app, db)
        self.exemple_repository = exemple_repository.ExempleRepository(app, db)
        # self.survey_repository = survey_repository.SurveyRepository(app, db)
        self.field_repository = field_repository.FieldRepository(app, db)
        self.question_response_repository = question_response_repository.QuestionResponseRepository(app, db)
        # self.question_survery_repository = question_survey_repository(app, db)
        # self.question_field_repository = question_field_repository(app, db)
        self.response_repository = response_repository.ResponseRepository(app, db)
        #self.question_response_user_repository = question_response_user_repository(app, db)
        self.report_repository = report_repository.ReportRepository(app,db)
        self.sub_question_repository = sub_question_repository.SubQuestionRepository(app,db)
        register_filters(app)

    def setup(self):
        self.db.create_all()

