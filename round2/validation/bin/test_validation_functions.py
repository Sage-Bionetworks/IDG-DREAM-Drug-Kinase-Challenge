#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 14:56:41 2019

@author: aelamb
"""

import unittest
import pandas as pd
import validation_functions as val
import synapseclient

syn = synapseclient.Synapse()
syn.login()

class TestMetrics(unittest.TestCase):
    def setUp(self):
        gs_entity = syn.get("syn16809884")
        self.gs_csv = gs_entity.path

        self.valid_csv = "test_files/valid.csv"
        self.valid_df = pd.read_csv(self.valid_csv)
        self.gs_df = pd.read_csv(self.gs_csv)
        self.combined_df = pd.merge(self.valid_df, self.gs_df, how='inner')
        
        self.missing_col_df = pd.read_csv("test_files/missing_col.csv")
        self.missing_two_col_df = pd.read_csv("test_files/missing_two_col.csv")
        self.extra_col_df = pd.read_csv("test_files/extra_col.csv")
        self.wrong_col_df = pd.read_csv("test_files/wrong_col.csv")
        self.bad_values_df = pd.read_csv("test_files/bad_values.csv")
        self.missing_row_df = pd.read_csv("test_files/missing_row.csv")
        self.duplicate_row_df = pd.read_csv("test_files/duplicate_row.csv")
        self.wrong_row_df = pd.read_csv("test_files/wrong_row.csv")
        
    def test_validate_submission_file(self):

        self.assertEqual(
            val.validate_submission_file(self.valid_csv, self.gs_csv),
            {"status": "", "reasons": []})

        self.assertEqual(
            val.validate_submission_file(None, self.gs_csv, "project"),
            {"status": "INVALID",
             "reasons": ["Expected FileEntity type but found project"]})

        self.assertEqual(
            val.validate_submission_file(
                    "test_files/invalid.tsv", self.gs_csv),
            {"status": "INVALID",
             "reasons": [(
                 "Error reading in submission file: " +
                 "Error tokenizing data. C error: " +
                 "Expected 1 fields in line 92, saw 2\n")]})

        self.assertEqual(
            val.validate_submission_file(
                    "test_files/rownums.csv", self.gs_csv),
            {"status": "INVALID",
             "reasons": [(
                 "Error reading in submission file: " +
                 "Error tokenizing data. C error: " +
                 "Expected 8 fields in line 92, saw 9\n")]})

        self.assertEqual(
            val.validate_submission_file(
                    "test_files/rownames.csv", self.gs_csv),
            {"status": "INVALID",
             "reasons": [(
                 "Error reading in submission file: " +
                 "Error tokenizing data. C error: " +
                 "Expected 8 fields in line 92, saw 9\n")]})

        self.assertEqual(
            val.validate_submission_file(
                    "test_files/missing_col.csv", self.gs_csv),
            {"status": "INVALID",
             "reasons": [(
                 "Submission file is missing column(s): pKd_[M]_pred")]})

        self.assertEqual(
            val.validate_submission_file(
                "test_files/missing_two_col.csv", self.gs_csv),
            {"status": "INVALID",
             "reasons": [(
                 "Submission file is missing column(s): " +
                 "UniProt_Id;pKd_[M]_pred")]})

        self.assertEqual(
            val.validate_submission_file(
                "test_files/extra_col.csv", self.gs_csv),
            {"status": "INVALID",
             "reasons": ["Submission file has extra column(s): extra_col"]})

        self.assertEqual(
            val.validate_submission_file(
                "test_files/wrong_col.csv", self.gs_csv),
            {"status": "INVALID",
             "reasons": [
                 "Submission file is missing column(s): pKd_[M]_pred",
                 "Submission file has extra column(s): extra_col",
                 ]})

        self.assertEqual(
            val.validate_submission_file(
                "test_files/bad_values.csv", self.gs_csv),
            {"status": "INVALID",
             "reasons": [
                 ("Submission file has non-numeric values in column " +
                  "pKd_[M]_pred at rows: 2;3;8;9;10"),
                 ("Submission file has infinite values in column " +
                  "pKd_[M]_pred at rows: 4;5"),
                 ("Submission file has values in one of or more " + 
                  "[Compound_SMILES, Compound_InchiKeys, Compound_Name, " + 
                  "UniProt_Id, Entrez_Gene_Symbol, DiscoveRx_Gene_Symbol] " + 
                  "that do not match template file.")
                 ]})
                 
        self.assertEqual(
            val.validate_submission_file(
                "test_files/missing_row.csv", self.gs_csv),
            {"status": "INVALID",
             "reasons": [
                 ("Submission file has values in one of or more " + 
                  "[Compound_SMILES, Compound_InchiKeys, Compound_Name, " + 
                  "UniProt_Id, Entrez_Gene_Symbol, DiscoveRx_Gene_Symbol] " + 
                  "that do not match template file.")
                 ]})

        self.assertEqual(
            val.validate_submission_file(
                "test_files/duplicate_row.csv", self.gs_csv),
            {"status": "INVALID",
             "reasons": [
                 ("Submission file has values in one of or more " + 
                  "[Compound_SMILES, Compound_InchiKeys, Compound_Name, " + 
                  "UniProt_Id, Entrez_Gene_Symbol, DiscoveRx_Gene_Symbol] " + 
                  "that do not match template file.")
                 ]})

        self.assertEqual(
            val.validate_submission_file(
                "test_files/wrong_row.csv", self.gs_csv),
            {"status": "INVALID",
             "reasons": [
                 ("Submission file has values in one of or more " + 
                  "[Compound_SMILES, Compound_InchiKeys, Compound_Name, " + 
                  "UniProt_Id, Entrez_Gene_Symbol, DiscoveRx_Gene_Symbol] " + 
                  "that do not match template file.")
                 ]})

        

    def test_check_entity_type(self):
        self.assertEqual(
            val.check_entity_type(
                {"status": "", "reasons": []}, self.valid_csv, "file"),
            {"status": "", "reasons": []})
        self.assertEqual(
            val.check_entity_type(
                {"status": "", "reasons": []}, None, "project"),
            {"status": "INVALID",
             "reasons": ["Expected FileEntity type but found project"]})

    def test_try_reading_file(self):
        self.assertEqual(
            val.try_reading_file(
                {"status": "", "reasons": []}, self.valid_csv)[0],
            {"status": "", "reasons": []})

        self.assertEqual(
            val.try_reading_file(
                {"status": "", "reasons": []}, "test_files/invalid.tsv")[0],
            {"status": "INVALID",
             "reasons": [(
                 "Error reading in submission file: " +
                 "Error tokenizing data. C error: " +
                 "Expected 1 fields in line 92, saw 2\n")]})

        self.assertEqual(
            val.try_reading_file(
                {"status": "", "reasons": []}, "test_files/rownums.csv")[0],
            {"status": "INVALID",
             "reasons": [(
                 "Error reading in submission file: " +
                 "Error tokenizing data. C error: " +
                 "Expected 8 fields in line 92, saw 9\n")]})

        self.assertEqual(
            val.try_reading_file(
                {"status": "", "reasons": []}, "test_files/rownames.csv")[0],
            {"status": "INVALID",
             "reasons": [(
                 "Error reading in submission file: " +
                 "Error tokenizing data. C error: " +
                 "Expected 8 fields in line 92, saw 9\n")]})

    def test_check_for_correct_columns(self):

        self.assertEqual(
            val.check_for_correct_columns(
                {"status": "", "reasons": []},
                self.valid_df),
            {"status": "", "reasons": []})

        self.assertEqual(
            val.check_for_correct_columns(
                {"status": "", "reasons": []},
                self.missing_col_df),
            {"status": "INVALID",
             "reasons": [(
                 "Submission file is missing column(s): pKd_[M]_pred")]})

        self.assertEqual(
            val.check_for_correct_columns(
                {"status": "", "reasons": []},
                self.missing_two_col_df),
            {"status": "INVALID",
             "reasons": [(
                 "Submission file is missing column(s): " +
                 "UniProt_Id;pKd_[M]_pred")]})

        self.assertEqual(
            val.check_for_correct_columns(
                {"status": "", "reasons": []},
                self.extra_col_df),
            {"status": "INVALID",
             "reasons": ["Submission file has extra column(s): extra_col"]})

        self.assertEqual(
            val.check_for_correct_columns(
                {"status": "", "reasons": []},
                self.wrong_col_df),
            {"status": "INVALID",
             "reasons": [
                 "Submission file is missing column(s): pKd_[M]_pred",
                 "Submission file has extra column(s): extra_col",
                 ]})

    def test_check_values(self):
        self.assertEqual(
            val.check_values(
                {"status": "", "reasons": []},
                self.valid_df, 
                self.gs_df),
            {"status": "", "reasons": []})
        self.assertEqual(
            val.check_values(
                {"status": "", "reasons": []},
                self.bad_values_df,
                self.gs_df),
            {"status": "INVALID",
             "reasons": [
                 ("Submission file has non-numeric values in column " +
                  "pKd_[M]_pred at rows: 2;3;8;9;10"),
                 ("Submission file has infinite values in column " +
                  "pKd_[M]_pred at rows: 4;5"),
                 ("Submission file has values in one of or more " + 
                  "[Compound_SMILES, Compound_InchiKeys, Compound_Name, " + 
                  "UniProt_Id, Entrez_Gene_Symbol, DiscoveRx_Gene_Symbol] " + 
                  "that do not match template file.")
                 ]})
                 
        self.assertEqual(
            val.check_values(
                {"status": "", "reasons": []},
                self.missing_row_df,
                self.gs_df),
            {"status": "INVALID",
             "reasons": [
                 ("Submission file has values in one of or more " + 
                  "[Compound_SMILES, Compound_InchiKeys, Compound_Name, " + 
                  "UniProt_Id, Entrez_Gene_Symbol, DiscoveRx_Gene_Symbol] " + 
                  "that do not match template file.")
                 ]})

        self.assertEqual(
            val.check_values(
                {"status": "", "reasons": []},
                self.duplicate_row_df,
                self.gs_df),
            {"status": "INVALID",
             "reasons": [
                 ("Submission file has values in one of or more " + 
                  "[Compound_SMILES, Compound_InchiKeys, Compound_Name, " + 
                  "UniProt_Id, Entrez_Gene_Symbol, DiscoveRx_Gene_Symbol] " + 
                  "that do not match template file.")
                 ]})

        self.assertEqual(
            val.check_values(
                {"status": "", "reasons": []},
                self.wrong_row_df,
                self.gs_df),
            {"status": "INVALID",
             "reasons": [
                 ("Submission file has values in one of or more " + 
                  "[Compound_SMILES, Compound_InchiKeys, Compound_Name, " + 
                  "UniProt_Id, Entrez_Gene_Symbol, DiscoveRx_Gene_Symbol] " + 
                  "that do not match template file.")
                 ]})

    def test_try_joining_dfs(self):        
        self.assertEqual(
            val.try_joining_dfs(
                {"status": "", "reasons": []}, 
                self.valid_df, 
                self.gs_df)[0],
            {"status": "", "reasons": []})


if __name__ == '__main__':
    unittest.main()
    