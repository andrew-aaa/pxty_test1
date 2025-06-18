from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import TodoViewSet
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'app', TodoViewSet, basename='todo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framewok.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
