from ..regex.regex_users import regex_users_name, regex_users_eid, regex_users_password
from ...utils.utils import titlecase, lowercase


class Eid(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[a-zA-Z0-9\x20]{5,8}$',
            examples='Must Be: Alphanumeric characters, 5-8 characters in length',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_users_eid.fullmatch(v)
        if not m:
            raise ValueError('Must Be: Alphanumeric characters, 5-8 characters in length')

        m = lowercase(cls(f'{m.group()}'))

        return m

    def __repr__(self):
        return f'Name({super().__repr__()})'


class Name(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[a-zA-Z0-9\x20]{3,50}$',
            examples='Must Be: Alphanumeric characters, 3-50 characters in length',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_users_name.fullmatch(v)
        if not m:
            raise ValueError('Must Be: Alphanumeric characters, 3-50 characters in length')

        m = titlecase(cls(f'{m.group()}'))

        return m

    def __repr__(self):
        return f'Name({super().__repr__()})'


class Password(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
            examples='Must Be: 8 characters minimun, Uppercase, Lowercase, Number, Special Character [#?!@$%^&*-]',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_users_password.fullmatch(v)
        if not m:
            raise ValueError('Must Be: 8 characters minimun, Uppercase, Lowercase, Number, Special Character [#?!@$%^&*-]')
        return cls(m.group())

    def __repr__(self):
        return f'Password({super().__repr__()})'
