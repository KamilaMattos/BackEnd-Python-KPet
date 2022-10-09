from django.test import TestCase
from traits.models import Trait


class TraitTestModel(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.data = {"name": "pelo longo"}
        cls.trait = Trait.objects.create(**cls.data)

    def test_traits_max_length_atribute(self):
        trait = Trait.objects.get(id=1)
        name = Trait._meta.get_field("name").max_length

        self.assertEqual(name, 20)

    def test_traits_atribute_unique(self):
        trait = Trait.objects.get(id=1)
        name = Trait._meta.get_field("name").unique

        self.assertTrue(name)
