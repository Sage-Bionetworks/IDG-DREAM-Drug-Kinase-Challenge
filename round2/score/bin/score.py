#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:44:52 2019

@author: aelamb
"""

import argparse
import json
import pandas as pd
import evaluation_metrics as ev



parser = argparse.ArgumentParser()

parser.add_argument(
    "-i",
    "--submission_file",
    required=True,
    help="Submission File")

parser.add_argument(
    "-g",
    "--goldstandard_file",
    required=True,
    help="Goldstandard for scoring")

parser.add_argument(
    "-s",
    "--status",
    required=True,
    help="current submission status")

args = parser.parse_args()


args = parser.parse_args()

if __name__ == '__main__':
    
    
    if args.status == "VALIDATED":
        sub_df = pd.read_csv(args.submission_file)
        gs_df = pd.read_csv(args.goldstandard_file)
        combined_df = pd.merge(sub_df, gs_df, how='inner')
        actual = combined_df["pKd_[M]"]
        predicted = combined_df["pKd_[M]_pred"]
        
        rmse = ev.rmse(actual, predicted)
        spearman = ev.spearman(actual, predicted)
        average_auc = ev.average_AUC(actual, predicted)
        
        rounded_rmse = round(rmse, 3)
        rounded_spearman = round(spearman, 3)
        rounded_average_auc = round(average_auc, 3)
        
        result = {
            "prediction_file_status":"SCORED",
            "rmse": rmse,
            "spearman": spearman,
            "average_auc": average_auc,
            "rounded_rmse": rounded_rmse,
            "rounded_spearman": rounded_spearman,
            "rounded_average_auc": rounded_average_auc}
            
    else:
        result = {"prediction_file_status":"INVALID"}

    with open("results.json", 'w') as o:
        o.write(json.dumps(result))
    