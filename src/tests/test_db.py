from sqlalchemy import URL, create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from database.base_items import Base
from database.models.item_type import item_type
from database.models.item import item, Quality
from database.models.employee import employee, AccessLevel
from database.models.item_transit import item_transit, Locations


from pytest import Session

# url = URL.create(
#     drivername="sqlite",
#     username="",
#     host="sqlite:///project.db",
#     database=""
#     )

engine = create_engine("sqlite://")
Session = sessionmaker(bind=engine)


class TestItem_type:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        self.valid_item_type = item_type(
            item_name = "Item Type 1",
            item_desc = "This is the Item Type of 1"
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_item_type_valid(self):   
        self.session.add(self.valid_item_type)
        self.session.commit()
        res = self.session.query(item_type).filter_by(item_name="Item Type 1").first()
        assert res.item_name == "Item Type 1"
        assert res.item_desc == "This is the Item Type of 1"

class TestItem:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        self.valid_item = item(
            type_id = 1,
            condition = Quality(1)
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_item_valid(self):   
        self.session.add(self.valid_item)
        self.session.commit()
        res = self.session.query(item).filter_by(item_id=1).first()
        assert res.type_id == 1
        assert res.condition == Quality.needs_replacing

class TestEmployee:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        self.valid_employee = employee(
            employee_id = "EMP123",
            name = "John Smith",
            password = generate_password_hash("Test Password 123"),
            access_level = AccessLevel(2)
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_employee_valid(self):   
        self.session.add(self.valid_employee)
        self.session.commit()
        res = self.session.query(employee).filter_by(employee_id="EMP123").first()
        assert res.employee_id == "EMP123"
        assert res.name == "John Smith"
        assert check_password_hash(res.password, "Test Password 123")
        assert res.access_level == AccessLevel.admin

class TestMovement:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        self.fixed_timestamp = datetime.now()
        self.valid_item_transit = item_transit(
            item_id = 1,
            move_date = self.fixed_timestamp,
            from_loc = Locations.Birmingham_and_Solihull_Mental_Health_NHS_Foundation_Trust,
            to_loc = Locations.Black_Country_Healthcare_NHS_Foundation_Trust,
            employee_id = "EMP123"
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_item_transit_valid(self):   
        self.session.add(self.valid_item_transit)
        self.session.commit()
        res = self.session.query(item_transit).filter(and_(item_transit.item_id==1, item_transit.move_date==self.fixed_timestamp)).first()
        assert res.item_id == 1
        assert res.move_date == self.fixed_timestamp
        assert res.from_loc == Locations.Birmingham_and_Solihull_Mental_Health_NHS_Foundation_Trust
        assert res.to_loc == Locations.Black_Country_Healthcare_NHS_Foundation_Trust
        assert res.employee_id == "EMP123"