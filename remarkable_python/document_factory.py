from .client import Client
from .content_metadata import ContentMetadataBuilder
from .document import Document
from .document_metadata import DocumentMetadataBuilder
from .models.index import Index
from .utils import Utils

import json


class DocumentFactory:
    CONTENT_METADATA_SUFFIX = '.content'
    DOCUMENT_METADATA_SUFFIX = '.metadata'
    DOCUMENT_CONTENT_SUFFIX = '.pdf'
    PAGEDATA_SUFFIX = '.pagedata'
    

    def __init__(self, client: Client, index: Index):
        self.client = client
        self.index = index
    
    def create(self):
        self._validate_index()

        return Document(
            document_metadata=self._create_document_metadata(),
            content_metadata=self._create_content_metadata(),
            pagedata=self.client.get_file(self._find_entry_by_suffix(self.PAGEDATA_SUFFIX).path_id),
            content=self.client.get_file_bin(self._find_entry_by_suffix(self.DOCUMENT_CONTENT_SUFFIX).path_id)
        )

    def _validate_index(self):
        if self.index.content_type != Index.ContentType.FILE:
            raise Exception("Index does not represent a document")

    def _create_content_metadata(self):
        content_metadata_entry = self._find_entry_by_suffix(self.CONTENT_METADATA_SUFFIX)
        content_metadata_content = self.client.get_file(content_metadata_entry.path_id)
        content_metadata_dict = json.loads(content_metadata_content)
        content_metadata_dict_in_snake_case = Utils.dict_to_snake_case(content_metadata_dict)

        return ContentMetadataBuilder(**content_metadata_dict_in_snake_case).build()

    def _create_document_metadata(self):
        document_metadata_entry = self._find_entry_by_suffix(self.DOCUMENT_METADATA_SUFFIX)
        document_metadata_content = self.client.get_file(document_metadata_entry.path_id)
        document_metadata_dict = json.loads(document_metadata_content)
        document_metadata_dict_in_snake_case = Utils.dict_to_snake_case(document_metadata_dict)

        # This key is represented by remarkable as 'metadatamodified'
        # As it's not in Camel Case it's not converted by the Utils function,
        # So we need to convert it manually and delete the incorrect entry
        document_metadata_dict_in_snake_case['metadata_modified'] = document_metadata_dict_in_snake_case['metadatamodified']
        del document_metadata_dict_in_snake_case['metadatamodified']

        # We already know it's a document, so we don't include this key in the model
        del document_metadata_dict_in_snake_case['type']

        return DocumentMetadataBuilder(**document_metadata_dict_in_snake_case).build()

    def _find_entry_by_suffix(self, suffix):
        wanted_entry = [entry for entry in self.index if entry.uuid.lower().endswith(suffix)][0]
        return wanted_entry