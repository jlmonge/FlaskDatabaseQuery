import os
import json
import io
from flask import Flask, render_template, request, redirect, url_for #imports from flask
from userInput import exampleForm, kickStarterForm # import forms here. We import these to keep ourselves organized.
from category_searches import catagory_search, state_search, launched_month_search, highest_usd_pledged_search#functions from the category_searches file. Use them to search a specific category
from add_function import add_to_json
# notice here that index.html does not need to be passed in. That is because it is in the templates folder
# In the future we might use templates to reduce redundant html code.

# export FLASK_APP=app_interface.py
# export FLASK_DEBUG=1

app = Flask(__name__) # neccessary for flask
databaseFile = os.path.join(app.static_folder, 'WORKING-2018ksprojects.json') # Location of our file. Call it in functions rather than writing this whole thing out again

@app.route("/") # creates "/" directory for homepage
def indexPage():
    return render_template('index.html')

@app.route("/search",methods=['POST','GET'])
def search():
    if request.method == 'POST': # will only run below code if client is posting
        choiceSearch = request.form.get('choice')
        if not choiceSearch or choiceSearch.isspace():
            return redirect(request.url)
        #return redirect(url_for('get_id', id=id))
    return render_template('searches.html')


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
    with open(databaseFile, "r+") as file:
        located = False
        pos = 0
        data = json.load(file)
        for i in data:
            if i['ID'] == id_to_delete:
                located = True
                break
            else:
                pos += 1
        if located:
            data.pop(pos)
            file.seek(0)
            json.dump(data, file, indent = 4)
            file.truncate()
            successMessage = "Project %s was deleted successfully."%id_to_delete
            return render_template('sentanceMessage.html',message = successMessage)
        else:
            errorMessage = "Error: Project %s could not be found!"%id_to_delete
            return render_template('sentanceMessage.html',message = errorMessage)


@app.route("/update",methods=['POST','GET'])#NOT WORKING
def update_kickstarter():
    if request.method == 'POST': # will only run below code if client is posting
        ksToUpdate = kickStarterForm(request.form.get('id'),request.form.get('name'),request.form.get('category'),request.form.get('main_category'),request.form.get('currency'),
        request.form.get('deadline'),request.form.get('goal'),request.form.get('date_launched'), request.form.get('time_launched'),request.form.get('number_pledged'),request.form.get('state'),
        request.form.get('number_backers'), request.form.get('country'), request.form.get('amount_usd_pledged'), request.form.get('amount_usd_pledged_real'))
        if not len(ksToUpdate.error_msgs) == 0:
            return render_template('sentanceMessage.html',message = "Error on one or more field")
        return redirect(url_for('do_update', ksToUpdate=ksToUpdate))
    return render_template('updateKickstarter.html')

@app.route("/update/<ksToUpdate>")#NOR WORKING
def do_update(ksToUpdate):
    #YOUR CODE HERE
    updateSuccessful = True
    if updateSuccessful:
        return render_template('sentanceMessage.html',message = "Successfully updated Kickstarter")
    else:
        return render_template('sentanceMessage.html',message = "error")

@app.route("/add",methods=['POST','GET'])#NOT WORKING
def add_kickstarter():
    if request.method == 'POST': # will only run below code if client is posting
        ksToAdd = kickStarterForm(request.form.get('id'),request.form.get('name'),request.form.get('category'),request.form.get('main_category'),request.form.get('currency'),
        request.form.get('deadline'),request.form.get('goal'),request.form.get('date_launched'), request.form.get('time_launched'),request.form.get('number_pledged'),request.form.get('state'),
        request.form.get('number_backers'), request.form.get('country'), request.form.get('amount_usd_pledged'), request.form.get('amount_usd_pledged_real'))
        if not len(ksToAdd.error_msgs) == 0:
            return render_template('sentanceMessage.html',message = "Error on one or more field")
        add_to_json(ksToAdd.id, ksToAdd.name, ksToAdd.category, ksToAdd.main_category, ksToAdd.currency, ksToAdd.deadline, ksToAdd.goal, ksToAdd.date_launched, ksToAdd.number_pledged, 
        ksToAdd.state, ksToAdd.number_backers, ksToAdd.country, ksToAdd.amount_usd_pledged, ksToAdd.amount_usd_pledged_real)
        #if addSuccessful:
        return render_template('sentanceMessage.html',message = "Successfully added Kickstarter " + ksToAdd.name)
        #else:
         #   return render_template('sentanceMessage.html',message = "error")
        #return redirect(url_for('do_add', ksToAdd=ksToAdd))
    return render_template('addKickstarter.html')

#@app.route("/add/<ksToAdd>")
#def do_add(ksToAdd):
    #print(type(ksToAdd))
    #addSuccessful = add_to_json(ksToAdd.id, ksToAdd.name, ksToAdd.category, ksToAdd.main_category, ksToAdd.currency, ksToAdd.deadline, ksToAdd.goal, ksToAdd.date_launched, ksToAdd.number_pledged, 
    #ksToAdd.state, ksToAdd.number_backers, ksToAdd.country, ksToAdd.amount_usd_pledged, ksToAdd.amount_usd_pledged_real)
    #if addSuccessful:
    #    return render_template('sentanceMessage.html',message = "Successfully added Kickstarter " + ksToAdd.name)
    #else:
    #    return render_template('sentanceMessage.html',message = "error")

@app.route("/id", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_id():
    if request.method == 'POST': # will only run below code if client is posting
        # below code: exampleForm is just an imported class.
        # request.form looks at the html in the render_template function.
        # It finds the input given the name 'nm' and returns the user input.
        #form = exampleForm(request.form["id"])
        id = request.form.get('id')
        if not id or id.isspace():
            return redirect(request.url)
        #with open('test.txt', 'w') as f:   # needed once we edit values in the json file
            #f.write(id)
        return redirect(url_for('get_id', id=id))
    return render_template('search-id.html')

@app.route("/id/<id>")
def get_id(id):
    project = {} # the project being looked for
    with open(databaseFile, encoding='utf-8-sig') as json_file:
        data = json.load(json_file) # json --> dictionary
        for proj in data:
            if proj['ID'] == id:
                project = proj
    return render_template('get-id.html', project=project)

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
        return redirect(url_for('get_name', name=name))
    return render_template('search-name.html')

@app.route("/name/<name>")
def get_name(name):
    projects = [] # the project being looked for
    with open(databaseFile, encoding='utf-8-sig') as json_file:
        data = json.load(json_file) # json --> dictionary
        for proj in data:
            if name.lower() in proj['name'].lower():
                projects.append(proj)
    return render_template('get-name.html', projects=projects)

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
        return redirect(url_for('get_category', category=category))
    return render_template('search-category.html')

@app.route("/category/<category>")
def get_category(category):
    project = {} # the project being looked for
    with open(databaseFile, encoding='utf-8-sig') as json_file:
        data = json.load(json_file) # json --> dictionary
        projects = catagory_search(category)

    return render_template('get-name.html', projects=projects)



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
        return redirect(url_for('get_state', state=state))
    return render_template('search-state.html')

@app.route("/state/<state>")
def get_state(state):
    project = {} # the project being looked for
    with open(databaseFile, encoding='utf-8-sig') as json_file:
        data = json.load(json_file) # json --> dictionary
        projects = state_search(state)

    return render_template('get-name.html', projects=projects)


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
        return redirect(url_for('get_month', month=month))
    return render_template('search-month.html')

@app.route("/month/<month>")
def get_month(month):
    project = {} # the project being looked for
    with open(databaseFile, encoding='utf-8-sig') as json_file:
        data = json.load(json_file) # json --> dictionary
        projects = launched_month_search(month)

    return render_template('get-name.html', projects=projects)




'''
@app.route("/id/<id>/edit") # needed to edit later on
def set_id()
'''
