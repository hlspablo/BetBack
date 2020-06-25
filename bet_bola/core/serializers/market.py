from rest_framework import serializers
from core.models import Market
from core.serializers.cotation import StandardCotationSerializer, CotationsFromMarketSerializer


class GetGameIdListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
    
        game_id = data[1]
        data = super().to_representation(data[0])
        new_data = {
            'game_id': game_id,
            'data': data
        }
        return [new_data]

class MarketCotationSerializerWithNoCotations(serializers.HyperlinkedModelSerializer):
    #cotations = serializers.SerializerMethodField()

    class Meta:
        model = Market
        list_serializer_class = GetGameIdListSerializer
        fields = ('id','name')


class MarketCotationSerializer(serializers.HyperlinkedModelSerializer):
    cotations = serializers.SerializerMethodField()
    
    class Meta:
        model = Market
        fields = ('id','name','cotations')

    def get_cotations(self, market):
        serializer = CotationsFromMarketSerializer(market.my_cotations, many=True, context={'context':self.context})
        return serializer.data


class MarketSerializer(serializers.HyperlinkedModelSerializer):	
    my_modifications = serializers.SerializerMethodField()

    class Meta:
        model = Market
        fields = ('id','name','my_modifications')	
    
    def get_my_modifications(self, market):		
        store = self.context['request'].user.my_store
        if market.my_modifications.filter(store=store).exists():
            return {"reduction":market.my_modifications.filter(store=store).first().reduction_percentual, "available": market.my_modifications.filter(store=store).first().available, "modification_available": market.my_modifications.filter(store=store).first().modification_available}
        return {"reduction":100, "available":True, "modification_available":False}