import sys
sys.path.append('../../Analysis')
import unittest

from BasicStatAnalysis import *

class TestBasicStatAnalysis(unittest.TestCase):
    def test_analysis(self):
        # print("\nTest the function -- analysis")
        flag = True

        test_post = [
            {'_id': 1,
             'category': ['A', 'B'],
             'published': '1997-01-01',
             'author': [1, 3, 4]
             },
            {'_id': 3,
             'category': ['A', 'B'],
             'published': '1998-10',
             'author': [1, 5]
             },
            {'_id': 4,
             'category': ['A'],
             'published': '1997-11',
             'author': [1, 4, 6]
             }]

        test_post2 = [
            {'_id': 1,
             'category': ['A', 'B'],
             'year': 1997,
             'authors': [{'name': 1}, {'name': 3}, {'name': 4}]
            },
            {'_id': 3,
             'category': ['A', 'B'],
             'year': 1998,
             'authors': [{'name': 1}, {'name': 5}]
            },
            {'_id': 4,
             'category': ['A'],
             'year': 1997,
             'authors': [{'name': 1}, {'name': 4}, {'name': 6}]
            }]
        test_list1 = {1997: 2, 1998: 1}
        test_list2 = {1997: 0.5, 1998: 0.5}
        test_list3 = {1997: 4, 1998: 2}
        test_list4 = {1997: 3.0, 1998: 2.0}
        test_list5 = {1997: 1.5, 1998: 1.0}

        # arxiv
        m = 'arxiv'
        list1, list2, list3, list4, list5 = analysis(test_post, 'A', method = m)
        
        # compare two dictionary
        if(len(list1) == 2 and len(list2) == 2 and len(list3) == 2):
            for i in test_list1.keys():
                if (i not in list1.keys()) or list1[i] != test_list1[i]:
                    flag = False
                    break
            if flag:
                for i in test_list2.keys():
                    if (i not in list2.keys()) or list2[i] != test_list2[i]:
                        flag = False
                        break
            if flag:
                for i in test_list3.keys():
                    if (i not in list3.keys()) or list3[i] != test_list3[i]:
                        flag = False
                        break
            if flag:
                for i in test_list4.keys():
                    if i not in list4.keys() or list4[i] != test_list4[i]:
                        flag = False
                        break
            if flag:
                for i in test_list5.keys():
                    if i not in list5.keys() or list5[i] != test_list5[i]:
                        flag = False
                        break

        # for mag
        m = 'mag'
        list1, list2, list3, list4, list5 = analysis(test_post2, 'A', method = m)
        # compare two dictionary
        if flag:
            if(len(list1) == 2 and len(list2) == 2 and len(list3) == 2):
                for i in test_list1.keys():
                    if (i not in list1.keys()) or list1[i] != test_list1[i]:
                        flag = False
                        break
                if flag:
                    for i in test_list2.keys():
                        if (i not in list2.keys()) or list2[i] != test_list2[i]:
                            flag = False
                            break
                if flag:
                    for i in test_list3.keys():
                        if (i not in list3.keys()) or list3[i] != test_list3[i]:
                            flag = False
                            break
                if flag:
                    for i in test_list4.keys():
                        if i not in list4.keys() or list4[i] != test_list4[i]:
                            flag = False
                            break
                if flag:
                    for i in test_list5.keys():
                        if i not in list5.keys() or list5[i] != test_list5[i]:
                            flag = False
                            break

        self.assertTrue(flag)

    def test_loadData(self):
        # print("\nTest the function -- loadData")
        flag = False
        # test whether the mongo url is right
        test_url = "mongodb://146.169.45.150:3306/arxiv"
        mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
        # test the second parameter: 'stat.ML', 'econ.EM'
        category1 = 'stat.ML'
        category2 = 'econ.EM'
        try:
            data = loadData(test_url, category1)
            res = data.find({})
            data = loadData(test_url, category2)
            res = data.find({})
        except Exception:
            flag = True

        if flag:
            flag = False
            try:
                data1 = loadData(mongo_url, category1)
                # test the first paper get from the mongo database
                for i in data1[0]['category']:
                    if i == category1:
                        flag = True
                        break

                if flag:
                    flag = False
                    data2 = loadData(mongo_url, category2)
                    for i in data2[0]['category']:
                       if i ==  category2:
                           flag = True
                           break

            except Exception:
                flag = False
        self.assertTrue(flag)

    def test_basic_stat_analysis(self):
        # print("\nTest the function -- basic_stat_analysis")
        flag = True
        mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
        test_list1 = {2018: 60, 2017: 59}
        test_list2 = {2018: 0.4918032786885246, 2017: 0.48760330578512395}
        test_list3 = {2018: 122, 2017: 121}
        test_list4 = {2018: 2.25, 2017: 2.305084745762712}
        test_list5 = {2018: 1.1065573770491803, 2017: 1.1239669421487604}
        list1, list2, list3, list4, list5 = basic_stat_analysis(mongo_url, 'econ.EM')
        # print(list1, list2, list3, list4, list5)
        # compare two dictionary
        if(len(list1) == 2 and len(list2) == 2 and len(list3) == 2):
            for i in test_list1.keys():
                if (i not in list1.keys()) or list1[i] != test_list1[i]:
                    flag = False
                    break
            if flag:
                for i in test_list2.keys():
                    if (i not in list2.keys()) or abs(list2[i] - test_list2[i]) > 0.00001:
                        flag = False
                        break
            if flag:
                for i in test_list3.keys():
                    if (i not in list3.keys()) or list3[i] != test_list3[i]:
                        flag = False
                        break
            if flag:
                for i in test_list4.keys():
                    if i not in list4.keys() or abs(list4[i] - test_list4[i]) > 0.00001:
                        flag = False
                        break
            if flag:
                for i in test_list5.keys():
                    if i not in list5.keys() or abs(list5[i] - test_list5[i]) > 0.00001:
                        flag = False
                        break

        self.assertTrue(flag)

if __name__ == "__main__":
    unittest.main()
