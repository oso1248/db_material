from ..regex.regex_universial import regex_note, regex_phone
from ... utils.utils import convert_phone_number, titlecase, strip_non_numeric


class Note(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[a-zA-Z0-9,.\x20]{0,256}$',
            examples='Must Be: Alphanumeric characters + ,. | 5-256 characters in length',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not v:
            return v
        m = regex_note.fullmatch(v)
        if not m:
            raise ValueError('Must Be: Alphanumeric characters, [,.], 5-256 characters in length')

        converted_str = titlecase(cls(f'{m.group()}'))
        return converted_str

    def __repr__(self):
        return f'Note({super().__repr__()})'


class PhoneNumber(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[0-9]{10}$b',
            examples='Must Be: Numeric Characters, 10 Digits',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        v = strip_non_numeric(v)
        m = regex_phone.fullmatch(v)
        if not m:
            raise ValueError('Must Be: Numeric Characters, 10 Digits')

        converted_str = convert_phone_number(cls(f'{m.group()}'))

        return converted_str

    def __repr__(self):
        return f'PhoneNumber({super().__repr__()})'