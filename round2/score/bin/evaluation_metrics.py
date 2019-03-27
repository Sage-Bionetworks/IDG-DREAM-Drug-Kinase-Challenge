"""
Created on Fri Sep  7 14:38:29 2018

@author: Anna Cichonska
"""

import numpy as np
import copy
from math import sqrt
from scipy import stats
from sklearn import preprocessing, metrics


def rmse(y, f):
    """
    Task:    To compute root mean squared error (RMSE)
    Input:   y: Vector with original labels (pKd [M])
             f: Vector with predicted labels (pKd [M])
    Output:  rmse   RSME
    """

    rmse = sqrt(((y - f)**2).mean(axis=0))
    return rmse

def spearman(y, f):
    """
    Task:    To compute Spearman's rank correlation coefficient

    Input:   y      Vector with original labels (pKd [M])
             f      Vector with predicted labels (pKd [M])

    Output:  rs     Spearman's rank correlation coefficient
    """

    rs = stats.spearmanr(y, f)[0]
    return rs


def average_AUC(y,f):

    """
    Task:    To compute average area under the ROC curves (AUC) given ten
             interaction threshold values from the pKd interval [6 M, 8 M]
             to binarize pKd's into true class labels.

    Input:   y      Vector with original labels (pKd [M])
             f      Vector with predicted labels (pKd [M])

    Output:  avAUC   average AUC

    """

    thr = np.linspace(6,8,10)
    auc = np.empty(np.shape(thr)); auc[:] = np.nan

    for i in range(len(thr)):
        y_binary = copy.deepcopy(y)
        y_binary = preprocessing.binarize(
                y_binary.values.reshape(1,-1), 
                threshold=thr[i], 
                copy=False)[0]
        fpr, tpr, thresholds = metrics.roc_curve(y_binary, f, pos_label=1)
        auc[i] = metrics.auc(fpr, tpr)

    avAUC = np.mean(auc)

    return avAUC
