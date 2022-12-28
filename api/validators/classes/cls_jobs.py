from ..regex.regex_jobs import regex_jobs_jobname, regex_jobs_jobarea
from ...utils.utils import titlecase


class JobName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[a-zA-Z0-9\x20]{5,50}$',
            examples='Must Be: Alphanumeric characters, 5-50 characters in length',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_jobs_jobname.fullmatch(v)
        if not m:
            raise ValueError('Must Be: Alphanumeric characters, 5-50 characters in length')

        m = titlecase(cls(f'{m.group()}'))

        return m

    def __repr__(self):
        return f'JobName({super().__repr__()})'


class JobArea(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='\b(Brewhouse|Finishing)\b',
            examples='Must Be: Brewhouse or Finishing',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_jobs_jobarea.fullmatch(v)
        if not m:
            raise ValueError('Must Be: Brewhouse or Finishing')

        m = titlecase(cls(f'{m.group()}'))

        return m

    def __repr__(self):
        return f'JobArea({super().__repr__()})'
