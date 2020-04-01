# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 10:46:47 2020

@author: Pronay
ProjectName:COVID19_BOT
"""

import datetime
import json
import requests
# import argparse
import logging
from bs4 import BeautifulSoup
from tabulate import tabulate
from slack_client import slacker

FORMAT = '[%(asctime)-15s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename='bot.log', filemode='a')

URL = 'https://www.mohfw.gov.in'
SHORT_HEADERS = ('State', 'Inf', 'Cure', 'Dt')
FILE_NAME = 'corona_india_data.json'
extract_contents = lambda row: [x.text.replace('\n', '') for x in row]


def save(x):
    with open(FILE_NAME, 'w') as f:
        json.dump(x, f)


def load():
    res = {}
    with open(FILE_NAME, 'r') as f:
        res = json.load(f)
    return res


def tableCreator(dataSet):
    return tabulate(dataSet, headers = SHORT_HEADERS,tablefmt = "presto", missingval = "X")

if __name__ == '__main__':

    current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    info = []

    try:
        response = requests.get(URL).content
        soup = BeautifulSoup(response, 'html.parser')
        header = extract_contents(soup.tr.find_all('th'))

        stats = []
        all_rows = soup.find_all('tr')
        for row in all_rows:
            stat = extract_contents(row.find_all('td'))
            if stat:
                if len(stat) == 5 or len(stat) == 4:
                    # last row
                    stat = ['', *stat]
                    stats.append(stat)

        p = 1
        temp = []
        print(stats)
        print("\n\n\n\n\n\n\n")
        for x in stats:
            x = x[2:6]
            temp.append(x)

        y = ["Total", temp[len(temp) - 1]]
        temp = temp[0:len(temp) - 1]
        y1 = []
        print(temp)
        print("\n\n\n\n\n\n\n")
        y1.append("Total")
        y1.append(y[1][0])
        y1.append(y[1][1])
        y1.append(y[1][2])
        print(y1)

        # save(temp)
        past_data = load()

        t = current_time

        cur_data = temp
        # for x in stats:
        # cur_data.append(x[2:6])

        flag = 0
        change = []
        change1 = [["State", "Infected", "Cured", "Death"], ]
        for (x, y) in zip(past_data, cur_data):

            if (int(x[1]) != int(y[1])):
                inf = abs(int(x[1]) - int(y[1]))
                c = abs(int(x[2]) - int(y[2]))
                dt = abs(int(x[3]) - int(y[3]))
                change.append(y[0])
                change.append(inf)
                change.append(c)
                change.append(dt)
                flag = 1
            change1.append(change)

        events_info = ''
        # print(cur_data)
        if flag:
            save(cur_data)
            events_info = "Aleart !!!COVID-19 increases " + t
            slack_text = f'CoronaVirus Summary for India below:\n{events_info}'
            # slacker()(slack_text)

            events_info = "Leatest Summary :: "
            table = tableCreator(change1)
            slack_text = f'CoronaVirus leatest Summary for India:\n{table}'
            # slacker()(slack_text)

            cur_data.append(y1)
            table = tableCreator(cur_data)
            

        else:
            events_info = "No COVID-19 updation in India on " + t
            slack_text = f'CoronaVirus Summary for India below:\n{events_info}'
            slacker()(slack_text)
            # events_info="Previous Summary :: "
            past_data.append(y1)
            table = tableCreator(past_data)
            # print(table)
            slack_text = f'CoronaVirus Previous Summary for India:\n{table}'
            
        print(table)    
        slacker()(slack_text)

    except Exception as e:
        logging.exception('oops, corona script failed.')
        slacker()(f'Exception occured: [{e}]')


    print("\nUpdation Done")
