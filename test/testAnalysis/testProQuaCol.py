import unittest

import sys
sys.path.append('../../Analysis')

import ProQuaCol as pqc

class TestBasicFunction(unittest.TestCase):
  def testProQuaCol(self):
    trueFlag = True
    startYear = 2014
    endYear = 2016
    collectionName = 'astrophysics'
    graphFile = '../../pickle_file/mag_spec_cn_graph_astrophysics.pkl'
    sampleNo = 20
    outputFileName = 'unittestProQuaColpklFile.pkl'
    try:
        pqc.getOneCategory(startYear, endYear, collectionName, graphFile, sampleNo, outputFileName)
    except Exception as e:
        trueFlag = False

        self.assertTrue(trueFlag)


if __name__ == '__main__':
    unittest.main()
