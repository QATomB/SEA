from dataclasses import dataclass

# Class which contains the view for the dashboard, this is not a database model, rather a template
@dataclass
class DisplayTransit:
    item_id: int
    type: str
    from_loc: str
    to_loc: str
    datetime_moved: str
    overseer: str