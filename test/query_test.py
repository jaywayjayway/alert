#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import jsonify
from libs.utils import UserConfig
from influxdb import InfluxDBClient
import json
config =  UserConfig()

class InfluxResource():

    def get(self):
        global  config 
        results = []
        _config = config.get('influxdb', {})
        client = InfluxDBClient.from_DSN(_config['uri'], timeout=5)
        query = _config.get('query', [])
        result = client.query(query, epoch='ms')
        for  dataset in  result.raw['series']:
            series = {}
            series['data'] = dataset['values']
            series['name'] = dataset['name']
            series['columns'] = dataset['columns']
        #print series['columns']
        for index,value  in enumerate(series['data']):
             #print index,value
             results.append(dict(zip(series['columns'],value)))
        print   results
        #print json.dumps(series)
        
        
            #print  series
#        series = {}
#        series['data'] = dataset['values']
#        series['label'] = metric['labels'][index] if 'labels' in metric else None
#        series['lines'] = dict(fill=True)
#        series['mode'] = metric['mode'] if 'mode' in metric else None
#        series['color'] = metric['colors'][index] if 'colors' in metric else None
#

InfluxResource().get()
