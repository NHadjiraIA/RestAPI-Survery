import sys

from domain.entities.exemple import Exemple
from infrastructure.repositories import repository_base

class ExempleRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(ExempleRepository, self).__init__(db)

    def get_all(self):
        try:
            return self.session().query(Exemple).all()
        except:
            return None

    def get_by_id(self, id):
        try:
            return self.session().query(Exemple).filter_by(exemple_id=id).one()
        except:
            return None