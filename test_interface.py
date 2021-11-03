#this file will contain all the functions that test the analytic functions from analytic_functions.py

from app_interface import loadJsonFile
from analytic_functions import average_length_ks, most_funded_category_per_year, gatherYears, findAmbitious #other analytic function here

global data

class testSuite_mostAmbitious:
    # Necessary details: ID, Goal, Pledged, Launch
    badList = [
        {'ID:':'10250','goal':'999.99','pledged':'990.00','launched':'1970-12-01 18:30:44'}, # Invalid year
        {'ID:':'10251','goal':'111.99','pledged':'190.00','launched':'2036-13-01 18:31:44'}, # Invalid month
        {'ID:':'10252','goal':'888.22','pledged':'0.00','launched':'2009-09-00 18:32:44'}, # Invalid day
    ]
    emptyList = [{}]
    mockList = [
        {'ID':'10253','goal':'10000.00','pledged':'9999.00','launched':'2021-11-01 18:33:44'}, # Note misorder of years
        {'ID':'10254','goal':'1000.00','pledged':'10000.00','launched':'2015-11-02 18:34:44'},
        {'ID':'10255','goal':'1100.00','pledged':'15000.00','launched':'2018-11-02 18:35:44'},
        {'ID':'10256','goal':'1200.00','pledged':'14000.00','launched':'2010-11-02 18:36:44'},
        {'ID':'10257','goal':'20000.00','pledged':'10000.00','launched':'2015-11-20 18:37:44'} # Higher goal than 10254
    ]
    def run_all(self):
        self.run_years()
        self.run_ambit()

    # gatherYears Test Suite
    def run_years(self):
        self.years_empty()
        self.years_bad()
        self.years_mock()
    def years_empty(self):
        assert(gatherYears(self.emptyList).pop(0) == IndexError)
    def years_bad(self):
        assert(gatherYears(self.badList).pop(0) == IndexError)
    def years_mock(self):
        expectedList = ['2010','2015','2018','2021']
        assert(gatherYears(self.mockList) == expectedList)

    # findAmbitious Test Suite
    def run_ambit(self):
        self.ambit_empty()
    def ambit_empty(self):
        assert(findAmbitious(self.emptyList).popitem() == IndexError)
    def ambit_bad(self):
        assert(findAmbitious(self.badList).popitem() == IndexError)
    def ambit_mock(self):
        expectedDict = {
            '2010-11':[10256,1200,14000],
            '2015-11':[10257,20000,10000], # 10254 is ignored
            '2018-11':[10255,1100,15000],
            '2021-11':[10253,10000,9999]
        }
        testDict = findAmbitious(self.mockList)
        for item in testDict:
            assert(testDict.popitem() == expectedDict.popitem())

testSuite_mostAmbitious_object = testSuite_mostAmbitious()
testSuite_mostAmbitious_object.run_all()