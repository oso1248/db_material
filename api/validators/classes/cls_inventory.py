from ... utils.utils import uppercase, strip_non_alphanumeric, convert_brew_number, lowercase
from .. regex import regex_inventory


class LastBrew(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[A-Z0-9]{4,4} [0-9]{5,5}$',
            examples='Must Be: LLNN NNNNN',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        v = uppercase(v)
        v = strip_non_alphanumeric(v)
        v = convert_brew_number(v)
        m = regex_inventory.inv_last_brews_regex.fullmatch(v)
        if not m:
            raise ValueError('Must Be: LLNN NNNNN')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'LastBrew({super().__repr__()})'


class HopLot(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='[^A-Za-z0-9]$',
            examples='Must Be: Alphanumeric only',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        v = lowercase(v)
        v = strip_non_alphanumeric(v)
        m = regex_inventory.inv_hop_lot_regex.fullmatch(v)
        if not m:
            raise ValueError('Must Be: Alphanumeric only')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'HopLot({super().__repr__()})'
