from datetime import date


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


