""" Module that can update articles and delte them """
import csv
import sched
import time
import json
import logging
from uk_covid19 import Cov19API
from flask import request
from covid_news_handling import news_articles

logging.basicConfig(filename='dashboard.log', level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(module)s '
                           '%(message)s')

UPDATE = []
DELETED_ARTICLES = []

s = sched.scheduler(time.time, time.sleep)

with open('config.json') as config_file:
    data = json.load(config_file)
loc = data['location']
loc_type = data['location_type']
nation_loc = data['nation_location']
nation_loc_type = data['nation_location_type']


def parse_csv_data(csv_filename: str) -> list:
    """Return all teh rows of the csv file in a list.

    :param csv_filename: arg1
    :return: list of all the rows
    """
    file = open(csv_filename)
    reader = csv.reader(file)
    list_data = []
    for row in reader:
        list_data.append(row)
    return list_data


def process_covid_csv_data(covid_csv_data) -> tuple:
    """Return the number of new cases of covid in the last 7 days,
    the number of hospital cases, and the total of deaths.

    :param covid_csv_data: arg1
    :return: number of new cases, hospital cases and deaths
    """
    nb_cases_7days = 0
    hospital_cases = 0
    tot_deaths = 0
    for i in covid_csv_data[3:10]:
        number_case_1day = i[6]
        number_case_1day = int(number_case_1day)
        nb_cases_7days += number_case_1day
    for j in covid_csv_data[1:2]:
        hospital_cases = j[5]
        hospital_cases = int(hospital_cases)
    for k in covid_csv_data[14:15]:
        tot_deaths = k[4]
        tot_deaths = int(tot_deaths)
    return nb_cases_7days, hospital_cases, tot_deaths


def covid_API_request(location: str = 'Exeter', location_type: str = 'ltla') \
        -> dict:
    """Return according to the location the number of new cases of covid in
    the last 7 days, the number of current hospital cases, and the total of
    deaths with the location or the number of new cases in the last 7 days
    and the location.

    :param location: exact location, can be a city or a nation within the UK
    :param location_type: type of location for the API
    :return: return number of new cases, hospital cases, deaths and the
    location in a dictionary
    """
    logging.info('covid data has been updated')
    data = {}
    area = [
        'areaType=' + location_type,
        'areaName=' + location
    ]
    if location_type != 'nation':
        cases = {
            "date": "date",
            "areaName": "areaName",
            "newCasesByPublishDate": "newCasesByPublishDate",
        }
    else:
        cases = {
            "date": "date",
            "areaName": "areaName",
            "newCasesByPublishDate": "newCasesByPublishDate",
            "hospitalCases": "hospitalCases",
            "cumDeaths60DaysByDeathDate": "cumDeaths60DaysByDeathDate"
        }
    api = Cov19API(filters=area, structure=cases)
    covid_data = api.get_json()
    nb_cases_7day = 0
    for i in range(7):
        nb_cases_1day = (covid_data['data'][i]['newCasesByPublishDate'])
        nb_cases_7day += nb_cases_1day
    data['nb_cases_7day'] = nb_cases_7day
    data['location'] = location
    if location_type == 'nation':
        nb_hospital_cases = None
        nb_cum_deaths = None
        j = 0
        k = 0
        while isinstance(nb_hospital_cases, type(None)):
            nb_hospital_cases = covid_data['data'][j]['hospitalCases']
            j += 1
        while isinstance(nb_cum_deaths, type(None)):
            nb_cum_deaths = covid_data['data'][k]["cumDeaths60DaysByDeathDate"]
            k += 1
        data['nb_hospital_cases'] = 'Hospital cases: ' + str(nb_hospital_cases)
        data['nb_cum_deaths'] = 'Number of deaths: ' + str(nb_cum_deaths)
        return data
    else:
        return data


def update_covid_data():
    """Extract the data from the dictionary.

    :return: None
    """
    global local_7day_infections, location, national_7day_infections, \
        hospital_cases, deaths_total, nation_location
    city_data = covid_API_request(loc, loc_type)
    local_7day_infections = city_data['nb_cases_7day']
    location = city_data['location']
    nation_data = covid_API_request(nation_loc, nation_loc_type)
    national_7day_infections = nation_data['nb_cases_7day']
    hospital_cases = nation_data['nb_hospital_cases']
    deaths_total = nation_data['nb_cum_deaths']
    nation_location = nation_data['location']


def periodic(scheduler, interval, action, actionargs=()):
    """Schedule indefinitely an event

    :param scheduler: the scheudler
    :param interval: the time interval in seconds
    :param action: the function
    :param actionargs: the argument of teh function
    :return: None
    """
    scheduler.enter(interval, 1, periodic,
                    (scheduler, interval, action, actionargs))
    action(*actionargs)


def schedule_covid_updates(update_interval: float, update_name: str):
    """Schedules update of the covid data and news articles. The can be
    scheduled separately or together. It can be a one time event or a daily
    event.

    :param update_interval: the time interval in seconds
    :param update_name: the name of the scheudled update
    :return: None
    """
    logging.info(update_name + 'has been updated')
    global UPDATE
    update_time = request.args.get('update')
    repeat_update = request.args.get('repeat')
    covid_data = request.args.get('covid-data')
    news = request.args.get('news')
    if covid_data and not news:
        content = 'update covid data at ' + update_time
        e_1 = s.enter(update_interval, 1, update_covid_data)
        cancel_update = e_1
        if repeat_update:
            e_2 = s.enter(update_interval, 1, periodic, (s, 86400,
                                                         update_covid_data))
            cancel_update = e_1, e_2
    elif news and not covid_data:
        content = 'update news articles at ' + update_time
        e_3 = s.enter(update_interval, 1, news_articles)
        cancel_update = e_3
        if repeat_update:
            e_4 = s.enter(update_interval, 1, periodic, (s, 86400,
                                                         news_articles))
            cancel_update = e_3, e_4
    elif news and covid_data:
        content = 'update covid data and news articles at ' + update_time
        e_5 = s.enter(update_interval, 1, update_covid_data)
        e_6 = s.enter(update_interval, 1, news_articles)
        cancel_update = e_5, e_6
        if repeat_update:
            e_7 = s.enter(update_interval, 1, periodic, (s, 86400,
                                                         update_covid_data))
            e_8 = s.enter(update_interval, 1, periodic, (s, 86400,
                                                         news_articles))
            cancel_update = e_5, e_6, e_7, e_8
    UPDATE.append({
        'title': update_name,
        'content': content,
        'cancel': cancel_update
    })
    if covid_data and not news:
        if not repeat_update:
            e_2 = s.enter(update_interval, 1, deleted_automated_update,
                          argument=update_name)
            cancel_update = e_1, e_2
    elif news and not covid_data:
        if not repeat_update:
            e_4 = s.enter(update_interval, 1, deleted_automated_update,
                          argument=update_name)
            cancel_update = e_3, e_4
    elif news and covid_data:
        if not repeat_update:
            e_7 = s.enter(update_interval, 1, deleted_automated_update,
                          argument=update_name)
            cancel_update = e_5, e_6, e_7
    UPDATE[-1]['cancel'] = cancel_update


def deleted_automated_update(*arguments: str):
    """If the scheduled update a one time only event, if will delete  the
    update from the interface.

    :param arguments: here the update name, decomposed into single letter
    string.
    :return: None
    """
    logging.info(arguments + 'has been deleted from teh interface')
    global UPDATE
    name = ''.join(arguments)
    del_update = list(filter(lambda up: up['title'] == name, UPDATE))
    UPDATE.remove(del_update[0])


def delete_schedule():
    """Delete the the scheduled event from the queue if the user delete the
    update from the interface.

    :return: None
    """
    logging.info('update has been deleted from interface and queue')
    global UPDATE
    remove_schedule = request.args.get('update_item')
    if remove_schedule:
        del_update = list(filter(lambda up: up['title'] == remove_schedule,
                                 UPDATE))
        UPDATE.remove(del_update[0])
        remove_update = del_update[0]['cancel']
        for i in range(len(remove_update)):
            try:
                s.cancel(remove_update[i])
            except ValueError:
                continue


update_covid_data()
