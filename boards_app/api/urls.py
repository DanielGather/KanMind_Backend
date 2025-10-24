from django.urls import path
from .views import BoardsView
# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('boards/', BoardsView.as_view(), name='boards')
]