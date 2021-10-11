import json



def catagory_search(wanted_category):

    fileInstance = open('ks-projects-201801.json',encoding = "utf-8-sig")
    dictonary = json.load(fileInstance) #whole jason file in dictonary

    returnDictionary = {}

    for key in dictonary:
        if key['category'] == wanted_category:
            returnDictionary[key['ID']] = key

    fileInstance.close()
    return returnDictionary  #(at this point the return dictonary is loaded with every entry of the desired category)


def state_search(wanted_state):

    fileInstance = open('ks-projects-201801.json',encoding = "utf-8-sig")
    dictonary = json.load(fileInstance) 

    returnDictionary = {}

    for key in dictonary:
        if key['state'] == wanted_state:
            returnDictionary[key['ID']] = key

    fileInstance.close()
    return returnDictionary  #(at this point the return dictonary is loaded with every entry of the desiredstate)

def launched_month_search(wanted_month):#DATE MUST BE PASSED IN AS A STRING WITH FORMAT XX(example 01,11,12)

    fileInstance = open('ks-projects-201801.json',encoding = "utf-8-sig")
    dictonary = json.load(fileInstance) 

    returnDictionary = {}

    for key in dictonary:
        if key['launched'][5:6] == wanted_month:
            returnDictionary[key['ID']] = key

    fileInstance.close()
    return returnDictionary  #(at this point the return dictonary is loaded with every entry of the desiredstate)

def highest_usd_pledged_search():

    fileInstance = open('ks-projects-201801.json',encoding = "utf-8-sig")
    dictonary = json.load(fileInstance) 

    returnDictionary = {}
    largestNumber = float(0)

    for key in dictonary:
        if key['usd pledged'] != "": # makes sure that any empty usd pledged is ignored
            if float(key['usd pledged']) > largestNumber:
                returnDictionary[0] = key
                largestNumber = float(key['usd pledged'])
    
            

    fileInstance.close()
    return returnDictionary  #(at this point the return dictonary is loaded with every entry of the desiredstate)