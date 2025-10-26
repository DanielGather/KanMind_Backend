from django.urls import path
from .views import BoardsView, BoardSingleView
# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('boards/', BoardsView.as_view(), name='boards'),
    path('boards/<int:board_id>/', BoardSingleView.as_view(), name='board-single')
]