from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.views import Verification, HomePage, UserRegistration

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation of my diploma project",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="misha.yats@gmail.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', UserRegistration.as_view(), name='register_user'),
    path('verify/', Verification.as_view(), name='user-verification'),
    path('success/', HomePage.as_view(), name='user-success'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
