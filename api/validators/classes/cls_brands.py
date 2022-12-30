from ... utils.utils import uppercase
from .. regex import regex_brands


class BrandName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[A-Z0-9]{4,4}$b',
            examples='Must Be: Alphanumeric characters, 4 characters in length, Uppercase Only',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        v = uppercase(v)
        m = regex_brands.brands_name_regex.fullmatch(v)
        if not m:
            raise ValueError('Must Be: Alphanumeric characters, 4 characters in length, Uppercase Only')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'BrandName({super().__repr__()})'