import unittest
import sys
sys.path.append('../../Analysis')

import Analysis as aly

class TestGraphSystem(unittest.TestCase):
    
    def test_loadMongoConnection(self):

        wrong_domain = "mongod://xxx@xxx:xxx/arxiv"
        wrong_login = "mongodb://xxx:xxx@xxx:xxx/arxiv"
        correct_login = "mongodb://xxx:xxx@xxx:xxx/arxiv"
        control_category = "stat.ML"
        
        self.assertRaises(Exception, aly.loadMongo, wrong_domain, control_category)
        self.assertRaises(Exception, aly.loadMongo, wrong_login,control_category)

        
if __name__ == '__main__':
    unittest.main()
    
