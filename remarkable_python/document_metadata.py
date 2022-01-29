from dataclasses import dataclass

from dataclass_builder import dataclass_builder


@dataclass
class DocumentMetadata:
    """
    Class that represents the metadata of a document existing in the Remarkable cloud
    """
    deleted: bool
    last_modified: str
    last_opened: str
    last_opened_page: int
    metadata_modified: bool
    modified: bool
    parent: str
    pinned: bool
    synced: bool
    version: int
    visible_name: str

DocumentMetadataBuilder = dataclass_builder(DocumentMetadata)
