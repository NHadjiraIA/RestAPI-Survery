from domain.entities.user import User
from infrastructure.repositories import repository_base


class UserRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(UserRepository, self).__init__(db)

    def get_all(self):
        try:
            print("in user repo")
            return self.session().query(User).all()
        except:
            return None

    def get_by_id(self, id):
        try:
            return self.session().query(User).filter_by(id_user=id).one()
        except:
            return None

    def get_by_email(self, email):
        try:
            return self.session().query(User).filter_by(email_user=email).one()
        except:
            return None



    def get_by_username(self, first_name):
        try:
            return self.session().query(User).filter_by(first_name_user=first_name).one()
        except:
            return None

    def Update(self, item):
        try:
            existing = self.session().query(User).filter_by(id_user=item.id_user).one()
            if existing:
                existing.id_user = item.id_user
                existing.first_name_user = item.first_name_user
                existing.last_name_user = item.last_name_user
                existing.email_user = item.email_user
                existing.password_user = item.password_user
                self.session().commit()
                return existing
            return None
        except:
            return None

    def delete(self, id):
        try:
            existing = self.session().query(User).filter_by(id_user=id).one()
            if existing:
                self.session().delete(existing)
                self.session().commit()
                return True
            return False
        except:
            return False
