#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#    virtualenv env-asn-ajax
#    source env-asn-ajax/bin/active
#    pip install flask

# Copyright 2015 (Audrey) Xuefeng Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.2

import flask
from flask import Flask, request, url_for, redirect, render_template
import json
app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    # world.space={'entity':{x,y,colour}...} 
    # world.index=['entity1','entity2',...]

    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data
        self.index.append(entity)

    def clear(self):
        self.space = dict()
        self.index = []

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: appication/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1,"colour":"red"}' 

myWorld = World()          

# This is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    '''Redirect to /static/index.html '''
    return redirect("/static/index.html")

@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    '''update the entities via this interface'''
    error = None
    if request.method=='POST' or request.method=='PUT':
	data = flask_post_json()
	myWorld.set(entity, data)
    else:
        abort(405)
    return (json.dumps(data), 200, {"Content-type":"application/json"})

'''
@app.route("/world/<idx>", methods=['POST','GET'])
def worldIndex(idx):
    error = None
    if request.method=='POST' or request.method=='GET':
        entities = {}
        indices = myWorld.index[int(idx):]
        for entity in indices:
                entities[entity] = myWorld.get(entity)
        #print(">>>>>>>>/world/<idx>: %s >>>>>>>>" % entities)
        return (json.dumps({"delta":entities,"index":len(myWorld.index)}), 200, {"Content-type":"application/json"})
    else:
        abort(405)
'''

@app.route("/world", methods=['POST','GET'])    
def world():
    '''you should probably return the world here'''
    error = None
    if request.method=='POST' or request.method=='GET':
        #print(">>>>>>>>/world/: %s >>>>>>>>" % myWorld.world())
	return (json.dumps(myWorld.world()), 200, {"Content-type":"application/json"})
    else:
        abort(405)

@app.route("/entity/<entity>")    
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    #print(">>>>>>>>/entity/<entity>GET: %s >>>>>>>>" % myWorld.get(entity))
    return (json.dumps(myWorld.get(entity)), 200, {"Content-type":"application/json"})

@app.route("/clear", methods=['POST','GET'])
def clear():
    '''Clear the world out!'''
    error = None
    if request.method=='POST' or request.method == 'GET':
        myWorld.clear()
        if request.method == 'GET':
            return redirect("/static/index.html")   
    else:
        abort(405)
    return ("", 200, {})

if __name__ == "__main__":
    app.run()

