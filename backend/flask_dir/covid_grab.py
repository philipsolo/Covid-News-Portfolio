import os

from flask_dir.database_store import fetch_our_world, fetch_john_covid
import json
import datetime
from spellchecker import SpellChecker

country_colors = [("#3e95cd", 'rgba(62, 149, 205, 0.3)'), ("#8e5ea2", 'rgba(142, 94, 162, 0.3)'),
                  ("#3cba9f", 'rgba(60, 186, 159, 0.3)'), ("#e8c3b9", 'rgba(232, 195, 185, 1)'),
                  ("#c45850", "rgba(196, 88, 80, 0.3)"), ("#ff5733", "rgba(255, 87, 51, 0.3)"),
                  ("#ca33ff", 'rgba(202, 51, 255, 0.3)')]


# Adds Country codes from json file into db for use in graph data
def get_countries():
    countries_dict = {}
    top_dir = os.getcwd().split('/')
    print(top_dir)
    with open('flask_dir/countries_code.json') as f:
        data = json.load(f)
    for index, value in enumerate(data):
        countries_dict[value] = data[value]['Code']
    return countries_dict


def get_current_time():
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    past = now - datetime.timedelta(days=18)
    return now, past


# For date range EG all_dates = list(date_range(date_start, date_end, 8))
def date_range(start, end, intv):
    diff = (end - start) / intv
    for i in range(intv):
        yield (start + diff * i).strftime("%d-%b")
    yield (end - datetime.timedelta(days=1)).strftime("%d-%b")


def get_dates(date_start, date_end):
    if not date_start:
        date_end, date_start = get_current_time()
    else:
        date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')
        date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d')
    return date_start, date_end


def grab_john_hop(countries: tuple, date_start=None, date_end=None) -> dict:
    all_dict = {'cases': {}, 'deaths': {}, 'dates': [], 'color': {}, 'date_range': {}}
    count = 0

    date_start, date_end = get_dates(date_start, date_end)

    all_dict['date_range'] = {'from': date_start.strftime('%Y-%m-%d'), 'to': date_end.strftime('%Y-%m-%d')}

    all_data = fetch_john_covid('john_covid', countries, date_start - datetime.timedelta(days=1), date_end)
    if not all_data:
        return {}
    for index, data_point in enumerate(all_data):

        country = data_point['Country']
        date = data_point['Date'].strftime("%d-%b")

        if date not in all_dict['dates']:
            all_dict['dates'].append(date)

        if country not in all_dict['cases']:
            all_dict['cases'][country] = []
            all_dict['deaths'][country] = []
            all_dict['color'][country] = country_colors[count]

            # Remove first date (Since no previous cases to compare)
            count += 1
        else:
            all_dict['cases'][country].append(abs(all_data[index - 1]['Cases'] - data_point['Cases']))
            all_dict['deaths'][country].append(abs(all_data[index - 1]['Deaths'] - data_point['Deaths']))
    del all_dict['dates'][0]

    return all_dict


def grab_our_world(countries_tuple):
    our_world_data = {}
    country_list = fetch_our_world('our_world', countries_tuple)
    for country in country_list:
        our_world_data[country['Country']] = country

    return our_world_data


spell = SpellChecker()


def check_country(word):
    if word in spell:
        def_country = word.capitalize()
    else:
        cor = spell.correction(word)
        def_country = cor.capitalize()
    if def_country == 'Us':
        def_country = 'USA'
    elif def_country == 'United states':
        def_country = 'USA'
    elif def_country == 'Usa':
        def_country = 'USA'
    elif def_country == 'Uk':
        def_country = 'UK'
    elif def_country == 'United kingdom':
        def_country = 'UK'
    return def_country


def try_round(num, decim):
    try:
        num = round(num, decim)
    except TypeError:
        num = None
    return num


def grab_our_world_tests(countries, date_start=None, date_end=None):
    all_dict = {'daily_change_total_thousand': {}, 'daily_change_total': {},
                'short_term_tests_per_case': {}, 'cumulative_total_per_thousand': {}, 'dates': [], 'countries': [],
                'color': {}, 'date_range': {}}
    count = 0

    date_start, date_end = get_dates(date_start, date_end)
    all_data = fetch_john_covid('our_world_tests', countries, date_start, date_end)

    for index, data_point in enumerate(all_data):

        country = data_point['Country']
        date = data_point['Date'].strftime("%d-%b")

        if date not in all_dict['dates']:
            all_dict['dates'].append(date)

        if country not in all_dict['countries']:
            all_dict['daily_change_total_thousand'][country] = [
                try_round(data_point['Daily change in cumulative total per thousand'], 2)]
            all_dict['daily_change_total'][country] = [try_round(data_point['Daily change in cumulative total'], 2)]
            all_dict['short_term_tests_per_case'][country] = [try_round(data_point['Short-term tests per case'], 2)]
            all_dict['cumulative_total_per_thousand'][country] = [
                try_round(data_point['Cumulative total per thousand'], 2)]
            all_dict['color'][country] = country_colors[count]
            all_dict['countries'].append(country)
            count += 1
        else:
            all_dict['daily_change_total_thousand'][country].append(
                try_round(data_point['Daily change in cumulative total per thousand'], 2))
            all_dict['daily_change_total'][country].append(
                try_round(data_point['Daily change in cumulative total'], 2))
            all_dict['short_term_tests_per_case'][country].append(
                try_round(data_point['Short-term tests per case'], 2))
            all_dict['cumulative_total_per_thousand'][country].append(
                try_round(data_point['Cumulative total per thousand'], 2))
    return all_dict


if __name__ == '__main__':
    print("Running from within")

    print(grab_our_world_tests(('Greece', 'null')))
