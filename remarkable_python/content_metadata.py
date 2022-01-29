from dataclasses import dataclass, field
from typing import List

from dataclass_builder import dataclass_builder


@dataclass
class ContentMetadata:
    # Arguments that will always be present in Remarkable
    file_type: str
    orientation: str
    page_count: int
    # Arguments that can be omitted in Remarkable
    cover_page_number: int = 0
    document_metadata: dict = field(default_factory=dict)
    dummy_document: bool = False
    extra_metadata: dict = field(default_factory=dict)
    font_name: str = ''
    last_opened_page: int = 0
    line_height: int = -1
    margins: int = -1
    original_page_count: int = -1
    pages: List = None
    redirection_page_map: List = field(default_factory=list)
    size_in_bytes: int = -1
    text_alignment: str = 'justify'
    text_scale: int = 1
    transform: dict = field(default_factory=dict)

ContentMetadataBuilder = dataclass_builder(ContentMetadata)