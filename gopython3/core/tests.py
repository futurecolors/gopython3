from django.test import TestCase
from core.util import parse


class SpecParserTest(TestCase):

    def test_spec_parser(self):
        incoming_requirements = "django==1.4.3\ndjango-storages"

        self.assertEqual(parse(incoming_requirements),
                         [('django', '1.4.3'),
                          ('django-storages', None)])
