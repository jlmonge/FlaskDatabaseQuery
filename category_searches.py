import json

def search_helper(wanted_key, wanted_value):
    fileInstance = open('ks-projects-201801.json',encoding = "utf-8-sig") 
    #fileInstance = open(r'parser\Files\output\2018ksprojects.json',encoding = "utf-8-sig")
    data = json.load(fileInstance) #whole json file in data

    projs = []

    for proj in data:
        if wanted_value in proj[f'{wanted_key}']:
            projs.append(proj)

    fileInstance.close()
    return projs  # at this point the return data is loaded with every entry of the 
    #desired category


def category_search(wanted_category):
    return search_helper("category", wanted_category)

def state_search(wanted_state):
    return search_helper("state", wanted_state)

def launched_month_search(wanted_month):#DATE MUST BE PASSED IN AS A STRING WITH FORMAT XX(example 01,11,12)
    fileInstance = open('ks-projects-201801.json',encoding = "utf-8-sig")
    #fileInstance = open(r'parser\Files\output\2018ksprojects.json',encoding = "utf-8-sig")
    data = json.load(fileInstance) 

    projs = []

    for proj in data:
        if proj['launched'][0:7] == wanted_month:
            projs.append(proj)

    fileInstance.close()
    return projs  #(at this point the return data is loaded with every entry of the desiredstate)

def highest_usd_pledged_search():##FIX ME
    fileInstance = open('ks-projects-201801.json',encoding = "utf-8-sig")
    #fileInstance = open(r'parser\Files\output\2018ksprojects.json',encoding = "utf-8-sig")
    data = json.load(fileInstance) 

    projs = [data[0]]
    largestNumber = float(0)

    for proj in data:
        if proj['usd pledged'] != "": # makes sure that any empty usd pledged is ignored
            if float(proj['usd pledged']) > largestNumber:
                projs[0] = proj
                largestNumber = float(proj['usd pledged'])

    fileInstance.close()
    return projs  #(at this point the return data is loaded with every entry of the desired state)