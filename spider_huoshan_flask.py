# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 17:36:14 2019

@author: Lenovo
"""

from flask import Flask,render_template,request
from spider_huoshan import spider_huoshan
import json
from redis import StrictRedis
app = Flask(__name__)
r = StrictRedis(db='3',port='6379')
spider = spider_huoshan()

@app.route('/data',methods=['GET','POST'])
def data():
    
    return r.get('info')
#    return json.dumps(spider.spider_ziduan())

@app.route('/list')
def ls():
    
#    spider.spider_ziduan()
    context = json.loads(r.get('info_to'))
    
    return render_template('data.html',context=context)

@app.route('/search')
def search():
    name = request.args.get('name')
    
    if name == '':
        name = '小一姐姐11'        
#    context = json.loads(r.get(name))
    context = spider.search_spider(name)
    
    return render_template('find.html',context = context)

app.run(host='localhost',port=5001,debug=True)