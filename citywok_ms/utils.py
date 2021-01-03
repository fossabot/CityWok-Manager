from functools import total_ordering
from sqlalchemy_utils import Country, i18n
from sqlalchemy_utils.utils import str_coercible

SEX = [('M', 'Male'),
       ('F', 'Female')]

ID = [('passport', 'Passport'),
      ('id_card', 'ID Card'),
      ('green_card', 'Permanent Resident Card'),
      ('residence_permit', 'Residence Permit'),
      ('other', 'Other')]


@total_ordering
@str_coercible
class BlankCountry(Country):
    def __init__(self, code_or_country):
        super(BlankCountry, self).__init__(code_or_country)

    @classmethod
    def validate(self, code):
        try:
            i18n.babel.Locale('en').territories[code]
        except KeyError:
            if code == '':
                pass
            else:
                raise ValueError(
                    'Could not convert string to country code: {0}'.format(
                        code)
                )
        except AttributeError:
            # As babel is optional, we may raise an AttributeError accessing it
            pass
