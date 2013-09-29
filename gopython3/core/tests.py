from django.test import TestCase
from core.util import parse_requirements


class SpecParserTest(TestCase):

    def test_spec_parser(self):
        incoming_requirements = "django==1.4.3\ndjango-storages"

        self.assertEqual(parse_requirements(incoming_requirements),
                         [('django', '1.4.3'),
                          ('django-storages', None)])
