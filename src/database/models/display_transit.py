from dataclasses import dataclass

@dataclass
class DisplayTransit:
    item_id: int
    type: str
    from_loc: str
    to_loc: str
    datetime_moved: str
    overseer: str