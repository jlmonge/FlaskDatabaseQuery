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

