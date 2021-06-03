import sys

from domain.entities.question import Question
from infrastructure.repositories import repository_base

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
            return self.session().query(Question).filter_by(id_question=id).one()
        except:
            return None

    def get_by_content(self, content):
        try:
            return self.session().query(Question).filter_by(content_question=content).one()
        except:
            return None
            


