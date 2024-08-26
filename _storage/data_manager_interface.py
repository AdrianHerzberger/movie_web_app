from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass
    
    @abstractmethod
    def add_user(self, first_name, last_name, birth_date):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass