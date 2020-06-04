
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView

from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="schema-swagger-ui")),
    path("admin/", admin.site.urls, name="admin"),
    url(r'^api/', include('apps.histories.urls', namespace='histories')),
    url(r'^api/', include('apps.authentication.urls', namespace='authentication')),
    url(r'^api/', include('apps.profiles.urls', namespace='profiles')),
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
