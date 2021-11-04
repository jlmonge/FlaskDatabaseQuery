#this file will contain all the functions that test the analytic functions from analytic_functions.py

from app_interface import loadJsonFile
from analytic_functions import * #other analytic function here

global data


class pop_cat_perNationTests:
    def run_all(self):
        self.single_Entry()


    def single_Entry(self):
        mockData = [{ 'country': 'GB', 'main_category': 'Publishing'}]
        test_dict = get_countrys_category(mockData)
        assert(list(test_dict.keys())[0] == 'GB'),"One entry in the dictionary allows the test"
        assert(dict.get('GB')[5] == 1),"Tests whether the index of Publishing goes up"

pop_cat_perNationTests_obj = pop_cat_perNationTests()
pop_cat_perNationTests_obj.run_all()