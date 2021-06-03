import sys

from domain.entities.field import Field
from infrastructure.repositories import repository_base

class FieldRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(FieldRepository, self).__init__(db)

    def get_all(self):
        try:
            return self.session().query(Field).all()
        except:
            return None

    def get_by_id(self, id):
        try:
            return self.session().query(Field).filter_by(id_field=id).one()
        except:
            return None

    def get_by_name(self, name):
        try:
            return self.session().query(Field).filter_by(name_field=name).one()
        except:
            return None

    def Update(self, item):
        try:
            existing = self.session().query(Field).filter_by(id_field=item.id_field).one()
            if existing:
                existing.name_field = item.name_field 
                self.session().commit()
                return existing
            return None
        except:
            return None

    def delete(self, id_field):
        try:
            existing = self.session().query(Field).filter_by(id_field=id_field).one()
            print('this is the existing field', existing)
            if existing:
                self.session().delete(existing)
                self.session().commit()
                return True
            return False
        except:
            return False


