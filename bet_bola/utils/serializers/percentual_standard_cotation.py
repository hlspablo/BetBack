from rest_framework import serializers
from core.models import Store
from utils.models import PercentualStandardCotation, GeneralConfigurations
from utils.cache import invalidate_cache_group

class PercentualStandardCotationSerializer(serializers.HyperlinkedModelSerializer):

    store = serializers.SlugRelatedField(queryset=Store.objects.all(), slug_field='id')
    
    def create(self, validated_data):
        percentual_standard_cotation = PercentualStandardCotation.objects.filter(store=validated_data['store'])
        if percentual_standard_cotation:
            percentual_standard_cotation_instance = percentual_standard_cotation.first()
            percentual_standard_cotation_instance.home_percentual = validated_data.get('home_percentual',None)
            percentual_standard_cotation_instance.tie_percentual = validated_data.get('tie_percentual',None)
            percentual_standard_cotation_instance.away_percentual = validated_data.get('away_percentual',None)
            percentual_standard_cotation_instance.active = validated_data.get('active')
            percentual_standard_cotation_instance.save()

            invalidate_cache_group(
            [
                '/today_games/', 
                '/tomorrow_games/',
                '/after_tomorrow_games/',
                '/search_games/',
            ],
                validated_data['store'].pk
            )
            return percentual_standard_cotation_instance
        else:
            obj = PercentualStandardCotation(**validated_data)
            obj.save()

            invalidate_cache_group(
            [
                '/today_games/', 
                '/tomorrow_games/',
                '/after_tomorrow_games/',
                '/search_games/',
            ],
                validated_data['store'].pk
            )
            return obj
            
    class Meta:
        model = PercentualStandardCotation
        fields = ('id','home_percentual','tie_percentual','away_percentual','active','store')

