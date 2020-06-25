from core.models import Cotation, Game, Market
from .market_translations import MARKET_TRANSLATIONS
import re
import decimal
from django.core.exceptions import MultipleObjectsReturned

def translate_cotation(cotation_name):
    TRANSLATE_TABLE = {
        '1':'Casa',
        '2':'Fora',
        'X':'Empate',
        '1X':'Casa/Empate',
        'X2':'Empate/Fora',
        '12':'Casa/Fora',
        'Draw': 'Empate',
        'No Goal': 'Sem Gols',
        'No': 'Não',
        'Yes': 'Sim',
        'Over': 'Acima',
        'Under': 'Abaixo',
        'Even': 'Par',
        'Odd':'Ímpar',
        '1st Half': '1° Tempo',
        '2nd Half': '2° Tempo',
        'Tie':'Igual',
        'Both Teams':'Ambos os Times',
        'Only':'Apenas',

    }
    
    cotation_translated = cotation_name.strip()
    for header in TRANSLATE_TABLE.keys():
        cotation_translated = re.sub('\\b' + header + '\\b', TRANSLATE_TABLE.get(header, header), cotation_translated)
    return cotation_translated.strip()


def get_translated_cotation_with_header_name_special(cotation_name):
    TRANSLATE_TABLE = {
        '1': 'Casa',
        '2': 'Fora',
        'Home': 'Casa',
        'Away': 'Fora',
        'To Win to Nil':'Ganhar sem tomar Gol',
        'To Win Either Half': 'Ganhar Qualquer Etapa',
        'To Win Both Halves': 'Ganhar Ambas Etapas',
        'To Score in Both Halves': 'Marcar em Ambas Etapas'
    }

    cotation_translated = cotation_name.strip()
    for header in TRANSLATE_TABLE.keys():
        cotation_translated = re.sub('\\b' + header + '\\b', TRANSLATE_TABLE.get(header, header), cotation_translated)
    return cotation_translated.strip()


def partial_translate_cotation(cotation_name):
    TRANSLATE_TABLE = {
        'Over': 'Acima',
        'Under': 'Abaixo',
        'Draw': 'Empate'
    }
    
    cotation_translated = cotation_name.strip()
    for header in TRANSLATE_TABLE.keys():
        cotation_translated = re.sub('\\b' + header + '\\b', TRANSLATE_TABLE.get(header, header), cotation_translated)
    return cotation_translated.strip()


def goals_translate_cotation(cotation_name):
    TRANSLATE_TABLE = {
        'Goal': 'Gol',
        'Goals': 'Gols',
        'Over': 'Acima',
        'Under': 'Abaixo',
        'Yes': 'Sim',
        'No': 'Não',
        'Draw': 'Empate'
    }
    
    cotation_translated = cotation_name.strip()
    for header in TRANSLATE_TABLE.keys():
        cotation_translated = re.sub('\\b' + header + '\\b', TRANSLATE_TABLE.get(header, header), cotation_translated)
    return cotation_translated.strip()


def goals_translate_cotation_wm(cotation_name):
    TRANSLATE_TABLE = {
        '1': 'Casa',
        '2': 'Fora'
    }
    
    cotation_translated = cotation_name.strip()
    for header in TRANSLATE_TABLE.keys():
        cotation_translated = re.sub('\\b' + header + '\\b', TRANSLATE_TABLE.get(header, header), cotation_translated)
    return cotation_translated.strip()


def extract_goals_from_string(string):
    total_goals = re.findall(r"[-+]?\d*\.\d+|\d+", string)
    return total_goals[-1] if total_goals else None


def cotation_with_extract_goals_from_name_and_name_translation(cotations, market_name, game_id):
    
    for cotation in cotations:
        if str.strip(cotation.get('odds', '')) and str.strip(cotation.get('name', '')):
            try:
                price = decimal.Decimal(cotation.get('odds', ''))
            except decimal.InvalidOperation:
                price = 1

            total_goals = extract_goals_from_string(cotation.get('name', ''))
            if total_goals:
                Cotation.objects.update_or_create(
                    name=goals_translate_cotation(cotation.get('name', '')),
                    game=Game.objects.get(pk=game_id),
                    market=Market.objects.get_or_create(
                        name=MARKET_TRANSLATIONS.get(market_name, market_name)
                    )[0],
                    defaults={
                        'price': price,
                        'total_goals': total_goals
                    }
                )


def cotation_with_extract_goals_from_name_and_header_translation_wm(cotations, market_name, game_id):
    
    for cotation in cotations:
        if str.strip(cotation.get('odds', '')) and str.strip(cotation.get('name', '')) and str.strip(cotation.get('header', '')):
            try:
                price = decimal.Decimal(cotation.get('odds', ''))
            except decimal.InvalidOperation:
                price = 1

            total_goals = extract_goals_from_string(cotation.get('name', ''))
            if total_goals:
                Cotation.objects.update_or_create(
                    name=goals_translate_cotation_wm(cotation.get('header', '')) + ' ' + cotation.get('name', ''),
                    game=Game.objects.get(pk=game_id),
                    market=Market.objects.get_or_create(
                        name=MARKET_TRANSLATIONS.get(market_name, market_name)
                    )[0],
                    defaults={
                        'price': price,
                        'total_goals': total_goals
                    }
                )


def cotation_with_extract_goals_from_name_and_header_translation(cotations, market_name, game_id):
    
    for cotation in cotations:
        if str.strip(cotation.get('odds', '')) and str.strip(cotation.get('name', '')) and str.strip(cotation.get('header', '')):
            try:
                price = decimal.Decimal(cotation.get('odds', ''))
            except decimal.InvalidOperation:
                price = 1

            total_goals = extract_goals_from_string(cotation.get('name', ''))
            if total_goals:
                Cotation.objects.update_or_create(
                    name=goals_translate_cotation(cotation.get('header', '')) + ' ' + cotation.get('name', ''),
                    game=Game.objects.get(pk=game_id),
                    market=Market.objects.get_or_create(
                        name=MARKET_TRANSLATIONS.get(market_name, market_name)
                    )[0],
                    defaults={
                        'price': price,
                        'total_goals': total_goals
                    }
                )



def cotation_with_header_name_special(cotations, market_name, game_id):
    allowed = ('To Win to Nil','To Win Either Half','To Win Both Halves','To Score in Both Halves')
    for cotation in cotations:
        if str.strip(cotation.get('odds', '')) and str.strip(cotation.get('header', '')) and str.strip(cotation.get('name', '')):
            try:
                price = decimal.Decimal(cotation.get('odds', ''))
            except decimal.InvalidOperation:
                price = 1

            if cotation.get('name', '') in allowed:
                Cotation.objects.update_or_create(
                    name=get_translated_cotation_with_header_name_special(cotation.get('header', '') + ' - ' + cotation.get('name', '')),
                    game=Game.objects.get(pk=game_id),
                    market=Market.objects.get_or_create(
                        name=MARKET_TRANSLATIONS.get(market_name, market_name),
                    )[0],
                    defaults={
                        'price': price
                    }
                )

def cotation_without_translation(cotations, market_name, game_id):
    for cotation in cotations:
        if str.strip(cotation.get('odds', '')) and str.strip(cotation.get('name', '')):
            try:
                price = decimal.Decimal(cotation.get('odds', ''))
            except decimal.InvalidOperation:
                price = 1
            
                Cotation.objects.update_or_create(
                    name=cotation['name'],
                    game=Game.objects.get(pk=game_id),
                    market=Market.objects.get_or_create(
                        name=MARKET_TRANSLATIONS.get(market_name, market_name)
                    )[0],
                    defaults={
                        'price': price
                    }
                )


def cotation_with_translatable_header_and_name(cotations, market_name, game_id):
    for cotation in cotations:
        if str.strip(cotation.get('odds', '')) and str.strip(cotation.get('header', '')) and str.strip(cotation.get('name', '')):
            try:
                price = decimal.Decimal(cotation.get('odds', ''))
            except decimal.InvalidOperation:
                price = 1

            Cotation.objects.update_or_create(
                name=translate_cotation(cotation['header'] + ' - ' + cotation['name']),
                game=Game.objects.get(pk=game_id),
                market=Market.objects.get_or_create(
                    name=MARKET_TRANSLATIONS.get(market_name, market_name),
                )[0],
                defaults={
                    'price': price
                }
            )

def cotation_with_translatable_header(cotations, market_name, game_id):
    for cotation in cotations:
        if str.strip(cotation.get('odds', '')) and str.strip(cotation.get('header', '')) and str.strip(cotation.get('name', '')):
            try:
                price = decimal.Decimal(cotation.get('odds', ''))
            except decimal.InvalidOperation:
                price = 1

            Cotation.objects.update_or_create(
                name=translate_cotation(cotation.get('header', '')) + ' ' + cotation.get('name', ''),
                game=Game.objects.get(pk=game_id),
                market=Market.objects.get_or_create(
                    name=MARKET_TRANSLATIONS.get(market_name, market_name),
                )[0],
                defaults={
                    'price': price
                }
            )


def cotation_correct_score(cotations, market_name, game_id):
    for cotation in cotations:
        if str.strip(cotation.get('odds', '')) and str.strip(cotation.get('header', '')) and str.strip(cotation.get('name', '')):
            try:
                price = decimal.Decimal(cotation.get('odds', ''))
            except decimal.InvalidOperation:
                price = 1
            
            score = cotation['name'].strip()
            if cotation['header'].strip() == "2":
                score = score.split('-')
                score = str(score[1]) + '-' + str(score[0])

            Cotation.objects.update_or_create(
                name=score,
                game=Game.objects.get(pk=game_id),
                market=Market.objects.get_or_create(
                    name=MARKET_TRANSLATIONS.get(market_name, market_name),
                )[0],
                defaults={
                    'price': price
                }
            )


def cotation_with_translatable_name(cotations, market_name, game_id):

    for cotation in cotations:
        if str.strip(cotation.get('odds', '')) and str.strip(cotation.get('name', '')):
            try:
                price = decimal.Decimal(cotation.get('odds', ''))
            except decimal.InvalidOperation:
                price = 1

            Cotation.objects.update_or_create(
                name=translate_cotation(cotation.get('name', '')),
                game=Game.objects.get(pk=game_id),
                market=Market.objects.get_or_create(
                    name=MARKET_TRANSLATIONS.get(market_name, market_name)
                )[0],
                defaults={
                    'price': price
                }
            )


def cotation_with_partial_translatable_name(cotations, market_name, game_id):
    
    for cotation in cotations:
        if str.strip(cotation.get('odds', '')) and str.strip(cotation.get('name', '')):
            try:
                price = decimal.Decimal(cotation.get('odds', ''))
            except decimal.InvalidOperation:
                price = 1

            Cotation.objects.update_or_create(
                name=partial_translate_cotation(cotation.get('name', '')),
                game=Game.objects.get(pk=game_id),
                market=Market.objects.get_or_create(
                    name=MARKET_TRANSLATIONS.get(market_name, market_name)
                )[0],
                defaults={
                    'price': price
                }
            )
