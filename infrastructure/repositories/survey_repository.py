import sys

from domain.entities.survey import Survey
from infrastructure.repositories import repository_base

class SurveyRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(SurveyRepository, self).__init__(db)

    def get_all(self):
        try:
            return self.session().query(Survey).all()
        except:
            return None

    def get_by_id(self, id):
        try:
            return self.session().query(Survey).filter_by(id_survey=id).one()
        except:
            return None

    def get_by_field(self, field):
        try:
            return self.session().query(Survey).filter_by(id_field=field).one()
        except:
            return None

    def Update(self, item):
        try:
            existing = self.session().query(Survey).filter_by(id_survey=item.id_survey).one()
            if existing:
                existing.title_survey = item.title_survey
                existing.number_questions = item.number_questions
                self.session().commit()
                return existing
            return None
        except:
            return None

    def delete(self, id_survey):
        try:
            existing = self.session().query(Survey).filter_by(id_survey=id_survey).one()
            print('this is the existing survey', existing)
            if existing:
                self.session().delete(existing)
                self.session().commit()
                return True
            return False
        except:
            return False


