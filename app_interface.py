import os
import json
import io
from flask import Flask, render_template, request, redirect, url_for, flash #imports from flask
from userInput import exampleForm, kickStarterForm # import forms here. We import these to keep ourselves organized.
from category_searches import highest_usd_pledged_search#functions from the category_searches file. Use them to search a specific category
from add_function import add_to_json
import plotly # pip install plotly==5.3.1
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from stat_functions import average_length_ks#might move average_length_ks to app_interface
# notice here that index.html does not need to be passed in. That is because it is in the templates folder
# In the future we might use templates to reduce redundant html code.

# instructions to run app 
# py -m venv env
# env/Scripts/Activate
# export FLASK_APP=app_interface.py
# export FLASK_DEBUG=1
# flask run

# GLOBAL VARIABLES
file_name =  'ks-projects-201801.json'
data = list()

def search_helper(key, method="GET", input_type=''):
    if method == 'POST': # will only run below code if client is posting
        value = request.form.get(key) # request.form looks at the html in current route
        if not value or value.isspace(): # refresh page if search is blank 
            return redirect(request.url)
        return redirect(url_for('results', key=key, value=value)) # go to results function
    return render_template('search-input.html', type=input_type, name=key) # load page

app = Flask(__name__) # neccessary for flask

@app.before_first_request
def loadJsonFile():
    file = os.path.join(app.static_folder, file_name) # location of json file
    with open(file ,encoding='utf-8-sig') as json_file:
        global data 
        data = json.load(json_file) # json --> list of dictionaries

@app.route("/") # creates "/" directory for homepage
def index():
    return render_template('index.html')

@app.route("/id", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_ID():
    return search_helper('ID', request.method, "number")

@app.route("/name", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_name():
    return search_helper('name', request.method, "text")

@app.route("/category", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_category():
    return search_helper('category', request.method, "text")

@app.route("/state", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_state():
    return search_helper('state', request.method, "text")

@app.route("/launched", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_month():
    return search_helper('launched', request.method, "month")

@app.route("/update_database")
def update_database():
    file = os.path.join(app.static_folder, file_name) # location of json file
    with open(file,"r+" ,encoding='utf-8-sig') as json_file:
        json_file.seek(0) # go to start of file
        json.dump(data, json_file, indent=4) # write data to json file
        # necessary since we open the file with r+
        # if we dump a lesser amount of lines than the file originally had,
        # we end up with trailing garbage values; truncate() gets rid of that
        json_file.truncate() 
    return render_template('results.html', projects=[], message="Successfully updated database file")

@app.route("/import_file", methods=['POST','GET'])
def import_file():
    if request.method == 'POST':
        if 'passed_file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files["passed_file"]
        if file: #and allowed_file(request.url)
            file_path = os.path.join(app.static_folder, file.filename)
            file.save(file_path) 
            with open(file_path, encoding='utf-8-sig') as json_file:
                global data
                data = json.load(json_file) # json --> list of dictionaries
            global file_name
            file_name = file.filename
            return redirect(request.url)
    return render_template("import_file.html")

@app.route("/search/key=<key>&value=<value>")
def results(key, value):
    #file = os.path.join(app.static_folder, file_name) # location of json file
    projects = [] # the project(s) being looked for
    #with open(file, encoding='utf-8-sig') as json_file:
        #data = json.load(json_file) # json --> list of dictionaries
    for proj in data:
        if key == 'ID' and value == proj.get(key):
            projects.append(proj)
        elif (key == 'name' or key == 'state' or key == 'category' or key == 'launched') and value.lower() in proj.get(key).lower():
            projects.append(proj)
    return render_template('results.html', projects=projects, message="Project not found")

@app.route("/search",methods=['POST','GET'])
def search():
    if request.method == 'POST': # will only run below code if client is posting
        choiceSearch = request.form.get('choice')
        if not choiceSearch or choiceSearch.isspace():
            return redirect(request.url)
        #return redirect(url_for('get_id', id=id))
    return render_template('search-options.html')


@app.route("/delete",methods=['POST','GET'])
def delete_kickstarter():
    if request.method == 'POST': # will only run below code if client is posting
        deleteChoice = request.form.get('id_to_delete')
        if not deleteChoice or deleteChoice.isspace():
            return redirect(request.url)
        return redirect(url_for('do_delete', id_to_delete=deleteChoice))
    return render_template('deleteKickstarter.html')

@app.route("/delete/<id_to_delete>")
def do_delete(id_to_delete):
    #databaseFile = os.path.join(app.static_folder, file_name)
    #with open(databaseFile, "r+") as file:
    #with open(databaseFile, "r+",encoding='utf-8-sig') as file:
        located = False
        pos = 0
        #data = json.load(file) # json --> list of dictionaries
        #data = json.load(file)
        for i in data:
            if i['ID'] == id_to_delete:
                located = True
                break
            else:
                pos += 1
        if located:
            data.pop(pos)
            successMessage = "Project %s was deleted successfully."%id_to_delete
            return render_template('results.html', projects=[], message=successMessage)
        else:
            errorMessage = "Error: Project %s could not be found!"%id_to_delete
            return render_template('results.html', projects=[], message=errorMessage)

@app.route("/add",methods=['POST','GET'])#NOT WORKING
def add_kickstarter():
    if request.method == 'POST': # will only run below code if client is posting
        ksToAdd = kickStarterForm(request.form.get('id'),request.form.get('name'),request.form.get('category'),request.form.get('main_category'),request.form.get('currency'),
        request.form.get('deadline'),request.form.get('goal'),request.form.get('date_launched'),request.form.get('time_launched'),request.form.get('number_pledged'),request.form.get('state'),
        request.form.get('number_backers'), request.form.get('country'), request.form.get('amount_usd_pledged'), request.form.get('amount_usd_pledged_real'))      
        if not len(ksToAdd.error_msgs) == 0:
            return render_template('results.html', projects=[], message="Error on one or more fields")
        
        add_to_json(data,ksToAdd.id,ksToAdd.name,ksToAdd.category,ksToAdd.main_category,ksToAdd.currency,ksToAdd.deadline,ksToAdd.goal,ksToAdd.date_launched,
            ksToAdd.number_pledged,ksToAdd.state,ksToAdd.number_backers,ksToAdd.country,ksToAdd.amount_usd_pledged,ksToAdd.amount_usd_pledged_real)
        return render_template('results.html', message="Successfully added kickstarter "+ksToAdd.name)
    return render_template('addKickstarter.html')

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
        else:
            # slicing is done to match the format of the rest of the launched values
            new_launched = new_launched[:10] + " " + new_launched[11:]
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
    #file = os.path.join(app.static_folder, file_name) # location of json file
    projectFound = False # the project being looked for
    #with open(file, 'r+', encoding='utf-8-sig') as json_file:
        #data = json.load(json_file) # json --> list of dictionaries
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
        return render_template('results.html', projects=[], message="Project not found")
        
    return render_template('results.html', projects=[proj])

@app.route("/analytics")
def category_fail():
    category_dict = { # key=main category, value=#successful[0],#failed[1]
        'Games':[0,0], 'Design':[0,0], 'Technology':[0,0], 'Film & Video':[0,0], 'Music':[0,0], 
        'Publishing':[0,0], 'Fashion':[0,0], 'Food':[0,0], 'Art':[0,0], 
        'Comics':[0,0], 'Photography':[0,0], 'Theater':[0,0], 'Crafts':[0,0], 
        'Journalism':[0,0], 'Dance':[0,0]}
    for proj in data:
        if proj['state'] == 'successful':
            category_dict[proj['main_category']][0] += 1
        elif proj['state'] == 'failed' or proj['state'] == 'canceled':
            category_dict[proj['main_category']][1] += 1
   
    category_names = list(category_dict.keys())
    # FOR DEBUGGING: category_successful = [x[0] for x in list(category_dict.values())]
    # FOR DEBUGGING: category_failed = [x[1] for x in list(category_dict.values())]
    category_failed_ratio = [x[1] / (x[0] + x[1]) if x[0] or x[1] else 0 for x \
        in list(category_dict.values())] # list comprehension

    fig = go.Figure(data=[
        go.Bar(x=category_names, y=category_failed_ratio) # create the bar chart
    ])

    fig.update_layout( # change the bar mode
        barmode='stack', title="Ratio of failed projects in each main category", xaxis_title="Main categories", 
        yaxis_title="Ratio of failed projects"
    ) 
    fig.update_xaxes(categoryorder='total ascending') # sort x-axis in ascending order
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) # send json of graph to analytics.html

    return render_template('analytics.html', graphJSON=graphJSON)

@app.route("/analytic_length")
def make_length_analytic():
    labels, analyticByMonth, totalAverage = average_length_ks(data)

    #Joseph's work
    fig = go.Figure(data=[
        go.Bar(x=labels, y=analyticByMonth) # create the bar chart
    ])

    fig.update_layout( # change the bar mode
        barmode='stack', title="Average Expected Length of Kickstarter by Year", xaxis_title="Year", 
        yaxis_title="Average expected length(days)"
    )
    fig.update_xaxes(categoryorder='total ascending') # sort x-axis in ascending order
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) # send json of graph to analytics.html

    return render_template('analytics.html', graphJSON=graphJSON)
