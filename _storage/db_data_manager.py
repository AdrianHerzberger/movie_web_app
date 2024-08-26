from .user_storage import db, User
from .data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_instance):
        self.db = db_instance
     
    def add_user(self, first_name, last_name, birth_date):
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
        )
        self.db.session.add(new_user)
        self.db.session.commit()
        
    def get_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        pass
