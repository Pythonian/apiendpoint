from django.urls import path

from .views import (add_user_to_organisation, create_organisation,
                    get_organisation, get_organisations, get_user, login,
                    register)

urlpatterns = [
    path(
        "auth/register/",
        register,
        name="register",
    ),
    path(
        "auth/login/",
        login,
        name="login",
    ),
    path(
        "api/users/<str:id>/",
        get_user,
        name="get_user",
    ),
    path(
        "api/organisations/",
        get_organisations,
        name="get_organisations",
    ),
    path(
        "api/organisations/<str:orgId>/",
        get_organisation,
        name="get_organisation",
    ),
    path(
        "api/organisations/",
        create_organisation,
        name="create_organisation",
    ),
    path(
        "api/organisations/<str:orgId>/users/",
        add_user_to_organisation,
        name="add_user_to_organisation",
    ),
]
