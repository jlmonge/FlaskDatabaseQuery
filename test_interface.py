#this file will contain all the functions that test the analytic functions from analytic_functions.py

from app_interface import loadJsonFile
from analytic_functions import average_length_ks, most_funded_category_per_year, count_words, count_cat_fail_success, count_categories_per_month#other analytic function here

global data


class most_funded_category_per_year_test():
    def run_all(self):
        self.single_ks()
        self.empty_file()
        self.multiple_ks_for_same_year()
        self.multiple_ks_for_multiple_years()

    def single_ks(self):#tests list with a single value
        mockData = [{ "main_category": "Music" , "pledged": "2381.00" , "launched": "2016-05-27 15:44:55"}]
        test = most_funded_category_per_year('2016', mockData)
        assert (test[0] == 2381.0 ),"With only one ks, we pass back its pledge amount"
        assert (test[1] == "Music"), "With only one ks, the average is the length of the ks"

    def empty_file(self):#tests list with a single value
        mockData = [{}]
        test = most_funded_category_per_year('2016', mockData)
        assert (test == "" ),"With empty dataset funciton returns empty string"

    def multiple_ks_for_same_year(self):
        mockData = [{ "main_category": "Music" , "pledged": "2381.00" , "launched": "2016-05-27 15:44:55"} , {"main_category": "Music", "pledged": "400.00" , "launched": "2016-01-05 15:46:50"} , {"main_category": "Art", "pledged": "400.00" , "launched": "2016-01-05 15:46:50"} ]
        test = most_funded_category_per_year('2016', mockData)
        #returns the sums of the one in a given year who has the highest is the main_category
        assert (test[0] == 2781.0 ),"With only one ks, we pass back its pledge amount" 
        assert (test[1] == "Music"), "With only one ks, the average is the length of the ks"

    def multiple_ks_for_multiple_years(self):
        mockData = [{ "main_category": "Music" , "pledged": "2381.00" , "launched": "2016-05-27 15:44:55"} , {"main_category": "Music", "pledged": "400.00" , "launched": "2016-01-05 15:46:50"} , {"main_category": "Art", "pledged": "400.00" , "launched": "2016-01-05 15:46:50"}, {"main_category": "Music", "pledged": "400.00" , "launched": "2014-01-05 15:46:50"}, {"main_category": "Music", "pledged": "400.00" , "launched": "2015-01-05 15:46:50"}, {"main_category": "Music", "pledged": "4000.00" , "launched": "2016-01-05 15:46:50"}]
        test = most_funded_category_per_year('2016', mockData)
        #returns the sums of the one in a given year who has the highest is the main_category
        assert (test[0] == 6781.0 ),"With only one ks, we pass back its pledge amount" 
        assert (test[1] == "Music"), "With only one ks, the average is the length of the ks"

class count_cat_fail_success_test():
    def run_all(self):
        self.single_ks()
        self.empty_file()
        self.several_ks_one_cat()
        self.several_ks_multiple_cat()

    def single_ks(self):#tests list with a single value
        mockData = [{ "main_category": "Music" , "state": "failed"}]
        test = count_cat_fail_success(mockData)
        assert (test == (['Games', 'Design', 'Technology', 'Film & Video', 'Music', 'Publishing', 'Fashion', 'Food', 'Art', 'Comics', 'Photography', 'Theater', 'Crafts', 'Journalism', 'Dance'], [0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])),"With 1 failed in music, music should have a fail ratio of 1 and result should be default or zero it returns the default dictionary"

    def empty_file(self):
        mockData = [{}]
        test = count_cat_fail_success(mockData)
        assert ( test == [{}] ), "With nothing it should return the empty"

    def several_ks_one_cat(self):
        mockData = [{ "main_category": "Music" , "state": "failed"}, { "main_category": "Music" , "state": "failed"}, { "main_category": "Music" , "state": "successful"}, { "main_category": "Music" , "state": "successful"}]
        test = count_cat_fail_success(mockData)
        #will be just testing the ratios
        assert ( test[1][4] == 0.5 ), "2 successful and 2 fails should have music's ratio at 0.5"

    def several_ks_multiple_cat(self):
        mockData = [{ "main_category": "Music" , "state": "failed"}, 
        { "main_category": "Music" , "state": "failed"}, { "main_category": "Music" , "state": "successful"}, 
        { "main_category": "Music" , "state": "successful"}, { "main_category": "Games" , "state": "successful"}, 
        { "main_category": "Games" , "state": "successful"}, { "main_category": "Games" , "state": "successful"}, 
        { "main_category": "Games" , "state": "successful"}, { "main_category": "Games" , "state": "successful"}, 
        { "main_category": "Games" , "state": "successful"}, { "main_category": "Games" , "state": "failed"}, 
        { "main_category": "Games" , "state": "failed"},{ "main_category": "Games" , "state": "successful"} , 
        { "main_category": "Games" , "state": "failed"}, { "main_category": "Design" , "state": "failed"}, 
        { "main_category": "Design" , "state": "failed"}, { "main_category": "Design" , "state": "failed"},
        { "main_category": "Design" , "state": "successful"}] 
        test = count_cat_fail_success(mockData)
        #will be just testing the ratios
        assert ( test[1][4] == 0.5 ), "2 successful and 2 fails should have music's ratio at 0.5"
        assert ( test[1][0] == 0.3 ), "7 successful and 3 fails should have music's ratio at 0.3"
        assert ( test[1][1] == 0.75 ), "1 successful and 3 fails should have music's ratio at 0.75"

class count_words_test():
    def run_all(self):
        self.single_ks()
        self.single_ks_fail()
        self.empty_file()
        self.multiple_ks_for_same_succ()
        self.multiple_ks_for_multiple_years_both()

    def single_ks(self):#tests list with a single value
        mockData = [ {"name": "Egidio Scognamillo: Realize a dream to change a life life life dream", "state": "successful"} ]
        labels = count_words(mockData)
        assert (labels[0][0] == "life"),"With one ks pass back life because it occurs 3 times"
        assert (labels[0][1] == "dream"),"With one ks pass back life because it occurs 2 times"
        assert (labels[1][0] == 3), "With one ks, life occurs 3 times"
        assert (labels[1][1] == 2), "With one ks, dream occurs 2 times"

    def single_ks_fail(self):#tests list with a single value
        mockData = [ {"name": "Egidio Scognamillo: Realize a dream to change a life life life dream", "state": "failed"} ]
        test = count_words(mockData)
        assert (test == ([], [])),"With no successful projects it returns nothing"

    def empty_file(self):#tests list with a single value
        mockData = [ {} ]
        test = count_words(mockData)
        assert (test == ([], [])),"With no projects it returns nothing"
    
    def multiple_ks_for_same_succ(self):
        mockData = [ {"name": "Egidio Scognamillo: Realize a dream to change a life life life dream", "state": "successful"}, {"name": "Egidio Scognamillo: Realize a dream to change a life life life dream", "state": "successful"}]
        labels = count_words(mockData)
        assert (labels[0][0] == "life"),"With one ks pass back life because it occurs 6 times"
        assert (labels[0][1] == "dream"),"With one ks pass back life because it occurs 4 times"
        assert (labels[1][0] == 6), "With one ks, life occurs 6 times"
        assert (labels[1][1] == 4), "With one ks, dream occurs 4 times"

    def multiple_ks_for_multiple_years_both(self):
        mockData = [ {"name": "Egidio Scognamillo: Realize a dream to change a life life life dream", "state": "successful"}, {"name": "Egidio Scognamillo: Realize a dream to change a life life life dream", "state": "successful"}, {"name": "Egidio Scognamillo: Realize a dream to change a life life life dream", "state": "failed"}]
        labels = count_words(mockData)
        assert (labels[0][0] == "life"),"With one ks pass back life because it occurs 6 times"
        assert (labels[0][1] == "dream"),"With one ks pass back life because it occurs 4 times"
        assert (labels[1][0] == 6), "With one ks, life occurs 6 times"
        assert (labels[1][1] == 4), "With one ks, dream occurs 4 times"

class count_categories_per_month_test():
    def run_all(self):
        self.single_ks()
        self.empty_file()
        self.multiple_ks_for_same_month()
        self.multiple_ks_for_multiple_months()

    def single_ks(self):
        mockData = [ {"main_category": "Music","launched": "2012-08-02 14:11:32"} ]
        test = count_categories_per_month(mockData)
        assert (test['08'][4] == 1),"added to music on aug so count for music aug should be 1"
    
    def empty_file(self):
        mockData = [{}]
        test = count_categories_per_month(mockData)
        assert (test == [{}]),"empty dict returns empty"
    
    def multiple_ks_for_same_month(self):
        mockData = [ {"main_category": "Music","launched": "2012-08-02 14:11:32"}, {"main_category": "Music","launched": "2012-08-04 14:11:32"}, {"main_category": "Design","launched": "2012-08-02 14:11:32"}, {"main_category": "Games","launched": "2012-08-02 14:11:32"} ]
        test = count_categories_per_month(mockData)
        assert (test['08'][4] == 2),"added to 2 music on aug so count for music aug should be 2"
        assert (test['08'][0] == 1),"added to 1 game on aug so count for Games aug should be 1"
        assert (test['08'][1] == 1),"added to design on aug so count for Design aug should be 1"

    def multiple_ks_for_multiple_months(self):
        mockData = [ {"main_category": "Music","launched": "2012-08-02 14:11:32"}, {"main_category": "Music","launched": "2012-08-04 14:11:32"}, 
        {"main_category": "Design","launched": "2012-08-02 14:11:32"}, {"main_category": "Games","launched": "2012-08-02 14:11:32"}, 
        {"main_category": "Design","launched": "2012-10-02 14:11:32"}, {"main_category": "Games","launched": "2012-09-02 14:11:32"},
        {"main_category": "Design","launched": "2012-10-02 14:11:32"}, {"main_category": "Games","launched": "2012-10-02 14:11:32"},
        {"main_category": "Design","launched": "2012-12-02 14:11:32"}, {"main_category": "Games","launched": "2012-12-02 14:11:32"}]
        test = count_categories_per_month(mockData)
        assert (test['08'][4] == 2),"added to 2 music on aug so count for music aug should be 2"
        assert (test['08'][0] == 1),"added to 1 game on aug so count for Games aug should be 1"
        assert (test['08'][1] == 1),"added to design on aug so count for Design aug should be 1"
        assert (test['09'][0] == 1),"added 1 game on sept so count is 1"
        assert (test['10'][0] == 1),"added 1 game on oct so count is 1"
        assert (test['12'][0] == 1),"added 1 game on dec so count is 1"
        assert (test['10'][1] == 2),"added 2 design on oct so count is 2"
        assert (test['12'][1] == 1),"added 1 design on dec so count is 1"

    

test = most_funded_category_per_year_test()
test.run_all()

test = count_words_test()
test.run_all()

test = count_cat_fail_success_test()
test.run_all()

test = count_categories_per_month_test()
test.run_all()