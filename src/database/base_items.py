from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Defauly init for base model class
class Base(DeclarativeBase):
  pass

# Initialisation of SQLAlchemy for database access
db:SQLAlchemy = SQLAlchemy(model_class=Base)