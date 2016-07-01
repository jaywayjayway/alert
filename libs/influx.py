#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libs.utils import UserConfig
from influxdb import InfluxDBClient
from flask import jsonify
config =  UserConfig()

class InfluxResource():
    def __init__(self,body=None):
        global config
        self.config = config.get('influxdb', {})
        self.client = InfluxDBClient.from_DSN(self.config['uri'], timeout=5)
        if  body :
            self.json_body = [
                {
                    "measurement": "cpu_load_short",
                    "tags": {
                        "host": body['host'],
                        "region": body['region'],
                        "level": body['level'],
                        "receiver": body['receiver'],
                        "tyep": body['type']
                    },
                    "fields": {
                        "msg" : body['msg'],
                        "value": 0.64
                    }
                }
            ]

    def write_points(self):
        print("Write points: {0}".format(self.json_body))
        try:
            self.client.write_points(self.json_body)
            return True
        except Exception, e:
            print e
            return False

    def query_points(self,limit=None):
        results = []
        query = self.config.get('query', [])
        if limit:
            query =  query + "limit %d" %(limit)
        result = self.client.query(query, epoch='ms')
        for  dataset in  result.raw['series']:
            series = {}
            series['data'] = dataset['values']
            series['name'] = dataset['name']
            series['columns'] = dataset['columns']
        for index,value  in enumerate(series['data']):
             results.append(dict(zip(series['columns'],value)))
        return    results
