import os
import json
import io
from flask import Flask, render_template, request, redirect, url_for #imports from flask
from userInput import exampleForm # import forms here. We import these to keep ourselves organized.
# notice here that index.html does not need to be passed in. That is because it is in the templates folder
# In the future we might use templates to reduce redundant html code.

app = Flask(__name__) # neccessary for flask

@app.route("/") # creates "/" directory for homepage
def indexPage():
    return render_template('index.html')

@app.route("/id", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def set_id():
    if request.method == 'POST': # will only run below code if client is posting
        # below code: exampleForm is just an imported class.
        # request.form looks at the html in the render_template function.
        # It finds the input given the name 'nm' and returns the user input.
        #form = exampleForm(request.form["id"])
        id = request.form.get('id')
        #with open('test.txt', 'w') as f:   # needed once we edit values in the json file
            #f.write(id)
        return redirect(url_for('get_id', id=id))
    return render_template('set-id.html')

@app.route("/id/<id>")
def get_id(id):
    file = os.path.join(app.static_folder, 'ks-projects-201801.json') # location of json file
    project = {} # the project being looked for
    with open(file, encoding='utf-8-sig') as json_file:
        data = json.load(json_file) # json --> dictionary
        for proj in data:
            if proj['ID'] == id:
                project = proj
    return render_template('get-id.html', project=project)