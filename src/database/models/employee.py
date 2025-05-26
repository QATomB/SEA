from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database.base_items import db

# Employee model for valid overseers of asset movement
class employee(db.Model):
    __tablename__ = "employee"
    employee_id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)

    def __str__(self):
        return self.employee_id