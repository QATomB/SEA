from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from database.base_items import db
import enum

# Enum of access levels of employees of the NHS Midlands
class AccessLevel(enum.Enum):
    user = 1
    admin = 2

    def __str__(self):
        return str(self.name)

# Employee model for valid overseers of asset movement
class employee(db.Model):
    __tablename__ = "employee"
    employee_id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    def get_id(self):
        return str(self.employee_id)

    def __str__(self):
        return self.employee_id