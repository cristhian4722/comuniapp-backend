from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="ComuniApp API",
      default_version='v1',
      description="Backend API documentation for ComuniApp. Supports User Registration, JWT authentication, and user profile management.",
      contact=openapi.Contact(email="admin@comuniapp.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),
    
    # Authentication App APIs (Register, Login/Token, Refresh, Profile)
    path('api/auth/', include('authentication.urls')),
    
    # Emprendedores App APIs (Categories, Services, Requests, Reviews)
    path('api/emprendedores/', include('emprendedores.urls')),
    
    # API Documentation (Swagger and ReDoc)
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

