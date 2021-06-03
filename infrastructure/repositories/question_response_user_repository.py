import sys

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

    def get_by_id_question(self, id):
        try:
            return self.session().query(QuestionResponseUser).filter_by(id_question=id).one()
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
            


