from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .serializers import BoardSerializer
from boards_app.models import Board
from django.db.models import Q
from rest_framework.exceptions import NotFound

User = get_user_model()

class BoardsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request):
        """
        Gibt alle Boards zurück, in denen der User 
        entweder Owner oder Mitglied ist.
        """
        user = request.user
        
        # Finde alle Boards, wo der User Owner IST ODER als Member eingetragen ist
        boards = Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()
        
        # Serialisiere die *Liste* von Boards (wichtig: many=True)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)









class BoardSingleView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, board_id):
        """
        Holt die Details für ein einzelnes Board.
        """
        try:
            # Hole das Board ODER wirf einen 404-Fehler
            # Bonus: Stelle sicher, dass der User Zugriff hat
            board = Board.objects.get(id=board_id, owner=request.user) 
            
            serializer = BoardSerializer(board) # many=True wird hier NICHT benötigt
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Board.DoesNotExist:
            # Gibt eine saubere 404-Meldung zurück
            raise NotFound(detail="Board not found or no permission")
    def delete (self, request, board_id=None):
        try:
            print(request.user)
            board = Board.objects.get(pk=board_id, owner=request.user)
            board.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)