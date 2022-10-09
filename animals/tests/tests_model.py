from django.test import TestCase
from animals.models import Animal
from groups.models import Group
from traits.models import Trait


class AnimalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.group_data = {"name": "cão", "scientific_name": "canis familiaris"}
        cls.group = Group.objects.create(**cls.group_data)

        cls.animal_data = {
            "name": "Logan",
            "age": 5,
            "weight": 8.5,
            "sex": "Macho",
            "group": cls.group,
        }
        cls.animal = Animal.objects.create(**cls.animal_data)

    def test_animals_atributes(self):
        animal = Animal.objects.get(id=1)
        name = Animal._meta.get_field("name").max_length
        sex = Animal._meta.get_field("sex").max_length

        self.assertEqual(name, 50)
        self.assertEqual(sex, 15)
        self.assertEqual(animal.weight, self.animal_data["weight"])
        self.assertIs(animal.age, self.animal_data["age"])
        self.assertIsInstance(self.animal, Animal)


class RelationsGroupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.animal_data = {"name": "Yoshi", "age": 9, "weight": 8.5, "sex": "Macho"}
        cls.group_data1 = {"name": "cão", "scientific_name": "canis familiaris"}
        cls.group_data2 = {"name": "gato", "scientific_name": "felis catus"}

        cls.group1 = Group.objects.create(**cls.group_data1)
        cls.group2 = Group.objects.create(**cls.group_data2)

        cls.animals = [
            Animal.objects.create(**cls.animal_data, group=cls.group1)
            for _ in range(10)
        ]

    def test_group_contain_multiple_animals(self):
        for animal in self.animals:
            animal.group = self.group1
            animal.save()

        self.assertEquals(len(self.animals), self.group1.animals.count())

        for animal in self.animals:
            self.assertIs(animal.group, self.group1)

    def test_animal_cannot_belong_to_more_than_one_group(self):
        for animal in self.animals:
            animal.group = self.group2
            animal.save()

        for animal in self.animals:
            self.assertNotIn(animal, self.group1.animals.all())
            self.assertIs(animal.group, self.group2)


class RelationsTraitTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.animal_data = {"name": "Logan", "age": 5, "weight": 8.5, "sex": "Macho"}
        cls.group_data = {"name": "cão", "scientific_name": "canis familiaris"}
        cls.trait_data = {"name": "pelo curto"}

        cls.trait = Trait.objects.create(**cls.trait_data)
        cls.group = Group.objects.create(**cls.group_data)
        cls.animals = [
            Animal.objects.create(**cls.animal_data, group=cls.group) for _ in range(10)
        ]

    def test_many_traits_for_many_animals(self):
        for animal in self.animals:
            self.trait.animals.add(animal)

        self.assertEquals(len(self.animals), self.trait.animals.count())

        for animal in self.animals:
            self.assertIn(self.trait, animal.traits.all())
