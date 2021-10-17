# This is the file to make forms. Forms organized collections of user data.
# a good example of a form is registration. A registration form will accept 
#   and check a username and password.

#The information collected on a form will be added to a database


class exampleForm:#very basic form. It does not error check.
    def __init__(self, passedName):
        self.nm = passedName


class kickStarterForm:
    
    def empty_error(self):
        if self.id == "":
            return "error: empty id"
        if self.name == "":
            return "error: empty name"
        if self.category == "":
            return "error: empty category"
        if self.main_category == "":
            return "error: empty main_category"
        if self.currency == "":
            return "error: empty currency"
        if self.deadline == "":
            return "error: empty deadline"
        if self.goal == "":
            return "error: empty goal"
        if self.date_launched == "":
            return "error: empty date_launched"
        if self.number_pledged == "":
            return "error: empty number_pledged"
        if self.state == "":
            return "error: empty state"
        if self.number_backers == "":
            return "error: empty number_backers"
        if self.country == "":
            return "error: empty country"
        if self.amount_usd_pledged == "":
            return "error: empty amount_usd_pledged"
        return "passed"

    def errorRunner(self):
        errorList = list()#create an instant of the errorList to pass back
        currentError = ""#use it to track the current error
        currentError = empty_error()
        if currentError != "passed": #if an error does not return "passed" we append it to the list.
            errorList.append(currentError)
        #other errors are placed below here to be ran on form init





    def __init__(self,id,name,category,main_category,currency,deadline,goal,date_launched,number_pledged,state,number_backers,country,amount_usd_pledged):
        self.id = id #print
        self.name = name #print
        self.category = category #print
        self.main_category = main_category #print
        self.currency = currency #the type of currency
        self.deadline = deadline
        self.date_launched = date_launched
        self.number_pledged = number_pledged #the number of times someone has pledged
        self.state = state
        self.number_backers = number_backers
        self.country = country
        self.amount_usd_pledged = amount_usd_pledged# the actual cash
        self.error_msgs = errorRunner()#if error_msg is not equal to "passed" then an error occured



    
