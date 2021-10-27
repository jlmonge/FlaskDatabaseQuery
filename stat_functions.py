from datetime import date
def average_length_ks(pyfile):
    labels = list() #labels for each datapoint
    returnData = list() #datapoints(average length per year)
    totalAverage = 0
    totalDates = 0
    dataByMonth = list() #
    #listValues = ["year",0.0,0]#"year or total", sum of lengths, number of values
    for i in pyfile:
        #print(i["launched"][0:4] + "-" + i["launched"][5:7] + "-" + i["launched"][8:10])
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