from flask import Flask, render_template, flash, request, redirect, url_for
from _storage.db_data_manager import SQLiteDataManager
import os
from datetime import datetime
from _storage.user_storage import db  

app = Flask(__name__)
app.secret_key = "supersecretkey"

database_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "_data", "movies_data.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"

db.init_app(app)

data_manager = SQLiteDataManager(db)

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        first_name = request.form["firstname"]
        last_name = request.form["lastname"]
        birth_date = request.form["birthdate"]
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        
        data_manager.add_user(first_name, last_name, birth_date)
        
        flash(f"User: {first_name} {last_name} added successfully!")
        return redirect(url_for('add_user'))
        
    return render_template("add_user.html")
        
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
