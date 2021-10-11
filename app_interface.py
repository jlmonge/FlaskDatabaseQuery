from flask import Flask, render_template, request#imports from flask
from userInput import exampleForm#import forms here. We import these to keep ourselves organized.
from category_searches import catagory_search, state_search, launched_month_search, highest_usd_pledged_search#functions from the category_searches file. Use them to search a specific category
#notice here that homepage.html does not need to be passed in. That is because it is in the templates folder
#In the future we might use templates to reduce redundant html code.

app = Flask(__name__)#neccessary for flask

@app.route("/", methods=['POST','GET'])#creates "/" directory and accepts 'POST' and 'GET' Requests
def hello_world():
    if request.method == 'POST': #will only run below code if client is posting
        #below code: exampleForm is just an imported class.
        #request.form looks at the html in the render_template function.
        # It finds the input given the name 'nm' and returns the user input.
        form = exampleForm(request.form["nm"])
        print(form.nm) #prints recieved user input on terminal
    return render_template('homePage.html')






