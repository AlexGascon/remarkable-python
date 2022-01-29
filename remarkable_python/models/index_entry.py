from __future__ import annotations
from dataclasses import dataclass


@dataclass
class IndexEntry:
    path_id: str
    uuid: str
    subentries_amount: int

    FIELD_SEPARATOR = ':'

    @classmethod
    def parse_from_string(cls, index_entry_string: str) -> IndexEntry:
        path_id, _, uuid, subentries_amount, _size = index_entry_string.split(cls.FIELD_SEPARATOR)
        return cls(path_id, uuid, int(subentries_amount))

    def __str__(self):
        return f'IndexEntry({self.path_id})'
