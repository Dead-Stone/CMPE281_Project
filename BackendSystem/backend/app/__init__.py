from flask import Flask
from .database import init_mysql_db
from .mongodb import init_mongo_db

# Initialize the Flask app
app = Flask(__name__)

# Load the configuration
app.config.from_object('app.config.Config')

# Initialize MySQL and MongoDB
init_mysql_db(app)
init_mongo_db()

# Import routes
from . import routes
