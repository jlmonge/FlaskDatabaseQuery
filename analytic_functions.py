#this file will contain all the functions that we use to create the data that we will pass to the graphs

from datetime import date

def check_float(potential_float): 
    try:
        float(potential_float)
        return True

    except ValueError:
        return False

#input a year and python dict
#output returns a list with first value of the most funded category of the year and second value as the category that was most funded
def most_funded_category_per_year(year , file_data):
    category_dict = { # key=main category, value= total amount pledged for the year
        'Games':0, 'Design': 0, 'Technology': 0, 'Film & Video': 0, 'Music': 0, 
        'Publishing': 0, 'Fashion': 0, 'Food': 0, 'Art': 0, 
        'Comics': 0, 'Photography': 0, 'Theater': 0, 'Crafts': 0, 
        'Journalism': 0, 'Dance': 0}

    result = []

    
    for key in file_data:
        if key['main_category'] in category_dict.keys():
            if check_float(key['pledged']):
                str = key['launched']
                if str[0:4] == year:
                    category_dict[key['main_category']] += float(key['pledged'])
    
    list_of_values = category_dict.values()
    max_value = max(list_of_values)
    result.append(max_value)

    max_key = max(category_dict, key=category_dict.get)
    result.append(max_key)

    return result




def bad_date(date):

    if(len(date) < 10):
        return True
    try:
        yearNum = int(date[0:4])
        monthNum = int(date[5:7])
        dayNum = int(date[8:10])
    except:
        return True

    if yearNum < 2008 or yearNum > 3000:
        return True
    if  monthNum < 1 or monthNum > 12:
        return True
    if dayNum < 1 or dayNum > 31:
        return True
    return False


def average_length_ks(pyfile):
    labels = list() #labels for each datapoint
    returnData = list() #datapoints(average length per year)
    totalAverage = 0
    totalDates = 0
    dataByMonth = list() #
    #listValues = ["year",0.0,0]#"year or total", sum of lengths, number of values
    for i in pyfile:
        if bad_date(i["launched"]) or bad_date(i["deadline"]):#if the lanch or deadline date return true then they are bad dates and we ignore the input
            continue
        startDate = date(int(i["launched"][0:4]),int(i["launched"][5:7]),int(i["launched"][8:10]))
        endDate = date(int(i["deadline"][0:4]),int(i["deadline"][5:7]),int(i["deadline"][8:10]))
        
        timeBetween = endDate - startDate 
        
        yearNotInList = True
        for val in range(len(dataByMonth)):
            if dataByMonth[val][0] == i["launched"][0:4]:
                yearNotInList = False
                dataByMonth[val][1] = dataByMonth[val][1] + timeBetween.days
                dataByMonth[val][2] = dataByMonth[val][2] + 1
        if yearNotInList:
            dataByMonth.append([i["launched"][0:4],timeBetween.days,1])
    
    #sort by year

    for iteration in dataByMonth:
        labels.append(iteration[0])
        returnData.append(iteration[1]/iteration[2])
        totalDates = iteration[2] + totalDates
        totalAverage = iteration[1] + totalAverage
    totalAverage = totalAverage/totalDates


    return labels, returnData, totalAverage

# ----- countProjects() -----
# Helper function for analytics, namely popularMonth().
# Passes in the datafile to be read.
# Calls on bad_date for input validation.
# Reads each entry, collects the date launched, and increments the corresponding list.
# Returns the completed dictionary.
# ----------------
def countProjects(dataFile):
    # list format: {Year}:[Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec]
    # each value represents the number of projects launched in that month for that year.
    retDict = {
        '2009':[0,0,0,0,0,0,0,0,0,0,0,0],
        '2010':[0,0,0,0,0,0,0,0,0,0,0,0],
        '2011':[0,0,0,0,0,0,0,0,0,0,0,0],
        '2012':[0,0,0,0,0,0,0,0,0,0,0,0],
        '2013':[0,0,0,0,0,0,0,0,0,0,0,0],
        '2013':[0,0,0,0,0,0,0,0,0,0,0,0],
        '2014':[0,0,0,0,0,0,0,0,0,0,0,0],
        '2015':[0,0,0,0,0,0,0,0,0,0,0,0],
        '2016':[0,0,0,0,0,0,0,0,0,0,0,0],
        '2017':[0,0,0,0,0,0,0,0,0,0,0,0],
        '2018':[0,0,0,0,0,0,0,0,0,0,0,0]}

    for item in dataFile:
        launchTime = item['launched'] # 2012-03-17 03:24:11
        if (bad_date(launchTime) == False): #checks to see if launch time is actually a date
            launchVals = launchTime.split('-') # ['2012', '03', '17 03:24:11']
            if (launchVals[0] != '1970'): # ignoring "start of time" projects
                retDict[launchVals[0]][(int(launchVals[1]) - 1)] += 1

    return retDict
# ----------------------------

def count_cat_fail_success(data):
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
    return category_names, category_failed_ratio




def count_categories_per_country(data):
    month_dict = {'01':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], '02':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        '03':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], '04':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], '05':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        '06':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], '07':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], '08':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        '09':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], '10':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], '11':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        '12':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
    categories = ['Games', 'Design', 'Technology', 'Film & Video', 'Music', 'Publishing',
        'Fashion', 'Food', 'Art', 'Comics', 'Photography', 'Theater', 'Crafts', 'Journalism',
        'Dance']
    #increments each category respectively
    for proj in data:
        projDate = proj['launched']
        if bad_date(projDate):
            continue
        projMonth = projDate[5:7]
        projCat = proj['main_category']
        catIndex = categories.index(projCat)
        month_dict[projMonth][catIndex] += 1
    return month_dict