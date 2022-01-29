from .content_metadata import ContentMetadata
from .document_metadata import DocumentMetadata

from dataclasses import dataclass


@dataclass
class Document:
    document_metadata: DocumentMetadata
    content_metadata: ContentMetadata
    content: bytes
    pagedata: str

    def __repr__(self):
        return f'Document("{self.name}")'

    @property
    def name(self):
        return self.document_metadata.visible_name
