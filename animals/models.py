import math
from django.db import models


class SexAnimal(models.TextChoices):
    MALE = "Macho"
    FEMALE = "Fêmea"
    OTHER = "Não informado  "


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=15, choices=SexAnimal.choices, default=SexAnimal.OTHER
    )
    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="animals"
    )
    traits = models.ManyToManyField("traits.Trait", related_name="animals")

    def get_age_in_human_years(self) -> str:
        human_age = 16 * int(math.log(self.age)) + 31
        return f"O seu pet {self.name} tem {human_age} anos humanos!"
