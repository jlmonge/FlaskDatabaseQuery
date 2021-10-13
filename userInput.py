# This is the file to make forms. Forms organized collections of user data.
# a good example of a form is registration. A registration form will accept 
#   and check a username and password.

#The information collected on a form will be added to a database


class exampleForm:#very basic form. It does not error check.
    def __init__(self, passedName):
        self.id = passedName