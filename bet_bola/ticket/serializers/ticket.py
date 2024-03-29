from rest_framework import serializers
from rest_framework.response import Response
from ticket.serializers.reward import RewardSerializer, RewardSerializer
from ticket.serializers.payment import PaymentSerializerWithSeller, PaymentSerializer
from core.serializers.cotation import CotationTicketSerializer, CotationTicketWithCopiedPriceSerializer
from user.serializers.owner import OwnerSerializer
from ticket.paginations import TicketPagination
from utils.models import TicketCustomMessage
from utils.models import GeneralConfigurations
from utils import timezone as tzlocal
from ticket.models import Ticket
from user.models import TicketOwner
from user.models import CustomUser, Seller, Manager
from core.models import Store, Cotation, CotationCopy
from decimal import Decimal
import datetime
from utils.models import TicketCustomMessage


class ShowTicketSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.SlugRelatedField(read_only=True,slug_field='first_name')
    creator = serializers.SerializerMethodField()
    payment = PaymentSerializerWithSeller()
    reward = RewardSerializer()
    cotation_sum = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    cotations = serializers.SerializerMethodField()
    creation_date = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    ticket_message = serializers.SerializerMethodField()
    show_link = serializers.SerializerMethodField()
    show_league = serializers.SerializerMethodField()
    show_bonus_ticket_message = serializers.SerializerMethodField()
    bonus_ticket_value = serializers.SerializerMethodField()
    net_value_reward = serializers.SerializerMethodField()

    def get_cotations(self, data):
        serializer = CotationTicketWithCopiedPriceSerializer(data.cotations.filter(history_cotation__ticket__pk=data.pk),many=True, context={'ticket_id':data.pk})
        return serializer.data

    def get_creator(self, data):
        if data.creator:
            return {
                'name': data.creator.first_name,
                'user_type': data.creator.user_type
            }

    def get_net_value_reward(self, data):
        if data.store.my_configuration.separate_gross_and_net_value and data.store.my_configuration.bonus_won_ticket:

            return round(Decimal((( 100 - data.store.my_configuration.bonus_by_won_ticket) / 100)) * data.reward.value, 2)


    def get_ticket_message(self, data):        
        ticket_message = TicketCustomMessage.objects.filter(store=data.store).first()
        
        if ticket_message:
            return {
                'message': ticket_message.text
            }

    def get_show_league(self, data):
        return data.store.my_configuration.add_league_to_ticket_print

    def get_show_link(self, data):
        return data.store.my_configuration.add_link_to_ticket_whats
    
    def get_show_bonus_ticket_message(self, data):
        return data.store.my_configuration.bonus_won_ticket

    def get_bonus_ticket_value(self, data):
        if data.store.my_configuration.bonus_won_ticket:
            return data.store.my_configuration.bonus_by_won_ticket

    def get_cotation_sum(self, obj):
        return obj.cotation_sum()[1]
    
    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Ticket
        fields = (
            'id','ticket_id','owner','creator','cotations','show_link','show_league','show_bonus_ticket_message',
            'cotation_sum','creation_date','reward','payment','bet_value','available','status','ticket_message','bonus_ticket_value',
            'net_value_reward'
        )



class TicketSerializer(serializers.HyperlinkedModelSerializer):
    
    owner = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    payment = PaymentSerializerWithSeller()
    reward = RewardSerializer()
    cotation_sum = serializers.SerializerMethodField()
    cotations_count = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    cotations = CotationTicketSerializer(many=True)
    creation_date = serializers.DateTimeField(format='%d/%m/%Y %H:%M')


    def get_creator(self, data):
        if data.creator:
            return {
                'name': data.creator.first_name,
                'user_type': data.creator.user_type
            }

    def get_owner(self, data):
        if data.owner:
            return {
                'first_name': data.owner.first_name,
                'cellphone': data.owner.cellphone
            }

    def get_cotation_sum(self, obj):        
        return obj.cotation_sum()[1]
    
    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_cotations_count(self, obj):
        return CotationCopy.objects.filter(active=True, ticket__pk=obj.pk).count()
    class Meta:
        model = Ticket
        fields = ('id','ticket_id','owner','creator','cotations','cotation_sum','cotations_count','creation_date','reward','payment','bet_value','available','status')




class CreateTicketSerializer(serializers.HyperlinkedModelSerializer):	
    owner = OwnerSerializer()
    creation_date = serializers.DateTimeField(read_only=True)
    payment = PaymentSerializer(read_only=True)	
    reward = RewardSerializer(read_only=True)
    cotations = serializers.PrimaryKeyRelatedField(many=True, queryset=Cotation.objects.all(), required=True)

    def create(self, validated_data):
        owner_serializer = OwnerSerializer(data=validated_data.pop('owner'), context=self.context)
        owner_serializer.is_valid()
        owner = owner_serializer.save()

        cotations = validated_data.pop('cotations')		
        ticket = Ticket.objects.create(owner=owner, **validated_data)
        ticket.cotations.set(cotations)
        return ticket

    def validate(self, data):
        store_id = self.context['request'].GET.get('store')
        store = Store.objects.get(pk=store_id)
        
        user = self.context['request'].user
        if not user.is_anonymous and user.has_perm('user.be_admin'):
            raise serializers.ValidationError("Conta administradora não pode fazer aposta :)")

        if not user.is_anonymous and user.has_perm('user.be_manager'):
            raise serializers.ValidationError("Conta gerente não pode fazer aposta :)")

        try:
            config = GeneralConfigurations.objects.get(store=store)
            min_number_of_choices_per_bet = config.min_number_of_choices_per_bet
            max_number_of_choices_per_bet = config.max_number_of_choices_per_bet
            min_bet_value = config.min_bet_value
            max_bet_value = config.max_bet_value
            min_cotation_sum = config.min_cotation_sum
            max_cotation_sum = config.max_cotation_sum
            block_bets = config.block_bets
            #alert_bet_value = config.alert_bet_value

        except GeneralConfigurations.DoesNotExist:
            min_number_of_choices_per_bet = 1
            max_number_of_choices_per_bet = 1000
            min_bet_value = 0
            max_bet_value = 1000000
            min_cotation_sum = 0
            max_cotation_sum = 1000000
            block_bets = False
            #alert_bet_value = 1500
        
        if block_bets:
            raise serializers.ValidationError("A criação de Bilhetes está desligada no momento.")

        cotations_len = len(data['cotations'])
    
        cotation_mul = 1
        for cotation in data['cotations']:
            cotation_mul *= cotation.get_store_price(store)
        
        cotation_mul = 0 if cotation_mul == 1 else cotation_mul

        if cotations_len < min_number_of_choices_per_bet:
            raise serializers.ValidationError("Você deve escolher pelo menos " + str(min_number_of_choices_per_bet) + " apostas.")
        
        if cotations_len > max_number_of_choices_per_bet :
            raise serializers.ValidationError("Você deve escolher no máximo " + str(max_number_of_choices_per_bet) + " apostas.")
        
        if data['bet_value'] < min_bet_value:
            raise serializers.ValidationError("O valor mínimo para apostas é R$ " + str(min_bet_value))

        if data['bet_value'] > max_bet_value:
            raise serializers.ValidationError("O valor máximo para apostas é R$ " + str(max_bet_value))
        
        if cotation_mul < min_cotation_sum:
            raise serializers.ValidationError("O valor da cotação total deve ser maior que "+ str(min_cotation_sum))
        
        return data


    class Meta:
        model = Ticket
        fields = ('id','owner','creation_date','reward','cotations','payment','bet_value')


class TicketCustomMessageSerializer(serializers.HyperlinkedModelSerializer):

    store = serializers.SlugRelatedField(queryset = Store.objects.all(),slug_field='id')

    class Meta:
        model =  TicketCustomMessage
        fields = ('text','store')

