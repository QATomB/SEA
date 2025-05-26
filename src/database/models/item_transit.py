import enum
from datetime import datetime
from sqlalchemy import Integer, Enum, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database.base_items import db

# Enum of all valid locations for items to exist in NHS Midlands remit
class Locations(enum.Enum):
    hospital1 = 1
    hospital2 = 2

    def __str__(self):
        return str(self.name)

# Item Movement model for a record of where items have been moved from and their destinations
class item_transit(db.Model):
    __tablename__ = "item_transit"
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey("item.item_id"), primary_key=True)
    move_date: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    from_loc: Mapped[Locations] = mapped_column(Enum(Locations))
    to_loc: Mapped[Locations] = mapped_column(Enum(Locations))
    employee_id: Mapped[str] = mapped_column(String, ForeignKey("employee.employee_id"))