from django.urls import path
from django.contrib import admin
from .views import AuthAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', AuthAPIView.as_view()),
]