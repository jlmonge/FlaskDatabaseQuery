import os
import json
import io
from flask import Flask, render_template, request, redirect, url_for #imports from flask
from userInput import exampleForm # import forms here. We import these to keep ourselves organized.
#functions from the category_searches file. Use them to search a specific category
from category_searches import category_search, state_search, launched_month_search, highest_usd_pledged_search 
#import utils
# notice here that index.html does not need to be passed in. That is because it is in the templates folder
# In the future we might use templates to reduce redundant html code.

# export FLASK_APP=app_interface.py
# export FLASK_DEBUG=1

app = Flask(__name__) # neccessary for flask

@app.route("/") # creates "/" directory for homepage
def indexPage():
    return render_template('index.html')

@app.route("/id", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_id():
    if request.method == 'POST': # will only run below code if client is posting
        # below code: exampleForm is just an imported class.
        # request.form looks at the html in the render_template function.
        # It finds the input given the name 'nm' and returns the user input.
        # form = exampleForm(request.form["id"])
        id = request.form.get('id')
        if not id or id.isspace():
            return redirect(request.url)
        #with open('test.txt', 'w') as f:   # needed once we edit values in the json file
            #f.write(id)
        return redirect(url_for('results', key='ID', value=id))
    return render_template('search-id.html')

@app.route("/name", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_name():
    if request.method == 'POST': # will only run below code if client is posting
        # below code: exampleForm is just an imported class.
        # request.form looks at the html in the render_template function.
        # It finds the input given the name 'nm' and returns the user input.
        #form = exampleForm(request.form["nm"])
        name = request.form.get('name')
        if not name or name.isspace():
            return redirect(request.url)
        #with open('test.txt', 'w') as f:   # needed once we edit values in the json file
            #f.write(name)
        return redirect(url_for('results', key='name', value=name))
    return render_template('search-name.html')

@app.route("/category", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_category():
    if request.method == 'POST': # will only run below code if client is posting
        # below code: exampleForm is just an imported class.
        # request.form looks at the html in the render_template function.
        # It finds the input given the name 'nm' and returns the user input.
        #form = exampleForm(request.form["id"])
        category = request.form.get('category')
        if not category or category.isspace():
            return redirect(request.url)
        #with open('test.txt', 'w') as f:   # needed once we edit values in the json file
            #f.write(id)
        return redirect(url_for('results', key='category', value=category))
    return render_template('search-category.html')

@app.route("/state", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_state():
    if request.method == 'POST': # will only run below code if client is posting
        # below code: exampleForm is just an imported class.
        # request.form looks at the html in the render_template function.
        # It finds the input given the name 'nm' and returns the user input.
        #form = exampleForm(request.form["id"])
        state = request.form.get('state')
        if not state or state.isspace():
            return redirect(request.url)
        #with open('test.txt', 'w') as f:   # needed once we edit values in the json file
            #f.write(id)
        return redirect(url_for('results', key='state', value=state))
    return render_template('search-state.html')

@app.route("/month", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_month():
    if request.method == 'POST': # will only run below code if client is posting
        # below code: exampleForm is just an imported class.
        # request.form looks at the html in the render_template function.
        # It finds the input given the name 'nm' and returns the user input.
        #form = exampleForm(request.form["id"])
        month = request.form.get('month')
        if not month or month.isspace():
            return redirect(request.url)
        #with open('test.txt', 'w') as f:   # needed once we edit values in the json file
            #f.write(id)
        return redirect(url_for('results', key='launched', value=month))
    return render_template('search-month.html')

@app.route("/search/<key><value>")
def results(key, value):
    file = os.path.join(app.static_folder, 'ks-projects-201801.json') # location of json file
    projects = [] # the project(s) being looked for
    with open(file, encoding='utf-8-sig') as json_file:
        data = json.load(json_file) # json --> dictionary
        for proj in data:
            if key == 'ID' and value == proj.get(key):
                projects.append(proj)
            elif (key == 'name' or key == 'state' or key == 'main_category' or key == 'launched') and value in proj.get(key):
                projects.append(proj)
    return render_template('results.html', projects=projects)

'''
@app.route("/id/<id>/edit") # needed to edit later on
def set_id()
'''
