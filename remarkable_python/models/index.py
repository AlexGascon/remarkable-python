# Required to use own class in type hints
from __future__ import annotations

from .index_entry import IndexEntry

from dataclasses import dataclass
from enum import Enum
from typing import List, Union


@dataclass
class Index:
    index_entries: List[IndexEntry]

    @classmethod
    def parse_from_content(cls, index_content):
        _control_digit, *index_files = index_content.split()

        return cls([IndexEntry.parse_from_string(index_file) for index_file in index_files])

    def __getitem__(self, position) -> Union[Index, IndexEntry]:
        if type(position) == slice:
            return Index(self.index_entries[position])
        
        return self.index_entries[position]

    def __len__(self):
        return len(self.index_entries)

    def __iter__(self):
        return iter(self.index_entries)

    def __repr__(self):
        return f'Index({", ".join(ie.path_id for ie in self.index_entries)})'
        
    @property
    def content_type(self):
        if all(index_entry.subentries_amount == 0 for index_entry in self.index_entries):
            return self.ContentType.FILE
        else:
            return self.ContentType.DIRECTORY

    class ContentType(Enum):
        FILE = 'file'
        DIRECTORY = 'directory'
    