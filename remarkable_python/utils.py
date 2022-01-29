import re


class Utils:
    CAMEL_TO_SNAKE_FIRST_REGEX = re.compile(r'(.)([A-Z][a-z]+)')
    CAMEL_TO_SNAKE_SECOND_REGEX = re.compile(r'([a-z0-9])([A-Z])')

    @staticmethod
    def extract_file_id(file_meta_identifier):
        file_id, _other_info = file_meta_identifier.split(':', maxsplit=1)
        return file_id

    @classmethod
    def camel_to_snake_case(cls, name):
        intermediate_name = cls.CAMEL_TO_SNAKE_FIRST_REGEX.sub(r'\1_\2', name)
        return cls.CAMEL_TO_SNAKE_SECOND_REGEX.sub(r'\1_\2', intermediate_name).lower()

    @classmethod
    def dict_to_snake_case(cls, dictionary):
        return {cls.camel_to_snake_case(key): value for key, value in dictionary.items()}
