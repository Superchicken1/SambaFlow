import os, sys, inspect
sys.path.insert(1, os.path.join(sys.path[0],'..'))
import unittest
import math
import numpy as np
import pandas as pd
from test import test_path as path
import src.misc.split_train_valid as split

"""
Test method for split_train_valid.py
"""
class TestDatasetSplit(unittest.TestCase):

    #def setUp(self):
        #df1 = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])
    
    def test_real_dataset(self):
        #load trajectories file
        df1 = pd.DataFrame.from_csv(path.trajectories_training_file2, index_col=[0,1,2])
        train_df, valid_df, test_df = split.split_dataset(df1, 0.7, 0.1)
        self.assertEquals(len(train_df.index) + len(test_df.index) + len(valid_df.index), len(df1.index))
        #It's ok if it diverges by 1, because that is in the margin of randomness
        self.assertTrue(len(train_df.index) - int(len(df1.index) <= 1))
        self.assertTrue(len(valid_df.index) - int(len(df1.index) <= 1))
        self.assertTrue(len(test_df.index) - int(len(df1.index) <= 1))

    def test_normal_split(self):       
        df1 = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])
        train_df, valid_df, test_df = split.split_dataset(df1, 0.6, 0.2)
        self.assertEquals(len(train_df.index) + len(test_df.index) + len(valid_df.index), len(df1.index))
        self.assertEquals(len(train_df.index), 6)
        self.assertEquals(len(valid_df.index), 2)
        self.assertEquals(len(test_df.index), 2)


    def test_no_validation_set(self):
        df1 = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])
        train_df, valid_df, test_df = split.split_dataset(df1, 0.6, 0.0)
        self.assertEquals(len(train_df.index) + len(test_df.index), len(df1.index))
        self.assertEquals(len(train_df.index), 6)
        self.assertEquals(valid_df, pd.DataFrame.empty)
        self.assertEquals(len(test_df.index), 4)


    def test_wrong_params(self):
        df1 = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])
        """
        Validation set has a parameter that is too big
        """
        self.assertRaises(ValueError, lambda: split.split_dataset(df1, 0.6, 0.6))

if __name__ == '__main__':
    unittest.main()
