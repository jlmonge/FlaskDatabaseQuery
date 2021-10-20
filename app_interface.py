import os
import json
import io
from flask import Flask, render_template, request, redirect, url_for #imports from flask
from userInput import exampleForm # import forms here. We import these to keep ourselves organized.
#functions from the category_searches file. Use them to search a specific category
#import utils
# notice here that index.html does not need to be passed in. That is because it is in the templates folder
# In the future we might use templates to reduce redundant html code.

# py -m venv env
# env/Scripts/Activate
# export FLASK_APP=app_interface.py
# export FLASK_DEBUG=1
# flask run

def search_helper(key, method="GET"):
    if method == 'POST': # will only run below code if client is posting
        # below code: exampleForm is just an imported class.
        # request.form looks at the html in the render_template function.
        # It finds the input given the name 'nm' and returns the user input.
        # form = exampleForm(request.form["id"])
        value = request.form.get(key)
        if not value or value.isspace():
            return redirect(request.url)
        #with open('test.txt', 'w') as f:   # needed once we edit values in the json file
            #f.write(id)
        return redirect(url_for('results', key=key, value=value))
    return render_template(f'search-{key.lower()}.html')

app = Flask(__name__) # neccessary for flask

@app.route("/") # creates "/" directory for homepage
def index():
    return render_template('index.html')

@app.route("/id", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_ID():
    return search_helper('ID', request.method)

@app.route("/name", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_name():
    return search_helper('name', request.method)

@app.route("/category", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_category():
    return search_helper('category', request.method)

@app.route("/state", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_state():
    return search_helper('state', request.method)

@app.route("/launched", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_month():
    return search_helper('launched', request.method)

@app.route("/search/key=<key>&value=<value>")
def results(key, value):
    file = os.path.join(app.static_folder, 'ks-projects-201801.json') # location of json file
    projects = [] # the project(s) being looked for
    with open(file, encoding='utf-8-sig') as json_file:
        data = json.load(json_file) # json --> dictionary
        for proj in data:
            if key == 'ID' and value == proj.get(key):
                projects.append(proj)
            elif (key == 'name' or key == 'state' or key == 'category' or key == 'launched') and value.lower() in proj.get(key).lower():
                projects.append(proj)
    return render_template('results.html', projects=projects)

@app.route("/edit", methods=['POST','GET'])
def edit_project():
    if request.method == 'POST':
        id = request.form.get('id_to_edit')
        # these if statements prevent flask errors when any new value is left blank
        if not id or id.isspace():
            return redirect(request.url)
        new_id = request.form.get('new_id')
        if not new_id:
            new_id = '\n'
        new_name = request.form.get('new_name')
        if not new_name:
            new_name = '\n'
        new_category = request.form.get('new_category')
        if not new_category:
            new_category = '\n'
        new_main_category = request.form.get('new_main_category')
        if not new_main_category:
            new_main_category = '\n'
        new_currency = request.form.get('new_currency')
        if not new_currency:
            new_currency = '\n'
        new_deadline = request.form.get('new_deadline')
        if not new_deadline:
            new_deadline = '\n'
        new_goal = request.form.get('new_goal')
        if not new_goal:
            new_goal = '\n'
        new_launched = request.form.get('new_launched')
        if not new_launched:
            new_launched = '\n'
        new_pledged = request.form.get('new_pledged')
        if not new_pledged:
            new_pledged = '\n'
        new_state = request.form.get('new_state')
        if not new_state:
            new_state = '\n'
        new_backers = request.form.get('new_backers')
        if not new_backers:
            new_backers = '\n'
        new_country = request.form.get('new_country')
        if not new_country:
            new_country = '\n'
        return redirect(url_for('do_edit', id=id, new_id=new_id, new_name=new_name, new_category=new_category,
            new_main_category=new_main_category, new_currency=new_currency, new_deadline=new_deadline,
            new_goal=new_goal, new_launched=new_launched, new_pledged=new_pledged, new_state=new_state,
            new_backers=new_backers, new_country=new_country))
    return render_template('edit.html')

@app.route('''/edit/id=<id>&new_id=<new_id>&new_name=<new_name>&new_category=<new_category>
    &new_main_category=<new_main_category>&new_currency=<new_currency>&new_deadline=<new_deadline>
    &new_goal=<new_goal>&new_launched=<new_launched>&new_pledged=<new_pledged>&new_state=<new_state>
    &new_backers=<new_backers>&new_country=<new_country>''', methods=['POST','GET'])
def do_edit(id, new_id, new_name, new_category, new_main_category, new_currency, new_deadline, new_goal, 
    new_launched, new_pledged, new_state, new_backers, new_country):
    file = os.path.join(app.static_folder, 'ks-projects-201801.json') # location of json file
    projectFound = False # the project being looked for
    with open(file, 'r+', encoding='utf-8-sig') as json_file:
        data = json.load(json_file) # json --> dictionary
        for proj in data:
            if id == proj.get('ID'):
                projectFound = True
                # these if statements prevent flask errors when any new value is left blank
                if new_id != '\n':
                    proj['ID'] = new_id 
                if new_name != '\n':
                    proj['name'] = new_name
                if new_category != '\n':
                    proj['category'] = new_category
                if new_main_category != '\n':
                    proj['main_category'] = new_main_category
                if new_currency != '\n':
                    proj['currency'] = new_currency
                if new_deadline != '\n':
                    proj['deadline'] = new_deadline
                if new_goal != '\n':
                    proj['goal'] = new_goal
                if new_launched != '\n':
                    proj['launched'] = new_launched
                if new_pledged != '\n':
                    proj['pledged'] = new_pledged
                if new_state != '\n':
                    proj['state'] = new_state
                if new_backers != '\n':
                    proj['backers'] = new_backers
                if new_country != '\n':
                    proj['country'] = new_country
                break
        if not projectFound:
            return render_template('edit-failure.html')
    
        json_file.seek(0)
        json.dump(data, json_file, indent=4)
        json_file.truncate()
    '''
    with open(file, 'w', encoding='utf-8-sig') as json_file:
        json.dump(data, json_file, indent=4)
    print(proj)
    print(new_id, new_name, new_category, new_main_category, new_currency, new_deadline, new_goal, new_launched, \
        new_pledged, new_state, new_backers, new_country)
    print(proj['ID'], proj['name'], proj['category'], proj['main_category'], proj['currency'], proj['deadline'], \
        proj['goal'], proj['launched'], proj['pledged'], proj['state'], proj['backers'], proj['country'])
    '''
    return render_template('edit-success.html', project=proj)

'''
@app.route("/id/<id>/edit") # needed to edit later on
def set_id()
'''