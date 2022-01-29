from remarkable_python.models.index import Index
from remarkable_python.models.index_entry import IndexEntry


class TestIndex:
    def test_parse_from_content(self):
        expected_first_entry = IndexEntry(
            path_id='9df9fffd3a6f79c4b50f6231cf9e1e75e21b376545cc87ee388354d96fbc8b0a',
            uuid='fdd46ce2-f9f9-49d1-ab99-b1b38c8694cb.content',
            subentries_amount=0
        )
        expected_second_entry = IndexEntry(
            path_id='5694afbb7fcacc45cf8eb8eb43acbbc4cf592034ec8883951cd14a5a79dcd526',
            uuid='fdd46ce2-f9f9-49d1-ab99-b1b38c8694cb.metadata',
            subentries_amount=0
        )
        expected_third_entry = IndexEntry(
            path_id='c4dba5fe446a2047940c869b5b075528207bff65f0cf688c9b37bcc32fdd430d',
            uuid='fdd46ce2-f9f9-49d1-ab99-b1b38c8694cb.pagedata',
            subentries_amount=0
        )
        expected_fourth_entry = IndexEntry(
            path_id='5953ab24adfc6aa1858c3501a29ab0156246fd733f6f5d3401032742e70c7686',
            uuid='fdd46ce2-f9f9-49d1-ab99-b1b38c8694cb.pdf',
            subentries_amount=0
        )

        content = open('test/data/file_index.txt', 'r').read()
        index = Index.parse_from_content(content)

        assert len(index) == 4
        assert index[0] == expected_first_entry
        assert index[1] == expected_second_entry
        assert index[2] == expected_third_entry
        assert index[3] == expected_fourth_entry

    def test_content_type_for_file(self):
        content = open('test/data/file_index.txt', 'r').read()
        index = Index.parse_from_content(content)

        assert index.content_type == Index.ContentType.FILE

    def test_content_type_for_directory(self):
        content = open('test/data/directory_index.txt', 'r').read()
        index = Index.parse_from_content(content)

        assert index.content_type == Index.ContentType.DIRECTORY

    def test_get_for_single_item_returns_index_entry(self):
        content = open('test/data/directory_index.txt', 'r').read()
        index = Index.parse_from_content(content)

        assert type(index[0]) == IndexEntry
    
    def test_get_for_single_item_returns_correct_element(self):
        expected_entry = IndexEntry(
            path_id='9df9fffd3a6f79c4b50f6231cf9e1e75e21b376545cc87ee388354d96fbc8b0a',
            uuid='fdd46ce2-f9f9-49d1-ab99-b1b38c8694cb.content',
            subentries_amount=0
        )
        index = Index.parse_from_content(open('test/data/file_index.txt', 'r').read())

        assert index[0] == expected_entry

    def test_get_with_slice_returns_index(self):
        content = open('test/data/file_index.txt', 'r').read()
        index = Index.parse_from_content(content)

        subindex = index[0:4]
        assert type(subindex) == Index

    def test_get_with_slice_returns_correct_elements(self):
        expected_first_entry = IndexEntry(
            path_id='9df9fffd3a6f79c4b50f6231cf9e1e75e21b376545cc87ee388354d96fbc8b0a',
            uuid='fdd46ce2-f9f9-49d1-ab99-b1b38c8694cb.content',
            subentries_amount=0
        )
        expected_second_entry = IndexEntry(
            path_id='5694afbb7fcacc45cf8eb8eb43acbbc4cf592034ec8883951cd14a5a79dcd526',
            uuid='fdd46ce2-f9f9-49d1-ab99-b1b38c8694cb.metadata',
            subentries_amount=0
        )

        index = Index.parse_from_content(open('test/data/file_index.txt', 'r').read())
        subindex = index[0:2]

        assert len(subindex) == 2
        assert subindex[0] == expected_first_entry
        assert subindex[1] == expected_second_entry



