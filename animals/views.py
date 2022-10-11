from functools import partial
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from .models import Animal
from .serializers import AnimalSerializer, AnimalListSerializer


class AnimalView(APIView):
    def get(self, req: Request) -> Response:
        animals = Animal.objects.all()

        if not animals:
            return Response({"detail": "Not found!"}, status.HTTP_404_NOT_FOUND)

        serializer = AnimalSerializer(animals, many=True)

        return Response(serializer.data)

    def post(self, req: Request) -> Response:
        serializer = AnimalSerializer(data=req.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class AnimalDetailView(APIView):
    def get(self, req: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)
        serializer = AnimalSerializer(animal)

        return Response(serializer.data)

    def patch(self, req: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)
        serializer = AnimalSerializer(animal, req.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except KeyError as error:
            return Response(*error.args)

        return Response(serializer.data)

    def delete(self, req: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)
        animal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
