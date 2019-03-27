#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:44:52 2019

@author: aelamb
"""

import argparse
import validation_functions as val


parser = argparse.ArgumentParser()

parser.add_argument(
    "-e", 
    "--entity_type",
    required=True, 
    help="synapse entity type downloaded")

parser.add_argument(
    "-s",
    "--submission_file",
    help="Submission File")

parser.add_argument(
    "-g",
    "--goldstandard_file",
    required=True,
    help="Goldstandard for scoring")

args = parser.parse_args()

if __name__ == '__main__':
    val.create_validation_json(
        args.submission_file, 
        args.goldstandard_file, 
        args.entity_type)
    