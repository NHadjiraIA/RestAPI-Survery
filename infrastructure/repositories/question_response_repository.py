from domain.entities.response import Response
import sys
import json
#from domain.entities.question_response import QuestionResponse
from infrastructure.repositories import repository_base

class QuestionResponseRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(QuestionResponseRepository, self).__init__(db)

    # def get_all(self):
    #     try:
    #         return self.session().query(QuestionResponse).all()
    #     except:
    #         return None

    # def get_by_id_question(self, id):
    #     try:
    #         return self.session().query(QuestionResponse).filter_by(id_question = id).one()
             
    #     except:
    #         return None
                   
     
    def get_by_id_response(self, id):
        try:
           # return self.session().query(QuestionResponse).filter_by(id_response=id).one()
           return None
        except:
            return None
            


