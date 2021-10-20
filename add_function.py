import json
#from os import get_exec_path, set_inheritable


#pass in strings or the format of the JSON WILL NOT HAVE STRINGS IN IT !!
def add_to_json(ID, name, category, main_category, currency, deadline, goal, launched, pledged, state, backers, country, usd_pledged, usd_pledged_real ):

    filename = 'WORKING-2018ksprojects.json'
    entry = {
        "ID": ID,
		"name": name,
		"category": category,
		"main_category": main_category,
		"currency": currency,
		"deadline": deadline,
		"goal": goal,
		"launched": launched,
		"pledged": pledged,
		"state": state,
		"backers": backers,
		"country": country,
		"usd pledged": usd_pledged,
		"usd_pledged_real": usd_pledged_real}
    # 1. Read file contents
    with open(filename, "r") as file:
        data = json.load(file)
    # 2. Update json object
    data.append(entry)
    # 3. Write json file
    with open(filename, "w") as file:
        json.dump(data, file)

#test case
#add_to_json("999320001988282","TEST69420", "Performance Art", "Art", "USD", "2011-08-16","2000.00", "2011-07-19 09:07:47","524.00","failed", "17", "US", "524.00", "524.00")