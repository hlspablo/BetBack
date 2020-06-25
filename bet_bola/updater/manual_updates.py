import random
from core.models import Cotation, Game, Market
import  decimal

def insert_both_team_to_score_manually(game_id, full_time_result):
    if full_time_result:
        invalid_game = False
        results = {}
        for result in full_time_result:
            name_or_opp = result.get('name') if result.get('name') else result.get('opp')
            if name_or_opp:
                results[name_or_opp] = result['odds']
            else:
                invalid_game = True
        try:
            difference = float(results['1']) - float(results['2'])
        except ValueError:
            invalid_game = True

        if not invalid_game:
            if difference >= 8:
                yes_value = random.uniform(1.40, 1.80)
                no_value = random.uniform(1.30, 1.70)
                price_dict = {
                    'Sim': yes_value,
                    'Não': no_value
                }

                for cotation_name in ['Sim', 'Não']:
                    Cotation.objects.update_or_create(
                        name=cotation_name,
                        game=Game.objects.get(pk=game_id),
                        market=Market.objects.get_or_create(
                            name='Ambos Marcam'
                        )[0],
                        defaults={
                            'price': price_dict[cotation_name]
                        }
                    )

            else:
                yes_value = round(random.uniform(1.30, 1.70),2)
                no_value = round(random.uniform(1.30, 1.50),2)
                price_dict = {
                    'Sim': yes_value,
                    'Não': no_value
                }

                for cotation_name in ['Sim', 'Não']:
                    Cotation.objects.update_or_create(
                        name=cotation_name,
                        game=Game.objects.get(pk=game_id),
                        market=Market.objects.get_or_create(
                            name='Ambos Marcam'
                        )[0],
                        defaults={
                            'price': price_dict[cotation_name]
                        }
                    )

