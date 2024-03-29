from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
import utils.timezone as tzlocal


def toggle_availability(self):
    self.available = not self.available
    self.save()
    
    return {
        'success': True,
        'message': 'Disponibilidade Alterada.'
    }
  

def cancel_ticket(self, who_canceling):    

    if who_canceling.my_store != self.store:        
        return {
            'success': False,
            'message': 'Esse Usuário não tem permissão para cancelar Bilhetes.'
        }

    if who_canceling.has_perm('user.be_seller') and not who_canceling.seller.can_cancel_ticket:
        return {
            'success': False,
            'message': 'Esse Usuário não tem permissão para cancelar Bilhetes.'
        }
        
    elif who_canceling.has_perm('user.be_manager') and not who_canceling.manager.can_cancel_ticket:
        return {
            'success': False,
            'message': 'Esse Usuário não tem permissão para cancelar Bilhetes.'
        }
    
    if not who_canceling.user_type == 4:
        if not self.status == 0:
            return {
                'success': False,
                'message': 'Não é possível cancelar esse Bilhete '+ self.ticket_id+ ' pois o mesmo não está em aberto.'
            }
        
        if not self.payment.status == 2:
            return {
                'success': False,
                'message': 'O Bilhete '+ self.ticket_id +' não foi Pago para ser cancelado.'
            }
    
    if who_canceling.user_type == 3:
        if self.payment.date + timezone.timedelta(minutes=int(who_canceling.manager.limit_time_to_cancel)) < tzlocal.now():
            return {
                'success':False,
                'message':' Tempo limite para cancelar o Bilhete '+ self.ticket_id +' foi excedido.'
            }

    if who_canceling.user_type == 2:
        if self.payment.date + timezone.timedelta(minutes=int(who_canceling.seller.limit_time_to_cancel)) < tzlocal.now():
            return {
                'success':False,
                'message':' Tempo limite para cancelar o Bilhete '+ self.ticket_id +' foi excedido.'
            }
        
        if not who_canceling == self.payment.who_paid:
            return {
                'success':False,
                'message':'Você não pode cancelar um Bilhete que você não Pagou.'
            }
                   
    
    who_paid = self.payment.who_paid
    if who_paid.user_type == 2 and not who_paid.seller.can_sell_unlimited:
        who_paid.seller.credit_limit += self.bet_value
        who_paid.seller.save()        

    self.status = 5
    self.payment.status = 3
    self.payment.save()
    self.save()

    from history.models import TicketCancelationHistory

    TicketCancelationHistory.objects.create(
        who_cancelled=who_canceling,
        ticket=self,
        date=tzlocal.now(),
        who_paid=who_paid,
        store=self.store
    )

    return {
        'success':True,
        'message':'O Bilhete '+ self.ticket_id +' foi cancelado.'
    }

def validate_ticket(self, who_validating):
    if not who_validating.has_perm('user.be_seller') or who_validating.is_superuser or who_validating.my_store != self.store:
        return {
            'success': False,
            'message': 'Esse Usuário não tem permissão para validar bilhetes.'
        }
    
    if not self.payment.status == 0:
        return {
            'success':False,
            'message':'O Bilhete '+ self.ticket_id +' não está Aguardando Pagamento.'
        }

    if not self.status == 0:
        return {
            'success': False,
            'message': 'Não é possível validar esse Bilhete ' + self.ticket_id + ' pois o mesmo não está em aberto.'
        }

    for cotation in self.cotations.all():
        if cotation.game.start_date < tzlocal.now():
            return {
                'success': False,
                'message':'O Bilhete '+ self.ticket_id +' não pode ser pago, pois contém cotas de jogo(s) que já iniciaram.'
            }
    
    seller_before_balance = 0
    seller_after_balance= 0

    message = None
    
    if not who_validating.seller.can_sell_unlimited:        
        if self.bet_value > who_validating.seller.credit_limit:                
            message = 'Seu saldo não foi suficiente para validar esse Bilhete.'
            return {
                'success':False,
                'message': message
            }
        else:            
            seller_before_balance = who_validating.seller.credit_limit
            who_validating.seller.credit_limit -= self.bet_value
            seller_after_balance = who_validating.seller.credit_limit
            who_validating.seller.save()
            self.payment.status = 2
            self.payment.who_paid = who_validating
            self.payment.date = tzlocal.now()

            from history.models import TicketValidationHistory

            TicketValidationHistory.objects.create(
                who_validated=who_validating,
                ticket=self,
                bet_value=self.bet_value,
                date=tzlocal.now(),
                balance_before=seller_before_balance,
                balance_after=seller_after_balance,
                store=self.store
            )

    else:    
        self.payment.status = 2
        self.payment.who_paid = who_validating
        self.payment.date = tzlocal.now()    

        from history.models import TicketValidationHistory

        TicketValidationHistory.objects.create(
            who_validated=who_validating,
            ticket=self,
            bet_value=self.bet_value,
            date=tzlocal.now(),
            balance_before=seller_before_balance,
            balance_after=seller_after_balance,
            store=self.store
        ) 

    self.save()
    self.payment.save()
    
    if not message:
        message = 'Bilhete '+ self.ticket_id +' PAGO com Sucesso.'

    return {
        'success':True,
        'message': message
    }


def cotation_sum(self):
    from core.models import CotationCopy
    from utils.models import GeneralConfigurations

    valid_cotations = CotationCopy.objects.filter(ticket=self, original_cotation__game__status__in = (0,1,2,3), active=True)
    
    cotation_mul = 1
    for cotation in valid_cotations:      
        cotation_mul *= cotation.price

    if cotation_mul == 1:
        return (False, round(cotation_mul, 2))
    
    try:
        general_config = self.store.my_configuration
        max_cotation_sum = general_config.max_cotation_sum
    except GeneralConfigurations.DoesNotExist:
        max_cotation_sum = 1000000
    
    cotation_changed = False
    if cotation_mul > max_cotation_sum:
        cotation_mul = max_cotation_sum
        cotation_changed = True

    return (cotation_changed, round(cotation_mul, 2))
