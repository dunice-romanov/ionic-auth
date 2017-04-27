from django.conf.urls import url, include
from django.contrib import admin

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from users import views 

router = routers.DefaultRouter()
router.register(r'users', views.UsersViewSet)

urlpatterns = [
    url('^', include(router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),
]
