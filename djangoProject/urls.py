from django.urls import path, include
from django.contrib import admin
from .views import UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', UserViewSet.as_view(), name='student-list'),
    path('v1/', include('dj_rest_auth.urls')),
]