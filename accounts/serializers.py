from rest_framework import serializers

from .models import Organisation, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "userId",
            "firstName",
            "lastName",
            "email",
            "password",
            "phone",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "firstName": {"required": True},
            "lastName": {"required": True},
            "email": {"required": True},
        }

    def create(self, validated_data):
        user = User(
            firstName=validated_data["firstName"],
            lastName=validated_data["lastName"],
            email=validated_data["email"],
            phone=validated_data.get("phone", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ["orgId", "name", "description"]
