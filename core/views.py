from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Person
from .serializers import PersonSerializer


class UserExistsAlready(Exception):
    pass


@api_view(["POST"])
def create_user(request):
    if request.method == "POST":
        user_name = request.data.get("name")

        try:
            Person(name=user_name).full_clean()
        except ValidationError as e:
            return Response(
                {"error": f"Validation Error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if not Person.objects.filter(name=user_name).exists():
                user = Person.objects.create(name=user_name)
                serializer = PersonSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise UserExistsAlready
        except UserExistsAlready:
            return Response(
                {"error": f"user {user_name} already exists"},
                status=status.HTTP_409_CONFLICT,
            )


@api_view(["GET", "PUT", "DELETE"])
def get_user(request, user_id):
    try:
        user = Person.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return Response(
            {"error": f"User with ID {user_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = PersonSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        user.delete()
        return Response({"message": f"User with ID {user_id} deleted"}, status=200)
    elif request.method == "PUT":
        new_name = request.data.get("name", user.name)
        if not new_name:
            return Response(
                {"error": "Name cannot be empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.name = new_name
        try:
            user.save()
            serializer = PersonSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response(
                {"error": f"IntegrityError: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["GET", "POST", "PUT", "DELETE"])
def get_user_name(request, name):
    try:
        user = Person.objects.get(name=name)
    except ObjectDoesNotExist:
        user = None

    if request.method == "GET":
        if user:
            serializer = PersonSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": f"The User {name} was not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    elif request.method == "POST":
        # Create a new user with the specified name
        try:
            if user:
                raise UserExistsAlready
            else:
                user = Person.objects.create(name=name)
                serializer = PersonSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except UserExistsAlready:
            return Response(
                {"error": f"User {name} already exists"},
                status=status.HTTP_409_CONFLICT,
            )
        except IntegrityError as e:
            return Response(
                {"error": f"IntegrityError: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    elif request.method == "PUT":
        if not user:
            return Response(
                {"error": f"The User {name} was not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_name = request.data.get("name", user.name)
        if not new_name:
            return Response(
                {"error": "Name cannot be empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.name = new_name
        try:
            user.save()
            serializer = PersonSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response(
                {"error": f"IntegrityError: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    elif request.method == "DELETE":
        if not user:
            return Response(
                {"error": f"The User {name} was not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user.delete()
        return Response(
            {"message": f"The User {name} has been deleted"},
            status=status.HTTP_200_OK,
        )
