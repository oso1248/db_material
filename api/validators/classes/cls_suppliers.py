from .. regex import regex_suppliers
from ... utils.utils import titlecase


class SupplierName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[a-zA-Z0-9\x20]{5,50}$b',
            examples='Must Be: Alphanumeric characters, 5-50 characters in length',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_suppliers.supplier_name_regex.fullmatch(v)
        if not m:
            raise ValueError('Must Be: Alphanumeric characters, 5-50 characters in length')

        converted_str = titlecase(cls(f'{m.group()}'))

        return converted_str

    def __repr__(self):
        return f'SupplierName({super().__repr__()})'