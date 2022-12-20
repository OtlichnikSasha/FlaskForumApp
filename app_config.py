from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


app = Flask(__name__)
DATABASE_CONNECTION = "mysql+mysqlconnector://root:root@localhost/forum"

# engine = create_engine("mysql+mysqlconnector://root:root@localhost/forum")


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)






