from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database.base_items import db

class employee(db.Model):
    __tablename__ = "employee"
    employee_id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)