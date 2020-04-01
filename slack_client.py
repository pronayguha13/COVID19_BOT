# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 16:24:00 2020

@author: pronay
ProjectName:COVID19_BOT
"""
import requests
import json
import logging
from auth import DEFAULT_SLACK_WEBHOOK

HEADERS = {
    'Content-type': 'application/json'
}


def slacker(webhook_url=DEFAULT_SLACK_WEBHOOK):
    def slackit(msg):
        logging.info('Sending {msg} to slack'.format(msg=msg))
        payload = { 'text': msg }
        return requests.post(webhook_url, headers=HEADERS, data=json.dumps(payload))
    return slackit
