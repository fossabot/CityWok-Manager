from citywok_ms import create_app, db
from citywok_ms.models import Employee

from sqlalchemy_utils import Country, i18n
from flask_babel import get_locale

i18n.get_locale = lambda: get_locale()

e = Employee(first_name='H', last_name='L', sex='M', nationality=None)

app = create_app()


with app.test_request_context():
    db.drop_all()
    db.create_all()
    db.session.add(e)
    db.session.commit()
    print(e)
