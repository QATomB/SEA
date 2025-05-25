from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database.base_items import db

class item_type(db.Model):
    __tablename__ = "item_type"
    type_id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    item_name: Mapped[str] = mapped_column(String, unique=True)
    item_desc: Mapped[str] = mapped_column(String, unique=True)