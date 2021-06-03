from domain.entities.planet import Planet


class Exemple(object):
    def __init__(self, exemple_id=None, exemple_name=None,date_report=None,planets=None):
        self.exemple_id =  exemple_id
        self.exemple_name = exemple_name
        self.date_report = date_report
        self.planets =planets
        
        