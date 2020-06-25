from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from user.permissions import IsAdmin
from utils.serializers.percentual_standard_cotation import PercentualStandardCotationSerializer
from utils.models import PercentualStandardCotation
import json


class PercentualStandardCotationView(ModelViewSet):
    queryset = PercentualStandardCotation.objects.all()
    serializer_class = PercentualStandardCotationSerializer
    permission_classes = [IsAdmin,]

    def get_queryset(self):
        store = self.request.user.my_store
        return PercentualStandardCotation.objects.filter(store=store).order_by('store__pk')

    def create(self, validated_data):
        data = self.request.data.get('data')        
        data = json.loads(data)
        data['store'] = self.request.user.my_store.pk           
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)        	
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
