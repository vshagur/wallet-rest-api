from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# TODO: change name and description
# created vshagur@gmail.com, 2021-06-19
schema_view = get_schema_view(
    openapi.Info(
        title="<YOU PROJECT NAME>",
        default_version='v1',
        description="<PROJECT DESCRIPTION>",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
