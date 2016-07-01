#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask ,request
import json
from os.path import dirname
from os.path import join
from flask import current_app
from libs.utils import UserConfig
from libs import  sendmail
from libs import influx


app = Flask(__name__)
#app.config['USER_CONFIG'] = UserConfig()
@app.route('/register',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        user_agent = request.headers.get('User-Agent')
        body = {}
        body['type'] = request.json.get('type','default')
        body['host'] = request.json.get('host','')
        body['region'] = request.json.get('region','')
        body['msg'] = request.json.get('msg','Alert.....')
        body['level'] = request.json.get('level',0)
        body['receiver'] = request.json.get('receiver',[])
        body['sub'] = request.json.get('sub',"运维报警")
        if  sendmail.send_mail(body['receiver'],body['sub'],body['msg']):
            response = 'OK'
        else: response = "Error"
        body['receiver']=' '.join(body['receiver'])
        obj = influx.InfluxResource(body)
        obj.write_points()
        return '<h1>%s</h1>' %(response)
    elif request.method == "GET":
        limit = request.args.get('limit','')
        result = influx.InfluxResource().query_points(int(limit))
        return "%s" %(result)
        
if __name__ == '__main__':
     app.run(host='0.0.0.0',port=2222,debug=True)
