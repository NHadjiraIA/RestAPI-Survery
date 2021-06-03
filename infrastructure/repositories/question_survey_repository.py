import sys

from domain.entities.question_survey import QuestionSurvey
from infrastructure.repositories import repository_base

class QuestionSurveyRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(QuestionSurveyRepository, self).__init__(db)

    def get_all(self):
        try:
            return self.session().query(QuestionSurvey).all()
        except:
            return None

    def get_by_id_survery(self, id):
        try:
            return self.session().query(QuestionSurvey).filter_by(id_survery=id).one()
        except:
            return None


            


