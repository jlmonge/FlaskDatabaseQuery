import json



def catagory_search(wanted_category):

    fileInstance = open('WORKING-2018ksprojects.json',encoding = "utf-8-sig") 
    #fileInstance = open(r'parser\Files\output\2018ksprojects.json',encoding = "utf-8-sig")
    dictonary = json.load(fileInstance) #whole jason file in dictonary

    returnDictionary = list()

    for key in dictonary:
        if key['category'] == wanted_category:
            returnDictionary.append(key)

    fileInstance.close()
    return returnDictionary  #(at this point the return dictonary is loaded with every entry of the desired category)


def state_search(wanted_state):

    fileInstance = open('WORKING-2018ksprojects.json',encoding = "utf-8-sig")
    #fileInstance = open(r'parser\Files\output\2018ksprojects.json',encoding = "utf-8-sig")
    dictonary = json.load(fileInstance) 

    returnDictionary = list()

    for key in dictonary:
        if key['state'] == wanted_state:
            returnDictionary.append(key)

    fileInstance.close()
    return returnDictionary  #(at this point the return dictonary is loaded with every entry of the desiredstate)

def launched_month_search(wanted_month):#DATE MUST BE PASSED IN AS A STRING WITH FORMAT XX(example 01,11,12)

    fileInstance = open('WORKING-2018ksprojects.json',encoding = "utf-8-sig")
    #fileInstance = open(r'parser\Files\output\2018ksprojects.json',encoding = "utf-8-sig")
    dictonary = json.load(fileInstance) 

    returnDictionary = list()

    for key in dictonary:
        if key['launched'][0:7] == wanted_month:
            returnDictionary.append(key)

    fileInstance.close()
    return returnDictionary  #(at this point the return dictonary is loaded with every entry of the desiredstate)

def highest_usd_pledged_search():##FIX ME

    fileInstance = open('WORKING-2018ksprojects.json',encoding = "utf-8-sig")
    #fileInstance = open(r'parser\Files\output\2018ksprojects.json',encoding = "utf-8-sig")
    dictonary = json.load(fileInstance) 

    returnDictionary = [dictonary[0]]
    largestNumber = float(0)

    for key in dictonary:
        if key['usd pledged'] != "": # makes sure that any empty usd pledged is ignored
            if float(key['usd pledged']) > largestNumber:
                returnDictionary[0] = key
                largestNumber = float(key['usd pledged'])
    
            

    fileInstance.close()
    return returnDictionary  #(at this point the return dictonary is loaded with every entry of the desiredstate)
