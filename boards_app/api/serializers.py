from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from boards_app.models import Board



class BoardSerializer(serializers.ModelSerializer):
    ticket_count = serializers.SerializerMethodField(read_only=True)
    tasks_to_do_count = serializers.SerializerMethodField(read_only=True)
    tasks_high_prio_count = serializers.SerializerMethodField(read_only=True)
    member_count = serializers.SerializerMethodField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Board
        fields = [
            'id','title','members','member_count',
            'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id'
        ]
        read_only_fields = ['owner','id']

    def get_member_count(self, obj):
        return obj.members.count()
    def get_ticket_count(self, obj):
        # obj.tickets.all() 
        # funktioniert wegen related_name="tickets" im Ticket-Model
        return obj.tickets.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tickets.filter(status='todo').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tickets.filter(priority='high').count()