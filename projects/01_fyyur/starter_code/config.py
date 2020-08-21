import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI ="postgres://wtufwwks:JM9TJYtSDFIdBXi7Y9XYl78PRD7dPK5a@kandula.db.elephantsql.com:5432/wtufwwks"
SQLALCHEMY_DATABASE_URI = '"postgres://root:YouMayPass@localhost:5432/Fyyr";'
