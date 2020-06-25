from rest_framework import serializers
from core.exceptions import NotAllowedException
from core.models import Store
from user.models import CustomUser
from utils.models import Entry


class EntrySerializer(serializers.ModelSerializer):
    creator_user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)   
    creation_date = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)             

    class Meta:
        model = Entry
        fields = ("id",'creator_user','user', 'value', 'creation_date','store')