from remarkable_python.models.index_entry import IndexEntry


class TestIndexEntry:
    def test_parse_from_string(self):
        example_index_string = 'e0057223029bce883bff3f0f1211a0a17085c85da4460e1c8c1d7b8dde044d0e:80000000:fdd46ce2-f9f9-49d1-ab99-b1b38c8694cb:4:0'
        index_entry = IndexEntry.parse_from_string(example_index_string)

        assert index_entry.path_id == 'e0057223029bce883bff3f0f1211a0a17085c85da4460e1c8c1d7b8dde044d0e'
        assert index_entry.uuid == 'fdd46ce2-f9f9-49d1-ab99-b1b38c8694cb'
        assert index_entry.subentries_amount == 4