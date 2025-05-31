import enum
from datetime import datetime
from sqlalchemy import Integer, Enum, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database.base_items import db

# Enum of all valid locations for items to exist in NHS Midlands remit
class Locations(enum.Enum):
    Birmingham_Community_Health_Care_NHS_Foundation_Trust = 1
    Birmingham_and_Solihull_Mental_Health_NHS_Foundation_Trust = 2
    Birmingham_Womens_and_Childrens_Hospitals_NHS_Foundation_Trust = 3
    The_Royal_Orthopaedic_Hospital_NHS_Foundation_Trust = 4
    University_Hospitals_Birmingham_NHS_Foundation_Trust = 5
    Black_Country_Healthcare_NHS_Foundation_Trust = 6
    Sandwell_and_West_Birmingham_Hospitals_NHS_Trust = 7
    The_Dudley_Group_NHS_Foundation_Trust = 8
    The_Royal_Wolverhampton_NHS_Trust = 9
    Walsall_Healthcare_NHS_Trust = 10
    West_Midlands_Ambulance_Service_NHS_Foundation_Trust = 11
    Coventry_and_Warwickshire_Partnership_NHS_Trust = 12
    George_Eliot_Hospital_NHS_Trust = 13
    South_Warwickshire_NHS_Foundation_Trust = 14
    University_Hospitals_Coventry_and_Warwickshire_NHS_Trust = 15
    Chesterfield_Royal_Hospital_NHS_Foundation_Trust = 16
    Derbyshire_Community_Health_Services_NHS_Foundation_Trust = 17
    Derbyshire_Healthcare_NHS_Foundation_Trust = 18
    East_Midlands_Ambulance_Service_NHS_Trust = 19
    University_Hospitals_of_Derby_and_Burton_NHS_Foundation_Trust = 20
    Herefordshire_and_Worcestershire_Health_and_Care_NHS_Trust = 21
    Worcestershire_Acute_Hospitals_NHS_Trust = 22
    Wye_Valley_NHS_Trust = 23
    Leicestershire_Partnership_NHS_Trust = 24
    University_Hospitals_of_Leicester_NHS_Trust = 25
    Lincolnshire_Community_Health_Services_NHS_Trust = 26
    Lincolnshire_Partnership_NHS_Foundation_Trust = 27
    United_Lincolnshire_Hospitals_NHS_Trust = 28
    Kettering_General_Hospital_NHS_Foundation_Trust = 29
    Northampton_General_Hospital_NHS_Trust = 30
    Northamptonshire_Healthcare_NHS_Foundation_Trusts = 31
    Nottinghamshire_Healthcare_NHS_Foundation_Trust = 32
    Nottingham_University_Hospitals_NHS_Trust = 33
    Sherwood_Forest_Hospitals_NHS_Foundation_Trust = 34
    Shrewsbury_and_Telford_Hospital_NHS_Trust = 35
    Shropshire_Community_Health_NHS_Trust = 36
    The_Robert_Jones_and_Agnes_Hunt_Orthopaedic_Hospital_NHS_Foundation_Trust = 37
    North_Staffordshire_Combined_Healthcare_NHS_Trust = 38
    Midlands_Partnership_NHS_Foundation_Trust = 39
    University_Hospitals_of_North_Midlands_NHS_Trust = 40

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