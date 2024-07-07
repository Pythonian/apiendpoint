import uuid

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Organisation, User
from .serializers import OrganisationSerializer, UserSerializer


@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            # Create default organization
            org_name = f"{user.firstName}'s Organisation"
            org = Organisation.objects.create(
                orgId=str(uuid.uuid4()),
                name=org_name,
                description="Default organisation",
            )
            org.users.add(user)
            org.save()

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "status": "success",
                    "message": "Registration successful",
                    "data": {
                        "accessToken": str(refresh.access_token),
                        "user": UserSerializer(user).data,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception:
            return Response(
                {
                    "status": "Bad request",
                    "message": "Registration unsuccessful",
                    "statusCode": 400,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        errors = [
            {"field": field, "message": error[0]}
            for field, error in serializer.errors.items()
        ]
        return Response(
            {"errors": errors},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, email=email, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": UserSerializer(user).data,
                },
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401,
        },
        status=status.HTTP_401_UNAUTHORIZED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    try:
        user = User.objects.get(userId=id)
        if (
            user == request.user
            or request.user.organisations.filter(users=user).exists()
        ):
            return Response(
                {
                    "status": "success",
                    "message": "User retrieved successfully",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": "Forbidden",
                "message": "You do not have permission to view this user",
                "statusCode": 403,
            },
            status=status.HTTP_403_FORBIDDEN,
        )
    except User.DoesNotExist:
        return Response(
            {
                "status": "Not found",
                "message": "User not found",
                "statusCode": 404,
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_organisations(request):
    organisations = request.user.organisations.all()
    if not organisations:
        return Response(
            {
                "status": "Not Found",
                "message": "No organisations found for the user",
                "statusCode": status.HTTP_404_NOT_FOUND,
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = OrganisationSerializer(organisations, many=True)
    return Response(
        {
            "status": "success",
            "message": "Organisations retrieved successfully",
            "data": {"organisations": serializer.data},
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_organisation(request, orgId):
    try:
        organisation = Organisation.objects.get(orgId=orgId)
        if request.user in organisation.users.all():
            serializer = OrganisationSerializer(organisation)
            return Response(
                {
                    "status": "success",
                    "message": "Organisation retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": "Unauthorized",
                "message": "You do not have access to this organisation",
                "statusCode": 403,
            },
            status=status.HTTP_403_FORBIDDEN,
        )
    except Organisation.DoesNotExist:
        return Response(
            {
                "status": "Not found",
                "message": "Organisation not found",
                "statusCode": 404,
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_organisation(request):
    serializer = OrganisationSerializer(data=request.data)
    if serializer.is_valid():
        organisation = serializer.save(orgId=str(uuid.uuid4()))
        organisation.users.add(request.user)
        organisation.save()
        return Response(
            {
                "status": "success",
                "message": "Organisation created successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {
            "status": "Bad Request",
            "message": "Client error",
            "errors": serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def add_user_to_organisation(request, orgId):
#     try:
#         organisation = Organisation.objects.get(orgId=orgId)
#         user = User.objects.get(userId=request.data.get("userId"))
#         if request.user in organisation.users.all():
#             organisation.users.add(user)
#             organisation.save()
#             return Response(
#                 {
#                     "status": "success",
#                     "message": "User added to organisation successfully",
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         return Response(
#             {
#                 "status": "Unauthorized",
#                 "message": "You do not have access to this organisation",
#                 "statusCode": 403,
#             },
#             status=status.HTTP_403_FORBIDDEN,
#         )
#     except Organisation.DoesNotExist:
#         return Response(
#             {
#                 "status": "Not found",
#                 "message": "Organisation not found",
#                 "statusCode": 404,
#             },
#             status=status.HTTP_404_NOT_FOUND,
#         )
#     except User.DoesNotExist:
#         return Response(
#             {
#                 "status": "Not found",
#                 "message": "User not found",
#                 "statusCode": 404,
#             },
#             status=status.HTTP_404_NOT_FOUND,
#         )


@api_view(["POST"])
def add_user_to_organisation(request, orgId):
    organisation = get_object_or_404(Organisation, orgId=orgId)
    user = get_object_or_404(User, userId=request.data.get("userId"))
    organisation.users.add(user)
    organisation.save()
    return Response(
        {
            "status": "success",
            "message": "User added to organisation successfully",
        },
        status=status.HTTP_200_OK,
    )
