#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 14:56:41 2019

@author: aelamb
"""

import unittest
import synapseclient
import pandas as pd
import evaluation_metrics as ev


syn = synapseclient.Synapse()
syn.login()

class TestMetrics(unittest.TestCase):
    
    def setUp(self):
        gs_entity = syn.get("syn16809884")
        self.gs_csv = gs_entity.path
        self.gs_df = pd.read_csv(self.gs_csv)
  
        
        self.sub_df = pd.read_csv("test_files/valid.csv")
        self.combined_df = pd.merge(self.sub_df, self.gs_df, how='inner')
        self.actual = self.combined_df["pKd_[M]"]
        self.predicted = self.combined_df["pKd_[M]_pred"]

    def test_rmse(self):
        self.assertEqual(ev.rmse(self.actual, self.predicted), 
                         1.282081879551014)
        
    def test_spearman(self):
        self.assertEqual(ev.spearman(self.actual, self.predicted), 
                         0.37569026743498013)
        
    def test_average_AUC(self):
        self.assertEqual(ev.average_AUC(self.actual, self.predicted), 
                         0.6676370366341904)


if __name__ == '__main__':
    unittest.main()
    