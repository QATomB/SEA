from dataclasses import dataclass
from ..item import Quality

# Class which contains the view for the existing items table, this is not a database model, rather a template
@dataclass
class DisplayItem:
    item_id: int
    type_id: int
    type_name: str
    condition: Quality