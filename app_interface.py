import os
import json
import io
from typing import final
from flask import Flask, render_template, request, redirect, url_for, flash
from userInput import exampleForm, kickStarterForm # import forms here. We import these to keep ourselves organized.
from category_searches import highest_usd_pledged_search#functions from the category_searches file. Use them to search a specific category
from add_function import add_to_json
import plotly # pip install plotly==5.3.1
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#from analytic_functions import average_length_ks, count_cat_fail_success, most_funded_category_per_year, bad_date, countProjects, count_cat_fail_success, findAmbitious, gatherYears
from analytic_functions import *
#from analytic_functions import average_length_ks, most_funded_category_per_year, bad_date, countProjects, count_words,count_categories_per_month
# notice here that index.html does not need to be passed in. That is because it is in the templates folder
# In the future we might use templates to reduce redundant html code.

# instructions to run app 
# py -m venv env
# env/Scripts/Activate
# export FLASK_APP=app_interface.py
# export FLASK_DEBUG=1
# flask run

# dummy_file.json
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

@app.route("/analytics",methods=['POST','GET'])
def redirect_to_analytics():
    return render_template('analytic_options.html')

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

@app.route("/update_ks_route",methods=['POST','GET'])
def update_ks():
    if request.method == 'POST': # will only run below code if client is posting
        choiceSearch = request.form.get('choice')
        if not choiceSearch or choiceSearch.isspace():
            return redirect(request.url)
        #return redirect(url_for('get_id', id=id))
    return render_template('updateDB-options.html')


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


#josephwork
@app.route("/analytic_likely_fail")
def category_fail():
    category_names, category_failed_ratio = count_cat_fail_success(data)

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

@app.route("/analytic_avg_length_ks")
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

@app.route("/analytics_most_funded_category")
def analytics_most_funded_category():
    
    #contains the most pledged categories for years 2012-15
    list_of_categories = []
    list_of_years = ['2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']
    list_of_values = []


    temp = []
    for str in list_of_years:
        temp = most_funded_category_per_year(str,data)
        #print(*temp, sep = "\n") 
        list_of_values.append(temp[0])
        list_of_categories.append(temp[1])
        
    
    for i in range(len(list_of_years)):
        list_of_years[i] = list_of_years[i] + " " + list_of_categories[i]
    
    
    fig = go.Figure(data=[
        go.Bar(x=list_of_years, y=list_of_values) # create the bar chart
    ])
    
    fig.update_layout( # change the bar mode
        title="Most Funded Category for each year", xaxis_title="Year", 
        yaxis_title="Total Amount Pledged in Most Funded Category"
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) # send json of graph to analytics.html

    
    return render_template('analytics.html', graphJSON=graphJSON)

@app.route("/analytics_popmonth")
def popularMonth():
    year_dict = countProjects(data)
    monthList = ['Jan', 'Feb', 'Mar', 'Apr', 'May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    # Create the graph
    fig = go.Figure(
        data=[go.Bar(name='2009', x=monthList, y=year_dict['2009']),
            go.Bar(name='2010', x=monthList, y=year_dict['2010']),
            go.Bar(name='2011', x=monthList, y=year_dict['2011']),
            go.Bar(name='2012', x=monthList, y=year_dict['2012']),
            go.Bar(name='2013', x=monthList, y=year_dict['2013']),
            go.Bar(name='2014', x=monthList, y=year_dict['2014']),
            go.Bar(name='2015', x=monthList, y=year_dict['2015']),
            go.Bar(name='2016', x=monthList, y=year_dict['2016']),
            go.Bar(name='2017', x=monthList, y=year_dict['2017']),
            go.Bar(name='2018', x=monthList, y=year_dict['2018'])])
    # Create the dropdown menu (Yes, you read that right. This massive chonker for one dropdown menu.)
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(
                        label="All",
                        method="update",
                        args=[{"visible": [True,True,True,True,True,True,True,True,True,True]},
                        {"title": "Kickstarters launched across all years"}]
                    ),
                    dict(
                        label="2009",
                        method="update",
                        args=[{"visible": [True,False,False,False,False,False,False,False,False,False]},
                        {"title": "Kickstarters launched in 2009"}]
                    ),
                    dict(
                        label="2010",
                        method="update",
                        args=[{"visible": [False,True,False,False,False,False,False,False,False,False]},
                        {"title": "Kickstarters launched in 2010"}]
                    ),
                    dict(
                        label="2011",
                        method="update",
                        args=[{"visible": [False,False,True,False,False,False,False,False,False,False]},
                        {"title": "Kickstarters launched in 2011"}]
                    ),
                    dict(
                        label="2012",
                        method="update",
                        args=[{"visible": [False,False,False,True,False,False,False,False,False,False]},
                        {"title": "Kickstarters launched in 2012"}]
                    ),
                    dict(
                        label="2013",
                        method="update",
                        args=[{"visible": [False,False,False,False,True,False,False,False,False,False]},
                        {"title": "Kickstarters launched in 2013"}]
                    ),
                    dict(
                        label="2014",
                        method="update",
                        args=[{"visible": [False,False,False,False,False,True,False,False,False,False]},
                        {"title": "Kickstarters launched in 2014"}]
                    ),
                    dict(
                        label="2015",
                        method="update",
                        args=[{"visible": [False,False,False,False,False,False,True,False,False,False]},
                        {"title": "Kickstarters launched in 2015"}]
                    ),
                    dict(
                        label="2016",
                        method="update",
                        args=[{"visible": [False,False,False,False,False,False,False,True,False,False]},
                        {"title": "Kickstarters launched in 2016"}]
                    ),
                    dict(
                        label="2017",
                        method="update",
                        args=[{"visible": [False,False,False,False,False,False,False,False,True,False]},
                        {"title": "Kickstarters launched in 2017"}]
                    ),
                    dict(
                        label="2018",
                        method="update",
                        args=[{"visible": [False,False,False,False,False,False,False,False,False,True]},
                        {"title": "Kickstarters launched in 2018"}]
                    ),
                ])
            ),
        ]
    )
    # Change the title and axis labels
    fig.update_layout(
        title="Kickstarters launched across all years", xaxis_title="Month", 
        yaxis_title="Number of projects launched"
    ) 
    # Export graph to analytics.html
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('analytics.html', graphJSON=graphJSON)

@app.route("/analytics_popcat")
def category_per_month(): # most popular category per month

    #used to keep track of the count of all the main categories
    categories = ['Games', 'Design', 'Technology', 'Film & Video', 'Music', 'Publishing',
        'Fashion', 'Food', 'Art', 'Comics', 'Photography', 'Theater', 'Crafts', 'Journalism',
        'Dance']
    final_Dict = count_categories_per_month(data)
    finalListCat = []
    finalListCount = []
    #listMonth = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    for key in final_Dict.keys():
        monthList = final_Dict[key]
        max_Ind = monthList.index(max(monthList))
        cat = categories[max_Ind]
        finalListCat.append(cat)
        finalListCount.append(monthList[max_Ind])

    print(finalListCat)
    print(len(finalListCount))
    fig = go.Figure(
        data =[go.Bar(name='January', x=categories, y=final_Dict['01']),
            go.Bar(name='February', x=categories, y=final_Dict['02']),
            go.Bar(name='March', x=categories, y=final_Dict['03']),
            go.Bar(name='April', x=categories, y=final_Dict['04']),
            go.Bar(name='May', x=categories, y=final_Dict['05']),
            go.Bar(name='June', x=categories, y=final_Dict['06']),
            go.Bar(name='July', x=categories, y=final_Dict['07']),
            go.Bar(name='August', x=categories, y=final_Dict['08']),
            go.Bar(name='September', x=categories, y=final_Dict['09']),
            go.Bar(name='October', x=categories, y=final_Dict['10']),
            go.Bar(name='November', x=categories, y=final_Dict['11']), 
            go.Bar(name='December', x=categories, y=final_Dict['12'])])


    fig.update_layout( # change the bar mode
        barmode='group', title="Most popular Category per Month", xaxis_title="Main categories", 
        yaxis_title="Project Count"
    ) 
    fig.update_xaxes(categoryorder='total ascending') # sort x-axis in ascending order
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) # send json of graph to analytics.html

    return render_template('analytics.html', graphJSON=graphJSON)

@app.route("/analytics_ambitious")
# I did some peculiar things with this function, but it allows for us to run this same analytic on any size of data (ex. completed 2018, 2019, 2020 data is added)
# I'll add some documentation for anyone who wants to look through it.
def ambitiousProjects():
    # Variable initialization
    monthList = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] # All months
    yearList = gatherYears(data) # All years in the data set
    projectDict = findAmbitious(data) # All ambitious projects in the data set
    tabList = [] # All tabs to be supported by the graph
    visList = [] # Visible statuses, needed for tabs
    fig = go.Figure() # Make the figure and add basic details
    fig.update_layout(
        title="Most Ambitious Projects",
        xaxis_title="Month",
        yaxis_title="US $"
    )

    # Data collection and formatting
    for year in yearList: # For every year,
        IDList = [] # Collect the ID's,
        goalList = [] # goals,
        pledgeList = [] # and amount pledged
        for m in range(1,13): # Across each year-month combination
            date = '-'.join((year,str(m).zfill(2)))
            try:
                proj = projectDict.get(date)
                IDList.append(('ID: ' + str(proj[0])))
                goalList.append(proj[1])
                pledgeList.append(proj[2])
            except:
                pass
        fig.add_trace(go.Bar( # Then, add a bar for this year-month's goals
            x=monthList,
            y=goalList,
            name='Goal',
            hovertext=IDList
        ))
        fig.add_trace(go.Bar( # and add a bar for this year-month's pledges
            x=monthList,
            y=pledgeList,
            name='Pledges',
            hovertext=IDList
        ))
        tabTitle = "Most Ambitious Projects for " + year
        tabList.append( # and add a new dictionary so this year can be isolated on the graph
            dict(
                label=year,
                method="update",
                args=[{"visible": []}, # This blank list will be filled later
                {"title": tabTitle}]
            )
        )
        visList.append(False) # and add two booleans to the visList, one for each new bar
        visList.append(False)

    # Graph formatting
    visIndex = 0 # Starting at index 0
    for item in tabList: # For every tab to be made,
        copyVis = visList.copy() # Create a copy of our visList
        try:
            copyVis[visIndex] = True # and allow only the two necessary bars to be seen
            copyVis[(visIndex + 1)] = True
        except:
            print('An error occurred! Graph may not display correctly!') # If something bad happens, don't crash
        finally:
            item['args'][0]['visible'] = copyVis # Update this bar's visible arguments to the proper values instead of a blank list
            visIndex += 2 # Increment visIndex by 2 for the next loop

    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=tabList
            )
        ]
    )
    
    # Finally, export the graph
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('analytics.html', graphJSON=graphJSON)



@app.route("/analytics_popnation")
def popular_category_perNation():
    
            
    #this variable holds the dictionary that has each country as a key and occurence of each main_category
    countryDict = get_countrys_category(data)    

    categories = ['Games', 'Design', 'Technology', 'Film & Video', 'Music', 'Publishing',
        'Fashion', 'Food', 'Art', 'Comics', 'Photography', 'Theater', 'Crafts', 'Journalism',
        'Dance'] 
        
    catList = []
    finalListCountry = []
    finalListCat = []
    finalListCount = []
    #used to separate dictionary info into individual lists
    for i in countryDict:
        catList = countryDict[i]
        max_Ind = catList.index(max(catList)) 
        finalListCountry.append(i)
        finalListCount.append(catList[max_Ind])
        finalListCat.append(categories[max_Ind])

    keysList = list(countryDict.keys())

    
    print(countryDict[keysList[0]])
    fig = go.Figure(
        data =[go.Bar(name=keysList[0], x=categories, y=countryDict[keysList[0]]),
            go.Bar(name=keysList[1], x=categories, y=countryDict[keysList[1]]),
            go.Bar(name=keysList[2], x=categories, y=countryDict[keysList[2]]),
            go.Bar(name= keysList[3], x=categories, y=countryDict[keysList[3]]),
            go.Bar(name= keysList[4], x=categories, y=countryDict[keysList[4]]),
            go.Bar(name= keysList[5], x=categories, y=countryDict[keysList[5]]),
            go.Bar(name= keysList[6], x=categories, y=countryDict[keysList[6]]),
            go.Bar(name= keysList[7], x=categories, y=countryDict[keysList[7]]),
            go.Bar(name= keysList[8], x=categories, y=countryDict[keysList[8]]),
            go.Bar(name= keysList[9], x=categories, y=countryDict[keysList[9]]),
            go.Bar(name= keysList[10], x=categories, y=countryDict[keysList[10]]), 
            go.Bar(name= keysList[11], x=categories, y=countryDict[keysList[11]]), 
            go.Bar(name= keysList[12], x=categories, y=countryDict[keysList[12]]), 
            go.Bar(name= keysList[13], x=categories, y=countryDict[keysList[13]]), 
            go.Bar(name= keysList[14], x=categories, y=countryDict[keysList[14]]),
            go.Bar(name=keysList[15], x=categories, y=countryDict[keysList[15]]),
            go.Bar(name=keysList[16], x=categories, y=countryDict[keysList[16]]),
            go.Bar(name= keysList[17], x=categories, y=countryDict[keysList[17]]),
            go.Bar(name= keysList[18], x=categories, y=countryDict[keysList[18]]),
            go.Bar(name= keysList[19], x=categories, y=countryDict[keysList[19]]),
            go.Bar(name= keysList[20], x=categories, y=countryDict[keysList[20]]),
            go.Bar(name= keysList[21], x=categories, y=countryDict[keysList[21]]),
            go.Bar(name= keysList[22], x=categories, y=countryDict[keysList[22]])
            ])


    fig.update_layout( # change the bar mode
        barmode='group', title="Most Popular Category in Each Country", xaxis_title="Countries", 
        yaxis_title="Project Count"
    ) 
    fig.update_xaxes(categoryorder='total ascending') # sort x-axis in ascending order
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) # send json of graph to analytics.html
    return render_template('analytics.html', graphJSON=graphJSON)

@app.route("/success_words")
def most_successful_words():
    
    list_of_words, list_of_count = count_words(data)

    fig = go.Figure(data=[
        go.Bar(x=list_of_words, y=list_of_count) # create the bar chart
    ])
    
    fig.update_layout( # change the bar mode
        title="Most frequent words in successful projects", xaxis_title="Words", 
        yaxis_title="Count"
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) # send json of graph to analytics.html

    return render_template('analytics.html', graphJSON=graphJSON)
