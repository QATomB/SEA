import enum
from sqlalchemy import Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database.base_items import db

# Quality enum for listing the quality of an item
class Quality(enum.Enum):
    needs_replacing = 1
    ok = 2
    good = 3

    def __str__(self):
        return str(self.name)

# Item model for unique instances of types of items NHS Midlands holds
class item(db.Model):
    __tablename__ = "item"
    item_id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey("item_type.type_id"))
    condition: Mapped[Quality] = mapped_column(Enum(Quality))