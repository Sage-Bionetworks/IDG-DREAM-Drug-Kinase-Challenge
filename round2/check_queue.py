#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 09:32:30 2019

@author: aelamb
"""

import synapseclient
import challengeutils

queue = "evaluation_9614079"


syn = synapseclient.Synapse(configPath=".synapseConfig")
syn.login()

query = (
    "select objectId from " + queue + " where status ==  'ACCEPTED' and " + 
    "prediction_file_status == 'INVALID'")
generator = challengeutils.utils.evaluation_queue_query(syn, query)
lst = list(generator)

for dct in lst:
    print("id: " + dct['objectId'])
    status = syn.getSubmissionStatus(dct['objectId'])
    status.status = 'INVALID'
    syn.store(status)

