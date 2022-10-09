import math
from rest_framework import serializers
from .models import Animal, SexAnimal
from groups.models import Group
from groups.serializers import GroupSerializer
from traits.models import Trait
from traits.serializers import TraitSerializer


class AnimalListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexAnimal.choices,
        default=SexAnimal.OTHER,
    )
    group = GroupSerializer(many=False)
    traits = TraitSerializer(many=True)


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexAnimal.choices,
        default=SexAnimal.OTHER,
    )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
    age_in_human_years = serializers.SerializerMethodField()
    
    def get_age_in_human_years(self, obj):
        human_age = 16 * math.log(obj.age) + 31
        return round(human_age)

    def create(self, validated_data: dict) -> Animal:
        group_data = validated_data.pop("group")
        traits_data = validated_data.pop("traits")

        group, created = Group.objects.get_or_create(**group_data)
        animal = Animal.objects.create(**validated_data, group=group)

        for new_trait in traits_data:
            trait, created = Trait.objects.get_or_create(**new_trait)
            animal.traits.add(trait)

        return animal

    def update(self, instance: Animal, validated_data: dict) -> Animal:
        not_updatable_key = ["group", "traits", "sex"]
        errors = []

        for key, value in validated_data.items():
            if key in not_updatable_key:
                errors.append({key: f"You can not update {key} property!"})
            else:
                setattr(instance, key, value)

        if errors:
            raise KeyError(errors, 422)

        instance.save()

        return instance
