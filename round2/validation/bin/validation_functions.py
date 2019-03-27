#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 08:28:54 2019

@author: aelamb
"""


import pandas as pd
import numpy as np
import json

LABEL_COLUMNS = [
    "Compound_SMILES", "Compound_InchiKeys", "Compound_Name", "UniProt_Id",
    "Entrez_Gene_Symbol", "DiscoveRx_Gene_Symbol"]
REQUIRED_COLUMNS = LABEL_COLUMNS + ["pKd_[M]_pred"]


def create_validation_json(submission_file, gs_file, entity_string):
    status = validate_submission_file(submission_file, gs_file, entity_string)
    if status["status"] == "":
        result = {'prediction_file_errors':"",
                  'prediction_file_status':"VALIDATED"}
    else:
        result = {'prediction_file_errors':"\n".join(status["reasons"]),
                  'prediction_file_status':"INVALID"}
    
    with open("results.json", 'w') as o:
        o.write(json.dumps(result))

def validate_submission_file(submission_file, gs_file, entity_string = "file"):
    status = {"status": "", "reasons": []}
    gs_df = pd.read_csv(gs_file)

    status = check_entity_type(status, submission_file, entity_string)
    if status["status"] == "INVALID":
        return status

    status, sub_df = try_reading_file(status, submission_file)
    if status["status"] == "INVALID":
        return status

    status = check_for_correct_columns(status, sub_df)
    if status["status"] == "INVALID":
        return status

    status = check_values(status, sub_df, gs_df)
    if status["status"] == "INVALID":
        return status

    status, combined_df = try_joining_dfs(status, sub_df, gs_df)
    if status["status"] == "INVALID":
        return status

    status = check_variation(status, combined_df)
    return status



def check_entity_type(status, submission_file, entity_string):
    if submission_file is None:
        message = 'Expected FileEntity type but found ' + entity_string
        status['status'] = "INVALID"
        status['reasons'].append(message)
    return status

def try_reading_file(status, submission_file):
    try:
        sub_df = pd.read_csv(submission_file)
    except Exception as error:
        message = "Error reading in submission file: " + str(error)
        sub_df = None
        status['status'] = "INVALID"
        status['reasons'].append(message)
    return(status, sub_df)

def check_for_correct_columns(status, sub_df):
    #print(REQUIRED_COLUMNS)
    missing_columns = [col for col in REQUIRED_COLUMNS
                       if col not in sub_df.columns]
    if len(missing_columns) > 0:
        status['status'] = "INVALID"
        message = (
            "Submission file is missing column(s): " +
            ";".join(missing_columns))
        status['reasons'].append(message)

    extra_columns = [col for col in sub_df.columns
                     if col not in REQUIRED_COLUMNS]
    if len(extra_columns) > 0:
        status['status'] = "INVALID"
        message = (
            "Submission file has extra column(s): " +
            ";".join(extra_columns))
        status['reasons'].append(message)
    return status

def check_values(status, sub_df, gs_df):
    values = sub_df["pKd_[M]_pred"]
    coerced_values = pd.to_numeric(values, errors='coerce')
    nan_values = values[np.isnan(coerced_values)]

    if len(nan_values) > 0:
        nan_index_list = nan_values.index.values.tolist()
        nan_string = ';'.join(str(i + 2) for i in nan_index_list)
        status['status'] = "INVALID"
        message = (
            "Submission file has non-numeric values in column pKd_[M]_pred " +
            "at rows: " +
            nan_string)
        status['reasons'].append(message)

    inf_values = values[np.isinf(coerced_values)]
    if len(inf_values) > 0:
        inf_index_list = inf_values.index.values.tolist()
        inf_string = ';'.join(str(i + 2) for i in inf_index_list)
        status['status'] = "INVALID"
        message = (
            "Submission file has infinite values in column pKd_[M]_pred " +
            "at rows: " +
            inf_string)
        status['reasons'].append(message)

    if not sub_df[LABEL_COLUMNS].equals(gs_df[LABEL_COLUMNS]):
        status['status'] = "INVALID"
        message = (
            "Submission file has values in one of or more [" +
            ", ".join(LABEL_COLUMNS) + "] that do not match template file.")
        status['reasons'].append(message)

    return status

def try_joining_dfs(status, sub_df, gs_df):
    try:
        combined_df = pd.merge(sub_df, gs_df, how='inner')
    except Exception as error:
        message = (
            "Error combing submission and gold standard file: " + str(error))
        combined_df = None
        status['status'] = "INVALID"
        status['reasons'].append(message)
    return(status, combined_df)

def check_variation(status, combined_df):
    if combined_df["pKd_[M]_pred"].var() == 0:
        message = (
            "After merging submission file and gold standard, pKd_[M]_pred " +
            "column has variance of 0.")
        status['status'] = "INVALID"
        status['reasons'].append(message)
    return(status)
    