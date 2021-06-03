import sys

from domain.entities.report import Report
from infrastructure.repositories import repository_base

class ReportRepository(repository_base.RepositoryBase):
    def __init__(self, app, db):
        super(ReportRepository, self).__init__(db)

    def get_all(self):
        try:
            return self.session().query(Report).all()
        except:
            return None

    def get_by_id(self, id):
        try:
            return self.session().query(Report).filter_by(id_report=id).one()
        except:
            return None

    def get_by_date(self, date):
        try:
            return self.session().query(Report).filter_by(date_report=date).one()
        except:
            return None
            


