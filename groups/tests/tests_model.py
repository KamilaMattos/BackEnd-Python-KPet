from django.test import TestCase
from groups.models import Group


class GroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.data = {"name": "cão", "scientific_name": "canis familiaris"}
        cls.group = Group.objects.create(**cls.data)

    def test_group_max_length_atributes(self):
        group = Group.objects.get(id=1)
        name = Group._meta.get_field("name").max_length
        scientific_name = Group._meta.get_field("scientific_name").max_length

        self.assertEqual(name, 20)
        self.assertEqual(scientific_name, 20)

    def test_group_atribute_unique(self):
        group = Group.objects.get(id=1)
        name = group._meta.get_field("name").unique
        scientific_name = group._meta.get_field("scientific_name").unique

        self.assertTrue(name)
        self.assertTrue(scientific_name)
