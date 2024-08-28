from abc import ABC, abstractmethod

class DataManagerInterface(ABC): 
    @abstractmethod
    def get_user(self, user_id):
        pass
    
    @abstractmethod
    def add_user(self, first_name, last_name, birth_date):
        pass
    
    @abstractmethod
    def add_movie(self, movie_title, release_date, directory, movie_rating, user_id):
        pass

    @abstractmethod
    def add_review(self, review_text, rating, user_id, movie_id):
        pass
    
    @abstractmethod
    def update_movie(self, movie_id):
        pass
    
    @abstractmethod
    def delete_movie(self, movie_id):
        pass
