def get_store_price(self, store):
    from utils.models import GeneralConfigurations
    from core.models import CotationModified
    from decimal import Decimal

    config = store.my_configuration
    percentual_standard_cotation = store.percentualstandardcotation_set.first()
    cotation_modified = CotationModified.objects.filter(cotation=self, store=store, price__gt=1)
    market_reducation = self.market.my_modifications.filter(store=store, modification_available=True)
    price = self.price    
        
    if cotation_modified:
        price = cotation_modified.first().price 
    elif self.market.name == "1X2" and percentual_standard_cotation and percentual_standard_cotation.active:                
        if self.name == "Casa" and percentual_standard_cotation.home_percentual:
            price = price * percentual_standard_cotation.home_percentual / 100
        if self.name == "Empate" and percentual_standard_cotation.tie_percentual:
            price = price * percentual_standard_cotation.tie_percentual / 100
        if self.name == "Fora" and percentual_standard_cotation.away_percentual: 
            price = price * percentual_standard_cotation.away_percentual / 100        
    elif market_reducation:						        	        
        price = price * market_reducation.first().reduction_percentual / 100										
    else:        
        price = price * config.cotations_percentage / 100													
    
    if price > config.max_cotation_value:
        price = config.max_cotation_value
        
    if price < 1:
        price = 1.01
    
    return Decimal(str(price))
