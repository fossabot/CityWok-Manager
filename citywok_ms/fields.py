import operator
import six
from sqlalchemy_utils import i18n
from sqlalchemy_utils.primitives.country import Country
from wtforms_components import SelectField
from wtforms_alchemy import CountryField
from citywok_ms.utils import BlankCountry


class BlankSelectField(SelectField):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message
        self.choices = [('', self.message)] + self.choices

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0] or None


class BlankCountryField(SelectField):
    def __init__(self, message, *args, **kwargs):
        kwargs['coerce'] = self.Coerce
        super(BlankCountryField, self).__init__(*args, **kwargs)
        self.choices = self._get_choices
        self.m = message

    def _get_choices(self):
        # Get all territories and filter out continents (3-digit code)
        # and some odd territories such as "Unknown or Invalid Region"
        # ("ZZ"), "European Union" ("QU") and "Outlying Oceania" ("QO").
        territories = [
            (code, name)
            for code, name in six.iteritems(i18n.get_locale().territories)
            if len(code) == 2 and code not in ('QO', 'QU', 'ZZ')
        ]
        return [('', self.m)] + sorted(territories, key=operator.itemgetter(1))

    @staticmethod
    def Coerce(value):
        if value == '':
            return None
        else:
            return BlankCountry(value)
