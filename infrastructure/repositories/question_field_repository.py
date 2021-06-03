import sys

from domain.entities.question_field import QuestionField
from infrastructure.repositories import repository_base

class QuestionFieldRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(QuestionFieldRepository, self).__init__(db)

    def get_all(self):
        try:
            return self.session().query(QuestionField).all()
        except:
            return None

    def get_by_id_field(self, id):
        try:
            return self.session().query(QuestionField).filter_by(id_field=id).one()
        except:
            return None

    def get_by_id_question(self, id):
        try:
            return self.session().query(QuestionField).filter_by(id_question=id).one()
        except:
            return None
            


